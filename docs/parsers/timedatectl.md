[Home](https://kellyjonbrazil.github.io/jc/)
# Table of Contents

* [jc.parsers.timedatectl](#jc.parsers.timedatectl)
  * [parse](#jc.parsers.timedatectl.parse)

<a id="jc.parsers.timedatectl"></a>

# jc.parsers.timedatectl

jc - JSON CLI output utility `timedatectl` command output parser

The `epoch_utc` calculated timestamp field is timezone-aware and is only
available if the `universal_time` field is available.

Usage (cli):

    $ timedatectl | jc --timedatectl

    or

    $ jc timedatectl

Usage (module):

    import jc
    result = jc.parse('timedatectl', timedatectl_command_output)

    or

    import jc.parsers.timedatectl
    result = jc.parsers.timedatectl.parse(timedatectl_command_output)

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

<a id="jc.parsers.timedatectl.parse"></a>

### parse

```python
def parse(data, raw=False, quiet=False)
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    Dictionary. Raw or processed structured data.

### Parser Information
Compatibility:  linux

Version 1.5 by Kelly Brazil (kellyjonbrazil@gmail.com)
