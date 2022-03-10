[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.pidstat_s"></a>

# jc.parsers.pidstat\_s

jc - JSON Convert `pidstat` command output streaming parser

> This streaming parser outputs JSON Lines

<<Short pidstat description and caveats>>

Usage (cli):

    $ pidstat | jc --pidstat-s

Usage (module):

    import jc
    # result is an iterable object (generator)
    result = jc.parse('pidstat_s', pidstat_command_output.splitlines())
    for item in result:
        # do something

    or

    import jc.parsers.pidstat_s
    # result is an iterable object (generator)
    result = jc.parsers.pidstat_s.parse(pidstat_command_output.splitlines())
    for item in result:
        # do something

Schema:

    {
      "pidstat":            string,

      # Below object only exists if using -qq or ignore_exceptions=True

      "_jc_meta":
        {
          "success":    boolean,     # false if error parsing
          "error":      string,      # exists if "success" is false
          "line":       string       # exists if "success" is false
        }
    }

Examples:

    $ pidstat | jc --pidstat-s
    {example output}
    ...

    $ pidstat | jc --pidstat-s -r
    {example output}
    ...

<a id="jc.parsers.pidstat_s.parse"></a>

### parse

```python
@add_jc_meta
def parse(data: Iterable[str],
          raw: bool = False,
          quiet: bool = False,
          ignore_exceptions: bool = False) -> Union[Iterable[Dict], tuple]
```

Main text parsing generator function. Returns an iterator object.

Parameters:

    data:              (iterable)  line-based text data to parse
                                   (e.g. sys.stdin or str.splitlines())

    raw:               (boolean)   unprocessed output if True
    quiet:             (boolean)   suppress warning messages if True
    ignore_exceptions: (boolean)   ignore parsing exceptions if True

Yields:

    Dictionary. Raw or processed structured data.

Returns:

    Iterator object (generator)

### Parser Information
Compatibility:  linux

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
