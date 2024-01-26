[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.acpi"></a>

# jc.parsers.acpi

jc - JSON Convert `acpi` command output parser

Usage (cli):

    $ acpi -V | jc --acpi

or

    $ jc acpi -V

Usage (module):

    import jc
    result = jc.parse('acpi', acpi_command_output)

Schema:

    [
      {
        "type":                             string,
        "id":                               integer,
        "state":                            string,
        "charge_percent":                   integer,
        "until_charged":                    string,
        "until_charged_hours":              integer,
        "until_charged_minuts":             integer,
        "until_charged_seconds":            integer,
        "until_charged_total_seconds":      integer,
        "charge_remaining":                 string,
        "charge_remaining_hours":           integer,
        "charge_remaining_minutes":         integer,
        "charge_remaining_seconds":         integer,
        "charge_remaining_total_seconds":   integer,
        "design_capacity_mah":              integer,
        "last_full_capacity":               integer,
        "last_full_capacity_percent":       integer,
        "on-line":                          boolean,
        "mode":                             string,
        "temperature":                      float,
        "temperature_unit":                 string,
        "trip_points": [
          {
            "id":                           integer,
            "switches_to_mode":             string,
            "temperature":                  float,
            "temperature_unit":             string
          }
        ],
        "messages": [
                                            string
        ]
      }
    ]

Examples:

    $ acpi -V | jc --acpi -p
    [
      {
        "type": "Battery",
        "id": 0,
        "state": "Charging",
        "charge_percent": 71,
        "until_charged": "00:29:20",
        "design_capacity_mah": 2110,
        "last_full_capacity": 2271,
        "last_full_capacity_percent": 100,
        "until_charged_hours": 0,
        "until_charged_minutes": 29,
        "until_charged_seconds": 20,
        "until_charged_total_seconds": 1760
      },
      {
        "type": "Adapter",
        "id": 0,
        "on-line": true
      },
      {
        "type": "Thermal",
        "id": 0,
        "mode": "ok",
        "temperature": 46.0,
        "temperature_unit": "C",
        "trip_points": [
          {
            "id": 0,
            "switches_to_mode": "critical",
            "temperature": 127.0,
            "temperature_unit": "C"
          },
          {
            "id": 1,
            "switches_to_mode": "hot",
            "temperature": 127.0,
            "temperature_unit": "C"
          }
        ]
      },
      {
        "type": "Cooling",
        "id": 0,
        "messages": [
          "Processor 0 of 10"
        ]
      },
      {
        "type": "Cooling",
        "id": 1,
        "messages": [
          "Processor 0 of 10"
        ]
      },
      {
        "type": "Cooling",
        "id": 2,
        "messages": [
          "x86_pkg_temp no state information available"
        ]
      },
      {
        "type": "Cooling",
        "id": 3,
        "messages": [
          "Processor 0 of 10"
        ]
      },
      {
        "type": "Cooling",
        "id": 4,
        "messages": [
          "intel_powerclamp no state information available"
        ]
      },
      {
        "type": "Cooling",
        "id": 5,
        "messages": [
          "Processor 0 of 10"
        ]
      }
    ]

    $ acpi -V | jc --acpi -p -r
    [
      {
        "type": "Battery",
        "id": "0",
        "state": "Charging",
        "charge_percent": "71",
        "until_charged": "00:29:20",
        "design_capacity_mah": "2110",
        "last_full_capacity": "2271",
        "last_full_capacity_percent": "100"
      },
      {
        "type": "Adapter",
        "id": "0",
        "on-line": true
      },
      {
        "type": "Thermal",
        "id": "0",
        "mode": "ok",
        "temperature": "46.0",
        "temperature_unit": "C",
        "trip_points": [
          {
            "id": "0",
            "switches_to_mode": "critical",
            "temperature": "127.0",
            "temperature_unit": "C"
          },
          {
            "id": "1",
            "switches_to_mode": "hot",
            "temperature": "127.0",
            "temperature_unit": "C"
          }
        ]
      },
      {
        "type": "Cooling",
        "id": "0",
        "messages": [
          "Processor 0 of 10"
        ]
      },
      {
        "type": "Cooling",
        "id": "1",
        "messages": [
          "Processor 0 of 10"
        ]
      },
      {
        "type": "Cooling",
        "id": "2",
        "messages": [
          "x86_pkg_temp no state information available"
        ]
      },
      {
        "type": "Cooling",
        "id": "3",
        "messages": [
          "Processor 0 of 10"
        ]
      },
      {
        "type": "Cooling",
        "id": "4",
        "messages": [
          "intel_powerclamp no state information available"
        ]
      },
      {
        "type": "Cooling",
        "id": "5",
        "messages": [
          "Processor 0 of 10"
        ]
      }
    ]

<a id="jc.parsers.acpi.parse"></a>

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

Source: [`jc/parsers/acpi.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/acpi.py)

Version 1.7 by Kelly Brazil (kellyjonbrazil@gmail.com)
