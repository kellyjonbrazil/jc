[Home](https://kellyjonbrazil.github.io/jc/)

# jc.parsers.dpkg_l
jc - JSON CLI output utility `dpkg -l` command output parser

Set the `COLUMNS` environment variable to a large value to avoid field truncation. For example:

    $ COLUMNS=500 dpkg -l | jc --dpkg-l

Usage (cli):

    $ dpkg -l | jc --dpkg-l

    or

    $ jc dpkg -l

Usage (module):

    import jc.parsers.dpkg
    result = jc.parsers.dpkg.parse(dpkg_command_output)

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

Compatibility:

    'linux'

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
        "description": "Advanced Configuration and Power Interface event daemon",
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
        "description": "Advanced Configuration and Power Interface event daemon"
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

Version 1.1 by Kelly Brazil (kellyjonbrazil@gmail.com)
