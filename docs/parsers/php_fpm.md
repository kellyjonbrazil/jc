[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.php_fpm"></a>

# jc.parsers.php_fpm

jc - JSON Convert `php-fpm -tt` command output parser

Usage (cli):

    $ php-fpm8.2 -tt 2>&1 | jc --php-fpm

Usage (module):

    import jc
    result = jc.parse('php_fpm', php_fpm_command_output)

Schema:

    [
      {
        "type":                   string,
        "<directive>":            string
      }
    ]

Examples:

    $ php-fpm8.2 -tt 2>&1 | jc --php-fpm -p
    [
      {
        "type": "global",
        "pid": "/run/php/php8.2-fpm.pid",
        "error_log": "/var/log/php8.2-fpm.log",
        "syslog.ident": "php-fpm",
        "syslog.facility": "24",
        "log_buffering": "yes",
        "log_level": "unknown value",
        "log_limit": "1024",
        "emergency_restart_interval": "0s",
        "emergency_restart_threshold": "0",
        "process_control_timeout": "0s",
        "process.max": "0",
        "process.priority": "undefined",
        "daemonize": "yes",
        "rlimit_files": "0",
        "rlimit_core": "0",
        "events.mechanism": "epoll",
        "systemd_interval": "10s"
      },
      {
        "type": "www",
        "prefix": "undefined",
        "user": "www-data",
        "group": "www-data",
        "listen": "/run/php/php8.2-fpm.sock",
        "listen.backlog": "-1",
        "pm": "dynamic",
        "pm.max_children": "4",
        "pm.start_servers": "1",
        "pm.min_spare_servers": "1",
        "pm.max_spare_servers": "1",
        ...
        "security.limit_extensions": ".php .phar"
      }
    ]

<a id="jc.parsers.php_fpm.parse"></a>

### parse

```python
def parse(data: str,
          raw: bool = False,
          quiet: bool = False) -> List[Dict[str, Any]]
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

### Parser Information
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Source: [`jc/parsers/php_fpm.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/php_fpm.py)

Version 1.0 by chensimian (chensimian@users.noreply.github.com)
