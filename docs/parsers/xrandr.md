[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.xrandr"></a>

# jc.parsers.xrandr

jc - JSON Convert `xrandr` command output parser

Usage (cli):

    $ xrandr | jc --xrandr
    $ xrandr --properties | jc --xrandr

or

    $ jc xrandr

Usage (module):

    import jc
    result = jc.parse('xrandr', xrandr_command_output)

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
          "devices": [
            {
              "props": {

                # either an EdidModel object or key value pairs
                <key_name> : {
                  "name": string,
                  "product_id": string,
                  "serial_number": string,
                }

              },
              "resolution_modes": [
                {
                  "resolution_width":          integer,
                  "resolution_height":         integer,
                  "is_high_resolution":        boolean,
                  "frequencies": [
                    {
                      "frequency":             float,
                      "is_current":            boolean,
                      "is_preferred":          boolean
                    }
                  ]
                }
              ]
            }
          ],
          "is_connected":                      boolean,
          "is_primary":                        boolean,
          "device_name":                       string,
          "model_name":                        string,
          "product_id"                         string,
          "serial_number":                     string,
          "resolution_width":                  integer,
          "resolution_height":                 integer,
          "offset_width":                      integer,
          "offset_height":                     integer,
          "dimension_width":                   integer,
          "dimension_height":                  integer,
          "rotation":                          string,
          "reflection":                        string
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
          "devices": [
            {
              "resolution_modes": [
                {
                  "resolution_width": 1920,
                  "resolution_height": 1080,
                  "is_high_resolution": false,
                  "frequencies": [
                    {
                      "frequency": 60.03,
                      "is_current": true,
                      "is_preferred": true
                    }
                  ]
                },
              ],
              "is_connected": true,
              "is_primary": true,
              "device_name": "eDP1",
              "resolution_width": 1920,
              "resolution_height": 1080,
              "offset_width": 0,
              "offset_height": 0,
              "dimension_width": 310,
              "dimension_height": 170,
              "rotation": "normal",
              "reflection": "normal"
            }
          ]
        }
      ]
    }

    $ xrandr --properties | jc --xrandr -p
    {
      "screens": [
        {
          "devices": [
            {
              "props": {
                "EDID": [
                  "00ffff5700000000",
                  "001c01a5544d9a27",
                  "0e50540101010101",
                  "010101383e401010",
                  "3500350f00000000",
                  "0000000000fe0041",
                  "554f0a20000000fe",
                  "00423137200a0070"
                ],
                "scaling mode": [
                  "Full aspect ",
                  "supported: Full, Center, Full aspect"
                ],
                "Colorspace": [
                  "Default ",
                  "supported: Default, RGB_Wide_Gamut_Fixed_Point, RGB_Wide_Gamut_Floating_Point, opRGB, DCI-P3_RGB_D65, BT2020_RGB, BT601_YCC, BT709_YCC, XVYCC_601, XVYCC_709, SYCC_601, opYCC_601, BT2020_CYCC, BT2020_YCC"
                ],
                "EdidModel": {
                  "name": "Generic",
                  "product_id": "22333",
                  "serial_number": "0"
                }
              },
              "resolution_modes": [
                {
                  "resolution_width": 320,
                  "resolution_height": 180,
                  "is_high_resolution": false,
                  "frequencies": [
                    {
                      "frequency": 59.84,
                      "is_current": false,
                      "is_preferred": false
                    }
                  ]
                }
              ],
              "is_connected": true,
              "is_primary": true,
              "device_name": "eDP-1",
              "rotation": "normal",
              "reflection": "normal",
              "resolution_width": 1920,
              "resolution_height": 1080,
              "offset_width": 0,
              "offset_height": 0,
              "dimension_width": 309,
              "dimension_height": 174
            }
          ],
          "screen_number": 0,
          "minimum_width": 320,
          "minimum_height": 200,
          "current_width": 1920,
          "current_height": 1080,
          "maximum_width": 16384,
          "maximum_height": 16384
        }
      ]
    }

<a id="jc.parsers.xrandr.parse"></a>

### parse

```python
def parse(data: str,
          raw: bool = False,
          quiet: bool = False) -> jc.parsers.xrandr.Response
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

Source: [`jc/parsers/xrandr.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/xrandr.py)

Version 2.1 by Kevin Lyter (code (at) lyterk.com)
