"""jc - JSON CLI output utility `uptime` command output parser

Usage (cli):

    $ uptime | jc --uptime

    or

    $ jc uptime

Usage (module):

    import jc.parsers.uptime
    result = jc.parsers.uptime.parse(uptime_command_output)

Schema:

    {
      "time":                   string,
      "time_hour":              integer,
      "time_minute":            integer,
      "time_second":            integer,        # null if not displayed
      "uptime":                 string,
      "uptime_days":            integer,
      "uptime_hours":           integer,
      "uptime_minutes":         integer,
      "uptime_total_seconds":   integer,
      "users":                  integer,
      "load_1m":                float,
      "load_5m":                float,
      "load_15m":               float
    }

Example:

    $ uptime | jc --uptime -p
    {
      "time": "11:35",
      "uptime": "3 days, 4:03",
      "users": 5,
      "load_1m": 1.88,
      "load_5m": 2.0,
      "load_15m": 1.94,
      "time_hour": 11,
      "time_minute": 35,
      "time_second": null,
      "uptime_days": 3,
      "uptime_hours": 4,
      "uptime_minutes": 3,
      "uptime_total_seconds": 273780
    }

    $ uptime | jc --uptime -p -r
    {
      "time": "11:36",
      "uptime": "3 days, 4:04",
      "users": "5",
      "load_1m": "1.88",
      "load_5m": "1.99",
      "load_15m": "1.94"
    }
"""
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.5'
    description = '`uptime` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'aix', 'freebsd']
    magic_commands = ['uptime']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data to conform to the schema.
    """
    if 'time' in proc_data:
        time_list = proc_data['time'].split(':')
        proc_data['time_hour'] = jc.utils.convert_to_int(time_list[0])
        proc_data['time_minute'] = jc.utils.convert_to_int(time_list[1])
        if len(time_list) == 3:
            proc_data['time_second'] = jc.utils.convert_to_int(time_list[2])
        else:
            proc_data['time_second'] = None

    # parse the uptime field. Here are the variations:
    # 0 min
    # 3 mins
    # 3 days,  2:54
    # 2 days, 19:32
    # 1 day, 29 min
    # 16:59
    if 'uptime' in proc_data:
        uptime_days = 0
        uptime_hours = 0
        uptime_minutes = 0
        uptime_total_seconds = 0

        if 'min' in proc_data['uptime']:
            uptime_minutes = jc.utils.convert_to_int(proc_data['uptime'].split()[-2])

        if ':' in proc_data['uptime']:
            uptime_hours = jc.utils.convert_to_int(proc_data['uptime'].split()[-1].split(':')[-2])
            uptime_minutes = jc.utils.convert_to_int(proc_data['uptime'].split(':')[-1])

        if 'day' in proc_data['uptime']:
            uptime_days = jc.utils.convert_to_int(proc_data['uptime'].split()[0])

        proc_data['uptime_days'] = uptime_days
        proc_data['uptime_hours'] = uptime_hours
        proc_data['uptime_minutes'] = uptime_minutes

        uptime_total_seconds = (uptime_days * 86400) + (uptime_hours * 3600) + (uptime_minutes * 60)
        proc_data['uptime_total_seconds'] = uptime_total_seconds

    # integer and float conversions
    int_list = ['users']
    float_list = ['load_1m', 'load_5m', 'load_15m']
    for key in proc_data:
        if key in int_list:
            proc_data[key] = jc.utils.convert_to_int(proc_data[key])
        if key in float_list:
            proc_data[key] = jc.utils.convert_to_float(proc_data[key])

    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = {}
    cleandata = data.splitlines()

    if jc.utils.has_data(data):
        time, _, *uptime, users, _, _, _, load_1m, load_5m, load_15m = cleandata[0].split()

        raw_output['time'] = time
        raw_output['uptime'] = ' '.join(uptime).rstrip(',')
        raw_output['users'] = users
        raw_output['load_1m'] = load_1m.rstrip(',')
        raw_output['load_5m'] = load_5m.rstrip(',')
        raw_output['load_15m'] = load_15m

    if raw:
        return raw_output
    else:
        return _process(raw_output)
