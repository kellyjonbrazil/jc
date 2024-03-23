[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.srt"></a>

# jc.parsers.srt

jc - JSON Convert `SRT` file parser

Usage (cli):

    $ cat foo.srt | jc --srt

Usage (module):

    import jc
    result = jc.parse('srt', srt_file_output)

Schema:

    [
      {
        "index":              int,
        "start": {
          "hours":            int,
          "minutes":          int,
          "seconds":          int,
          "milliseconds":     int,
          "timestamp":        string
        },
        "end": {
          "hours":            int,
          "minutes":          int,
          "seconds":          int,
          "milliseconds":     int,
          "timestamp":        string
        },
        "content":            string
      }
    ]

Examples:

    $ cat attack_of_the_clones.srt
    1
    00:02:16,612 --> 00:02:19,376
    Senator, we're making
    our final approach into Coruscant.

    2
    00:02:19,482 --> 00:02:21,609
    Very good, Lieutenant.
    ...

    $ cat attack_of_the_clones.srt | jc --srt
    [
        {
            "index": 1,
            "start": {
                "hours": 0,
                "minutes": 2,
                "seconds": 16,
                "milliseconds": 612,
                "timestamp": "00:02:16,612"
            },
            "end": {
                "hours": 0,
                "minutes": 2,
                "seconds": 19,
                "milliseconds": 376,
                "timestamp": "00:02:19,376"
            },
            "content": "Senator, we're making\nour final approach into Coruscant."
        },
        {
            "index": 2,
            "start": {
                "hours": 0,
                "minutes": 2,
                "seconds": 19,
                "milliseconds": 482,
                "timestamp": "00:02:19,482"
            },
            "end": {
                "hours": 0,
                "minutes": 2,
                "seconds": 21,
                "milliseconds": 609,
                "timestamp": "00:02:21,609"
            },
            "content": "Very good, Lieutenant."
        },
        ...
    ]

<a id="jc.parsers.srt.parse"></a>

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

    Dictionary. Raw or processed structured data.

### Parser Information
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Source: [`jc/parsers/srt.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/srt.py)

Version 1.0 by Mark Rotner (rotner.mr@gmail.com)
