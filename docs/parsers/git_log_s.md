[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.git_log_s"></a>

# jc.parsers.git\_log\_s

jc - JSON Convert `git log` command output streaming parser

> This streaming parser outputs JSON Lines (cli) or returns an Iterable of
  Dictionaries (module)

Usage (cli):

    $ git log | jc --git-log-s

Usage (module):

    import jc

    result = jc.parse('git_log_s', git_log_command_output.splitlines())
    for item in result:
        # do something

Schema:

    {
      "git_log_s":            string,

      # below object only exists if using -qq or ignore_exceptions=True
      "_jc_meta": {
        "success":      boolean,     # false if error parsing
        "error":        string,      # exists if "success" is false
        "line":         string       # exists if "success" is false
      }
    }

Examples:

    $ git log | jc --git-log-s
    {example output}
    ...

    $ git log | jc --git-log-s -r
    {example output}
    ...

<a id="jc.parsers.git_log_s.parse"></a>

### parse

```python
@add_jc_meta
def parse(data: Iterable[str],
          raw: bool = False,
          quiet: bool = False,
          ignore_exceptions: bool = False) -> Union[Iterable[Dict], tuple]
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
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
