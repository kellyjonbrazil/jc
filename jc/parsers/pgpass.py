"""jc - JSON Convert PostgreSQL password file parser

Usage (cli):

    $ cat /var/lib/postgresql/.pgpass | jc --pgpass

Usage (module):

    import jc
    result = jc.parse('pgpass', postgres_password_file)

Schema:

    [
      {
        "hostname":               string,
        "port":                   string,
        "database":               string,
        "username":               string,
        "password":               string
      }
    ]

Examples:

    $ cat /var/lib/postgresql/.pgpass | jc --pgpass -p
    [
      {
        "hostname": "dbserver",
        "port": "*",
        "database": "db1",
        "username": "dbuser",
        "password": "pwd123"
      },
      {
        "hostname": "dbserver2",
        "port": "8888",
        "database": "inventory",
        "username": "joe:user",
        "password": "abc123"
      },
      ...
    ]
"""
from typing import List, Dict
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'PostgreSQL password file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['file']


__version__ = info.version


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

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):

            # ignore comment lines
            if line.strip().startswith('#'):
                continue

            # convert escaped characters (\ and :)
            line = line.replace(':', '\u2063')
            line = line.replace('\\\\', '\\')
            line = line.replace('\\\u2063', ':')

            hostname, port, database, username, password = line.split('\u2063')

            raw_output.append(
                {
                    'hostname': hostname,
                    'port': port,
                    'database': database,
                    'username': username,
                    'password': password
                }
            )

    return raw_output if raw else _process(raw_output)
