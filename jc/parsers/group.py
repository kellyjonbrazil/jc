"""jc - JSON CLI output utility `/etc/group` file parser

Usage (cli):

    $ cat /etc/group | jc --group

Usage (module):

    import jc.parsers.group
    result = jc.parsers.group.parse(group_file_output)

Schema:

    [
      {
        "group_name":    string,
        "password":      string,
        "gid":           integer,
        "members": [
                         string
        ]
      }
    ]

Examples:

    $ cat /etc/group | jc --group -p
    [
      {
        "group_name": "nobody",
        "password": "*",
        "gid": -2,
        "members": []
      },
      {
        "group_name": "nogroup",
        "password": "*",
        "gid": -1,
        "members": []
      },
      {
        "group_name": "wheel",
        "password": "*",
        "gid": 0,
        "members": [
          "root"
        ]
      },
      {
        "group_name": "certusers",
        "password": "*",
        "gid": 29,
        "members": [
          "root",
          "_jabber",
          "_postfix",
          "_cyrus",
          "_calendar",
          "_dovecot"
        ]
      },
      ...
    ]

    $ cat /etc/group | jc --group -p -r
    [
      {
        "group_name": "nobody",
        "password": "*",
        "gid": "-2",
        "members": [
          ""
        ]
      },
      {
        "group_name": "nogroup",
        "password": "*",
        "gid": "-1",
        "members": [
          ""
        ]
      },
      {
        "group_name": "wheel",
        "password": "*",
        "gid": "0",
        "members": [
          "root"
        ]
      },
      {
        "group_name": "certusers",
        "password": "*",
        "gid": "29",
        "members": [
          "root",
          "_jabber",
          "_postfix",
          "_cyrus",
          "_calendar",
          "_dovecot"
        ]
      },
      ...
    ]
"""
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.3'
    description = '`/etc/group` file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'aix', 'freebsd']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema.
    """
    for entry in proc_data:
        int_list = ['gid']
        for key in entry:
            if key in int_list:
                entry[key] = jc.utils.convert_to_int(entry[key])

        if entry['members'] == ['']:
            entry['members'] = []

    return proc_data


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

    raw_output = []
    cleandata = data.splitlines()

    # Clear any blank lines
    cleandata = list(filter(None, cleandata))

    if jc.utils.has_data(data):

        for entry in cleandata:
            if entry.startswith('#'):
                continue

            output_line = {}
            fields = entry.split(':')

            output_line['group_name'] = fields[0]
            output_line['password'] = fields[1]
            output_line['gid'] = fields[2]
            output_line['members'] = fields[3].split(',')

            raw_output.append(output_line)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
