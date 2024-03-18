[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.debconf_show"></a>

# jc.parsers.debconf_show

jc - JSON Convert `debconf-show` command output parser

Usage (cli):

    $ debconf-show onlyoffice-documentserver | jc --debconf-show

or

    $ jc debconf-show onlyoffice-documentserver

Usage (module):

    import jc
    result = jc.parse('debconf_show', debconf_show_command_output)

Schema:

    [
      {
        "asked":              boolean,
        "packagename":        string,
        "name":               string,
        "value":              string
      }
    ]

Examples:

    $ debconf-show onlyoffice-documentserver | jc --debconf-show -p
    [
      {
        "asked": true,
        "packagename": "onlyoffice",
        "name": "jwt_secret",
        "value": "aL8ei2iereuzee7cuJ6Cahjah1ixee2ah"
      },
      {
        "asked": false,
        "packagename": "onlyoffice",
        "name": "db_pwd",
        "value": "(password omitted)"
      },
      {
        "asked": true,
        "packagename": "onlyoffice",
        "name": "rabbitmq_pwd",
        "value": "(password omitted)"
      },
      {
        "asked": true,
        "packagename": "onlyoffice",
        "name": "db_port",
        "value": "5432"
      },
      {
        "asked": true,
        "packagename": "onlyoffice",
        "name": "db_user",
        "value": "onlyoffice"
      },
      {
        "asked": true,
        "packagename": "onlyoffice",
        "name": "rabbitmq_proto",
        "value": "amqp"
      },
      {
        "asked": true,
        "packagename": "onlyoffice",
        "name": "cluster_mode",
        "value": "false"
      }
    ]

<a id="jc.parsers.debconf_show.parse"></a>

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

Source: [`jc/parsers/debconf_show.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/debconf_show.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
