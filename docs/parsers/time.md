[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.time"></a>

# jc.parsers.time

jc - JSON Convert `/usr/bin/time` command output parser

Output from `/usr/bin/time` is sent to `STDERR`, so the `-o` option can be
used to redirect the output to a file that can be read by `jc`.

Alternatively, the output from `/usr/bin/time` can be redirected to `STDOUT`
so `jc` can receive it.

> Note: `/usr/bin/time` is similar but different from the Bash builtin
> `time` command.

Usage (cli):

    $ /usr/bin/time -o timefile.out sleep 2; cat timefile.out | \\
      jc --time -p

Usage (module):

    import jc
    result = jc.parse('time', time_command_output)

Schema:

Source: https://www.freebsd.org/cgi/man.cgi?query=getrusage,
https://man7.org/linux/man-pages/man1/time.1.html

    {
      "real_time":                          float,
      "user_time":                          float,
      "system_time":                        float,
      "elapsed_time":                       string,
      "elapsed_time_hours":                 integer,
      "elapsed_time_minutes":               integer,
      "elapsed_time_seconds":               integer,
      "elapsed_time_centiseconds":          integer,
      "elapsed_time_total_seconds":         float,
      "cpu_percent":                        integer,   # null if ?
      "average_shared_text_size":           integer,
      "average_unshared_data_size":         integer,
      "average_unshared_stack_size":        integer,
      "average_shared_memory_size":         integer,
      "maximum_resident_set_size":          integer,
      "block_input_operations":             integer,   # [0]
      "block_output_operations":            integer,   # [1]
      "major_pagefaults":                   integer,
      "minor_pagefaults":                   integer,
      "swaps":                              integer,
      "page_reclaims":                      integer,
      "page_faults":                        integer,
      "messages_sent":                      integer,
      "messages_received":                  integer,
      "signals_received":                   integer,
      "voluntary_context_switches":         integer,
      "involuntary_context_switches":       integer
      "command_being_timed":                string,
      "average_stack_size":                 integer,
      "average_total_size":                 integer,
      "average_resident_set_size":          integer,
      "signals_delivered":                  integer,
      "page_size":                          integer,
      "exit_status":                        integer
    }

    [0] aka File system inputs
    [1] aka File system outputs

Examples:

    $ /usr/bin/time --verbose -o timefile.out sleep 2; cat timefile.out | \\
      jc --time -p
    {
      "command_being_timed": "sleep 2",
      "user_time": 0.0,
      "system_time": 0.0,
      "cpu_percent": 0,
      "elapsed_time": "0:02.00",
      "average_shared_text_size": 0,
      "average_unshared_data_size": 0,
      "average_stack_size": 0,
      "average_total_size": 0,
      "maximum_resident_set_size": 2084,
      "average_resident_set_size": 0,
      "major_pagefaults": 0,
      "minor_pagefaults": 72,
      "voluntary_context_switches": 2,
      "involuntary_context_switches": 1,
      "swaps": 0,
      "block_input_operations": 0,
      "block_output_operations": 0,
      "messages_sent": 0,
      "messages_received": 0,
      "signals_delivered": 0,
      "page_size": 4096,
      "exit_status": 0,
      "elapsed_time_hours": 0,
      "elapsed_time_minutes": 0,
      "elapsed_time_seconds": 2,
      "elapsed_time_centiseconds": 50,
      "elapsed_time_total_seconds": 2.5
    }

    $ /usr/bin/time --verbose -o timefile.out sleep 2; cat timefile.out | \\
      jc --time -p -r
    {
      "command_being_timed": "\"sleep 2\"",
      "user_time": "0.00",
      "system_time": "0.00",
      "cpu_percent": "0",
      "elapsed_time": "0:02.00",
      "average_shared_text_size": "0",
      "average_unshared_data_size": "0",
      "average_stack_size": "0",
      "average_total_size": "0",
      "maximum_resident_set_size": "2084",
      "average_resident_set_size": "0",
      "major_pagefaults": "0",
      "minor_pagefaults": "72",
      "voluntary_context_switches": "2",
      "involuntary_context_switches": "0",
      "swaps": "0",
      "block_input_operations": "0",
      "block_output_operations": "0",
      "messages_sent": "0",
      "messages_received": "0",
      "signals_delivered": "0",
      "page_size": "4096",
      "exit_status": "0"
    }

<a id="jc.parsers.time.parse"></a>

### parse

```python
def parse(data, raw=False, quiet=False)
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    Dictionary. Raw or processed structured data.

### Parser Information
Compatibility:  linux, darwin, cygwin, aix, freebsd

Source: [`jc/parsers/time.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/time.py)

Version 1.5 by Kelly Brazil (kellyjonbrazil@gmail.com)
