r"""jc - JSON Convert `/etc/group` file parser

Usage (cli):

    $ cat /etc/group | jc --group

Usage (module):

    import jc
    result = jc.parse('group', group_file_output)

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
    version = '1.7'
    description = '`/etc/group` file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'aix', 'freebsd']
    tags = ['file']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema.
    """
    int_list = {'gid'}

    for entry in proc_data:
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
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = []
    cleandata = jc.utils.splitlines(data)

    # Clear any blank lines
    cleandata = [line for line in cleandata if line.strip()]

    if jc.utils.has_data(data):

        for entry in cleandata:
            # an entry ends at the first NUL byte, as it does in the C library,
            # and leading blanks are skipped before the comment test
            entry = entry.split('\0', maxsplit=1)[0].lstrip(' \t')

            if not entry or entry.startswith('#'):
                continue

            output_line = {}
            # the last field is the rest of the line: a colon after the
            # third one is part of that field and does not end it
            fields = entry.split(':', maxsplit=3)
            fields.extend([''] * (4 - len(fields)))

            output_line['group_name'] = fields[0]
            output_line['password'] = fields[1]
            output_line['gid'] = fields[2]
            output_line['members'] = [member.strip(' \t') for member in fields[3].split(',')]

            raw_output.append(output_line)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
