"""jc - JSON Convert `timedatectl` command output parser

Also supports the `timesync-status` option.

The `epoch_utc` calculated timestamp field is timezone-aware and is only
available if the `universal_time` field is available.

Usage (cli):

    $ timedatectl | jc --timedatectl

or

    $ jc timedatectl

Usage (module):

    import jc
    result = jc.parse('timedatectl', timedatectl_command_output)

Schema:

    {
      "local_time":                        string,
      "universal_time":                    string,
      "epoch_utc":                         integer,     # timezone-aware
      "rtc_time":                          string,
      "time_zone":                         string,
      "ntp_enabled":                       boolean,
      "ntp_synchronized":                  boolean,
      "system_clock_synchronized":         boolean,
      "systemd-timesyncd.service_active":  boolean,
      "rtc_in_local_tz":                   boolean,
      "dst_active":                        boolean,
      "server":                            string,
      "poll_interval":                     string,
      "leap":                              string,
      "version":                           integer,
      "stratum":                           integer,
      "reference":                         string,
      "precision":                         string,
      "root_distance":                     string,
      "offset":                            float,
      "offset_unit":                       string,
      "delay":                             float,
      "delay_unit":                        string,
      "jitter":                            float,
      "jitter_unit":                       string,
      "packet_count":                      integer,
      "frequency":                         float,
      "frequency_unit":                    string
    }

Examples:

    $ timedatectl | jc --timedatectl -p
    {
      "local_time": "Tue 2020-03-10 17:53:21 PDT",
      "universal_time": "Wed 2020-03-11 00:53:21 UTC",
      "rtc_time": "Wed 2020-03-11 00:53:21",
      "time_zone": "America/Los_Angeles (PDT, -0700)",
      "ntp_enabled": true,
      "ntp_synchronized": true,
      "rtc_in_local_tz": false,
      "dst_active": true,
      "epoch_utc": 1583888001
    }

    $ timedatectl | jc --timedatectl -p -r
    {
      "local_time": "Tue 2020-03-10 17:53:21 PDT",
      "universal_time": "Wed 2020-03-11 00:53:21 UTC",
      "rtc_time": "Wed 2020-03-11 00:53:21",
      "time_zone": "America/Los_Angeles (PDT, -0700)",
      "ntp_enabled": "yes",
      "ntp_synchronized": "yes",
      "rtc_in_local_tz": "no",
      "dst_active": "yes"
    }
"""
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.8'
    description = '`timedatectl status` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    magic_commands = ['timedatectl', 'timedatectl status']
    tags = ['command']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data to conform to the schema.
    """
    bool_list = {'ntp_enabled', 'ntp_synchronized', 'rtc_in_local_tz', 'dst_active',
                 'system_clock_synchronized', 'systemd-timesyncd.service_active'}
    int_list = {'version', 'stratum', 'packet_count'}
    float_list = {'offset', 'delay', 'jitter', 'frequency'}

    for key in ['offset', 'delay', 'jitter']:
        if key in proc_data:
            proc_data[key + '_unit'] = proc_data[key][-2:]

    if 'frequency' in proc_data:
        proc_data['frequency_unit'] = proc_data['frequency'][-3:]

    for key in proc_data:
        if key in bool_list:
            proc_data[key] = jc.utils.convert_to_bool(proc_data[key])

        if key in int_list:
            proc_data[key] = jc.utils.convert_to_int(proc_data[key])

        if key in float_list:
            proc_data[key] = jc.utils.convert_to_float(proc_data[key])

    if 'universal_time' in proc_data:
        ts = jc.utils.timestamp(proc_data['universal_time'], format_hint=(7300,))
        proc_data['epoch_utc'] = ts.utc

    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}
    valid_fields = {
        'local time', 'universal time', 'rtc time', 'time zone', 'ntp enabled',
        'ntp synchronized', 'rtc in local tz', 'dst active',
        'system clock synchronized', 'ntp service',
        'systemd-timesyncd.service active', 'server', 'poll interval', 'leap',
        'version', 'stratum', 'reference', 'precision', 'root distance',
        'offset', 'delay', 'jitter', 'packet count', 'frequency'
    }

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            try:
                key, val = line.split(':', maxsplit=1)
                key = key.lower().strip()
                val = val.strip()
            except ValueError:
                continue

            if key in valid_fields:
                keyname = key.replace(' ', '_')
                raw_output[keyname] = val

    return raw_output if raw else _process(raw_output)
