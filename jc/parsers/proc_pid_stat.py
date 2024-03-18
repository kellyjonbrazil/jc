r"""jc - JSON Convert `/proc/<pid>/stat` file parser

Usage (cli):

    $ cat /proc/1/stat | jc --proc

or

    $ jc /proc/1/stat

or

    $ cat /proc/1/stat | jc --proc-pid-stat

Usage (module):

    import jc
    result = jc.parse('proc', proc_pid_stat_file)

or

    import jc
    result = jc.parse('proc_pid_stat', proc_pid_stat_file)

Schema:

    {
      "pid":                            integer,
      "comm":                           string,
      "state":                          string,
      "state_pretty":                   string,
      "ppid":                           integer,
      "pgrp":                           integer,
      "session":                        integer,
      "tty_nr":                         integer,
      "tpg_id":                         integer,
      "flags":                          integer,
      "minflt":                         integer,
      "cminflt":                        integer,
      "majflt":                         integer,
      "cmajflt":                        integer,
      "utime":                          integer,
      "stime":                          integer,
      "cutime":                         integer,
      "cstime":                         integer,
      "priority":                       integer,
      "nice":                           integer,
      "num_threads":                    integer,
      "itrealvalue":                    integer,
      "starttime":                      integer,
      "vsize":                          integer,
      "rss":                            integer,
      "rsslim":                         integer,
      "startcode":                      integer,
      "endcode":                        integer,
      "startstack":                     integer,
      "kstkeep":                        integer,
      "kstkeip":                        integer,
      "signal":                         integer,
      "blocked":                        integer,
      "sigignore":                      integer,
      "sigcatch":                       integer,
      "wchan":                          integer,
      "nswap":                          integer,
      "cnswap":                         integer,
      "exit_signal":                    integer,
      "processor":                      integer,
      "rt_priority":                    integer,
      "policy":                         integer,
      "delayacct_blkio_ticks":          integer,
      "guest_time":                     integer,
      "cguest_time":                    integer,
      "start_data":                     integer,
      "end_data":                       integer,
      "start_brk":                      integer,
      "arg_start":                      integer,
      "arg_end":                        integer,
      "env_start":                      integer,
      "env_end":                        integer,
      "exit_code":                      integer,
    }

Examples:

    $ cat /proc/1/stat | jc --proc -p
    {
      "pid": 1,
      "comm": "systemd",
      "state": "S",
      "ppid": 0,
      "pgrp": 1,
      "session": 1,
      "tty_nr": 0,
      "tpg_id": -1,
      "flags": 4194560,
      "minflt": 23478,
      "cminflt": 350218,
      "majflt": 99,
      "cmajflt": 472,
      "utime": 107,
      "stime": 461,
      "cutime": 2672,
      "cstime": 4402,
      "priority": 20,
      "nice": 0,
      "num_threads": 1,
      "itrealvalue": 0,
      "starttime": 128,
      "vsize": 174063616,
      "rss": 3313,
      "rsslim": 18446744073709551615,
      "startcode": 94188219072512,
      "endcode": 94188219899461,
      "startstack": 140725059845296,
      "kstkeep": 0,
      "kstkeip": 0,
      "signal": 0,
      "blocked": 671173123,
      "sigignore": 4096,
      "sigcatch": 1260,
      "wchan": 1,
      "nswap": 0,
      "cnswap": 0,
      "exit_signal": 17,
      "processor": 0,
      "rt_priority": 0,
      "policy": 0,
      "delayacct_blkio_ticks": 18,
      "guest_time": 0,
      "cguest_time": 0,
      "start_data": 94188220274448,
      "end_data": 94188220555504,
      "start_brk": 94188243599360,
      "arg_start": 140725059845923,
      "arg_end": 140725059845934,
      "env_start": 140725059845934,
      "env_end": 140725059846125,
      "exit_code": 0,
      "state_pretty": "Sleeping in an interruptible wait"
    }

    $ cat /proc/1/stat | jc --proc-pid-stat -p -r
    {
      "pid": 1,
      "comm": "systemd",
      "state": "S",
      "ppid": 0,
      "pgrp": 1,
      "session": 1,
      "tty_nr": 0,
      "tpg_id": -1,
      "flags": 4194560,
      "minflt": 23478,
      "cminflt": 350218,
      "majflt": 99,
      "cmajflt": 472,
      "utime": 107,
      "stime": 461,
      "cutime": 2672,
      "cstime": 4402,
      "priority": 20,
      "nice": 0,
      "num_threads": 1,
      "itrealvalue": 0,
      "starttime": 128,
      "vsize": 174063616,
      "rss": 3313,
      "rsslim": 18446744073709551615,
      "startcode": 94188219072512,
      "endcode": 94188219899461,
      "startstack": 140725059845296,
      "kstkeep": 0,
      "kstkeip": 0,
      "signal": 0,
      "blocked": 671173123,
      "sigignore": 4096,
      "sigcatch": 1260,
      "wchan": 1,
      "nswap": 0,
      "cnswap": 0,
      "exit_signal": 17,
      "processor": 0,
      "rt_priority": 0,
      "policy": 0,
      "delayacct_blkio_ticks": 18,
      "guest_time": 0,
      "cguest_time": 0,
      "start_data": 94188220274448,
      "end_data": 94188220555504,
      "start_brk": 94188243599360,
      "arg_start": 140725059845923,
      "arg_end": 140725059845934,
      "env_start": 140725059845934,
      "env_end": 140725059846125,
      "exit_code": 0
    }
"""
import re
from typing import Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.2'
    description = '`/proc/<pid>/stat` file parser'
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
    state_map = {
        'R': 'Running',
        'S': 'Sleeping in an interruptible wait',
        'D': 'Waiting in uninterruptible disk sleep',
        'Z': 'Zombie',
        'T': 'Stopped (on a signal) or trace stopped',
        't': 'Tracing stop',
        'W': 'Paging',
        'X': 'Dead',
        'x': 'Dead',
        'K': 'Wakekill',
        'W': 'Waking',
        'P': 'Parked',
        'I': 'Idle'
    }

    if 'state' in proc_data:
        proc_data['state_pretty'] = state_map[proc_data['state']]

    for key, val in proc_data.items():
        try:
            proc_data[key] = int(val)
        except Exception:
            pass

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

        line_re = re.compile(r'''
            ^(?P<pid>\d+)\s
            \((?P<comm>.+)\)\s
            (?P<state>\S)\s
            (?P<ppid>\d+)\s
            (?P<pgrp>\d+)\s
            (?P<session>\d+)\s
            (?P<tty_nr>\d+)\s
            (?P<tpg_id>-?\d+)\s
            (?P<flags>\d+)\s
            (?P<minflt>\d+)\s
            (?P<cminflt>\d+)\s
            (?P<majflt>\d+)\s
            (?P<cmajflt>\d+)\s
            (?P<utime>\d+)\s
            (?P<stime>\d+)\s
            (?P<cutime>\d+)\s
            (?P<cstime>\d+)\s
            (?P<priority>\d+)\s
            (?P<nice>\d+)\s
            (?P<num_threads>\d+)\s
            (?P<itrealvalue>\d+)\s
            (?P<starttime>\d+)\s
            (?P<vsize>\d+)\s
            (?P<rss>\d+)\s
            (?P<rsslim>\d+)\s
            (?P<startcode>\d+)\s
            (?P<endcode>\d+)\s
            (?P<startstack>\d+)\s
            (?P<kstkeep>\d+)\s
            (?P<kstkeip>\d+)\s
            (?P<signal>\d+)\s
            (?P<blocked>\d+)\s
            (?P<sigignore>\d+)\s
            (?P<sigcatch>\d+)\s
            (?P<wchan>\d+)\s
            (?P<nswap>\d+)\s
            (?P<cnswap>\d+)\s
            (?P<exit_signal>\d+)\s
            (?P<processor>\d+)\s
            (?P<rt_priority>\d+)\s
            (?P<policy>\d+)\s
            (?P<delayacct_blkio_ticks>\d+)\s
            (?P<guest_time>\d+)\s
            (?P<cguest_time>\d+)\s
            (?P<start_data>\d+)\s
            (?P<end_data>\d+)\s
            (?P<start_brk>\d+)\s
            (?P<arg_start>\d+)\s
            (?P<arg_end>\d+)\s
            (?P<env_start>\d+)\s
            (?P<env_end>\d+)\s
            (?P<exit_code>\d+)
        ''', re.VERBOSE | re.DOTALL
        )

        line_match = line_re.search(data)

        if line_match:
            raw_output = line_match.groupdict()

    return raw_output if raw else _process(raw_output)
