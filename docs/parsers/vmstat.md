[Home](https://kellyjonbrazil.github.io/jc/)

# jc.parsers.vmstat
jc - JSON CLI output utility `vmstat` command output parser

Options supported: `-a`, `-w`, `-d`, `-t`

Usage (cli):

    $ vmstat | jc --vmstat

    or

    $ jc vmstat

Usage (module):

    import jc.parsers.vmstat
    result = jc.parsers.vmstat.parse(vmstat_command_output)

Schema:

    [
      {
        'runnable_procs':                    integer,
        'uninterruptible_sleeping_procs':    integer,
        'virtual_mem_used':                  integer,
        'free_mem':                          integer,
        'buffer_mem':                        integer,
        'cache_mem':                         integer,
        'inactive_mem':                      integer,
        'active_mem':                        integer,
        'swap_in':                           integer,
        'swap_out':                          integer,
        'blocks_in':                         integer,
        'blocks_out':                        integer,
        'interrupts':                        integer,
        'context_switches':                  integer,
        'user_time':                         integer,
        'system_time':                       integer,
        'idle_time':                         integer,
        'io_wait_time':                      integer,
        'stolen_time':                       integer,
        'disk':                              string,
        'total_reads':                       integer,
        'merged_reads':                      integer,
        'sectors_read':                      integer,
        'reading_ms':                        integer,
        'total_writes':                      integer,
        'merged_writes':                     integer,
        'sectors_written':                   integer,
        'writing_ms':                        integer,
        'current_io':                        integer,
        'io_seconds':                        integer,
        'timestamp':                         string,
        'timezone':                          string,
        'epoch':                             integer,     # naive timestamp if -t flag is used
        'epoch_utc':                         integer      # aware timestamp if -t flag is used and UTC TZ
      }
    ]

Examples:

    $ vmstat | jc --vmstat -p
    [
      {
        "runnable_procs": 2,
        "uninterruptible_sleeping_procs": 0,
        "virtual_mem_used": 0,
        "free_mem": 2794468,
        "buffer_mem": 2108,
        "cache_mem": 741208,
        "inactive_mem": null,
        "active_mem": null,
        "swap_in": 0,
        "swap_out": 0,
        "blocks_in": 1,
        "blocks_out": 3,
        "interrupts": 29,
        "context_switches": 57,
        "user_time": 0,
        "system_time": 0,
        "idle_time": 99,
        "io_wait_time": 0,
        "stolen_time": 0,
        "timestamp": null,
        "timezone": null
      }
    ]

    $ vmstat | jc --vmstat -p -r
    [
      {
        "runnable_procs": "2",
        "uninterruptible_sleeping_procs": "0",
        "virtual_mem_used": "0",
        "free_mem": "2794468",
        "buffer_mem": "2108",
        "cache_mem": "741208",
        "inactive_mem": null,
        "active_mem": null,
        "swap_in": "0",
        "swap_out": "0",
        "blocks_in": "1",
        "blocks_out": "3",
        "interrupts": "29",
        "context_switches": "57",
        "user_time": "0",
        "system_time": "0",
        "idle_time": "99",
        "io_wait_time": "0",
        "stolen_time": "0",
        "timestamp": null,
        "timezone": null
      }
    ]


## info
```python
info()
```
Provides parser metadata (version, author, etc.)

## parse
```python
parse(data, raw=False, quiet=False)
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) output preprocessed JSON if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

## Parser Information
Compatibility:  linux

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
