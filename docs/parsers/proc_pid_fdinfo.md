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
      "flags":                      integer,  # [0]
      "mnt_id":                     integer,
      "scm_fds":                    string,
      "ino":                        integer,
      "lock": [
                                    string
      ],
      "epoll": [
        {
          "tfd":                    integer,
          "events":                 string,
          "data":                   string,
          "pos":                    integer,
          "ino":                    string,
          "sdev":                   string
        }
      ],
      "inotify": [
        {
          "wd":                     integer,  # [1]
          "ino":                    string,
          "sdev":                   string,
          "mask":                   string,
          "ignored_mask":           string,
          "fhandle-bytes":          string,
          "fhandle-type":           string,
          "f_handle":               string
        }
      ],
      "fanotify": {
        "flags":                    string,
        "event-flags":              string,
        "marks": [
          {
            "mnt_id":               string,
            "mnt_ns":               string,
            "mflags":               string,
            "mask":                 string,
            "ignored_mask":         string,
            "ino":                  string,
            "sdev":                 string,
            "fhandle-bytes":        string,
            "fhandle-type":         string,
            "f_handle":             string
          }
        ]
      },
      "clockid":                    integer,
      "ticks":                      integer,
      "settime flags":              integer,  # [0]
      "it_value": [
                                    integer
      ],
      "it_interval": [
                                    integer
      ]
    }

    [0] converted from octal
    [1] converted from hexadecimal

Examples:

    $ cat /proc/1/fdinfo/5 | jc --proc -p
    {
      "pos": 0,
      "flags": 526336,
      "mnt_id": 19,
      "ino": 84,
      "inotify": [
        {
          "wd": 11,
          "ino": "9360d8",
          "sdev": "fc00000",
          "mask": "2",
          "ignored_mask": "0",
          "fhandle-bytes": "c",
          "fhandle-type": "81",
          "f_handle": "d8609300000000000ab79f4e"
        },
        {
          "wd": 10,
          "ino": "9360d7",
          "sdev": "fc00000",
          "mask": "2",
          "ignored_mask": "0",
          "fhandle-bytes": "c",
          "fhandle-type": "81",
          "f_handle": "d7609300000000005bcd4b8d"
        }
      ]
    }

    $ cat /proc/1/fdinfo/5 | jc --proc -p -r
    {
      "pos": "0",
      "flags": "02004000",
      "mnt_id": "19",
      "ino": "84",
      "inotify": [
        {
          "wd": "b",
          "ino": "9360d8",
          "sdev": "fc00000",
          "mask": "2",
          "ignored_mask": "0",
          "fhandle-bytes": "c",
          "fhandle-type": "81",
          "f_handle": "d8609300000000000ab79f4e"
        },
        {
          "wd": "a",
          "ino": "9360d7",
          "sdev": "fc00000",
          "mask": "2",
          "ignored_mask": "0",
          "fhandle-bytes": "c",
          "fhandle-type": "81",
          "f_handle": "d7609300000000005bcd4b8d"
        }
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

Version 2.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
