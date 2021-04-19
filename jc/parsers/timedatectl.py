"""jc - JSON CLI output utility `timedatectl` command output parser

The `epoch_utc` calculated timestamp field is timezone-aware and is only available if the `universal_time` field is available.

Usage (cli):

    $ timedatectl | jc --timedatectl

    or

    $ jc timedatectl

Usage (module):

    import jc.parsers.timedatectl
    result = jc.parsers.timedatectl.parse(timedatectl_command_output)

Schema:

    {
      "local_time":                        string,
      "universal_time":                    string,
      "epoch_utc":                         integer,     # timezone-aware timestamp
      "rtc_time":                          string,
      "time_zone":                         string,
      "ntp_enabled":                       boolean,
      "ntp_synchronized":                  boolean,
      "system_clock_synchronized":         boolean,
      "systemd-timesyncd.service_active":  boolean,
      "rtc_in_local_tz":                   boolean,
      "dst_active":                        boolean
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
    version = '1.4'
    description = '`timedatectl status` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux']
    magic_commands = ['timedatectl', 'timedatectl status']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data to conform to the schema.
    """
    bool_list = ['ntp_enabled', 'ntp_synchronized', 'rtc_in_local_tz', 'dst_active',
                 'system_clock_synchronized', 'systemd-timesyncd.service_active']
    for key in proc_data:
        if key in bool_list:
            proc_data[key] = jc.utils.convert_to_bool(proc_data[key])

    if 'universal_time' in proc_data:
        ts = jc.utils.timestamp(proc_data['universal_time'])
        proc_data['epoch_utc'] = ts.utc

    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = {}

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            linedata = line.split(':', maxsplit=1)
            raw_output[linedata[0].strip().lower().replace(' ', '_')] = linedata[1].strip()

            if linedata[0].strip() == 'DST active':
                break

    if raw:
        return raw_output
    else:
        return _process(raw_output)
