[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_pid_smaps"></a>

# jc.parsers.proc_pid_smaps

jc - JSON Convert `/proc/<pid>/smaps` file parser

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

<a id="jc.parsers.proc_pid_smaps.parse"></a>

### parse

```python
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[Dict]
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

### Parser Information
Compatibility:  linux

Source: [`jc/parsers/proc_pid_smaps.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_pid_smaps.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
