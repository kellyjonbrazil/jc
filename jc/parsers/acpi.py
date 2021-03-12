"""jc - JSON CLI output utility `acpi` command output parser

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
    []

    $ acpi -V | jc --acpi -p -r
    []
"""
import jc.utils


class info():
    version = '1.0'
    description = 'acpi command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux']
    magic_commands = ['acpi']


__version__ = info.version


def process(proc_data):
    """
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
    """

    # rebuild output for added semantic information
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

            if line.startswith('Battery'):
                if line_state != last_line_state:
                    if output_line:
                        raw_output.append(output_line)
                        last_line_state = line_state

                    output_line = {}
                    trip_points_list = []
                    messages_list = []

            if line.startswith('Adapter'):
                if line_state != last_line_state:
                    if output_line:
                        raw_output.append(output_line)
                        last_line_state = line_state

                    output_line = {}
                    trip_points_list = []
                    messages_list = []

            if line.startswith('Thermal'):
                if line_state != last_line_state:
                    if output_line:
                        raw_output.append(output_line)
                        last_line_state = line_state

                    output_line = {}
                    trip_points_list = []
                    messages_list = []

            if line.startswith('Cooling'):
                if line_state != last_line_state:
                    if output_line:
                        raw_output.append(output_line)
                        last_line_state = line_state

                    output_line = {}
                    trip_points_list = []
                    messages_list = []

            if obj_type == 'Battery':
                output_line['type'] = obj_type
                output_line['id'] = obj_id
                if 'Charging' in line:
                    output_line['state'] = line.split()[2][:-1]
                    output_line['charge_percent'] = line.split()[3][:-2]
                    if 'rate information unavailable' not in line:
                        output_line['until_charged'] = line.split()[4]

                if 'design capacity' in line:
                    output_line['design_capacity_mah'] = line.split()[4]
                    output_line['last_full_capacity'] = line.split()[9]
                    output_line['last_full_capacity_percent'] = line.split()[-1][:-1]

                if 'Discharging' in line:
                    output_line['state'] = line.split()[2][:-1]
                    output_line['charge_percent'] = line.split()[3][:-2]
                    if 'rate information unavailable' not in line:
                        output_line['charge_remaining'] = line.split()[4]

                last_line_state = line_state
                continue

            if obj_type == 'Adapter':
                output_line['type'] = obj_type
                output_line['id'] = obj_id
                if 'on-line' in line:
                    output_line['on-line'] = True
                else:
                    output_line['on-line'] = False

                last_line_state = line_state
                continue

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

                last_line_state = line_state
                continue

            if obj_type == 'Cooling':
                output_line['type'] = obj_type
                output_line['id'] = obj_id
                messages_list.append(line.split(maxsplit=2)[2])
                output_line['messages'] = messages_list

                last_line_state = line_state
                continue

    if output_line:
        raw_output.append(output_line)

    if raw:
        return raw_output
    else:
        return process(raw_output)
