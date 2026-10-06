r"""jc - JSON Convert `net localgroup` command output parser

Usage (cli):

    $ net localgroup | jc --net-localgroup
    $ net localgroup /domain | jc --net-localgroup
    $ net localgroup Administrators | jc --net-localgroup
    $ net localgroup Administrators /domain | jc --net-localgroup

Usage (module):

    import jc
    result = jc.parse('net_localgroup', net_localgroup_command_output)

Schema:

    {
        "account_origin":     string,
        "domain":             string,
        "comment":            string,
        "groups": [
            {
                "name":       string
                "members": [
                              string
                ]
            }
        ],
    }

Examples:

    $ net localgroup | jc --net-localgroup -p
    {
        "account_origin": null,
        "comment": null,
        "domain": null,
        "groups": [
            {
                "name": "Administrators",
                "members": [
                    "Administrator",
                    "Operator",
                    "ansible",
                    "user1"
                ]
            }
        ]
    }
"""
import re
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`net localgroup` command parser'
    author = 'joehacksalot'
    author_email = 'joehacksalot@gmail.com'
    compatible = ['win32']
    magic_commands = ['net localgroup']
    tags = ['command']


__version__ = info.version


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Parsed dictionary. The raw and processed data structures are the same.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}
    if jc.utils.has_data(data):
        # Initialize the parsed output dictionary with all fields set to None or empty lists
        raw_output = _parse(data)

    return raw_output if raw else _process(raw_output)

def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Processed Dictionary. Structured data to conform to the schema.
    """
    return proc_data


class _PushbackIterator:
    def __init__(self, iterator):
        self.iterator = iterator
        self.pushback_stack = []
    def __iter__(self):
        return self
    def __next__(self):
        if self.pushback_stack:
            return self.pushback_stack.pop()
        else:
            return next(self.iterator)
    def pushback(self, value):
        self.pushback_stack.append(value)

def _parse_net_localgroup_list(line_iter, expect_asterisk):
    name_list = []
    while True:
        try:
            line = next(line_iter)
            if not line.strip():
                continue  # Skip empty lines

            # Check if the line starts with an asterisk
            if line == 'The command completed successfully.':
                break
            elif expect_asterisk and line.startswith('*'):
                name_list.append(line[1:].strip())
            else:
                name_list.append(line)
        except StopIteration:
            break
    return name_list


def _parse(data):
    lines = data.splitlines()
    parse_type = None  # Can be 'groups_list' or 'members'

    result = {
        "account_origin": None,
        "domain": None,
        "comment": None,
        "groups": []
    }

    group_name = ""
    lines = data.splitlines()
    lines = [line.rstrip() for line in lines if line.strip() != ""]

    line_iter = _PushbackIterator(iter(lines))
    for line in line_iter:
        line = line.rstrip()

        # Skip empty lines
        if not line.strip():
            continue

        match_domain_processed = re.match(r"^The request will be processed at a domain controller for domain (.+)", line, re.IGNORECASE)
        match_localgroup_list = re.match(r"^Aliases for[\s]*([^:]+)", line, re.IGNORECASE)        #  "Aliases for \\DESKTOP-WIN11:"
        match_localgroup_members = re.match(r"^Alias name[\s]*([^:]+)", line, re.IGNORECASE)      #  "Alias name     administrators:"
        if match_domain_processed:
            # Extract the domain name
            result["domain"] = match_domain_processed.group(1).strip()
        elif match_localgroup_list:
            # Extract the account origin
            result["account_origin"] = match_localgroup_list.group(1).strip()
            parse_type = 'groups_list'   # Prepare to read groups
        elif match_localgroup_members:
            # We are querying a specific group
            group_name = match_localgroup_members.group(1).strip()
            parse_type = 'members_list'  # Prepare to read members
        elif line.startswith('Comment'):
            comment_line = line.split('Comment', 1)[1].strip()
            result["comment"] = comment_line if comment_line else None
        elif line.startswith('---'):
            # Start of a section (groups or members)
            if parse_type == 'groups_list':
                names_list = _parse_net_localgroup_list(line_iter, expect_asterisk=True)
                result["groups"] = [{"name": group_name, "members": []} for group_name in names_list]
            elif parse_type == 'members_list':
                names_list = _parse_net_localgroup_list(line_iter, expect_asterisk=False)
                result["groups"] = [{
                    "name": group_name,
                    "members": names_list
                }]

    return result