[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.update_alt_q"></a>

# jc.parsers.update_alt_q

jc - JSON Convert `update-alternatives --query` command output parser

Usage (cli):

    $ update-alternatives --query | jc --update-alt-q

or

    $ jc update-alternatives --query

Usage (module):

    import jc
    result = jc.parse('update_alt_q',
                      update_alternatives_query_command_output)

Schema:

    {
      "name":                 string,
      "link":                 string,
      "slaves": [
        {
          "name":             string,
          "path":             string
        }
      ],
      "status":               string,
      "best":                 string,
      "value":                string,   # (null if 'none')
      "alternatives": [
        {
          "alternative":      string,
          "priority":         integer,
          "slaves": [
            {
              "name":         string,
              "path":         string
            }
          ]
        }
      ]
    }

Examples:

    $ update-alternatives --query editor | jc --update-alt-q -p
    {
      "name": "editor",
      "link": "/usr/bin/editor",
      "slaves": [
        {
          "name": "editor.1.gz",
          "path": "/usr/share/man/man1/editor.1.gz"
        },
        {
          "name": "editor.da.1.gz",
          "path": "/usr/share/man/da/man1/editor.1.gz"
        }
      ],
      "status": "auto",
      "best": "/bin/nano",
      "value": "/bin/nano",
      "alternatives": [
        {
          "alternative": "/bin/ed",
          "priority": -100,
          "slaves": [
            {
              "name": "editor.1.gz",
              "path": "/usr/share/man/man1/ed.1.gz"
            }
          ]
        },
        {
          "alternative": "/bin/nano",
          "priority": 40,
          "slaves": [
            {
              "name": "editor.1.gz",
              "path": "/usr/share/man/man1/nano.1.gz"
            }
          ]
        }
      ]
    }

    $ update-alternatives --query | jc --update-alt-q -p -r
    {
      "name": "editor",
      "link": "/usr/bin/editor",
      "slaves": [
        {
          "name": "editor.1.gz",
          "path": "/usr/share/man/man1/editor.1.gz"
        },
        {
          "name": "editor.da.1.gz",
          "path": "/usr/share/man/da/man1/editor.1.gz"
        }
      ],
      "status": "auto",
      "best": "/bin/nano",
      "value": "/bin/nano",
      "alternatives": [
        {
          "alternative": "/bin/ed",
          "priority": "-100",
          "slaves": [
            {
              "name": "editor.1.gz",
              "path": "/usr/share/man/man1/ed.1.gz"
            }
          ]
        },
        {
          "alternative": "/bin/nano",
          "priority": "40",
          "slaves": [
            {
              "name": "editor.1.gz",
              "path": "/usr/share/man/man1/nano.1.gz"
            }
          ]
        }
      ]
    }

<a id="jc.parsers.update_alt_q.parse"></a>

### parse

```python
def parse(data: str, raw: bool = False, quiet: bool = False) -> Dict
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    Dictionary. Raw or processed structured data.

### Parser Information
Compatibility:  linux

Source: [`jc/parsers/update_alt_q.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/update_alt_q.py)

Version 1.2 by Kelly Brazil (kellyjonbrazil@gmail.com)
