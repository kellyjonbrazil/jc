"""jc - JSON CLI output utility crontab command and file Parser

Usage:

    specify --crontab as the first argument if the piped input is coming from crontab -l or a crontab file

Compatibility:

    'linux', 'darwin', 'aix', 'freebsd'

Examples:

    $ crontab -l | jc --crontab -p
    {
      "variables": [
        {
          "name": "MAILTO",
          "value": "root"
        },
        {
          "name": "PATH",
          "value": "/sbin:/bin:/usr/sbin:/usr/bin"
        },
        {
          "name": "SHELL",
          "value": "/bin/bash"
        }
      ],
      "schedule": [
        {
          "minute": [
            "5"
          ],
          "hour": [
            "10-11",
            "22"
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
          "command": "/var/www/devdaily.com/bin/mk-new-links.php"
        },
        {
          "minute": [
            "30"
          ],
          "hour": [
            "4/2"
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
          "command": "/var/www/devdaily.com/bin/create-all-backups.sh"
        },
        {
          "occurrence": "yearly",
          "command": "/home/maverick/bin/annual-maintenance"
        },
        {
          "occurrence": "reboot",
          "command": "/home/cleanup"
        },
        {
          "occurrence": "monthly",
          "command": "/home/maverick/bin/tape-backup"
        }
      ]
    }

    $ cat /etc/crontab | jc --crontab -p -r
    {
      "variables": [
        {
          "name": "MAILTO",
          "value": "root"
        },
        {
          "name": "PATH",
          "value": "/sbin:/bin:/usr/sbin:/usr/bin"
        },
        {
          "name": "SHELL",
          "value": "/bin/bash"
        }
      ],
      "schedule": [
        {
          "minute": "5",
          "hour": "10-11,22",
          "day_of_month": "*",
          "month": "*",
          "day_of_week": "*",
          "command": "/var/www/devdaily.com/bin/mk-new-links.php"
        },
        {
          "minute": "30",
          "hour": "4/2",
          "day_of_month": "*",
          "month": "*",
          "day_of_week": "*",
          "command": "/var/www/devdaily.com/bin/create-all-backups.sh"
        },
        {
          "occurrence": "yearly",
          "command": "/home/maverick/bin/annual-maintenance"
        },
        {
          "occurrence": "reboot",
          "command": "/home/cleanup"
        },
        {
          "occurrence": "monthly",
          "command": "/home/maverick/bin/tape-backup"
        }
      ]
    }
"""
import jc.utils
import jc.parsers.universal


class info():
    version = '1.2'
    description = 'crontab command and file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'aix', 'freebsd']
    magic_commands = ['crontab']


__version__ = info.version


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data with the following schema:

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
              "command":          string
            }
          ]
        }

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

    # Clear any commented lines
    for i, line in reversed(list(enumerate(cleandata))):
        if line.strip().startswith('#'):
            cleandata.pop(i)

    # Pop any variable assignment lines
    cron_var = []
    for i, line in reversed(list(enumerate(cleandata))):
        if '=' in line:
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
            cmd = shortcut_line.split(maxsplit=1)[1].strip()
            shortcut_list.append({'occurrence': occurrence,
                                  'command': cmd})

    # Add header row for parsing
    cleandata[:0] = ['minute hour day_of_month month day_of_week command']

    if len(cleandata) > 1:
        cron_list = jc.parsers.universal.simple_table_parse(cleandata)

        raw_output['schedule'] = cron_list

    # Add shortcut entries back in
    for item in shortcut_list:
        raw_output['schedule'].append(item)

    if raw:
        return raw_output
    else:
        return process(raw_output)
