"""jc - JSON Convert `/proc/net/dev` file parser

Usage (cli):

    $ cat /proc/net/dev | jc --proc

or

    $ jc /proc/net/dev

or

    $ cat /proc/net/dev | jc --proc-net-dev

Usage (module):

    import jc
    result = jc.parse('proc', proc_net_dev_file)

or

    import jc
    result = jc.parse('proc_net_dev', proc_net_dev_file)

Schema:

    [
      {
        "interface":                  string,
        "r_bytes":                    integer,
        "r_packets":                  integer,
        "r_errs":                     integer,
        "r_drop":                     integer,
        "r_fifo":                     integer,
        "r_frame":                    integer,
        "r_compressed":               integer,
        "r_multicast":                integer,
        "t_bytes":                    integer,
        "t_packets":                  integer,
        "t_errs":                     integer,
        "t_drop":                     integer,
        "t_fifo":                     integer,
        "t_colls":                    integer,
        "t_carrier":                  integer,
        "t_compressed":               integer
      }
    ]

Examples:

    $ cat /proc/net/dev | jc --proc -p
    [
      {
        "interface": "lo",
        "r_bytes": 13222,
        "r_packets": 152,
        "r_errs": 0,
        "r_drop": 0,
        "r_fifo": 0,
        "r_frame": 0,
        "r_compressed": 0,
        "r_multicast": 0,
        "t_bytes": 13222,
        "t_packets": 152,
        "t_errs": 0,
        "t_drop": 0,
        "t_fifo": 0,
        "t_colls": 0,
        "t_carrier": 0,
        "t_compressed": 0
      },
      ...
    ]

    $ cat /proc/net/dev | jc --proc-net-dev -p -r
    [
      {
        "interface": "lo:",
        "r_bytes": "13222",
        "r_packets": "152",
        "r_errs": "0",
        "r_drop": "0",
        "r_fifo": "0",
        "r_frame": "0",
        "r_compressed": "0",
        "r_multicast": "0",
        "t_bytes": "13222",
        "t_packets": "152",
        "t_errs": "0",
        "t_drop": "0",
        "t_fifo": "0",
        "t_colls": "0",
        "t_carrier": "0",
        "t_compressed": "0"
      },
      ...
    ]
"""
from typing import List, Dict
import jc.utils
from jc.parsers.universal import simple_table_parse


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`/proc/net/dev` file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    tags = ['file']
    hidden = True


__version__ = info.version


def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    for item in proc_data:
        if 'interface' in item:
            item['interface'] = item['interface'][:-1]

        for key, val in item.items():
            try:
                item[key] = int(val)
            except Exception:
                pass

    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> List[Dict]:
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

    raw_output: List = []

    if jc.utils.has_data(data):

        header = 'interface r_bytes r_packets r_errs r_drop r_fifo r_frame r_compressed r_multicast t_bytes t_packets t_errs t_drop t_fifo t_colls t_carrier t_compressed'
        data_splitlines = data.splitlines()
        data_splitlines.pop(0)
        data_splitlines[0] = header
        raw_output = simple_table_parse(data_splitlines)

    return raw_output if raw else _process(raw_output)
