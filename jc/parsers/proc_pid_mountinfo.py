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
        "module":                   string,
        "size":                     integer,
        "used":                     integer,
        "used_by": [
                                    string
        ],
        "status":                   string,
        "location":                 string
      }
    ]

Examples:

    $ cat /proc/1/mountinfo | jc --proc -p
    [
      {
        "module": "binfmt_misc",
        "size": 24576,
        "used": 1,
        "used_by": [],
        "status": "Live",
        "location": "0xffffffffc0ab4000"
      },
      {
        "module": "vsock_loopback",
        "size": 16384,
        "used": 0,
        "used_by": [],
        "status": "Live",
        "location": "0xffffffffc0a14000"
      },
      {
        "module": "vmw_vsock_virtio_transport_common",
        "size": 36864,
        "used": 1,
        "used_by": [
          "vsock_loopback"
        ],
        "status": "Live",
        "location": "0xffffffffc0a03000"
      },
      ...
    ]

    $ cat /proc/1/mountinfo | jc --proc_pid-mountinfo -p -r
    [
      {
        "module": "binfmt_misc",
        "size": "24576",
        "used": "1",
        "used_by": [],
        "status": "Live",
        "location": "0xffffffffc0ab4000"
      },
      {
        "module": "vsock_loopback",
        "size": "16384",
        "used": "0",
        "used_by": [],
        "status": "Live",
        "location": "0xffffffffc0a14000"
      },
      {
        "module": "vmw_vsock_virtio_transport_common",
        "size": "36864",
        "used": "1",
        "used_by": [
          "vsock_loopback"
        ],
        "status": "Live",
        "location": "0xffffffffc0a03000"
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
    int_list = {'size', 'used'}

    for entry in proc_data:
        for key in entry:
            if key in int_list:
                entry[key] = jc.utils.convert_to_int(entry[key])

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
            (?P<optional_fields>(?:\s?\S+:\S+\s?)*)\s?-\s
            (?P<fs_type>\S+)\s
            (?P<mount_source>\S+)\s
            (?P<super_options>\S+)
            ''', re.VERBOSE
        )

        for line in filter(None, data.splitlines()):

            line_match = line_pattern.search(line)
            if line_match:
                raw_output.append(line_match.groupdict())

    return raw_output if raw else _process(raw_output)
