[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.id"></a>

# jc.parsers.id

jc - JSON Convert `id` command output parser

Usage (cli):

    $ id | jc --id

or

    $ jc id

Usage (module):

    import jc
    result = jc.parse('id', id_command_output)

Schema:

    {
      "uid": {
        "id":       integer,
        "name":     string
      },
      "gid": {
        "id":       integer,
        "name":     string
      },
      "groups": [
        {
          "id":     integer,
          "name":   string
        },
        {
          "id":     integer,
          "name":   string
        }
      ],
      "context": {
        "user":     string,
        "role":     string,
        "type":     string,
        "level":    string
      }
    }

Examples:

    $ id | jc --id -p
    {
      "uid": {
        "id": 1000,
        "name": "joeuser"
      },
      "gid": {
        "id": 1000,
        "name": "joeuser"
      },
      "groups": [
        {
          "id": 1000,
          "name": "joeuser"
        },
        {
          "id": 10,
          "name": "wheel"
        }
      ],
      "context": {
        "user": "unconfined_u",
        "role": "unconfined_r",
        "type": "unconfined_t",
        "level": "s0-s0:c0.c1023"
      }
    }

    $ id | jc --id -p -r
    {
      "uid": {
        "id": "1000",
        "name": "joeuser"
      },
      "gid": {
        "id": "1000",
        "name": "joeuser"
      },
      "groups": [
        {
          "id": "1000",
          "name": "joeuser"
        },
        {
          "id": "10",
          "name": "wheel"
        }
      ],
      "context": {
        "user": "unconfined_u",
        "role": "unconfined_r",
        "type": "unconfined_t",
        "level": "s0-s0:c0.c1023"
      }
    }

<a id="jc.parsers.id.parse"></a>

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

    Dictionary. Raw or processed structured data.

### Parser Information
Compatibility:  linux, darwin, aix, freebsd

Source: [`jc/parsers/id.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/id.py)

This parser can be used with the `--slurp` command-line option.

Version 1.7 by Kelly Brazil (kellyjonbrazil@gmail.com)
