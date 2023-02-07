"""jc - JSON Convert `/proc/<pid>/smaps` file parser

Usage (cli):

    $ cat /proc/1/smaps | jc --proc

or

    $ jc /proc/1/smaps

or

    $ cat /proc/1/smaps | jc --proc-pid-smaps

Usage (module):

    import jc
    result = jc.parse('proc', proc_pid_smaps_file)

or

    import jc
    result = jc.parse('proc_pid_smaps', proc_pid_smaps_file)

Schema:

    [
      {
        "start":                          string,
        "end":                            string,
        "perms": [
                                          string
        ],
        "offset":                         string,
        "maj":                            string,
        "min":                            string,
        "inode":                          integer,
        "pathname":                       string,
        "Size":                           integer,
        "KernelPageSize":                 integer,
        "MMUPageSize":                    integer,
        "Rss":                            integer,
        "Pss":                            integer,
        "Shared_Clean":                   integer,
        "Shared_Dirty":                   integer,
        "Private_Clean":                  integer,
        "Private_Dirty":                  integer,
        "Referenced":                     integer,
        "Anonymous":                      integer,
        "LazyFree":                       integer,
        "AnonHugePages":                  integer,
        "ShmemPmdMapped":                 integer,
        "FilePmdMapped":                  integer,
        "Shared_Hugetlb":                 integer,
        "Private_Hugetlb":                integer,
        "Swap":                           integer,
        "SwapPss":                        integer,
        "Locked":                         integer,
        "THPeligible":                    integer,
        "VmFlags": [
                                          string
        ],
        "VmFlags_pretty": [
                                          string
        ]
      }
    ]

Examples:

    $ cat /proc/1/smaps | jc --proc -p
    [
      {
        "start": "55a9e753c000",
        "end": "55a9e7570000",
        "perms": [
          "read",
          "private"
        ],
        "offset": "00000000",
        "maj": "fd",
        "min": "00",
        "inode": 798126,
        "pathname": "/usr/lib/systemd/systemd",
        "Size": 208,
        "KernelPageSize": 4,
        "MMUPageSize": 4,
        "Rss": 208,
        "Pss": 104,
        "Shared_Clean": 208,
        "Shared_Dirty": 0,
        "Private_Clean": 0,
        "Private_Dirty": 0,
        "Referenced": 208,
        "Anonymous": 0,
        "LazyFree": 0,
        "AnonHugePages": 0,
        "ShmemPmdMapped": 0,
        "FilePmdMapped": 0,
        "Shared_Hugetlb": 0,
        "Private_Hugetlb": 0,
        "Swap": 0,
        "SwapPss": 0,
        "Locked": 0,
        "THPeligible": 0,
        "VmFlags": [
          "rd",
          "mr",
          "mw",
          "me",
          "dw",
          "sd",
          "mp"
        ],
        "VmFlags_pretty": [
          "readable",
          "may read",
          "may write",
          "may execute",
          "disabled write to the mapped file",
          "soft-dirty flag"
        ]
      },
      ...
    ]

    $ cat /proc/1/smaps | jc --proc-pid-smaps -p -r
    [
      {
        "start": "55a9e753c000",
        "end": "55a9e7570000",
        "perms": "r--p",
        "offset": "00000000",
        "maj": "fd",
        "min": "00",
        "inode": "798126",
        "pathname": "/usr/lib/systemd/systemd",
        "Size": "208 kB",
        "KernelPageSize": "4 kB",
        "MMUPageSize": "4 kB",
        "Rss": "208 kB",
        "Pss": "104 kB",
        "Shared_Clean": "208 kB",
        "Shared_Dirty": "0 kB",
        "Private_Clean": "0 kB",
        "Private_Dirty": "0 kB",
        "Referenced": "208 kB",
        "Anonymous": "0 kB",
        "LazyFree": "0 kB",
        "AnonHugePages": "0 kB",
        "ShmemPmdMapped": "0 kB",
        "FilePmdMapped": "0 kB",
        "Shared_Hugetlb": "0 kB",
        "Private_Hugetlb": "0 kB",
        "Swap": "0 kB",
        "SwapPss": "0 kB",
        "Locked": "0 kB",
        "THPeligible": "0",
        "VmFlags": "rd mr mw me dw sd"
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
    description = '`/proc/<pid>/smaps` file parser'
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
    non_int_list = {'start', 'end', 'perms', 'offset', 'maj', 'min', 'pathname', 'VmFlags'}

    perms_map = {
        'r': 'read',
        'w': 'write',
        'x': 'execute',
        's': 'shared',
        'p': 'private',
        '-': None
    }

    vmflags_map = {
        'rd': 'readable',
        'wr':  'writeable',
        'ex':  'executable',
        'sh':  'shared',
        'mr':  'may read',
        'mw':  'may write',
        'me':  'may execute',
        'ms':  'may share',
        'mp':  'MPX-specific VMA',
        'gd':  'stack segment growns down',
        'pf':  'pure PFN range',
        'dw':  'disabled write to the mapped file',
        'lo':  'pages are locked in memory',
        'io':  'memory mapped I/O area',
        'sr':  'sequential read advise provided',
        'rr':  'random read advise provided',
        'dc':  'do not copy area on fork',
        'de':  'do not expand area on remapping',
        'ac':  'area is accountable',
        'nr':  'swap space is not reserved for the area',
        'ht':  'area uses huge tlb pages',
        'ar':  'architecture specific flag',
        'dd':  'do not include area into core dump',
        'sd':  'soft-dirty flag',
        'mm':  'mixed map area',
        'hg':  'huge page advise flag',
        'nh':  'no-huge page advise flag',
        'mg':  'mergable advise flag'
    }

    for entry in proc_data:
        for key in entry:
            if key not in non_int_list:
                entry[key] = jc.utils.convert_to_int(entry[key])

        if 'perms' in entry:
            perms_list = [perms_map[x] for x in entry['perms'] if perms_map[x]]
            entry['perms'] = perms_list

        if 'VmFlags' in entry:
            entry['VmFlags'] = entry['VmFlags'].split()
            entry['VmFlags_pretty'] = [vmflags_map[x] for x in entry['VmFlags']]

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
    output_line: Dict = {}

    if jc.utils.has_data(data):
        map_line = re.compile(r'''
            ^(?P<start>[0-9a-f]{8,16})-
            (?P<end>[0-9a-f]{8,16})\s
            (?P<perms>[rwxsp\-]{4})\s
            (?P<offset>[0-9a-f]{8,9})\s
            (?P<maj>[0-9a-f]{2}):
            (?P<min>[0-9a-f]{2})\s
            (?P<inode>\d+)\s+
            (?P<pathname>.*)?
            ''', re.VERBOSE
        )

        for line in filter(None, data.splitlines()):

            map_line_found = map_line.search(line)

            if map_line_found:
                if output_line:
                    raw_output.append(output_line)

                output_line = map_line_found.groupdict()
                continue

            key, val = line.split(':', maxsplit=1)
            output_line[key] = val.strip()
            continue

        if output_line:
            raw_output.append(output_line)

    return raw_output if raw else _process(raw_output)
