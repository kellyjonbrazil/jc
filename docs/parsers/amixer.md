[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.amixer"></a>

# jc.parsers.amixer

jc - JSON Convert `amixer sget` command output parser

Usage (cli):

    $ amixer sget <control_name> | jc --amixer
    $ amixer sget Master | jc --amixer
    $ amixer sget Capture | jc --amixer
    $ amixer sget Speakers | jc --amixer

Usage (module):

    import jc
    result = jc.parse('amixer', <amixer_sget_command_output>)

Schema:

    {
        "control_name":                     string,
        "capabilities": [
                                            string
        ],
        "playback_channels": [
                                            string
        ],
        "limits": {
            "playback_min":                 integer,
            "playback_max":                 integer
        },
        "mono": {
            "playback_value":               integer,
            "percentage":                   integer,
            "db":                           float,
            "status":                       boolean
        }
    }

Examples:

    $ amixer sget Master | jc --amixer -p
    {
      "control_name": "Capture",
      "capabilities": [
        "cvolume",
        "cswitch"
      ],
      "playback_channels": [],
      "limits": {
        "playback_min": 0,
        "playback_max": 63
      },
      "front_left": {
        "playback_value": 63,
        "percentage": 100,
        "db": 30.0,
        "status": true
      },
      "front_right": {
        "playback_value": 63,
        "percentage": 100,
        "db": 30.0,
        "status": true
      }
    }

    $ amixer sget Master | jc --amixer -p -r
    {
        "control_name": "Master",
        "capabilities": [
            "pvolume",
            "pvolume-joined",
            "pswitch",
            "pswitch-joined"
        ],
        "playback_channels": [
            "Mono"
        ],
        "limits": {
            "playback_min": "0",
            "playback_max": "87"
        },
        "mono": {
            "playback_value": "87",
            "percentage": "100%",
            "db": "0.00db",
            "status": "on"
        }
    }

<a id="jc.parsers.amixer.parse"></a>

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

Source: [`jc/parsers/amixer.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/amixer.py)

Version 1.0 by Eden Refael (edenraf@hotmail.com)
