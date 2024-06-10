[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.apt_get_sqq"></a>

# jc.parsers.apt_get_sqq

jc - JSON Convert `apt-get -sqq` command output parser

Requires the `-sqq` options in `apt-get`.

Usage (cli):

    $ apt-get -sqq upgrade | jc --apt-get-sqq

or

    $ jc apt-get -sqq full-upgrade

Usage (module):

    import jc
    result = jc.parse('apt_get_sqq', apt_get_sqq_command_output)

Schema:

    [
      {
        "operation":            string,       # configure, remove, or unpack
        "package":              string,
        "broken":               string/null,
        "proposed_pkg_ver":     string,
        "existing_pkg_ver":     string/null,
        "architecture":         string
      }
    ]

Examples:

    $ apt-get -sqq upgrade | jc --apt-get-sqq -p
    [
      {
        "operation": "unpack",
        "package": "dpkg",
        "broken": "1.19.7",
        "proposed_pkg_ver": "1.19.8 Debian:10.13/oldstable",
        "existing_pkg_ver": "Debian-Security:10/oldstable",
        "architecture": "amd64"
      },
      {
        "operation": "unpack",
        "package": "dpkg",
        "broken": null,
        "proposed_pkg_ver": "1.19.8 Debian:10.13/oldstable",
        "existing_pkg_ver": "Debian-Security:10/oldstable",
        "architecture": "amd64"
      },
      {
        "operation": "configure",
        "package": "dpkg",
        "broken": "1.19.7",
        "proposed_pkg_ver": "1.19.8 Debian:10.13/oldstable",
        "existing_pkg_ver": "Debian-Security:10/oldstable",
        "architecture": "amd64"
      },
      {
        "operation": "remove",
        "package": "dpkg",
        "broken": "1.19.7",
        "proposed_pkg_ver": "1.19.8 Debian:10.13/oldstable",
        "existing_pkg_ver": "Debian-Security:10/oldstable",
        "architecture": "amd64"
      },
      {
        "operation": "unpack",
        "package": "base-files",
        "broken": "10.3+deb10u4",
        "proposed_pkg_ver": "10.3+deb10u13 Debian:10.13/oldstable",
        "existing_pkg_ver": null,
        "architecture": "amd64"
      },
      {
        "operation": "configure",
        "package": "base-files",
        "broken": null,
        "proposed_pkg_ver": "10.3+deb10u13 Debian:10.13/oldstable",
        "existing_pkg_ver": null,
        "architecture": "amd64"
      },
      {
        "operation": "unpack",
        "package": "dpkg",
        "broken": "1.19.7",
        "proposed_pkg_ver": "1.19.8 Debian:10.13/oldstable",
        "existing_pkg_ver": "Debian-Security:10/oldstable",
        "architecture": "amd64"
      },
      {
        "operation": "configure",
        "package": "dpkg",
        "broken": null,
        "proposed_pkg_ver": "1.19.8 Debian:10.13/oldstable",
        "existing_pkg_ver": "Debian-Security:10/oldstable",
        "architecture": "amd64"
      }
    ]

    $ apt-get -sqq upgrade | jc --apt-get-sqq -p -r
    [
      {
        "operation": "Inst",
        "package": "dpkg",
        "broken": "1.19.7",
        "proposed_pkg_ver": "1.19.8 Debian:10.13/oldstable",
        "existing_pkg_ver": "Debian-Security:10/oldstable",
        "architecture": "amd64"
      },
      {
        "operation": "Inst",
        "package": "dpkg",
        "broken": null,
        "proposed_pkg_ver": "1.19.8 Debian:10.13/oldstable",
        "existing_pkg_ver": "Debian-Security:10/oldstable",
        "architecture": "amd64"
      },
      {
        "operation": "Conf",
        "package": "dpkg",
        "broken": "1.19.7",
        "proposed_pkg_ver": "1.19.8 Debian:10.13/oldstable",
        "existing_pkg_ver": "Debian-Security:10/oldstable",
        "architecture": "amd64"
      },
      {
        "operation": "Remv",
        "package": "dpkg",
        "broken": "1.19.7",
        "proposed_pkg_ver": "1.19.8 Debian:10.13/oldstable",
        "existing_pkg_ver": "Debian-Security:10/oldstable",
        "architecture": "amd64"
      },
      {
        "operation": "Inst",
        "package": "base-files",
        "broken": "10.3+deb10u4",
        "proposed_pkg_ver": "10.3+deb10u13 Debian:10.13/oldstable",
        "existing_pkg_ver": null,
        "architecture": "amd64"
      },
      {
        "operation": "Conf",
        "package": "base-files",
        "broken": null,
        "proposed_pkg_ver": "10.3+deb10u13 Debian:10.13/oldstable",
        "existing_pkg_ver": null,
        "architecture": "amd64"
      },
      {
        "operation": "Inst",
        "package": "dpkg",
        "broken": "1.19.7",
        "proposed_pkg_ver": "1.19.8 Debian:10.13/oldstable",
        "existing_pkg_ver": "Debian-Security:10/oldstable",
        "architecture": "amd64"
      },
      {
        "operation": "Conf",
        "package": "dpkg",
        "broken": null,
        "proposed_pkg_ver": "1.19.8 Debian:10.13/oldstable",
        "existing_pkg_ver": "Debian-Security:10/oldstable",
        "architecture": "amd64"
      }
    ]

<a id="jc.parsers.apt_get_sqq.parse"></a>

### parse

```python
def parse(data: str,
          raw: bool = False,
          quiet: bool = False) -> List[Dict[str, Any]]
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

Source: [`jc/parsers/apt_get_sqq.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/apt_get_sqq.py)

Version 1.1 by Kelly Brazil (kellyjonbrazil@gmail.com)
