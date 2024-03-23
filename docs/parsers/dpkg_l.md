[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.dpkg_l"></a>

# jc.parsers.dpkg_l

jc - JSON Convert `dpkg -l` command output parser

Set the `COLUMNS` environment variable to a large value to avoid field
truncation. For example:

    $ COLUMNS=500 dpkg -l | jc --dpkg-l

Usage (cli):

    $ dpkg -l | jc --dpkg-l

or

    $ jc dpkg -l

Usage (module):

    import jc
    result = jc.parse('dpkg_l', dpkg_command_output)

Schema:

    [
      {
        "codes":            string,
        "name":             string,
        "version":          string,
        "architecture":     string,
        "description":      string,
        "desired":          string,
        "status":           string,
        "error":            string
      }
    ]

Examples:

    $ dpkg -l | jc --dpkg-l -p
    [
      {
        "codes": "ii",
        "name": "accountsservice",
        "version": "0.6.45-1ubuntu1.3",
        "architecture": "amd64",
        "description": "query and manipulate user account information",
        "desired": "install",
        "status": "installed"
      },
      {
        "codes": "rc",
        "name": "acl",
        "version": "2.2.52-3build1",
        "architecture": "amd64",
        "description": "Access control list utilities",
        "desired": "remove",
        "status": "config-files"
      },
      {
        "codes": "uWR",
        "name": "acpi",
        "version": "1.7-1.1",
        "architecture": "amd64",
        "description": "displays information on ACPI devices",
        "desired": "unknown",
        "status": "trigger await",
        "error": "reinstall required"
      },
      {
        "codes": "rh",
        "name": "acpid",
        "version": "1:2.0.28-1ubuntu1",
        "architecture": "amd64",
        "description": "Advanced Configuration and Power Interface...",
        "desired": "remove",
        "status": "half installed"
      },
      {
        "codes": "pn",
        "name": "adduser",
        "version": "3.116ubuntu1",
        "architecture": "all",
        "description": "add and remove users and groups",
        "desired": "purge",
        "status": "not installed"
      },
      ...
    ]

    $ dpkg -l | jc --dpkg-l -p -r
    [
      {
        "codes": "ii",
        "name": "accountsservice",
        "version": "0.6.45-1ubuntu1.3",
        "architecture": "amd64",
        "description": "query and manipulate user account information"
      },
      {
        "codes": "rc",
        "name": "acl",
        "version": "2.2.52-3build1",
        "architecture": "amd64",
        "description": "Access control list utilities"
      },
      {
        "codes": "uWR",
        "name": "acpi",
        "version": "1.7-1.1",
        "architecture": "amd64",
        "description": "displays information on ACPI devices"
      },
      {
        "codes": "rh",
        "name": "acpid",
        "version": "1:2.0.28-1ubuntu1",
        "architecture": "amd64",
        "description": "Advanced Configuration and Power Interface..."
      },
      {
        "codes": "pn",
        "name": "adduser",
        "version": "3.116ubuntu1",
        "architecture": "all",
        "description": "add and remove users and groups"
      },
      ...
    ]

<a id="jc.parsers.dpkg_l.parse"></a>

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

Source: [`jc/parsers/dpkg_l.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/dpkg_l.py)

Version 1.3 by Kelly Brazil (kellyjonbrazil@gmail.com)
