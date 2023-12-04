[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.apkindex"></a>

# jc.parsers.apkindex

jc - JSON Convert Alpine Linux Package Index files

Usage (cli):

    $ jc --apkindex < APKINDEX

Usage (module):

    import jc
    result = jc.parse('apkindex', apkindex_output)

Schema:

    [
      {
        "checksum":             string,
        "package":              string,
        "version":              string,
        "architecture":         string,
        "package_size":         integer,
        "installed_size":       integer,
        "description":          string,
        "url":                  string,
        "license":              string,
        "origin":               string,
        "maintainer": {
          "name":               string,
          "email":              string,
        },
        "build_time":           integer,
        "commit":               string,
        "provider_priority":    string,
        "dependencies": [
                                string
        ],
        "provides": [
                                string
        ],
        "install_if": [
                                string
        ],
      }
    ]

Example:

    $ jc --apkindex < APKINDEX
    [
      {
        "checksum": "Q1znBl9k+RKgY6gl5Eg3iz73KZbLY=",
        "package": "yasm",
        "version": "1.3.0-r4",
        "architecture": "x86_64",
        "package_size": 772109,
        "installed_size": 1753088,
        "description": "A rewrite of NASM to allow for multiple synta...",
        "url": "http://www.tortall.net/projects/yasm/",
        "license": "BSD-2-Clause",
        "origin": "yasm",
        "maintainer": {
          "name": "Natanael Copa",
          "email": "ncopa@alpinelinux.org"
        },
        "build_time": 1681228881,
        "commit": "84a227baf001b6e0208e3352b294e4d7a40e93de",
        "dependencies": [
          "so:libc.musl-x86_64.so.1"
        ],
        "provides": [
          "cmd:vsyasm=1.3.0-r4",
          "cmd:yasm=1.3.0-r4",
          "cmd:ytasm=1.3.0-r4"
        ]
      }
    ]

    $ jc --apkindex --raw < APKINDEX
    [
      {
        "C": "Q1znBl9k+RKgY6gl5Eg3iz73KZbLY=",
        "P": "yasm",
        "V": "1.3.0-r4",
        "A": "x86_64",
        "S": "772109",
        "I": "1753088",
        "T": "A rewrite of NASM to allow for multiple syntax supported...",
        "U": "http://www.tortall.net/projects/yasm/",
        "L": "BSD-2-Clause",
        "o": "yasm",
        "m": "Natanael Copa <ncopa@alpinelinux.org>",
        "t": "1681228881",
        "c": "84a227baf001b6e0208e3352b294e4d7a40e93de",
        "D": "so:libc.musl-x86_64.so.1",
        "p": "cmd:vsyasm=1.3.0-r4 cmd:yasm=1.3.0-r4 cmd:ytasm=1.3.0-r4"
      },
    ]

<a id="jc.parsers.apkindex.parse"></a>

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

Version 1.0 by Roey Darwish Dror (roey.ghost@gmail.com)
