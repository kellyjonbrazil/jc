[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_pid_status"></a>

# jc.parsers.proc_pid_status

jc - JSON Convert `/proc/<pid>/status` file parser

Usage (cli):

    $ cat /proc/1/status | jc --proc

or

    $ jc /proc/1/status

or

    $ cat /proc/1/status | jc --proc-pid-status

Usage (module):

    import jc
    result = jc.parse('proc', proc_pid_status_file)

or

    import jc
    result = jc.parse('proc_pid_status', proc_pid_status_file)

Schema:

    {
      "Name":                               string,
      "Umask":                              string,
      "State":                              string,
      "State_pretty":                       string,
      "Tgid":                               integer,
      "Ngid":                               integer,
      "Pid":                                integer,
      "PPid":                               integer,
      "TracerPid":                          integer,
      "Uid": [
                                            integer
      ],
      "Gid": [
                                            integer
      ],
      "FDSize":                             integer,
      "Groups":                             string,
      "NStgid":                             integer,
      "NSpid":                              integer,
      "NSpgid":                             integer,
      "NSsid":                              integer,
      "VmPeak":                             integer,
      "VmSize":                             integer,
      "VmLck":                              integer,
      "VmPin":                              integer,
      "VmHWM":                              integer,
      "VmRSS":                              integer,
      "RssAnon":                            integer,
      "RssFile":                            integer,
      "RssShmem":                           integer,
      "VmData":                             integer,
      "VmStk":                              integer,
      "VmExe":                              integer,
      "VmLib":                              integer,
      "VmPTE":                              integer,
      "VmSwap":                             integer,
      "HugetlbPages":                       integer,
      "CoreDumping":                        integer,
      "THP_enabled":                        integer,
      "Threads":                            integer,
      "SigQ":                               string,
      "SigQ_current":                       integer,
      "SigQ_limit":                         integer,
      "SigPnd":                             string,
      "ShdPnd":                             string,
      "SigBlk":                             string,
      "SigIgn":                             string,
      "SigCgt":                             string,
      "CapInh":                             string,
      "CapPrm":                             string,
      "CapEff":                             string,
      "CapBnd":                             string,
      "CapAmb":                             string,
      "NoNewPrivs":                         integer,
      "Seccomp":                            integer,
      "Speculation_Store_Bypass":           string,
      "Cpus_allowed": [
                                            string
      ],
      "Cpus_allowed_list":                  string,
      "Mems_allowed": [
                                            string
      ],
      "Mems_allowed_list":                  string,
      "voluntary_ctxt_switches":            integer,
      "nonvoluntary_ctxt_switches":         integer
    }

Examples:

    $ cat /proc/1/status | jc --proc -p
    {
      "Name": "systemd",
      "Umask": "0000",
      "State": "S",
      "Tgid": 1,
      "Ngid": 0,
      "Pid": 1,
      "PPid": 0,
      "TracerPid": 0,
      "Uid": [
        0,
        0,
        0,
        0
      ],
      "Gid": [
        0,
        0,
        0,
        0
      ],
      "FDSize": 128,
      "Groups": "",
      "NStgid": 1,
      "NSpid": 1,
      "NSpgid": 1,
      "NSsid": 1,
      "VmPeak": 235380,
      "VmSize": 169984,
      "VmLck": 0,
      "VmPin": 0,
      "VmHWM": 13252,
      "VmRSS": 13252,
      "RssAnon": 4576,
      "RssFile": 8676,
      "RssShmem": 0,
      "VmData": 19688,
      "VmStk": 1032,
      "VmExe": 808,
      "VmLib": 9772,
      "VmPTE": 96,
      "VmSwap": 0,
      "HugetlbPages": 0,
      "CoreDumping": 0,
      "THP_enabled": 1,
      "Threads": 1,
      "SigQ": "0/15245",
      "SigPnd": "0000000000000000",
      "ShdPnd": "0000000000000000",
      "SigBlk": "7be3c0fe28014a03",
      "SigIgn": "0000000000001000",
      "SigCgt": "00000001800004ec",
      "CapInh": "0000000000000000",
      "CapPrm": "000000ffffffffff",
      "CapEff": "000000ffffffffff",
      "CapBnd": "000000ffffffffff",
      "CapAmb": "0000000000000000",
      "NoNewPrivs": 0,
      "Seccomp": 0,
      "Speculation_Store_Bypass": "thread vulnerable",
      "Cpus_allowed": [
        "ffffffff",
        "ffffffff",
        "ffffffff",
        "ffffffff"
      ],
      "Cpus_allowed_list": "0-127",
      "Mems_allowed": [
        "00000000",
        "00000000",
        "00000000",
        "00000000",
        "00000000",
        "00000000",
        "00000000",
        "00000000",
        "00000000",
        "00000000",
        "00000000",
        "00000000",
        "00000000",
        "00000000",
        "00000000",
        "00000000",
        "00000000",
        "00000000",
        "00000000",
        "00000000",
        "00000000",
        "00000000",
        "00000000",
        "00000000",
        "00000000",
        "00000000",
        "00000000",
        "00000000",
        "00000000",
        "00000000",
        "00000000",
        "00000001"
      ],
      "Mems_allowed_list": "0",
      "voluntary_ctxt_switches": 1856,
      "nonvoluntary_ctxt_switches": 6620,
      "State_pretty": "sleeping",
      "SigQ_current": 0,
      "SigQ_limit": 15245
    }

    $ cat /proc/1/status | jc --proc-pid-status -p -r
    {
      "Name": "systemd",
      "Umask": "0000",
      "State": "S (sleeping)",
      "Tgid": "1",
      "Ngid": "0",
      "Pid": "1",
      "PPid": "0",
      "TracerPid": "0",
      "Uid": "0\t0\t0\t0",
      "Gid": "0\t0\t0\t0",
      "FDSize": "128",
      "Groups": "",
      "NStgid": "1",
      "NSpid": "1",
      "NSpgid": "1",
      "NSsid": "1",
      "VmPeak": "235380 kB",
      "VmSize": "169984 kB",
      "VmLck": "0 kB",
      "VmPin": "0 kB",
      "VmHWM": "13252 kB",
      "VmRSS": "13252 kB",
      "RssAnon": "4576 kB",
      "RssFile": "8676 kB",
      "RssShmem": "0 kB",
      "VmData": "19688 kB",
      "VmStk": "1032 kB",
      "VmExe": "808 kB",
      "VmLib": "9772 kB",
      "VmPTE": "96 kB",
      "VmSwap": "0 kB",
      "HugetlbPages": "0 kB",
      "CoreDumping": "0",
      "THP_enabled": "1",
      "Threads": "1",
      "SigQ": "0/15245",
      "SigPnd": "0000000000000000",
      "ShdPnd": "0000000000000000",
      "SigBlk": "7be3c0fe28014a03",
      "SigIgn": "0000000000001000",
      "SigCgt": "00000001800004ec",
      "CapInh": "0000000000000000",
      "CapPrm": "000000ffffffffff",
      "CapEff": "000000ffffffffff",
      "CapBnd": "000000ffffffffff",
      "CapAmb": "0000000000000000",
      "NoNewPrivs": "0",
      "Seccomp": "0",
      "Speculation_Store_Bypass": "thread vulnerable",
      "Cpus_allowed": "ffffffff,ffffffff,ffffffff,ffffffff",
      "Cpus_allowed_list": "0-127",
      "Mems_allowed": "00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000001",
      "Mems_allowed_list": "0",
      "voluntary_ctxt_switches": "1856",
      "nonvoluntary_ctxt_switches": "6620"
    }

<a id="jc.parsers.proc_pid_status.parse"></a>

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

Source: [`jc/parsers/proc_pid_status.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_pid_status.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
