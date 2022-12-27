"""jc - JSON Convert `/proc/<pid>/mountinfo` file parser

Usage (cli):

    $ cat /proc/1/mountinfo | jc --proc

or

    $ jc /proc/1/mountinfo

or

    $ cat /proc/1/mountinfo | jc --proc-pid-mountinfo

Usage (module):

    import jc
    result = jc.parse('proc', proc_pid_mountinfo_file)

or

    import jc
    result = jc.parse('proc_pid_mountinfo', proc_pid_mountinfo_file)

Schema:

    [
      {
        "mount_id":                 integer,
        "parent_id":                integer,
        "maj":                      integer,
        "min":                      integer,
        "root":                     string,
        "mount_point":              string,
        "mount_options": [
                                    string
        ],
        "optional_fields": {                   # [0]
          "<key>":                  integer    # [1]
        },
        "fs_type":                  string,
        "mount_source":             string,
        "super_options": [
                                    integer    # [2]
        ],
        "super_options_fields": {
          "<key>":                  string
        }
      }
    ]

    [0] if empty, then private mount
    [1] unbindable will always have a value of 0
    [2] integer conversions are attempted. Use --raw or raw=True for
        original string values.

Examples:

    $ cat /proc/1/mountinfo | jc --proc -p
    [
      {
        "mount_id": 24,
        "parent_id": 30,
        "maj": 0,
        "min": 22,
        "root": "/",
        "mount_point": "/sys",
        "mount_options": [
          "rw",
          "nosuid",
          "nodev",
          "noexec",
          "relatime"
        ],
        "optional_fields": {
          "master": 1,
          "shared": 7
        },
        "fs_type": "sysfs",
        "mount_source": "sysfs",
        "super_options": [
          "rw"
        ]
      },
      {
        "mount_id": 25,
        "parent_id": 30,
        "maj": 0,
        "min": 23,
        "root": "/",
        "mount_point": "/proc",
        "mount_options": [
          "rw",
          "nosuid",
          "nodev",
          "noexec",
          "relatime"
        ],
        "optional_fields": {
          "shared": 14
        },
        "fs_type": "proc",
        "mount_source": "proc",
        "super_options": [
          "rw"
        ]
      },
      ...
    ]

    $ cat /proc/1/mountinfo | jc --proc-pid-mountinfo -p -r
    [
      {
        "mount_id": "24",
        "parent_id": "30",
        "maj": "0",
        "min": "22",
        "root": "/",
        "mount_point": "/sys",
        "mount_options": "rw,nosuid,nodev,noexec,relatime",
        "optional_fields": "master:1 shared:7 ",
        "fs_type": "sysfs",
        "mount_source": "sysfs",
        "super_options": "rw"
      },
      {
        "mount_id": "25",
        "parent_id": "30",
        "maj": "0",
        "min": "23",
        "root": "/",
        "mount_point": "/proc",
        "mount_options": "rw,nosuid,nodev,noexec,relatime",
        "optional_fields": "shared:14 ",
        "fs_type": "proc",
        "mount_source": "proc",
        "super_options": "rw"
      },
      ...
    ]
"""
import re
from typing import List, Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`/proc/<pid>/mountinfo` file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    tags = ['file']
    hidden = True


__version__ = info.version


def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    int_list = {'mount_id', 'parent_id', 'maj', 'min'}

    for entry in proc_data:
        for key in entry:
            if key in int_list:
                entry[key] = int(entry[key])

        if 'mount_options' in entry:
            entry['mount_options'] = entry['mount_options'].split(',')

        if 'optional_fields' in entry:
            if 'unbindable' in  entry['optional_fields']:
                entry['optional_fields'] = {'unbindable': 0}
            else:
                entry['optional_fields'] = {x.split(':')[0]: int(x.split(':')[1]) for x in entry['optional_fields'].split()}

        if 'super_options' in entry:
            if entry['super_options']:
                super_options_split = entry['super_options'].split(',')
                s_options = [x for x in super_options_split if '=' not in x]
                s_options_fields = [x for x in super_options_split if '=' in x]

                if s_options:
                    entry['super_options'] = s_options
                else:
                    del entry['super_options']

                if s_options_fields:
                    if not 'super_options_fields' in entry:
                        entry['super_options_fields'] = {}

                    for field in s_options_fields:
                        key, val = field.split('=')
                        entry['super_options_fields'][key] = jc.utils.convert_to_int(val)

            else:
                del entry['super_options']

    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> List[Dict]:
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

    raw_output: List = []

    if jc.utils.has_data(data):

        line_pattern = re.compile(r'''
            ^(?P<mount_id>\d+)\s
            (?P<parent_id>\d+)\s
            (?P<maj>\d+):
            (?P<min>\d+)\s
            (?P<root>\S+)\s
            (?P<mount_point>\S+)\s
            (?P<mount_options>\S+)\s?
            # (?P<optional_fields>(?:\s?\S+:\S+\s?)*)\s?-\s
            (?P<optional_fields>(?:\s?(?:\S+:\S+|unbindable)\s?)*)\s?-\s
            (?P<fs_type>\S+)\s
            (?P<mount_source>\S+)\s
            (?P<super_options>\S+)?
            ''', re.VERBOSE
        )

        for line in filter(None, data.splitlines()):

            line_match = line_pattern.search(line)
            if line_match:
                raw_output.append(line_match.groupdict())

    return raw_output if raw else _process(raw_output)
