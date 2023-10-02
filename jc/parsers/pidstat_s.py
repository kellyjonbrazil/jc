"""jc - JSON Convert `pidstat -H` command output streaming parser

> This streaming parser outputs JSON Lines (cli) or returns an Iterable of
> Dictionaries (module)

Must use the `-H` (or `-h`, if `-H` is not available) option in `pidstat`.
All other `pidstat` options are supported in combination with this option.

Usage (cli):

    $ pidstat -H | jc --pidstat-s

> Note: When piping `jc` converted `pidstat` output to other processes it
> may appear the output is hanging due to the OS pipe buffers. This is
> because `pidstat` output is too small to quickly fill up the buffer. Use
> the `-u` option to unbuffer the `jc` output if you would like immediate
> output. See the [readme](https://github.com/kellyjonbrazil/jc/tree/master#unbuffering-output)
> for more information.

Usage (module):

    import jc

    result = jc.parse('pidstat_s', pidstat_command_output.splitlines())
    for item in result:
        # do something

Schema:

    {
      "time":             integer,
      "uid":              integer,
      "pid":              integer,
      "percent_usr":      float,
      "percent_system":   float,
      "percent_guest":    float,
      "percent_wait":     float,
      "percent_cpu":      float,
      "cpu":              integer,
      "minflt_s":         float,
      "majflt_s":         float,
      "vsz":              integer,
      "rss":              integer,
      "percent_mem":      float,
      "stksize":          integer,
      "stkref":           integer,
      "kb_rd_s":          float,
      "kb_wr_s":          float,
      "kb_ccwr_s":        float,
      "cswch_s":          float,
      "nvcswch_s":        float,
      "usr_ms":           integer,
      "system_ms":        integer,
      "guest_ms":         integer,
      "command":          string,

      # below object only exists if using -qq or ignore_exceptions=True
      "_jc_meta": {
        "success":        boolean,     # false if error parsing
        "error":          string,      # exists if "success" is false
        "line":           string       # exists if "success" is false
      }
    }

Examples:

    $ pidstat -Hl | jc --pidstat-s
    {"time":1646859134,"uid":0,"pid":1,"percent_usr":0.0,"percent_syste...}
    {"time":1646859134,"uid":0,"pid":6,"percent_usr":0.0,"percent_syste...}
    {"time":1646859134,"uid":0,"pid":9,"percent_usr":0.0,"percent_syste...}
    ...

    $ pidstat -Hl | jc --pidstat-s -r
    {"time":"1646859134","uid":"0","pid":"1","percent_usr":"0.00","perc...}
    {"time":"1646859134","uid":"0","pid":"6","percent_usr":"0.00","perc...}
    {"time":"1646859134","uid":"0","pid":"9","percent_usr":"0.00","perc...}
    ...
"""
from typing import List, Dict, Iterable, Union
import jc.utils
from jc.streaming import (
    add_jc_meta, streaming_input_type_check, streaming_line_input_type_check, raise_or_yield
)
from jc.parsers.universal import simple_table_parse
from jc.exceptions import ParseError


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.2'
    description = '`pidstat -H` command streaming parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    tags = ['command']
    streaming = True


__version__ = info.version


def _process(proc_data: Dict) -> Dict:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data to conform to the schema.
    """
    int_list = {
        'time', 'uid', 'pid', 'cpu', 'vsz', 'rss', 'stksize', 'stkref',
        'usr_ms', 'system_ms', 'guest_ms'
    }

    float_list = {
        'percent_usr', 'percent_system', 'percent_guest', 'percent_wait',
        'percent_cpu', 'minflt_s', 'majflt_s', 'percent_mem', 'kb_rd_s',
        'kb_wr_s', 'kb_ccwr_s', 'cswch_s', 'nvcswch_s'
    }

    for key in proc_data:
        if key in int_list:
            proc_data[key] = jc.utils.convert_to_int(proc_data[key])

        if key in float_list:
            proc_data[key] = jc.utils.convert_to_float(proc_data[key])

    return proc_data


def normalize_header(header: str) -> str:
    return header.replace('#', ' ')\
                 .replace('-', '_')\
                 .replace('/', '_')\
                 .replace('%', 'percent_')\
                 .lower()


@add_jc_meta
def parse(
    data: Iterable[str],
    raw: bool = False,
    quiet: bool = False,
    ignore_exceptions: bool = False
) -> Union[Iterable[Dict], tuple]:
    """
    Main text parsing generator function. Returns an iterable object.

    Parameters:

        data:              (iterable)  line-based text data to parse
                                       (e.g. sys.stdin or str.splitlines())

        raw:               (boolean)   unprocessed output if True
        quiet:             (boolean)   suppress warning messages if True
        ignore_exceptions: (boolean)   ignore parsing exceptions if True

    Returns:

        Iterable of Dictionaries
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    streaming_input_type_check(data)

    table_list: List = []
    header: str = ''

    for line in data:
        try:
            streaming_line_input_type_check(line)
            output_line: Dict = {}

            if not line.strip():
                # skip blank lines
                continue

            if line.startswith('#'):
                if len(table_list) > 1:
                    output_line = simple_table_parse(table_list)[0]
                    yield output_line if raw else _process(output_line)
                    header = ''

                header = normalize_header(line)
                table_list = [header]
                continue

            if header:
                table_list.append(line)
                output_line = simple_table_parse(table_list)[0]
                yield output_line if raw else _process(output_line)
                table_list = [header]
                continue

        except Exception as e:
            yield raise_or_yield(ignore_exceptions, e, line)

    try:
        if len(table_list) > 1:
            output_line = simple_table_parse(table_list)[0]
            yield output_line if raw else _process(output_line)

    except Exception as e:
        yield raise_or_yield(ignore_exceptions, e, str(table_list))
