"""jc - JSON Convert `/proc/net/dev_mcast` file parser

Usage (cli):

    $ cat /proc/net/dev_mcast | jc --proc

or

    $ jc /proc/net/dev_mcast

or

    $ cat /proc/net/dev_mcast | jc --proc-net-dev-mcast

Usage (module):

    import jc
    result = jc.parse('proc', proc_net_dev_mcast_file)

or

    import jc
    result = jc.parse('proc_net_dev_mcast', proc_net_dev_mcast_file)

Schema:

    [
      {
        "index":                      integer,
        "interface":                  string,
        "dmi_u":                      integer,
        "dmi_g":                      integer,
        "dmi_address":                string
      }
    ]

Examples:

    $ cat /proc/net/dev_mcast | jc --proc -p
    [
      {
        "index": 2,
        "interface": "ens33",
        "dmi_u": 1,
        "dmi_g": 0,
        "dmi_address": "333300000001"
      },
      {
        "index": 2,
        "interface": "ens33",
        "dmi_u": 1,
        "dmi_g": 0,
        "dmi_address": "01005e000001"
      },
      ...
    ]

    $ cat /proc/net/dev_mcast | jc --proc-net-dev-mcast -p -r
    [
      {
        "index": "2",
        "interface": "ens33",
        "dmi_u": "1",
        "dmi_g": "0",
        "dmi_address": "333300000001"
      },
      {
        "index": "2",
        "interface": "ens33",
        "dmi_u": "1",
        "dmi_g": "0",
        "dmi_address": "01005e000001"
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
    description = '`/proc/net/dev_mcast` file parser'
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
    no_convert = {'interface_name', 'dmi_address'}

    for item in proc_data:
        for key, val in item.items():
            if key not in no_convert:
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

        header = 'index interface dmi_u dmi_g dmi_address\n'
        data = header + data
        data_splitlines = data.splitlines()
        raw_output = simple_table_parse(data_splitlines)

    return raw_output if raw else _process(raw_output)
