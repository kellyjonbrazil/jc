"""jc - JSON Convert `/proc/softirqs` file parser

Usage (cli):

    $ cat /proc/softirqs | jc --proc

or

    $ jc /proc/softirqs

or

    $ cat /proc/softirqs | jc --proc-softirqs

Usage (module):

    import jc
    result = jc.parse('proc', proc_softirqs_file)

or

    import jc
    result = jc.parse('proc_softirqs', proc_softirqs_file)

Schema:

    [
      {
        "counter":                    string,
        "CPU<number>":                integer,
      }
    ]

Examples:

    $ cat /proc/softirqs | jc --proc -p
    [
      {
        "counter": "HI",
        "CPU0": 1,
        "CPU1": 34056,
        "CPU2": 0,
        "CPU3": 0,
        "CPU4": 0
      },
      {
        "counter": "TIMER",
        "CPU0": 322970,
        "CPU1": 888166,
        "CPU2": 0,
        "CPU3": 0,
        "CPU4": 0
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
    description = '`/proc/softirqs` file parser'
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

        cleandata =  list(filter(None, data.splitlines()))
        cleandata[0] = 'counter ' + cleandata[0]
        raw_output = simple_table_parse(cleandata)

        for item in raw_output:
            if 'counter' in item:
                item['counter'] = item['counter'][:-1]

            for key in item:
                try:
                    item[key] = int(item[key])
                except Exception:
                    pass

    return raw_output if raw else _process(raw_output)
