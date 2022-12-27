"""jc - JSON Convert `mpstat` command output streaming parser

> This streaming parser outputs JSON Lines (cli) or returns an Iterable of
> Dictionaries (module)

> Note: Latest versions of `mpstat` support JSON output (v11.5.1+)

Usage (cli):

    $ mpstat | jc --mpstat-s

Usage (module):

    import jc

    result = jc.parse('mpstat_s', mpstat_command_output.splitlines())
    for item in result:
        # do something

Schema:

    {
      "type":               string,
      "time":               string,
      "cpu":                string,
      "node":               string,
      "average":            boolean,
      "percent_usr":        float,
      "percent_nice":       float,
      "percent_sys":        float,
      "percent_iowait":     float,
      "percent_irq":        float,
      "percent_soft":       float,
      "percent_steal":      float,
      "percent_guest":      float,
      "percent_gnice":      float,
      "percent_idle":       float,
      "intr_s":             float,
      "<x>_s":              float,      # <x> is an integer
      "nmi_s":              float,
      "loc_s":              float,
      "spu_s":              float,
      "pmi_s":              float,
      "iwi_s":              float,
      "rtr_s":              float,
      "res_s":              float,
      "cal_s":              float,
      "tlb_s":              float,
      "trm_s":              float,
      "thr_s":              float,
      "dfr_s":              float,
      "mce_s":              float,
      "mcp_s":              float,
      "err_s":              float,
      "mis_s":              float,
      "pin_s":              float,
      "npi_s":              float,
      "piw_s":              float,
      "hi_s":               float,
      "timer_s":            float,
      "net_tx_s":           float,
      "net_rx_s":           float,
      "block_s":            float,
      "irq_poll_s":         float,
      "block_iopoll_s":     float,
      "tasklet_s":          float,
      "sched_s":            float,
      "hrtimer_s":          float,
      "rcu_s":              float,

      # below object only exists if using -qq or ignore_exceptions=True
      "_jc_meta": {
        "success":          boolean,     # false if error parsing
        "error":            string,      # exists if "success" is false
        "line":             string       # exists if "success" is false
      }
    }

Examples:

    $ mpstat -A | jc --mpstat-s
    {"cpu":"all","percent_usr":0.22,"percent_nice":0.0,"percent_sys":...}
    {"cpu":"0","percent_usr":0.22,"percent_nice":0.0,"percent_sys":0....}
    {"cpu":"all","intr_s":37.61,"type":"interrupts","time":"03:15:06 PM"}
    ...

    $ mpstat -A | jc --mpstat-s -r
    {"cpu":"all","percent_usr":"0.22","percent_nice":"0.00","percent_...}
    {"cpu":"0","percent_usr":"0.22","percent_nice":"0.00","percent_sy...}
    {"cpu":"all","intr_s":"37.61","type":"interrupts","time":"03:15:06 PM"}
    ...
"""
from typing import Dict, Iterable, Union
import jc.utils
from jc.parsers.universal import simple_table_parse
from jc.streaming import (
    add_jc_meta, streaming_input_type_check, streaming_line_input_type_check, raise_or_yield
)
from jc.exceptions import ParseError


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.1'
    description = '`mpstat` command streaming parser'
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
    float_list = {
        "percent_usr", "percent_nice", "percent_sys", "percent_iowait", "percent_irq",
        "percent_soft", "percent_steal", "percent_guest", "percent_gnice", "percent_idle", "intr_s",
        "nmi_s", "loc_s", "spu_s", "pmi_s", "iwi_s", "rtr_s", "res_s", "cal_s", "tlb_s", "trm_s",
        "thr_s", "dfr_s", "mce_s", "mcp_s", "err_s", "mis_s", "pin_s", "npi_s", "piw_s", "hi_s",
        "timer_s", "net_tx_s", "net_rx_s", "block_s", "irq_poll_s", "block_iopoll_s", "tasklet_s",
        "sched_s", "hrtimer_s", "rcu_s"
    }

    for key in proc_data:
        if (key in float_list or (key[0].isdigit() and key.endswith('_s'))):
            proc_data[key] = jc.utils.convert_to_float(proc_data[key])

    return proc_data


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

    header_found: bool = False

    for line in data:
        try:
            streaming_line_input_type_check(line)

            # skip blank lines
            if not line.strip():
                continue

            output_line: Dict = {}

            # check for header, normalize it, and fix the time column
            if ' CPU ' in line or ' NODE ' in line:
                header_found = True
                if '%usr' in line:
                    stat_type = 'cpu'
                else:
                    stat_type = 'interrupts'

                header_text: str = line.replace('/', '_')\
                                       .replace('%', 'percent_')\
                                       .lower()
                header_start = line.find('CPU ')

                if header_start == -1:
                    header_start = line.find('NODE ')

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

            if output_line:
                yield output_line if raw else _process(output_line)

        except Exception as e:
            yield raise_or_yield(ignore_exceptions, e, line)
