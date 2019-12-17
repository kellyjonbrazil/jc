# jc.parsers.pip_show
jc - JSON CLI output utility pip-show Parser

Usage:

    specify --pip-show as the first argument if the piped input is coming from pip show

Compatibility:

    'linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd'

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

## info
```python
info(self, /, *args, **kwargs)
```

## process
```python
process(proc_data)
```

Final processing to conform to the schema.

Parameters:

    proc_data:   (dictionary) raw structured data to process

Returns:

    dictionary   structured data with the following schema:

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

    dictionary   raw or processed structured data

