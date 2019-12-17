"""jc - JSON CLI output utility crontab file Parser

Usage:

    specify --crontab as the first argument if the piped input is coming from a crontab file

Compatibility:

    'linux', 'aix', 'freebsd'

Examples:

    $ crontab | jc --crontab -p
    []

    $ crontab | jc --crontab -p -r
    []
"""
import jc.utils
import jc.parsers.universal


class info():
    version = '1.0'
    description = '/etc/crontab file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'aix', 'freebsd']


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (dictionary) raw structured data to process

    Returns:

        dictionary   structured data with the following schema:

        [
          {
            "minute": [
                                string
            ],
            "hour": [
                                string
            ],
            "day_of_month": [
                                string
            ],
            "month": [
                                string
            ],
            "day_of_week": [
                                string
            ],
            "username":         string
          }
        ]

    """
    # put itmes in lists
    for entry in proc_data['schedule']:
        entry['minute'] = entry['minute'].split(',')
        entry['hour'] = entry['hour'].split(',')
        entry['day_of_month'] = entry['day_of_month'].split(',')
        entry['month'] = entry['month'].split(',')
        entry['day_of_week'] = entry['day_of_week'].split(',')

    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        dictionary   raw or processed structured data
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = {}
    cleandata = data.splitlines()

    # Clear any blank lines
    cleandata = list(filter(None, cleandata))

    # Clear any commented lines
    for i, line in reversed(list(enumerate(cleandata))):
        if line.strip().find('#') == 0:
            cleandata.pop(i)

    # Pop any variable assignment lines
    cron_var = []
    for i, line in reversed(list(enumerate(cleandata))):
        if line.find('=') != -1:
            var_line = cleandata.pop(i)
            var_name = var_line.split('=', maxsplit=1)[0]
            var_value = var_line.split('=', maxsplit=1)[1]
            cron_var.append({'name': var_name,
                             'value': var_value})

    raw_output['variables'] = cron_var

    # TODO: support @shortcuts

    # Add header row for parsing
    cleandata[0] = 'minute hour day_of_month month day_of_week username command'

    if len(cleandata) > 1:
        cron_list = jc.parsers.universal.simple_table_parse(cleandata)

    raw_output['schedule'] = cron_list

    if raw:
        return raw_output
    else:
        return process(raw_output)
