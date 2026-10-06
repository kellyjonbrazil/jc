[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.ldd"></a>

# jc.parsers.ldd

jc - JSON Convert `ldd` command output parser

Supports the `-v` option or no options, and one or more `FILE`
arguments. `file` is `null` when only a single file was given, since
`ldd` doesn't echo the filename back in that case. `version_info` is
only populated when `-v` is used. Lines that aren't a recognized
dependency or version requirement (e.g. `not a dynamic executable`)
are skipped.

Usage (cli):

    $ ldd /bin/ls | jc --ldd

or

    $ jc ldd /bin/ls

Usage (module):

    import jc
    result = jc.parse('ldd', ldd_command_output)

Schema:

    [
      {
        "file":               string/null,
        "dependencies": [
          {
            "name":           string,
            "path":           string/null,  # [0]
            "address":        string/null   # [0]
          }
        ],
        "version_info": [
          {
            "for":            string,
            "requires": [
              {
                "name":       string,
                "version":    string,
                "path":       string
              }
            ]
          }
        ]
      }
    ]

    [0] null if the library was not found, or if `name` is itself the
        resolved path (e.g. the dynamic linker)

Examples:

    $ ldd /bin/ls | jc --ldd -p
    [
      {
        "file": null,
        "dependencies": [
          {
            "name": "linux-vdso.so.1",
            "path": null,
            "address": "0x00007fe5c22ef000"
          },
          {
            "name": "libselinux.so.1",
            "path": "/lib64/libselinux.so.1",
            "address": "0x00007fe5c2287000"
          },
          {
            "name": "libc.so.6",
            "path": "/lib64/libc.so.6",
            "address": "0x00007fe5c207f000"
          },
          {
            "name": "/lib64/ld-linux-x86-64.so.2",
            "path": null,
            "address": "0x00007fe5c22f1000"
          }
        ],
        "version_info": []
      }
    ]

    $ ldd -v /bin/ls /bin/cat | jc --ldd -p
    [
      {
        "file": "/bin/ls",
        "dependencies": [
          ...
        ],
        "version_info": [
          {
            "for": "/bin/ls",
            "requires": [
              {
                "name": "libselinux.so.1",
                "version": "LIBSELINUX_1.0",
                "path": "/lib64/libselinux.so.1"
              }
            ]
          }
        ]
      },
      {
        "file": "/bin/cat",
        "dependencies": [
          ...
        ],
        "version_info": [
          ...
        ]
      }
    ]

<a id="jc.parsers.ldd.parse"></a>

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

    List of Dictionaries. Raw or processed structured data.

### Parser Information
Compatibility:  linux

Source: [`jc/parsers/ldd.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/ldd.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
