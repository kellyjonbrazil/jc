[Home](https://kellyjonbrazil.github.io/jc/)

# jc.parsers.vmstat_s
jc - JSON CLI output utility `vmstat` command output streaming parser

Options supported: `-a`, `-w`, `-d`, `-t`

The `epoch` calculated timestamp field is naive (i.e. based on the local time of the system the parser is run on)

The `epoch_utc` calculated timestamp field is timezone-aware and is only available if the timezone field is UTC.

Usage (cli):

    $ vmstat | jc --vmstat-s

> Note: When piping `jc` converted `vmstat` output to other processes it may appear the output is hanging due to the OS pipe buffers. This is because `vmstat` output is too small to quickly fill up the buffer. Use the `-u` option to unbuffer the `jc` output if you would like immediate output. See the [readme](https://github.com/kellyjonbrazil/jc/tree/master#unbuffering-output) for more information.

Usage (module):

    import jc.parsers.vmstat_s
    result = jc.parsers.vmstat_s.parse(vmstat_command_output.splitlines())    # result is an iterable object
    for item in result:
        # do something

Schema:

    {
      "runnable_procs":                    integer,
      "uninterruptible_sleeping_procs":    integer,
      "virtual_mem_used":                  integer,
      "free_mem":                          integer,
      "buffer_mem":                        integer,
      "cache_mem":                         integer,
      "inactive_mem":                      integer,
      "active_mem":                        integer,
      "swap_in":                           integer,
      "swap_out":                          integer,
      "blocks_in":                         integer,
      "blocks_out":                        integer,
      "interrupts":                        integer,
      "context_switches":                  integer,
      "user_time":                         integer,
      "system_time":                       integer,
      "idle_time":                         integer,
      "io_wait_time":                      integer,
      "stolen_time":                       integer,
      "disk":                              string,
      "total_reads":                       integer,
      "merged_reads":                      integer,
      "sectors_read":                      integer,
      "reading_ms":                        integer,
      "total_writes":                      integer,
      "merged_writes":                     integer,
      "sectors_written":                   integer,
      "writing_ms":                        integer,
      "current_io":                        integer,
      "io_seconds":                        integer,
      "timestamp":                         string,
      "timezone":                          string,
      "epoch":                             integer,     # naive timestamp if -t flag is used
      "epoch_utc":                         integer      # aware timestamp if -t flag is used and UTC TZ
      "_jc_meta":                                       # This object only exists if using -qq or ignore_exceptions=True
        {
          "success":                       booean,      # true if successfully parsed, false if error
          "error":                         string,      # exists if "success" is false
          "line":                          string       # exists if "success" is false
        }
    }

Examples:

    $ vmstat | jc --vmstat-s
    {"runnable_procs":2,"uninterruptible_sleeping_procs":0,"virtual_mem_used":0,"free_mem":2794468,"buffer_mem":2108,"cache_mem":741208,"inactive_mem":null,"active_mem":null,"swap_in":0,"swap_out":0,"blocks_in":1,"blocks_out":3,"interrupts":29,"context_switches":57,"user_time":0,"system_time":0,"idle_time":99,"io_wait_time":0,"stolen_time":0,"timestamp":null,"timezone":null}
    ...

    $ vmstat | jc --vmstat-s -r
    {"runnable_procs":"2","uninterruptible_sleeping_procs":"0","virtual_mem_used":"0","free_mem":"2794468","buffer_mem":"2108","cache_mem":"741208","inactive_mem":null,"active_mem":null,"swap_in":"0","swap_out":"0","blocks_in":"1","blocks_out":"3","interrupts":"29","context_switches":"57","user_time":"0","system_time":"0","idle_time":"99","io_wait_time":"0","stolen_time":"0","timestamp":null,"timezone":null}
    ...


## info
```python
info()
```
Provides parser metadata (version, author, etc.)

## parse
```python
parse(data, raw=False, quiet=False, ignore_exceptions=False)
```

Main text parsing generator function. Returns an iterator object.

Parameters:

    data:              (iterable)  line-based text data to parse (e.g. sys.stdin or str.splitlines())
    raw:               (boolean)   output preprocessed JSON if True
    quiet:             (boolean)   suppress warning messages if True
    ignore_exceptions: (boolean)   ignore parsing exceptions if True

Yields:

    Dictionary. Raw or processed structured data.

Returns:

    Iterator object

## Parser Information
Compatibility:  linux

Version 0.5 by Kelly Brazil (kellyjonbrazil@gmail.com)
