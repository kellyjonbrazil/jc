[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.passwd"></a>

# jc.parsers.passwd

jc - JSON Convert `/etc/passwd` file Parser

Usage (cli):

    $ cat /etc/passwd | jc --passwd

Usage (module):

    import jc
    result = jc.parse('passwd', passwd_file_output)

Schema:

    [
      {
        "username":     string,
        "password":     string,
        "uid":          integer,
        "gid":          integer,
        "comment":      string,
        "home":         string,
        "shell":        string
      }
    ]

Examples:

    $ cat /etc/passwd | jc --passwd -p
    [
      {
        "username": "nobody",
        "password": "*",
        "uid": -2,
        "gid": -2,
        "comment": "Unprivileged User",
        "home": "/var/empty",
        "shell": "/usr/bin/false"
      },
      {
        "username": "root",
        "password": "*",
        "uid": 0,
        "gid": 0,
        "comment": "System Administrator",
        "home": "/var/root",
        "shell": "/bin/sh"
      },
      {
        "username": "daemon",
        "password": "*",
        "uid": 1,
        "gid": 1,
        "comment": "System Services",
        "home": "/var/root",
        "shell": "/usr/bin/false"
      },
      ...
    ]

    $ cat /etc/passwd | jc --passwd -p -r
    [
      {
        "username": "nobody",
        "password": "*",
        "uid": "-2",
        "gid": "-2",
        "comment": "Unprivileged User",
        "home": "/var/empty",
        "shell": "/usr/bin/false"
      },
      {
        "username": "root",
        "password": "*",
        "uid": "0",
        "gid": "0",
        "comment": "System Administrator",
        "home": "/var/root",
        "shell": "/bin/sh"
      },
      {
        "username": "daemon",
        "password": "*",
        "uid": "1",
        "gid": "1",
        "comment": "System Services",
        "home": "/var/root",
        "shell": "/usr/bin/false"
      },
      ...
    ]

<a id="jc.parsers.passwd.parse"></a>

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
Compatibility:  linux, darwin, aix, freebsd

Source: [`jc/parsers/passwd.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/passwd.py)

Version 1.4 by Kelly Brazil (kellyjonbrazil@gmail.com)
