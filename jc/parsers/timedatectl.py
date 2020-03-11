"""jc - JSON CLI output utility timedatectl Parser

Usage:

    specify --timedatectl as the first argument if the piped input is coming from timedatectl or timedatectl status

Compatibility:

    'linux'

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
      "dst_active": true
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
    version = '1.0'
    description = 'timedatectl status command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux']
    magic_commands = ['timedatectl', 'timedatectl status']


__version__ = info.version


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data with the following schema:

        {
          "local_time":                        string,
          "universal_time":                    string,
          "rtc_time":                          string,
          "time_zone":                         string,
          "ntp_enabled":                       boolean,
          "ntp_synchronized":                  boolean,
          "system_clock_synchronized":         boolean,
          "systemd-timesyncd.service_active":  boolean,
          "rtc_in_local_tz":                   boolean,
          "dst_active":                        boolean
        }
    """
    # boolean changes
    bool_list = ['ntp_enabled', 'ntp_synchronized', 'rtc_in_local_tz', 'dst_active',
                 'system_clock_synchronized', 'systemd-timesyncd.service_active']
    for key in proc_data:
        if key in bool_list:
            try:
                proc_data[key] = True if proc_data[key] == 'yes' else False
            except (ValueError):
                proc_data[key] = None

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

    for line in filter(None, data.splitlines()):
        linedata = line.split(':', maxsplit=1)
        raw_output[linedata[0].strip().lower().replace(' ', '_')] = linedata[1].strip()

        if linedata[0].strip() == 'DST active':
            break

    if raw:
        return raw_output
    else:
        return process(raw_output)
