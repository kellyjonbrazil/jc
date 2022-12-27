"""jc - JSON Convert `/proc/net/protocols` file parser

Usage (cli):

    $ cat /proc/net/protocols | jc --proc

or

    $ jc /proc/net/protocols

or

    $ cat /proc/net/protocols | jc --proc-net-protocols

Usage (module):

    import jc
    result = jc.parse('proc', proc_net_protocols_file)

or

    import jc
    result = jc.parse('proc_net_protocols', proc_net_protocols_file)

Schema:

    [
      {
        "protocol":                   string,
        "size":                       integer,
        "sockets":                    integer,
        "memory":                     integer,
        "press":                      string,
        "maxhdr":                     integer,
        "slab":                       boolean,
        "module":                     string,
        "cl":                         boolean,
        "co":                         boolean,
        "di":                         boolean,
        "ac":                         boolean,
        "io":                         boolean,
        "in":                         boolean,
        "de":                         boolean,
        "sh":                         boolean,
        "ss":                         boolean,
        "gs":                         boolean,
        "se":                         boolean,
        "re":                         boolean,
        "sp":                         boolean,
        "bi":                         boolean,
        "br":                         boolean,
        "ha":                         boolean,
        "uh":                         boolean,
        "gp":                         boolean,
        "em":                         boolean,
      }
    ]

Examples:

    $ cat /proc/net/protocols | jc --proc -p
    [
      {
        "protocol": "AF_VSOCK",
        "size": 1216,
        "sockets": 0,
        "memory": -1,
        "press": "NI",
        "maxhdr": 0,
        "slab": true,
        "module": "vsock",
        "cl": false,
        "co": false,
        "di": false,
        "ac": false,
        "io": false,
        "in": false,
        "de": false,
        "sh": false,
        "ss": false,
        "gs": false,
        "se": false,
        "re": false,
        "sp": false,
        "bi": false,
        "br": false,
        "ha": false,
        "uh": false,
        "gp": false,
        "em": false
      },
      ...
    ]

    $ cat /proc/net/protocols | jc --proc-net-protocols -p -r
    [
      {
        "protocol": "AF_VSOCK",
        "size": "1216",
        "sockets": "0",
        "memory": "-1",
        "press": "NI",
        "maxhdr": "0",
        "slab": "yes",
        "module": "vsock",
        "cl": "n",
        "co": "n",
        "di": "n",
        "ac": "n",
        "io": "n",
        "in": "n",
        "de": "n",
        "sh": "n",
        "ss": "n",
        "gs": "n",
        "se": "n",
        "re": "n",
        "sp": "n",
        "bi": "n",
        "br": "n",
        "ha": "n",
        "uh": "n",
        "gp": "n",
        "em": "n"
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
    description = '`/proc/net/protocols` file parser'
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
    int_list = {'size', 'sockets', 'memory', 'maxhdr'}
    bool_list = {'slab', 'cl', 'co', 'di', 'ac', 'io', 'in', 'de', 'sh', 'ss',
                 'gs', 'se', 're', 'sp', 'bi', 'br', 'ha', 'uh', 'gp', 'em'}

    for item in proc_data:
        for key, val in item.items():
            if key in int_list:
                item[key] = int(val)
            if key in bool_list:
                item[key] = jc.utils.convert_to_bool(val)

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

        raw_output = simple_table_parse(data.splitlines())

    return raw_output if raw else _process(raw_output)
