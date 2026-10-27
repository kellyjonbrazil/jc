[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.apachectl"></a>

# jc.parsers.apachectl

jc - JSON Convert `apachectl -S` command output parser

Parses the virtual host summary and run configuration printed by
`apachectl -S`, which is a synonym for
`apachectl -t -D DUMP_VHOSTS -D DUMP_RUN_CFG`. This parser works with the
following commands:

- `apachectl -S`
- `apache2ctl -S` (Debian and Ubuntu)
- `apache2 -S` (Debian and Ubuntu)
- `httpd -S` (RHEL and Fedora)

The whole output becomes one object. `virtual_hosts` holds one entry per
virtual host, the server named by the `default server` line is marked, and
the `alias` and `wild alias` lines are collected on the entry they follow.
An IPv6 address is returned without the brackets the command prints. The run
configuration after the vhost list becomes top-level fields. Only the `-S`
output is parsed; a virtual host line whose shape doesn't match any of the
forms the command prints is skipped instead of failing the parse.

Usage (cli):

    $ apachectl -S | jc --apachectl

or

    $ jc apachectl -S

Usage (module):

    import jc
    result = jc.parse('apachectl', apachectl_command_output)

Schema:

    {
      "server_root":                     string,
      "main_document_root":              string,
      "main_error_log":                  string,
      "scoreboard_file":                 string,     # [0]
      "mutexes": [
        {
          "name":                        string,
          "using_defaults":              boolean,
          "none":                        boolean,
          "directory":                   string,     # [1]
          "mechanism":                   string,     # [1]
          "omit_pid":                    boolean
        }
      ],
      "pid_file":                        string,
      "defines": [
                                         string
      ],
      "user": {
        "name":                          string,
        "id":                            integer,
        "not_used":                      boolean
      },
      "group": {
        "name":                          string,
        "id":                            integer,
        "not_used":                      boolean
      },
      "chroot_dir":                      string,     # [0]
      "virtual_hosts": [
        {
          "address":                     string,     # [2]
          "port":                        string,     # [2]
          "port_num":                    integer,    # [3]
          "name":                        string,
          "default":                     boolean,
          "aliases": [
                                         string
          ],
          "wild_aliases": [
                                         string
          ],
          "path":                        string,
          "line":                        integer
        }
      ]
    }

    [0] omitted if not printed
    [1] null unless configured
    [2] '*' for a wildcard
    [3] omitted when port is '*'

Examples:

    $ apachectl -S | jc --apachectl -p
    {
      "server_root": "/etc/apache2",
      "main_document_root": "/var/www/html",
      "main_error_log": "/var/log/apache2/error.log",
      "mutexes": [
        {
          "name": "fcgid-proctbl",
          "using_defaults": true,
          "none": false,
          "directory": null,
          "mechanism": null,
          "omit_pid": false
        },
        ...
      ],
      "pid_file": "/var/run/apache2/apache2.pid",
      "defines": [
        "DUMP_VHOSTS",
        "DUMP_RUN_CFG"
      ],
      "user": {
        "name": "www-data",
        "id": 33,
        "not_used": false
      },
      "group": {
        "name": "www-data",
        "id": 33,
        "not_used": false
      },
      "virtual_hosts": [
        {
          "address": "127.0.0.1",
          "port": "80",
          "port_num": 80,
          "name": "localhost",
          "default": false,
          "aliases": [],
          "wild_aliases": [],
          "path": "/etc/apache2/sites-enabled/localhost.conf",
          "line": 4
        },
        ...
      ]
    }

<a id="jc.parsers.apachectl.parse"></a>

### parse

```python
def parse(data: str, raw: bool = False, quiet: bool = False) -> Dict[str, Any]
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    Dictionary. Raw or processed structured data.

### Parser Information
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Source: [`jc/parsers/apachectl.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/apachectl.py)

Version 1.1 by Tung Lam (53996158+tunglambk@users.noreply.github.com)
