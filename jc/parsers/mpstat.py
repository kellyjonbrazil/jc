"""jc - JSON Convert `mpstat` command output parser

<<Short mpstat description and caveats>>

Usage (cli):

    $ mpstat | jc --mpstat

    or

    $ jc mpstat

Usage (module):

    import jc
    result = jc.parse('mpstat', mpstat_command_output)

Schema:

    [
      {
        "mpstat":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ mpstat | jc --mpstat -p
    []

    $ mpstat | jc --mpstat -p -r
    []
"""
from typing import List, Dict
import jc.utils
from jc.parsers.universal import simple_table_parse


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`mpstat` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    magic_commands = ['mpstat']


__version__ = info.version


def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """

    # process the data here
    # rebuild output for added semantic information
    # use helper functions in jc.utils for int, float, bool
    # conversions and timestamps

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
    output_line: Dict = {}
    header_found = False
    header_start: int = 0
    stat_type: str = ''    # 'cpu' or 'interrupts'

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):

            # check for header, normalize it, and fix the time column
            if ' CPU ' in line:
                header_found = True
                if '%usr' in line:
                    stat_type = 'cpu'
                else:
                    stat_type = 'interrupts'

                header_text: str = line.replace('/', '_')\
                                  .replace('%', 'percent_')\
                                  .lower()
                header_start = line.find('CPU ')
                header_text = header_text[header_start:]
                continue

            # data line - pull time from beginning and then parse as a table
            if header_found:
                output_line = simple_table_parse([header_text, line[header_start:]])[0]
                output_line['type'] = stat_type
                item_time = line[:header_start].strip()
                if 'Average:' not in item_time:
                    output_line['time'] = line[:header_start].strip()
                else:
                    output_line['average'] = True
                raw_output.append(output_line)

    return raw_output if raw else _process(raw_output)
