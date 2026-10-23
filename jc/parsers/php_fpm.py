"""
`php-fpm -tt` command parser

Parses the configuration dump written to standard error by versioned and
unversioned PHP-FPM executables when invoked with the `-tt` option.

The output schema is:

    {
      "POOL_NAME": {
        "DIRECTIVE_NAME": "value"
      }
    }

All directive values are retained as strings. The same representation is used
when `raw=True`.
"""
import re
from typing import Dict, Optional, Union


class info:
    version = '1.0'
    description = '`php-fpm -tt` command parser'
    author = 'JC Contributors'
    author_email = ''
    compatible = ['linux']
    tags = ['command']


_NOTICE_RE = re.compile(
    r'^\[[^\]]+\]\s+NOTICE:\s?(?P<payload>.*)$'
)
_SECTION_RE = re.compile(r'^\[(?P<section>[^\]]+)\]$')
_SUCCESS_RE = re.compile(r'^configuration file .+ test is successful$')


def parse(
    data: Union[str, bytes],
    raw: bool = False,
    quiet: bool = False
) -> Dict[str, Dict[str, str]]:
    """
    Convert `php-fpm -tt` output to a dictionary.

    Parameters:

        data:   `php-fpm -tt` output as a string or bytes
        raw:    ignored because values are always retained as strings
        quiet:  accepted for parser API compatibility

    Returns:

        Dictionary keyed by PHP-FPM configuration section or pool name.
    """
    del raw, quiet

    if isinstance(data, bytes):
        data = data.decode('utf-8')

    output: Dict[str, Dict[str, str]] = {}
    current_section: Optional[str] = None

    for line in data.splitlines():
        notice = _NOTICE_RE.match(line)
        if not notice:
            continue

        payload = notice.group('payload').strip()
        if not payload or _SUCCESS_RE.match(payload):
            continue

        section = _SECTION_RE.match(payload)
        if section:
            current_section = section.group('section').strip()
            output.setdefault(current_section, {})
            continue

        if current_section is None or '=' not in payload:
            continue

        key, value = payload.split('=', 1)
        key = key.strip()
        value = value.strip()
        if key:
            output[current_section][key] = value

    return output
