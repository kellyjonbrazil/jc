[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.vmstat_s"></a>

# jc.parsers.vmstat_s

jc - JSON Convert `vmstat` command output streaming parser

> This streaming parser outputs JSON Lines (cli) or returns an Iterable of
> Dictionaries (module)

Options supported: `-a`, `-w`, `-d`, `-t`

The `epoch` calculated timestamp field is naive. (i.e. based on the local
time of the system the parser is run on)

The `epoch_utc` calculated timestamp field is timezone-aware and is only
available if the timezone field is UTC.

Usage (cli):

    $ vmstat | jc --vmstat-s

> Note: When piping `jc` converted `vmstat` output to other processes it may
> appear the output is hanging due to the OS pipe buffers. This is because
> `vmstat` output is too small to quickly fill up the buffer. Use the `-u`
> option to unbuffer the `jc` output if you would like immediate output. See
> the [readme](https://github.com/kellyjonbrazil/jc/tree/master#unbuffering-output)
> for more information.

Usage (module):

    import jc

    result = jc.parse('vmstat_s', vmstat_command_output.splitlines())
    for item in result:
        # do something

Schema:

    {
      "runnable_procs":                   integer,
      "uninterruptible_sleeping_procs":   integer,
      "virtual_mem_used":                 integer,
      "free_mem":                         integer,
      "buffer_mem":                       integer,
      "cache_mem":                        integer,
      "inactive_mem":                     integer,
      "active_mem":                       integer,
      "swap_in":                          integer,
      "swap_out":                         integer,
      "blocks_in":                        integer,
      "blocks_out":                       integer,
      "interrupts":                       integer,
      "context_switches":                 integer,
      "user_time":                        integer,
      "system_time":                      integer,
      "idle_time":                        integer,
      "io_wait_time":                     integer,
      "stolen_time":                      integer,
      "disk":                             string,
      "total_reads":                      integer,
      "merged_reads":                     integer,
      "sectors_read":                     integer,
      "reading_ms":                       integer,
      "total_writes":                     integer,
      "merged_writes":                    integer,
      "sectors_written":                  integer,
      "writing_ms":                       integer,
      "current_io":                       integer,
      "io_seconds":                       integer,
      "timestamp":                        string,
      "timezone":                         string,
      "epoch":                            integer,     # [0]
      "epoch_utc":                        integer      # [1]

      # below object only exists if using -qq or ignore_exceptions=True
      "_jc_meta": {
        "success":                        boolean,     # [2]
        "error":                          string,      # [3]
        "line":                           string       # [3]
      }
    }

    [0] naive timestamp if -t flag is used
    [1] aware timestamp if -t flag is used and UTC TZ
    [2] false if error parsing
    [3] exists if "success" is false

Examples:

    $ vmstat | jc --vmstat-s
    {"runnable_procs":2,"uninterruptible_sleeping_procs":0,"virtual_mem...}
    ...

    $ vmstat | jc --vmstat-s -r
    {"runnable_procs":"2","uninterruptible_sleeping_procs":"0","virtua...}
    ...

<a id="jc.parsers.vmstat_s.parse"></a>

### parse

```python
def parse(data, raw=False, quiet=False, ignore_exceptions=False)
```

Main text parsing generator function. Returns an iterable object.

Parameters:

    data:              (iterable)  line-based text data to parse
                                   (e.g. sys.stdin or str.splitlines())

    raw:               (boolean)   unprocessed output if True
    quiet:             (boolean)   suppress warning messages if True
    ignore_exceptions: (boolean)   ignore parsing exceptions if True

Returns:

    Iterable of Dictionaries

### Parser Information
Compatibility:  linux

Source: [`jc/parsers/vmstat_s.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/vmstat_s.py)

Version 1.3 by Kelly Brazil (kellyjonbrazil@gmail.com)
