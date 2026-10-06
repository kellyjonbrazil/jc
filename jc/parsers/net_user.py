r"""jc - JSON Convert `net user` command output parser


Usage (cli):

    $ net users | jc --net-user
    $ net users /domain | jc --net-user
    $ net users User1 | jc --net-user
    $ net users User1 /domain | jc --net-user

Usage (module):

    import jc
    result = jc.parse('net_user', net_user_command_output)

Schema:

    {
        "domain":                             string,
        "account_origin":                     string,
        "user_accounts": [
            {
                "user_name":                  string,
                "full_name":                  string,
                "comment":                    string,
                "user_comment":               string,
                "country_region_code":        string,
                "account_active":             boolean,
                "account_expires":            string,
                "password_last_set":          string,
                "password_expires":           string,
                "password_changeable":        string,
                "password_required":          boolean,
                "user_may_change_password":   boolean,
                "workstations_allowed":       string,
                "logon_script":               string,
                "user_profile":               string,
                "home_directory":             string,
                "last_logon":                 string,
                "logon_hours_allowed":        string,
                "local_group_memberships": [
                                              string,
                ],
                "global_group_memberships": [
                                              string,
                ]
            }
        ]
    }


Examples:

    $ net users | jc --net-user -p
    {
        "account_origin": "\\\\WIN-SERVER16",
        "domain": "",
        "user_accounts": [
            {
                "user_name": "Administrator"
            },
            {
                "user_name": "DefaultAccount"
            },
            {
                "user_name": "Guest"
            },
            {
                "user_name": "pentera_BnlLQVnd7p"
            },
            {
                "user_name": "user1"
            }
        ]
    }

    $ net users /domain | jc --net-user -p
    {
        "account_origin": "\\\\DESKTOP-WIN10-PRO.somecompany.corp",
        "domain": "somecompany.corp",
        "user_accounts": [
            {
                "user_name": "aaron"
            },
            {
                "user_name": "addison"
            },
            {
                "user_name": "Administrator"
            },
            {
                "user_name": "ansible"
            },
            {
                "user_name": "da"
            },
            {
                "user_name": "DefaultAccount"
            },
            {
                "user_name": "Guest"
            },
            {
                "user_name": "harrison"
            },
            {
                "user_name": "james"
            },
            {
                "user_name": "krbtgt"
            },
            {
                "user_name": "liam"
            },
            {
                "user_name": "localadmin"
            },
            {
                "user_name": "tiffany"
            }
        ]
    }

    $ net users Administrator | jc --net-user -p
    {
        "domain": "",
        "user_accounts": [
            {
                "account_active": true,
                "account_expires": "Never",
                "comment": "Built-in account for administering the computer/domain",
                "country_region_code": "000 (System Default)",
                "global_group_memberships": [],
                "last_logon": "2024-08-23T13:47:11",
                "local_group_memberships": [
                    "Administrators"
                ],
                "logon_hours_allowed": "All",
                "password_changeable": "2021-12-17T11:07:14",
                "password_expires": "2022-01-27T11:07:14",
                "password_last_set": "2021-12-16T11:07:14",
                "password_required": true,
                "user_may_change_password": true,
                "user_name": "Administrators",
                "workstations_allowed": "All"
            }
        ]
    }

    $ net users Administrator /domain | jc --net-user -p | jq
    {
        "domain": "somecompany.corp",
        "user_accounts": [
            {
                "account_active": true,
                "account_expires": "Never",
                "comment": "Built-in account for administering the computer/domain",
                "country_region_code": "000 (System Default)",
                "global_group_memberships": [
                    "Domain Admins",
                    "Domain Users",
                    "Group Policy Creator",
                    "Enterprise Admins",
                    "Schema Admins"
                ],
                "last_logon": "2024-07-17T13:46:12",
                "local_group_memberships": [
                    "Administrators"
                ],
                "logon_hours_allowed": "All",
                "password_changeable": "2023-09-30T11:44:26",
                "password_expires": "Never",
                "password_last_set": "2023-09-29T11:44:26",
                "password_required": true,
                "user_may_change_password": true,
                "user_name": "Administrators",
                "workstations_allowed": "All"
            }
        ]
    }
"""
from datetime import datetime
import re
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`net user` command parser'
    author = 'joehacksalot'
    author_email = 'joehacksalot@gmail.com'
    compatible = ['win32']
    magic_commands = ['net user']
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
        raw_output = _parse(data)

    if not raw_output:
        raw_output = {}

    return raw_output if raw else _process(raw_output)

def _set_if_not_none(output_dict, key, value):
    if value is not None:
        output_dict[key] = value

def _process_string_is_yes(text):
    if text:
        return text.lower() == "yes"
    else:
        return None

def _process_date(s):
    if s is not None:
        for fmt in ('%m/%d/%Y %I:%M:%S %p', '%m/%d/%Y %H:%M:%S %p'):
            try:
                return datetime.strptime(s, fmt).isoformat()
            except ValueError:
                continue
    return s  # Return the original string if parsing fails

def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Processed Dictionary. Structured data to conform to the schema.
    """
    for user_account in proc_data.get("user_accounts", []):
        _set_if_not_none(user_account, "account_active", _process_string_is_yes(user_account.get("account_active", None)))
        _set_if_not_none(user_account, "password_last_set", _process_date(user_account.get("password_last_set", None)))
        _set_if_not_none(user_account, "password_expires", _process_date(user_account.get("password_expires", None)))
        _set_if_not_none(user_account, "password_changeable", _process_date(user_account.get("password_changeable", None)))
        _set_if_not_none(user_account, "password_required", _process_string_is_yes(user_account.get("password_required", None)))
        _set_if_not_none(user_account, "user_may_change_password", _process_string_is_yes(user_account.get("user_may_change_password", None)))
        _set_if_not_none(user_account, "last_logon", _process_date(user_account.get("last_logon", None)))

    if not proc_data:
        proc_data = {}

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

def _parse_user_account_keypairs(keypair_dict):
    user_account_parsed = {}
    _set_if_not_none(user_account_parsed, "user_name", keypair_dict.get("user_name", None))
    _set_if_not_none(user_account_parsed, "full_name", keypair_dict.get("full_name", None))
    _set_if_not_none(user_account_parsed, "comment", keypair_dict.get("comment", None))
    _set_if_not_none(user_account_parsed, "users_comment", keypair_dict.get("users_comment", None))
    _set_if_not_none(user_account_parsed, "country_region_code", keypair_dict.get("country_region_code", None))
    _set_if_not_none(user_account_parsed, "account_active", keypair_dict.get("account_active", None))
    _set_if_not_none(user_account_parsed, "account_expires", keypair_dict.get("account_expires", None))
    _set_if_not_none(user_account_parsed, "password_last_set", keypair_dict.get("password_last_set", None))
    _set_if_not_none(user_account_parsed, "password_expires", keypair_dict.get("password_expires", None))
    _set_if_not_none(user_account_parsed, "password_changeable", keypair_dict.get("password_changeable", None))
    _set_if_not_none(user_account_parsed, "password_required", keypair_dict.get("password_required", None))
    _set_if_not_none(user_account_parsed, "user_may_change_password", keypair_dict.get("user_may_change_password", None))
    _set_if_not_none(user_account_parsed, "workstations_allowed", keypair_dict.get("workstations_allowed", None))
    _set_if_not_none(user_account_parsed, "logon_script", keypair_dict.get("logon_script", None))
    _set_if_not_none(user_account_parsed, "user_profile", keypair_dict.get("user_profile", None))
    _set_if_not_none(user_account_parsed, "home_directory", keypair_dict.get("home_directory", None))
    _set_if_not_none(user_account_parsed, "last_logon", keypair_dict.get("last_logon", None))
    _set_if_not_none(user_account_parsed, "logon_hours_allowed", keypair_dict.get("logon_hours_allowed", None))
    _set_if_not_none(user_account_parsed, "local_group_memberships", keypair_dict.get("local_group_memberships", None))
    _set_if_not_none(user_account_parsed, "global_group_memberships", keypair_dict.get("global_group_memberships", None))
    return user_account_parsed


def _parse_groups(line_iter):
    group_list = []
    # Process additional lines that belong to the current entry (e.g., additional DNS servers, DNS Suffix Search List)
    while True:
        try:
            next_line = next(line_iter).strip()
            if not next_line:
                continue  # Skip empty lines

            # Check if the line is indented (starts with whitespace)
            if next_line.startswith('*'):
                groups = next_line.split("*")
                groups = [group.strip() for group in groups if group.strip() != ""]
                if "None" in groups:
                    groups.remove("None")
                # It's an indented line; append the stripped line to entry_list
                group_list.extend(groups)
            else:
                # Not an indented line; push it back and exit
                line_iter.pushback(next_line)
                break
        except StopIteration:
            break
    return group_list

def _parse(data):
    result = {
        "domain": "",
        "user_accounts": []
    }

    lines = data.splitlines()
    lines = [line.rstrip() for line in lines if line.strip() != ""]

    line_iter = _PushbackIterator(iter(lines))
    for line in line_iter:
        line = line.rstrip()

        # Skip empty lines
        if not line.strip():
            continue

        match_domain_processed = re.match(r"^The request will be processed at a domain controller for domain (.+)\.$", line, re.IGNORECASE)
        if match_domain_processed:
            result["domain"] = match_domain_processed.group(1).strip()
        # Check if the text is of the first type (detailed user info)
        elif "User name" in line:
            line_iter.pushback(line)
            user_account_keypairs = {}

            # Regular expression to match key-value pairs
            kv_pattern = re.compile(r'^([\w\s\/\'\-]{1,29})\s*(.+)?$')
            key = None

            while True:
                # Process each line
                # Break when done
                try:
                    line = next(line_iter)
                    line = line.strip()
                    if not line:
                        continue  # Skip empty lines

                    match = kv_pattern.match(line)
                    if "The command completed" in line:
                        break
                    elif match:
                        key_raw = match.group(1).strip()
                        key = key_raw.lower().replace(" ", "_").replace("'", "").replace("/", "_").replace("-", "_")
                        if len(match.groups()) == 2 and match.group(2) is not None:
                            value = match.group(2).strip()
                            if key in ["local_group_memberships", "global_group_memberships"]:
                                line_iter.pushback(value)
                                user_account_keypairs[key] = _parse_groups(line_iter)
                            else:
                                user_account_keypairs[key] = value
                        else:
                            # Line without value, it's a key with empty value
                            user_account_keypairs[key] = None
                    else:
                        raise ValueError(f"Unexpected line: {line}")
                except StopIteration:
                    break

            # Convert specific fields
            result["user_accounts"].append(_parse_user_account_keypairs(user_account_keypairs))
        elif "User accounts for" in line:
            line_iter.pushback(line)
            collecting_users = False

            while True:
                # Process each line
                # Break when done
                try:
                    line = next(line_iter)
                    line = line.strip()
                    if not line:
                        continue  # Skip empty lines

                    # Check for domain line
                    domain_pattern = re.compile(r'^User accounts for (.+)$')
                    account_origin_match = domain_pattern.match(line)
                    if account_origin_match:
                        result["account_origin"] = account_origin_match.group(1)
                        continue

                    # Check for the line of dashes indicating start of user list
                    if line.startswith('---'):
                        collecting_users = True
                        continue

                    # Check for the completion message
                    if line.startswith('The command completed'):
                        break

                    if collecting_users:
                        # Split the line into usernames
                        user_matches = re.match(r'(.{1,20})(\s+.{1,20})?(\s+.{1,20})?', line)
                        if user_matches:
                            for username in user_matches.groups():
                                if username:
                                    username = username.strip()
                                    user_account = {"user_name": username}
                                    result["user_accounts"].append(user_account)
                except StopIteration:
                    break
        else:
            raise ValueError(f"Unexpected line: {line}")

    return result