
# jc.parsers.acpi
jc - JSON CLI output utility `acpi` command output parser

Usage (cli):

    $ acpi -V | jc --acpi

    or

    $ jc acpi -V

Usage (module):

    import jc.parsers.acpi
    result = jc.parsers.acpi.parse(acpi_command_output)

Compatibility:

    'linux'

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
        "last_full_capacity_percent": 100
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


## info
```python
info()
```


## process
```python
process(proc_data)
```

Final processing to conform to the schema.

Parameters:

    proc_data:   (List of Dictionaries) raw structured data to process

Returns:

    List of Dictionaries. Structured data with the following schema:

    [
      {
        "type":                         string,
        "id":                           integer,
        "state":                        string,
        "charge_percent":               integer,
        "until_charged":                string,
        "charge_remaining"              string,
        "design_capacity_mah":          integer,
        "last_full_capacity":           integer,
        "last_full_capacity_percent":   integer,
        "on-line":                      boolean,
        "mode":                         string,
        "temperature":                  float,
        "temperature_unit":             string,
        "trip_points": [
          {
            "id":                       integer,
            "switches_to_mode":         string,
            "temperature":              float,
            "temperature_unit":         string
          }
        ],
        "messages": [
                                        string
        ]
      }
    ]


## parse
```python
parse(data, raw=False, quiet=False)
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) output preprocessed JSON if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

