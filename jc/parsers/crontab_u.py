"""jc - JSON CLI output utility `crontab -l` command output and crontab file parser

This version of the `crontab -l` parser supports output that contains user information for processes.

Usage (cli):

    $ crontab -l | jc --crontab-u

Usage (module):

    import jc.parsers.crontab_u
    result = jc.parsers.crontab_u.parse(crontab_u_output)

Schema:

    {
      "variables": [
        "name":               string,
        "value":              string
      ],
      "schedule": [
        {
          "occurrence"        string,
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
          "occurrence":       string,
          "user":             string,
          "command":          string
        }
      ]
    }

Examples:

    $ cat /etc/crontab | jc --crontab-u -p
    {
      "variables": [
        {
          "name": "PATH",
          "value": "/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin"
        },
        {
          "name": "SHELL",
          "value": "/bin/sh"
        }
      ],
      "schedule": [
        {
          "minute": [
            "25"
          ],
          "hour": [
            "6"
          ],
          "day_of_month": [
            "*"
          ],
          "month": [
            "*"
          ],
          "day_of_week": [
            "*"
          ],
          "user": "root",
          "command": "test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )"
        },
        {
          "minute": [
            "47"
          ],
          "hour": [
            "6"
          ],
          "day_of_month": [
            "*"
          ],
          "month": [
            "*"
          ],
          "day_of_week": [
            "7"
          ],
          "user": "root",
          "command": "test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )"
        },
        {
          "minute": [
            "52"
          ],
          "hour": [
            "6"
          ],
          "day_of_month": [
            "1"
          ],
          "month": [
            "*"
          ],
          "day_of_week": [
            "*"
          ],
          "user": "root",
          "command": "test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )"
        }
      ]
    }

    $ cat /etc/crontab | jc --crontab-u -p -r
    {
      "variables": [
        {
          "name": "PATH",
          "value": "/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin"
        },
        {
          "name": "SHELL",
          "value": "/bin/sh"
        }
      ],
      "schedule": [
        {
          "minute": "25",
          "hour": "6",
          "day_of_month": "*",
          "month": "*",
          "day_of_week": "*",
          "user": "root",
          "command": "test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )"
        },
        {
          "minute": "47",
          "hour": "6",
          "day_of_month": "*",
          "month": "*",
          "day_of_week": "7",
          "user": "root",
          "command": "test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )"
        },
        {
          "minute": "52",
          "hour": "6",
          "day_of_month": "1",
          "month": "*",
          "day_of_week": "*",
          "user": "root",
          "command": "test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )"
        }
      ]
    }
"""
import jc.utils
import jc.parsers.universal


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.6'
    description = '`crontab` file parser with user support'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'aix', 'freebsd']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data to conform to the schema.
    """
    # put itmes in lists
    try:
        for entry in proc_data['schedule']:
            entry['minute'] = entry['minute'].split(',')
            entry['hour'] = entry['hour'].split(',')
            entry['day_of_month'] = entry['day_of_month'].split(',')
            entry['month'] = entry['month'].split(',')
            entry['day_of_week'] = entry['day_of_week'].split(',')
    except (KeyError):
        pass

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
    cleandata = data.splitlines()

    # Clear any blank lines
    cleandata = list(filter(None, cleandata))

    if jc.utils.has_data(data):

        # Clear any commented lines
        for i, line in reversed(list(enumerate(cleandata))):
            if line.strip().startswith('#'):
                cleandata.pop(i)

        # Pop any variable assignment lines
        cron_var = []
        for i, line in reversed(list(enumerate(cleandata))):
            if '=' in line and not line.strip()[0].isdigit() and not line.strip()[0] == '@':
                var_line = cleandata.pop(i)
                var_name = var_line.split('=', maxsplit=1)[0].strip()
                var_value = var_line.split('=', maxsplit=1)[1].strip()
                cron_var.append({'name': var_name,
                                 'value': var_value})

        raw_output['variables'] = cron_var

        # Pop any shortcut lines
        shortcut_list = []
        for i, line in reversed(list(enumerate(cleandata))):
            if line.strip().startswith('@'):
                shortcut_line = cleandata.pop(i)
                occurrence = shortcut_line.split(maxsplit=1)[0].strip().lstrip('@')
                usr = shortcut_line.split(maxsplit=2)[1].strip()
                cmd = shortcut_line.split(maxsplit=2)[2].strip()
                shortcut_list.append({'occurrence': occurrence,
                                      'user': usr,
                                      'command': cmd})

        # Add header row for parsing
        cleandata[:0] = ['minute hour day_of_month month day_of_week user command']

        if len(cleandata) > 1:
            cron_list = jc.parsers.universal.simple_table_parse(cleandata)

            raw_output['schedule'] = cron_list

        # Add shortcut entries back in
        for item in shortcut_list:
            raw_output['schedule'].append(item)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
