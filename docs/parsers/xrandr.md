[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.xrandr"></a>

# jc.parsers.xrandr

jc - JSON CLI output utility `xrandr` command output parser

Usage (cli):

    $ xrandr | jc --xrandr

    or

    $ jc xrandr

Usage (module):

    import jc
    result = jc.parse('xrandr', xrandr_command_output)

    or

    import jc.parsers.xrandr
    result = jc.parsers.xrandr.parse(xrandr_command_output)

Schema:

    {
      "screens": [
        {
          "screen_number":                     integer,
          "minimum_width":                     integer,
          "minimum_height":                    integer,
          "current_width":                     integer,
          "current_height":                    integer,
          "maximum_width":                     integer,
          "maximum_height":                    integer,
          "associated_device": {
          "associated_modes": [
            {
            "resolution_width":                integer,
            "resolution_height":               integer,
            "is_high_resolution":              boolean,
            "frequencies": [
              {
              "frequency":                     float,
              "is_current":                    boolean,
              "is_preferred":                  boolean
              }
          ],
          "is_connected":                      boolean,
          "is_primary":                        boolean,
          "device_name":                       string,
          "resolution_width":                  integer,
          "resolution_height":                 integer,
          "offset_width":                      integer,
          "offset_height":                     integer,
          "dimension_width":                   integer,
          "dimension_height":                  integer
          }
        }
      ],
      "unassociated_devices": [
        {
          "associated_modes": [
            {
              "resolution_width":              integer,
              "resolution_height":             integer,
              "is_high_resolution":            boolean,
              "frequencies": [
                {
                  "frequency":                 float,
                  "is_current":                boolean,
                  "is_preferred":              boolean
                }
              ]
            }
          ]
        }
      ]
    }

Examples:

    $ xrandr | jc --xrandr

<a id="jc.parsers.xrandr.parse"></a>

### parse

```python
def parse(data: str, raw=False, quiet=False)
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

### Parser Information
Compatibility:  linux, darwin, cygwin, aix, freebsd

Version 1.0 by Kevin Lyter (lyter_git at sent.com)
