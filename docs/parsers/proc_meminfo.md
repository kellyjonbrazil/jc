[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_meminfo"></a>

# jc.parsers.proc_meminfo

jc - JSON Convert `/proc/meminfo` file parser

Usage (cli):

    $ cat /proc/meminfo | jc --proc

or

    $ jc /proc/meminfo

or

    $ cat /proc/meminfo | jc --proc-meminfo

Usage (module):

    import jc
    result = jc.parse('proc', proc_meminfo_file)

or

    import jc
    result = jc.parse('proc_meminfo', proc_meminfo_file)

Schema:

All values are integers.

    {
      <keyName>             integer
    }

Examples:

    $ cat /proc/meminfo | jc --proc -p
    {
      "MemTotal": 3997272,
      "MemFree": 2760316,
      "MemAvailable": 3386876,
      "Buffers": 40452,
      "Cached": 684856,
      "SwapCached": 0,
      "Active": 475816,
      "Inactive": 322064,
      "Active(anon)": 70216,
      "Inactive(anon)": 148,
      "Active(file)": 405600,
      "Inactive(file)": 321916,
      "Unevictable": 19476,
      "Mlocked": 19476,
      "SwapTotal": 3996668,
      "SwapFree": 3996668,
      "Dirty": 152,
      "Writeback": 0,
      "AnonPages": 92064,
      "Mapped": 79464,
      "Shmem": 1568,
      "KReclaimable": 188216,
      "Slab": 288096,
      "SReclaimable": 188216,
      "SUnreclaim": 99880,
      "KernelStack": 5872,
      "PageTables": 1812,
      "NFS_Unstable": 0,
      "Bounce": 0,
      "WritebackTmp": 0,
      "CommitLimit": 5995304,
      "Committed_AS": 445240,
      "VmallocTotal": 34359738367,
      "VmallocUsed": 21932,
      "VmallocChunk": 0,
      "Percpu": 107520,
      "HardwareCorrupted": 0,
      "AnonHugePages": 0,
      "ShmemHugePages": 0,
      "ShmemPmdMapped": 0,
      "FileHugePages": 0,
      "FilePmdMapped": 0,
      "HugePages_Total": 0,
      "HugePages_Free": 0,
      "HugePages_Rsvd": 0,
      "HugePages_Surp": 0,
      "Hugepagesize": 2048,
      "Hugetlb": 0,
      "DirectMap4k": 192320,
      "DirectMap2M": 4001792,
      "DirectMap1G": 2097152
    }

<a id="jc.parsers.proc_meminfo.parse"></a>

### parse

```python
def parse(data: str, raw: bool = False, quiet: bool = False) -> Dict
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    Dictionary. Raw or processed structured data.

### Parser Information
Compatibility:  linux

Source: [`jc/parsers/proc_meminfo.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_meminfo.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
