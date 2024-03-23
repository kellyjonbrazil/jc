[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_pid_fdinfo"></a>

# jc.parsers.proc_pid_fdinfo

jc - JSON Convert `/proc/<pid>/fdinfo/<fd>` file parser

Usage (cli):

    $ cat /proc/1/fdinfo/5 | jc --proc

or

    $ jc /proc/1/fdinfo/5

or

    $ cat /proc/1/fdinfo/5 | jc --proc-pid-fdinfo

Usage (module):

    import jc
    result = jc.parse('proc', proc_pid_fdinfo_file)

or

    import jc
    result = jc.parse('proc_pid_fdinfo', proc_pid_fdinfo_file)

Schema:

Any unspecified fields are strings.

    {
      "pos":                        integer,
      "flags":                      integer,
      "mnt_id":                     integer,
      "scm_fds":                    string,
      "ino":                        integer,
      "lock":                       string,
      "epoll": {
        "tfd":                      integer,
        "events":                   string,
        "data":                     string,
        "pos":                      integer,
        "ino":                      string,
        "sdev":                     string
      },
      "inotify": {
        "wd":                       integer,
        "ino":                      string,
        "sdev":                     string,
        "mask":                     string,
        "ignored_mask":             string,
        "fhandle-bytes":            string,
        "fhandle-type":             string,
        "f_handle":                 string
      },
      "fanotify": {
        "flags":                    string,
        "event-flags":              string,
        "mnt_id":                   string,
        "mflags":                   string,
        "mask":                     string,
        "ignored_mask":             string,
        "ino":                      string,
        "sdev":                     string,
        "fhandle-bytes":            string,
        "fhandle-type":             string,
        "f_handle":                 string
      },
      "clockid":                    integer,
      "ticks":                      integer,
      "settime flags":              integer,
      "it_value": [
                                    integer
      ],
      "it_interval": [
                                    integer
      ]
    }

Examples:

    $ cat /proc/1/fdinfo/5 | jc --proc -p
    {
      "pos": 0,
      "flags": 2,
      "mnt_id": 9,
      "ino": 63107,
      "clockid": 0,
      "ticks": 0,
      "settime flags": 1,
      "it_value": [
        0,
        49406829
      ],
      "it_interval": [
        1,
        0
      ]
    }

<a id="jc.parsers.proc_pid_fdinfo.parse"></a>

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

Source: [`jc/parsers/proc_pid_fdinfo.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_pid_fdinfo.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
