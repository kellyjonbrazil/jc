"""jc - JSON CLI output utility `upower` command output parser

Usage (cli):

    $ upower -d | jc --upower

    or

    $ jc upower -d

Usage (module):

    import jc.parsers.upower
    result = jc.parsers.upower.parse(upower_command_output)

Compatibility:

    'linux'

Examples:

    $ upower | jc --upower -p
    []

    $ upower | jc --upower -p -r
    []
"""
import jc.utils


class info():
    version = '1.0'
    description = 'upower command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux']
    magic_commands = ['upower']


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
            "type":                 string,
            "device_name":          string,
            "native_path":          string,
            "power_supply":         boolean,
            "updated":              "Thu 11 Mar 2021 06:28:08 PM UTC (441975 seconds ago)",
            "has_history":          boolean,
            "has_statistics":       boolean,
            "detail": {
              "type":               string,
              "warning_level":      string,        # null if none
              "online":             boolean,
              "icon_name":          string
              "present":            boolean,
              "rechargeable":       boolean,
              "state":              string,
              "energy":             "22.3998 Wh",
              "energy_empty":       "0 Wh",
              "energy_full":        "52.6473 Wh",
              "energy_full_design": "62.16 Wh",
              "energy_rate":        "31.6905 W",
              "voltage":            "12.191 V",
              "time_to_full":       "57.3 minutes",
              "percentage":         "42.5469%",
              "capacity":           "84.6964%",
              "technology":         string
            },
            "history_charge": [
              {
                "time":             integer,
                "percent_charged":  float,
                "status":           string
              }
            ],
            "history_rate":[
              {
                "time":             integer,
                "percent_charged":  float,
                "status":           string
              }
            ],
            "daemon_version":       string,
            "on_battery":           boolean,
            "lid_is_closed":        boolean,
            "lid_is_present":       boolean,
            "critical_action":      string
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
    device_obj = {}
    device_name = None
    history_key = ''
    history_list = []
    history_list_obj = {}

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            if line.startswith('Device:') or line.startswith('Daemon:'):
                if device_obj:
                    raw_output.append(device_obj)
                    device_obj = {}

                if line.startswith('Device:'):
                    device_name = line.split(':', maxsplit=1)[1].strip()
                    device_obj = {
                        'type': 'Device',
                        "device_name": device_name
                    }

                elif line.startswith('Daemon:'):
                    device_obj = {
                        'type': 'Daemon'
                    }

                continue

            # history detail lines
            if line.startswith('    ') and ':' not in line:
                line_list = line.strip().split()
                history_list_obj = {
                    'time': line_list[0],
                    'percent_charged': line_list[1],
                    'status': line_list[2]
                }
                history_list.append(history_list_obj)
                device_obj[history_key] = history_list
                continue

            # general detail lines
            if line.startswith('    ') and ':' in line:
                key = line.split(':', maxsplit=1)[0].strip().lower().replace('-', '_').replace(' ', '_').replace('(', '').replace(')', '')
                val = line.split(':', maxsplit=1)[1].strip()
                device_obj['detail'][key] = val
                continue

            # history detail lines are a special case of detail lines
            # set the history detail key
            if line.startswith('  History (charge):') or line.startswith('  History (rate):'):
                if line.startswith('  History (charge):'):
                    history_key = 'history_charge'
                elif line.startswith('  History (rate):'):
                    history_key = 'history_rate'

                device_obj[history_key] = {}
                history_list = []
                continue

            # top level lines
            if line.startswith('  ') and ':' in line:
                key = line.split(':', maxsplit=1)[0].strip().lower().replace('-', '_').replace(' ', '_').replace('(', '').replace(')', '')
                val = line.split(':', maxsplit=1)[1].strip()
                device_obj[key] = val
                continue

            # set the general detail object
            if line.startswith('  ') and ':' not in line:
                detail_type = line.strip()
                device_obj['detail'] = {
                    'type': detail_type
                }
                continue

    if device_obj:
        raw_output.append(device_obj)

    if raw:
        return raw_output
    else:
        return process(raw_output)
