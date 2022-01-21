[Home](https://kellyjonbrazil.github.io/jc/)

# jc.parsers.crontab_u
jc - JSON CLI output utility `crontab -l` command output and crontab
file parser

This version of the `crontab -l` parser supports output that contains user
information for processes.

Usage (cli):

    $ crontab -l | jc --crontab-u

Usage (module):

    import jc
    result = jc.parse('crontab_u', crontab_u_output)

    or

    import jc.parsers.crontab_u
    result = jc.parsers.crontab_u.parse(crontab_u_output)

Schema:

    {
      "variables": [
        {
          "name":             string,
          "value":            string
        }
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
          "value": "/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sb..."
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
          "command": "test -x /usr/sbin/anacron || ( cd / && run-parts ..."
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
          "command": "test -x /usr/sbin/anacron || ( cd / && run-parts ..."
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
          "command": "test -x /usr/sbin/anacron || ( cd / && run-parts ..."
        }
      ]
    }

    $ cat /etc/crontab | jc --crontab-u -p -r
    {
      "variables": [
        {
          "name": "PATH",
          "value": "/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/..."
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
          "command": "test -x /usr/sbin/anacron || ( cd / && run-parts ..."
        },
        {
          "minute": "47",
          "hour": "6",
          "day_of_month": "*",
          "month": "*",
          "day_of_week": "7",
          "user": "root",
          "command": "test -x /usr/sbin/anacron || ( cd / && run-parts ..."
        },
        {
          "minute": "52",
          "hour": "6",
          "day_of_month": "1",
          "month": "*",
          "day_of_week": "*",
          "user": "root",
          "command": "test -x /usr/sbin/anacron || ( cd / && run-parts ..."
        }
      ]
    }


## info
```python
info()
```
Provides parser metadata (version, author, etc.)

## parse
```python
parse(data, raw=False, quiet=False)
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    Dictionary. Raw or processed structured data.

## Parser Information
Compatibility:  linux, darwin, aix, freebsd

Version 1.7 by Kelly Brazil (kellyjonbrazil@gmail.com)
