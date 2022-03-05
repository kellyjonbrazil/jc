[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.xrandr"></a>

# jc.parsers.xrandr

jc - JSON Convert `xrandr` command output parser

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
                "resolution_width":            integer,
                "resolution_height":           integer,
                "is_high_resolution":          boolean,
                "frequencies": [
                  {
                    "frequency":               float,
                    "is_current":              boolean,
                    "is_preferred":            boolean
                  }
                ]
              }
            ]
          },
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

    $ xrandr | jc --xrandr -p
    {
      "screens": [
        {
          "screen_number": 0,
          "minimum_width": 8,
          "minimum_height": 8,
          "current_width": 1920,
          "current_height": 1080,
          "maximum_width": 32767,
          "maximum_height": 32767,
          "associated_device": {
            "associated_modes": [
              {
                "resolution_width": 1920,
                "resolution_height": 1080,
                "is_high_resolution": false,
                "frequencies": [
                  {
                    "frequency": 60.03,
                    "is_current": true,
                    "is_preferred": true
                  },
                  {
                    "frequency": 59.93,
                    "is_current": false,
                    "is_preferred": false
                  }
                ]
              },
              {
                "resolution_width": 1680,
                "resolution_height": 1050,
                "is_high_resolution": false,
                "frequencies": [
                  {
                    "frequency": 59.88,
                    "is_current": false,
                    "is_preferred": false
                  }
                ]
              }
            ],
            "is_connected": true,
            "is_primary": true,
            "device_name": "eDP1",
            "resolution_width": 1920,
            "resolution_height": 1080,
            "offset_width": 0,
            "offset_height": 0,
            "dimension_width": 310,
            "dimension_height": 170
          }
        }
      ],
      "unassociated_devices": []
    }

<a id="jc.parsers.xrandr.parse"></a>

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
Compatibility:  linux, darwin, cygwin, aix, freebsd

Version 1.0 by Kevin Lyter (lyter_git at sent.com)
