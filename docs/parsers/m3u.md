[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.m3u"></a>

# jc.parsers.m3u

jc - JSON Convert M3U and M3U8 file parser

This parser will make a best-effort to parse extended field information. If
the extended fields cannot be successfully parsed, then an `unparsed_info`
field will be added to the object. If not using `--quiet`, then a warning
message also will be printed to `STDERR`.

Usage (cli):

    $ cat playlist.m3u | jc --m3u

Usage (module):

    import jc
    result = jc.parse('m3u', m3u_file_output)

Schema:

    [
      {
        "runtime":              integer,
        "display":              string,
        "path":                 string,
        <extended fields>:      string,  # [0]
        "unparsed_info":        string,  # [1]
      }
    ]

    [0] Field names are pulled directly from the #EXTINF: line
    [1] Only added if the extended information cannot be parsed

Examples:

    $ cat playlist.m3u | jc --m3u -p
    [
      {
        "runtime": 105,
        "display": "Example artist - Example title",
        "path": "C:\\Files\\My Music\\Example.mp3"
      },
      {
        "runtime": 321,
        "display": "Example Artist2 - Example title2",
        "path": "C:\\Files\\My Music\\Favorites\\Example2.ogg"
      }
    ]

    $ cat playlist.m3u | jc --m3u -p -r
    [
      {
        "runtime": "105",
        "display": "Example artist - Example title",
        "path": "C:\\Files\\My Music\\Example.mp3"
      },
      {
        "runtime": "321",
        "display": "Example Artist2 - Example title2",
        "path": "C:\\Files\\My Music\\Favorites\\Example2.ogg"
      }
    ]

<a id="jc.parsers.m3u.parse"></a>

### parse

```python
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[Dict]
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

Source: [`jc/parsers/m3u.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/m3u.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
