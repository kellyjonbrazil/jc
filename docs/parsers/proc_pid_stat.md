[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_pid_stat"></a>

# jc.parsers.proc_pid_stat

jc - JSON Convert `/proc/<pid>/stat` file parser

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

<a id="jc.parsers.proc_pid_stat.parse"></a>

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

Source: [`jc/parsers/proc_pid_stat.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_pid_stat.py)

Version 1.2 by Kelly Brazil (kellyjonbrazil@gmail.com)
