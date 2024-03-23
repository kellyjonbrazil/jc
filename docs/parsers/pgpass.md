[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.pgpass"></a>

# jc.parsers.pgpass

jc - JSON Convert PostgreSQL password file parser

Usage (cli):

    $ cat /var/lib/postgresql/.pgpass | jc --pgpass

Usage (module):

    import jc
    result = jc.parse('pgpass', postgres_password_file)

Schema:

    [
      {
        "hostname":               string,
        "port":                   string,
        "database":               string,
        "username":               string,
        "password":               string
      }
    ]

Examples:

    $ cat /var/lib/postgresql/.pgpass | jc --pgpass -p
    [
      {
        "hostname": "dbserver",
        "port": "*",
        "database": "db1",
        "username": "dbuser",
        "password": "pwd123"
      },
      {
        "hostname": "dbserver2",
        "port": "8888",
        "database": "inventory",
        "username": "joe:user",
        "password": "abc123"
      },
      ...
    ]

<a id="jc.parsers.pgpass.parse"></a>

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
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Source: [`jc/parsers/pgpass.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/pgpass.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
