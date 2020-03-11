"""jc - JSON CLI output utility airport Parser

Usage:

    specify --airport as the first argument if the piped input is coming from airport

Compatibility:

    'darwin'

Examples:

    $ airport | jc --airport -p
    {
      
    }

    $ airport | jc --airport -p -r
    {
      
    }
"""
import jc.utils


class info():
    version = '1.0'
    description = 'airport command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['darwin']
    magic_commands = ['airport']


__version__ = info.version


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data with the following schema:

        {
          
        }
    """
    # boolean changes
    '''
    bool_list = ['ntp_enabled', 'ntp_synchronized', 'rtc_in_local_tz', 'dst_active',
                 'system_clock_synchronized', 'systemd-timesyncd.service_active']
    for key in proc_data:
        if key in bool_list:
            try:
                proc_data[key] = True if proc_data[key] == 'yes' else False
            except (ValueError):
                proc_data[key] = None
    '''

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

    if raw:
        return raw_output
    else:
        return process(raw_output)
