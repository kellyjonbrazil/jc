"""jc - JSON CLI output utility `acpi` command output parser

Usage (cli):

    $ acpi -V | jc --acpi

    or

    $ jc acpi -V

Usage (module):

    import jc.parsers.acpi
    result = jc.parsers.acpi.parse(acpi_command_output)

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
"""
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.2'
    description = '`acpi` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux']
    magic_commands = ['acpi']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema.
    """
    int_list = ['id', 'charge_percent', 'design_capacity_mah', 'last_full_capacity', 'last_full_capacity_percent']
    float_list = ['temperature']

    for entry in proc_data:
        for key in entry:
            if key in int_list:
                entry[key] = jc.utils.convert_to_int(entry[key])
            if key in float_list:
                entry[key] = jc.utils.convert_to_float(entry[key])

        if 'trip_points' in entry:
            for tp in entry['trip_points']:
                for key in tp:
                    if key in int_list:
                        tp[key] = jc.utils.convert_to_int(tp[key])
                    if key in float_list:
                        tp[key] = jc.utils.convert_to_float(tp[key])

    for entry in proc_data:
        if 'until_charged' in entry:
            entry['until_charged_hours'] = int(entry['until_charged'].split(':')[0])
            entry['until_charged_minutes'] = int(entry['until_charged'].split(':')[1])
            entry['until_charged_seconds'] = int(entry['until_charged'].split(':')[2])
            entry['until_charged_total_seconds'] = (entry['until_charged_hours'] * 3600) + \
                (entry['until_charged_minutes'] * 60) + entry['until_charged_seconds']

        if 'charge_remaining' in entry:
            entry['charge_remaining_hours'] = int(entry['charge_remaining'].split(':')[0])
            entry['charge_remaining_minutes'] = int(entry['charge_remaining'].split(':')[1])
            entry['charge_remaining_seconds'] = int(entry['charge_remaining'].split(':')[2])
            entry['charge_remaining_total_seconds'] = (entry['charge_remaining_hours'] * 3600) + \
                (entry['charge_remaining_minutes'] * 60) + entry['charge_remaining_seconds']

    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = []
    output_line = {}
    line_state = ''
    last_line_state = ''
    obj_type = ''
    obj_id = ''
    trip_points_list = []
    trip_points_dict = {}
    messages_list = []

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            obj_type = line.split()[0]
            obj_id = line.split()[1][:-1]
            line_state = obj_type + obj_id

            if line_state != last_line_state:
                if output_line:
                    raw_output.append(output_line)

                output_line = {}
                trip_points_list = []
                messages_list = []

            if obj_type == 'Battery':
                output_line['type'] = obj_type
                output_line['id'] = obj_id
                if 'Charging' in line or 'Discharging' in line or 'Full' in line:
                    output_line['state'] = line.split()[2][:-1]
                    output_line['charge_percent'] = line.split()[3].rstrip('%,')
                    if 'rate information unavailable' not in line:
                        if 'Charging' in line:
                            output_line['until_charged'] = line.split()[4]
                        if 'Discharging' in line:
                            output_line['charge_remaining'] = line.split()[4]

                if 'design capacity' in line:
                    output_line['design_capacity_mah'] = line.split()[4]
                    output_line['last_full_capacity'] = line.split()[9]
                    output_line['last_full_capacity_percent'] = line.split()[-1][:-1]

            if obj_type == 'Adapter':
                output_line['type'] = obj_type
                output_line['id'] = obj_id
                if 'on-line' in line:
                    output_line['on-line'] = True
                else:
                    output_line['on-line'] = False

            if obj_type == 'Thermal':
                output_line['type'] = obj_type
                output_line['id'] = obj_id
                if 'trip point' not in line:
                    output_line['mode'] = line.split()[2][:-1]
                    output_line['temperature'] = line.split()[3]
                    output_line['temperature_unit'] = line.split()[-1]
                else:
                    trip_points_dict = {
                        "id": line.split()[4],
                        "switches_to_mode": line.split()[8],
                        "temperature": line.split()[11],
                        "temperature_unit": line.split()[-1]
                    }
                    trip_points_list.append(trip_points_dict)
                    output_line['trip_points'] = trip_points_list

            if obj_type == 'Cooling':
                output_line['type'] = obj_type
                output_line['id'] = obj_id
                messages_list.append(line.split(maxsplit=2)[2])
                output_line['messages'] = messages_list

            last_line_state = line_state

    if output_line:
        raw_output.append(output_line)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
