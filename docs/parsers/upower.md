[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.upower"></a>

# jc.parsers.upower

jc - JSON Convert `upower` command output parser

The `updated_epoch` calculated timestamp field is naive. (i.e. based on the
local time of the system the parser is run on)

The `updated_epoch_utc` calculated timestamp field is timezone-aware and is
only available if the timezone field is UTC.

Usage (cli):

    $ upower -d | jc --upower

or

    $ jc upower -d

Usage (module):

    import jc
    result = jc.parse('upower', upower_command_output)

Schema:

    [
      {
        "type":                         string,
        "device_name":                  string,
        "native_path":                  string,
        "power_supply":                 boolean,
        "updated":                      string,
        "updated_epoch":                integer,       # [0]
        "updated_epoch_utc":            integer,       # [0]
        "updated_seconds_ago":          integer,
        "has_history":                  boolean,
        "has_statistics":               boolean,
        "detail": {
          "type":                       string,
          "warning_level":              string,        # null if none
          "online":                     boolean,
          "icon_name":                  string
          "present":                    boolean,
          "rechargeable":               boolean,
          "state":                      string,
          "energy":                     float,
          "energy_unit":                string,
          "energy_empty":               float,
          "energy_empty_unit":          string,
          "energy_full":                float,
          "energy_full_unit":           string,
          "energy_full_design":         float,
          "energy_full_design_unit":    string,
          "energy_rate":                float,
          "energy_rate_unit":           string,
          "voltage":                    float,
          "voltage_unit":               string,
          "time_to_full":               float,
          "time_to_full_unit":          string,
          "percentage":                 float,
          "capacity":                   float,
          "technology":                 string
        },
        "history_charge": [
          {
            "time":                     integer,
            "percent_charged":          float,
            "status":                   string
          }
        ],
        "history_rate":[
          {
            "time":                     integer,
            "percent_charged":          float,
            "status":                   string
          }
        ],
        "daemon_version":               string,
        "on_battery":                   boolean,
        "lid_is_closed":                boolean,
        "lid_is_present":               boolean,
        "critical_action":              string
      }
    ]

    [0] null if date-time conversion fails

Examples:

    $ upower -i /org/freedesktop/UPower/devices/battery | jc --upower -p
    [
      {
        "native_path": "/sys/devices/LNXSYSTM:00/device:00/PNP0C0A:00/p...",
        "vendor": "NOTEBOOK",
        "model": "BAT",
        "serial": "0001",
        "power_supply": true,
        "updated": "Thu 11 Mar 2021 06:28:08 PM UTC",
        "has_history": true,
        "has_statistics": true,
        "detail": {
          "type": "battery",
          "present": true,
          "rechargeable": true,
          "state": "charging",
          "energy": 22.3998,
          "energy_empty": 0.0,
          "energy_full": 52.6473,
          "energy_full_design": 62.16,
          "energy_rate": 31.6905,
          "voltage": 12.191,
          "time_to_full": 57.3,
          "percentage": 42.5469,
          "capacity": 84.6964,
          "technology": "lithium-ion",
          "energy_unit": "Wh",
          "energy_empty_unit": "Wh",
          "energy_full_unit": "Wh",
          "energy_full_design_unit": "Wh",
          "energy_rate_unit": "W",
          "voltage_unit": "V",
          "time_to_full_unit": "minutes"
        },
        "history_charge": [
          {
            "time": 1328809335,
            "percent_charged": 42.547,
            "status": "charging"
          },
          {
            "time": 1328809305,
            "percent_charged": 42.02,
            "status": "charging"
          }
        ],
        "history_rate": [
          {
            "time": 1328809335,
            "percent_charged": 31.691,
            "status": "charging"
          }
        ],
        "updated_seconds_ago": 441975,
        "updated_epoch": 1615516088,
        "updated_epoch_utc": 1615487288
      }
    ]

    $ upower -i /org/freedesktop/UPower/devices/battery | jc --upower -p -r
    [
      {
        "native_path": "/sys/devices/LNXSYSTM:00/device:00/PNP0C0A:00/p...",
        "vendor": "NOTEBOOK",
        "model": "BAT",
        "serial": "0001",
        "power_supply": "yes",
        "updated": "Thu 11 Mar 2021 06:28:08 PM UTC (441975 seconds ago)",
        "has_history": "yes",
        "has_statistics": "yes",
        "detail": {
          "type": "battery",
          "present": "yes",
          "rechargeable": "yes",
          "state": "charging",
          "energy": "22.3998 Wh",
          "energy_empty": "0 Wh",
          "energy_full": "52.6473 Wh",
          "energy_full_design": "62.16 Wh",
          "energy_rate": "31.6905 W",
          "voltage": "12.191 V",
          "time_to_full": "57.3 minutes",
          "percentage": "42.5469%",
          "capacity": "84.6964%",
          "technology": "lithium-ion"
        },
        "history_charge": [
          {
            "time": "1328809335",
            "percent_charged": "42.547",
            "status": "charging"
          },
          {
            "time": "1328809305",
            "percent_charged": "42.020",
            "status": "charging"
          }
        ],
        "history_rate": [
          {
            "time": "1328809335",
            "percent_charged": "31.691",
            "status": "charging"
          }
        ]
      }
    ]

<a id="jc.parsers.upower.parse"></a>

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

    List of Dictionaries. Raw or processed structured data.

### Parser Information
Compatibility:  linux

Source: [`jc/parsers/upower.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/upower.py)

Version 1.4 by Kelly Brazil (kellyjonbrazil@gmail.com)
