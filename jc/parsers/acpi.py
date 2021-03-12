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

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            if line.startswith('Battery'):
                line_state = 'battery'
                if line_state != last_line_state:
                    if output_line:
                        raw_output.append(output_line)
                        last_line_state = line_state

                    output_line = {}

            if line.startswith('Adapter'):
                line_state = 'adapter'
                if line_state != last_line_state:
                    if output_line:
                        raw_output.append(output_line)
                        last_line_state = line_state

                    output_line = {}

            if line.startswith('Thermal'):
                line_state = 'thermal'
                if line_state != last_line_state:
                    if output_line:
                        raw_output.append(output_line)
                        last_line_state = line_state

                    output_line = {}

            if line.startswith('Cooling'):
                line_state = 'cooling'
                if line_state != last_line_state:
                    if output_line:
                        raw_output.append(output_line)
                        last_line_state = line_state

                    output_line = {}

            if line_state == 'battery':
                output_line['type'] = 'battery'
                output_line['id'] = line.split()[1][:-1]
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

                continue

            if line_state == 'adapter':
                continue

            if line_state == 'thermal':
                continue

            if line_state == 'cooling':
                continue

            last_line_state = line_state

    if output_line:
        raw_output.append(output_line)

    if raw:
        return raw_output
    else:
        return process(raw_output)
