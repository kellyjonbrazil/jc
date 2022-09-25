"""jc - JSON Convert `/proc/<pid>/stat` file parser

Usage (cli):

    $ cat /proc/1/stat | jc --proc

or

    $ jc /proc/1/stat

or

    $ cat /proc/1/stat | jc --proc-pid_stat

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

    $ cat /proc/1/stat | jc --proc -p -r
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
from typing import Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`/proc/<pid>/stat` file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
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
    }

    if 'state' in proc_data:
        proc_data['state_pretty'] = state_map[proc_data['state']]

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

        split_line = data.split()
        raw_output = {
            'pid': int(split_line[0]),
            'comm': split_line[1].strip('()'),
            'state': split_line[2],
            'ppid': int(split_line[3]),
            'pgrp': int(split_line[4]),
            'session': int(split_line[5]),
            'tty_nr': int(split_line[6]),
            'tpg_id': int(split_line[7]),
            'flags': int(split_line[8]),
            'minflt': int(split_line[9]),
            'cminflt': int(split_line[10]),
            'majflt': int(split_line[11]),
            'cmajflt': int(split_line[12]),
            'utime': int(split_line[13]),
            'stime': int(split_line[14]),
            'cutime': int(split_line[15]),
            'cstime': int(split_line[16]),
            'priority': int(split_line[17]),
            'nice': int(split_line[18]),
            'num_threads': int(split_line[19]),
            'itrealvalue': int(split_line[20]),
            'starttime': int(split_line[21]),
            'vsize': int(split_line[22]),
            'rss': int(split_line[23]),
            'rsslim': int(split_line[24]),
            'startcode': int(split_line[25]),
            'endcode': int(split_line[26]),
            'startstack': int(split_line[27]),
            'kstkeep': int(split_line[28]),
            'kstkeip': int(split_line[29]),
            'signal': int(split_line[30]),
            'blocked': int(split_line[31]),
            'sigignore': int(split_line[32]),
            'sigcatch': int(split_line[33]),
            'wchan': int(split_line[34]),
            'nswap': int(split_line[35]),
            'cnswap': int(split_line[36])
        }

        if len(split_line) > 37:
            raw_output['exit_signal'] = int(split_line[37])

        if len(split_line) > 38:
            raw_output['processor'] = int(split_line[38])

        if len(split_line) > 39:
            raw_output['rt_priority'] = int(split_line[39])
            raw_output['policy'] = int(split_line[40])

        if len(split_line) > 41:
            raw_output['delayacct_blkio_ticks'] = int(split_line[41])

        if len(split_line) > 42:
            raw_output['guest_time'] = int(split_line[42])
            raw_output['cguest_time'] = int(split_line[43])

        if len(split_line) > 44:
            raw_output['start_data'] = int(split_line[44])
            raw_output['end_data'] = int(split_line[45])
            raw_output['start_brk'] = int(split_line[46])

        if len(split_line) > 47:
            raw_output['arg_start'] = int(split_line[47])
            raw_output['arg_end'] = int(split_line[48])
            raw_output['env_start'] = int(split_line[49])
            raw_output['env_end'] = int(split_line[50])
            raw_output['exit_code'] = int(split_line[51])

    return raw_output if raw else _process(raw_output)
