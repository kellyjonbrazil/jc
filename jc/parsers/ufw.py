"""jc - JSON CLI output utility `ufw` command output parser

<<Short ufw description and caveats>>

Usage (cli):

    $ ufw status | jc --ufw

    or

    $ jc ufw status

Usage (module):

    import jc.parsers.ufw
    result = jc.parsers.ufw.parse(ufw_command_output)

Schema:

    [
      {
        "ufw":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ ufw status verbose | jc --ufw -p
    []

    $ ufw status verbose | jc --ufw -p -r
    []
"""
import jc.utils
import re


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`ufw status` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux']
    magic_commands = ['ufw status']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """

    # rebuild output for added semantic information
    # use helper functions in jc.utils for int, float, bool conversions and timestamps

    return proc_data


def _parse_to_from(linedata, direction):
    return {}


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = {}
    rules_list = []

    if jc.utils.has_data(data):

        rule_lines = False

        for line in filter(None, data.splitlines()):

            if line.startswith('Status: '):
                raw_output['status'] = line.split(': ', maxsplit=1)[1]
                continue

            if line.startswith('Logging: '):
                raw_output['logging'] = line.split(': ', maxsplit=1)[1]
                continue

            if line.startswith('Default: '):
                raw_output['default'] = line.split(': ', maxsplit=1)[1]
                continue

            if line.startswith('New profiles: '):
                raw_output['new_profiles'] = line.split(': ', maxsplit=1)[1]
                continue

            if 'To' in line and 'Action' in line and 'From' in line:
                rule_lines = True
                continue

            if rule_lines:
                if '------' in line:
                    continue

                # Split on action. Left of Action is 'to', right of Action is 'from'
                rule_obj = {}

                splitline = re.split(r'(ALLOW IN|ALLOW OUT|DENY IN|DENY OUT|ALLOW|DENY)', line)
                to_line = splitline[0]
                action_line = splitline[1]
                action_list = action_line.split()
                from_line = splitline[2]
                action_direction = None

                if len(action_list) == 1:
                    action = action_list[0]
                elif len(action_list) == 2:
                    action = action_list[0]
                    action_direction = action_list[1]

                rule_obj['action'] = action
                rule_obj['action_direction'] = action_direction
                rule_obj.update(_parse_to_from(to_line, 'to'))
                rule_obj.update(_parse_to_from(from_line, 'from'))

                rules_list.append(rule_obj)

        raw_output['rules'] = rules_list

    if raw:
        return raw_output
    else:
        return _process(raw_output)
