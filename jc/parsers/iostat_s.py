"""jc - JSON Convert `iostat` command output streaming parser

> This streaming parser outputs JSON Lines (cli) or returns an Iterable of
> Dictionaries (module)

> Note: `iostat` version 11 and higher include a JSON output option

Usage (cli):

    $ iostat | jc --iostat-s

> Note: When piping `jc` converted `iostat` output to other processes it may
> appear the output is hanging due to the OS pipe buffers. This is because
> `iostat` output is too small to quickly fill up the buffer. Use the `-u`
> option to unbuffer the `jc` output if you would like immediate output. See
> the [readme](https://github.com/kellyjonbrazil/jc/tree/master#unbuffering-output)
> for more information.

Usage (module):

    import jc

    result = jc.parse('iostat_s', iostat_command_output.splitlines())
    for item in result:
        # do something

Schema:

    {
      "type":             string,
      "percent_user":     float,
      "percent_nice":     float,
      "percent_system":   float,
      "percent_iowait":   float,
      "percent_steal":    float,
      "percent_idle":     float,
      "device":           string,
      "tps":              float,
      "kb_read_s":        float,
      "mb_read_s":        float,
      "kb_wrtn_s":        float,
      "mb_wrtn_s":        float,
      "kb_read":          integer,
      "mb_read":          integer,
      "kb_wrtn":          integer,
      "mb_wrtn":          integer,
      'kb_dscd':          integer,
      'mb_dscd':          integer,
      "rrqm_s":           float,
      "wrqm_s":           float,
      "r_s":              float,
      "w_s":              float,
      "rmb_s":            float,
      "rkb_s":            float,
      "wmb_s":            float,
      "wkb_s":            float,
      "avgrq_sz":         float,
      "avgqu_sz":         float,
      "await":            float,
      "r_await":          float,
      "w_await":          float,
      "svctm":            float,
      "aqu_sz":           float,
      "rareq_sz":         float,
      "wareq_sz":         float,
      "d_s":              float,
      "dkb_s":            float,
      "dmb_s":            float,
      "drqm_s":           float,
      "percent_drqm":     float,
      "d_await":          float,
      "dareq_sz":         float,
      "f_s":              float,
      "f_await":          float,
      "kb_dscd_s":        float,
      "mb_dscd_s":        float,
      "percent_util":     float,
      "percent_rrqm":     float,
      "percent_wrqm":     float,

      # below object only exists if using -qq or ignore_exceptions=True
      "_jc_meta": {
        "success":        boolean,     # false if error parsing
        "error":          string,      # exists if "success" is false
        "line":           string       # exists if "success" is false
      }
    }

Examples:

    $ iostat | jc --iostat-s
    {"percent_user":0.14,"percent_nice":0.0,"percent_system":0.16,...}
    {"device":"sda","tps":0.24,"kb_read_s":5.28,"kb_wrtn_s":1.1...}
    ...

    $ iostat | jc --iostat-s -r
    {"percent_user":"0.14","percent_nice":"0.00","percent_system":"0.16"...}
    {"device":"sda","tps":"0.24","kb_read_s":"5.28","kb_wrtn_s":"1.10"...}
    ...
"""
import jc.utils
from jc.streaming import (
    add_jc_meta, streaming_input_type_check, streaming_line_input_type_check, raise_or_yield
)
from jc.exceptions import ParseError
import jc.parsers.universal


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.3'
    description = '`iostat` command streaming parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    tags = ['command']
    streaming = True


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data to conform to the schema.
    """
    float_list = {
        'percent_user', 'percent_nice', 'percent_system', 'percent_iowait',
        'percent_steal', 'percent_idle', 'tps', 'kb_read_s', 'mb_read_s', 'kb_wrtn_s',
        'mb_wrtn_s', 'rrqm_s', 'wrqm_s', 'r_s', 'w_s', 'rmb_s', 'rkb_s', 'wmb_s',
        'wkb_s', 'avgrq_sz', 'avgqu_sz', 'await', 'r_await', 'w_await', 'svctm',
        'percent_util', 'percent_rrqm', 'percent_wrqm', 'aqu_sz', 'rareq_sz', 'wareq_sz',
        'd_s', 'dkb_s', 'dmb_s', 'drqm_s', 'percent_drqm', 'd_await', 'dareq_sz',
        'f_s', 'f_await', 'kb_dscd_s', 'mb_dscd_s'
    }

    int_list = {'kb_read', 'mb_read', 'kb_wrtn', 'mb_wrtn', 'kb_dscd', 'mb_dscd'}

    for key in proc_data:
        if key in int_list:
            proc_data[key] = jc.utils.convert_to_int(proc_data[key])

        if key in float_list:
            proc_data[key] = jc.utils.convert_to_float(proc_data[key])

    return proc_data


def _normalize_headers(line):
    return line.replace('%', 'percent_').replace('/', '_').replace('-', '_').lower()


def _create_obj_list(section_list, section_name):
    output_list = jc.parsers.universal.simple_table_parse(section_list)
    for item in output_list:
        item['type'] = section_name
    return output_list


@add_jc_meta
def parse(data, raw=False, quiet=False, ignore_exceptions=False):
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

    section = ''  # either 'cpu' or 'device'
    headers = ''
    cpu_list = []
    device_list = []

    for line in data:
        try:
            streaming_line_input_type_check(line)
            output_line = {}

            # ignore blank lines and header line
            if not line.strip() or line.startswith('Linux'):
                continue

            if line.startswith('avg-cpu:'):
                section = 'cpu'
                headers = _normalize_headers(line)
                headers = headers.strip().split(':', maxsplit=1)[1:]
                headers = ' '.join(headers)
                continue

            if line.startswith('Device'):
                section = 'device'
                headers = _normalize_headers(line)
                headers = headers.replace(':', ' ')
                continue

            if section == 'cpu':
                cpu_list.append(headers)
                cpu_list.append(line)
                output_line = _create_obj_list(cpu_list, 'cpu')[0]
                cpu_list = []

            if section == 'device':
                device_list.append(headers)
                device_list.append(line)
                output_line = _create_obj_list(device_list, 'device')[0]
                device_list = []

            if output_line:
                yield output_line if raw else _process(output_line)
            else:
                raise ParseError('Not iostat data')

        except Exception as e:
            yield raise_or_yield(ignore_exceptions, e, line)
