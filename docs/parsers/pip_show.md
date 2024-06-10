[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.pip_show"></a>

# jc.parsers.pip_show

jc - JSON Convert `pip-show` command output parser

Usage (cli):

    $ pip show | jc --pip-show

or

    $ jc pip show

Usage (module):

    import jc
    result = jc.parse('pip_show', pip_show_command_output)

Schema:

    [
      {
        "name":             string,
        "version":          string,
        "summary":          string,
        "home_page":        string,
        "author":           string,
        "author_email":     string,
        "license":          string,
        "location":         string,
        "requires":         string,
        "required_by":      string
      }
    ]

Examples:

    $ pip show wrapt jc wheel | jc --pip-show -p
    [
      {
        "name": "wrapt",
        "version": "1.11.2",
        "summary": "Module for decorators, wrappers and monkey patching.",
        "home_page": "https://github.com/GrahamDumpleton/wrapt",
        "author": "Graham Dumpleton",
        "author_email": "Graham.Dumpleton@gmail.com",
        "license": "BSD",
        "location": "/usr/local/lib/python3.7/site-packages",
        "requires": null,
        "required_by": "astroid"
      },
      {
        "name": "wheel",
        "version": "0.33.4",
        "summary": "A built-package format for Python.",
        "home_page": "https://github.com/pypa/wheel",
        "author": "Daniel Holth",
        "author_email": "dholth@fastmail.fm",
        "license": "MIT",
        "location": "/usr/local/lib/python3.7/site-packages",
        "requires": null,
        "required_by": null
      }
    ]

<a id="jc.parsers.pip_show.parse"></a>

### parse

```python
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[Dict]
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

### Parser Information
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Source: [`jc/parsers/pip_show.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/pip_show.py)

Version 1.5 by Kelly Brazil (kellyjonbrazil@gmail.com)
