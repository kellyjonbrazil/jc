r"""jc - JSON Convert `/proc/<pid>/status` file parser

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
"""
from typing import Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`/proc/<pid>/status` file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    tags = ['file']
    hidden = True


__version__ = info.version


def _process(proc_data: Dict) -> Dict:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured to conform to the schema.
    """
    int_list = {'Tgid', 'Ngid', 'Pid', 'PPid', 'TracerPid', 'FDSize', 'NStgid',
      'NSpid', 'NSpgid', 'NSsid', 'VmPeak', 'VmSize', 'VmLck', 'VmPin', 'VmHWM',
      'VmRSS', 'RssAnon', 'RssFile', 'RssShmem', 'VmData', 'VmStk', 'VmExe', 'VmLib',
      'VmPTE', 'VmSwap', 'HugetlbPages', 'CoreDumping', 'THP_enabled', 'Threads',
      'NoNewPrivs', 'Seccomp', 'voluntary_ctxt_switches', 'nonvoluntary_ctxt_switches'}

    for key, val in proc_data.items():
        if key in int_list:
            proc_data[key] = jc.utils.convert_to_int(val)

    if 'State' in proc_data:
        st, st_pretty = proc_data['State'].split()
        proc_data['State'] = st
        proc_data['State_pretty'] = st_pretty.strip('()')

    if 'Uid' in proc_data:
        proc_data['Uid'] = [int(x) for x in proc_data['Uid'].split()]

    if 'Gid' in proc_data:
        proc_data['Gid'] = [int(x) for x in proc_data['Gid'].split()]

    if 'SigQ' in proc_data:
        current_q, limit_q = proc_data['SigQ'].split('/')
        proc_data['SigQ_current'] = int(current_q)
        proc_data['SigQ_limit'] = int(limit_q)

    if 'Cpus_allowed' in proc_data:
        proc_data['Cpus_allowed'] = proc_data['Cpus_allowed'].split(',')

    if 'Mems_allowed' in proc_data:
        proc_data['Mems_allowed'] = proc_data['Mems_allowed'].split(',')


    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> Dict:
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: Dict = {}

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            key, val = line.split(':', maxsplit=1)
            raw_output[key] = val.strip()

    return raw_output if raw else _process(raw_output)
