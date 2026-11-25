r"""jc - JSON Convert `php-fpm -tt` command output parser

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
"""
import re
from typing import List, Dict, Optional
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`php-fpm -tt` command parser'
    author = 'chensimian'
    author_email = 'chensimian@users.noreply.github.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['command']


__version__ = info.version


# each line is a log message, e.g. `[25-Feb-2024 20:25:25] NOTICE:  pm = dynamic`
_NOTICE_RE = re.compile(r'\[[^\]]*\]\s+NOTICE:\s?(?P<message>.*)')
_SECTION_RE = re.compile(r'\[(?P<section>[^\]]+)\]')


def _process(proc_data: List[JSONDictType]) -> List[JSONDictType]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> List[JSONDictType]:
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[Dict] = []
    section: Optional[Dict] = None

    if jc.utils.has_data(data):

        for line in filter(None, jc.utils.splitlines(data)):
            notice = _NOTICE_RE.fullmatch(line.rstrip())
            if not notice:
                continue

            message = notice.group('message')

            # `[global]` or a pool name such as `[www]`
            section_match = _SECTION_RE.fullmatch(message.strip())
            if section_match:
                section = {'type': section_match.group('section')}
                raw_output.append(section)
                continue

            # directives are indented (`key = value`). Other messages, such as
            # `[pool www] pm.start_servers is not set...` or the
            # "configuration file ... test is successful" line, are skipped.
            if section is not None and message[:1].isspace() and '=' in message:
                key, value = message.split('=', maxsplit=1)
                if key.strip():
                    section[key.strip()] = value.strip()

    return raw_output if raw else _process(raw_output)
