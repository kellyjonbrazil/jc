"""jc - JSON CLI output utility `iostat` command output parser

Note: `iostat` version 11 and higher include a JSON output option

Usage (cli):

    $ iostat | jc --iostat

    or

    $ jc iostat

Usage (module):

    import jc.parsers.iostat
    result = jc.parsers.iostat.parse(iostat_command_output)

Schema:

    [
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
        "percent_wrqm":     float
      }
    ]

Examples:

    $ iostat | jc --iostat -p
    [
      {
          "percent_user": 0.15,
          "percent_nice": 0.0,
          "percent_system": 0.18,
          "percent_iowait": 0.0,
          "percent_steal": 0.0,
          "percent_idle": 99.67,
          "type": "cpu"
      },
      {
          "device": "sda",
          "tps": 0.29,
          "kb_read_s": 7.22,
          "kb_wrtn_s": 1.25,
          "kb_read": 194341,
          "kb_wrtn": 33590,
          "type": "device"
      },
      {
          "device": "dm-0",
          "tps": 0.29,
          "kb_read_s": 5.99,
          "kb_wrtn_s": 1.17,
          "kb_read": 161361,
          "kb_wrtn": 31522,
          "type": "device"
      },
      {
          "device": "dm-1",
          "tps": 0.0,
          "kb_read_s": 0.08,
          "kb_wrtn_s": 0.0,
          "kb_read": 2204,
          "kb_wrtn": 0,
          "type": "device"
      }
    ]

    $ iostat | jc --iostat -p -r
    [
      {
        "percent_user": "0.15",
        "percent_nice": "0.00",
        "percent_system": "0.18",
        "percent_iowait": "0.00",
        "percent_steal": "0.00",
        "percent_idle": "99.67",
        "type": "cpu"
      },
      {
        "device": "sda",
        "tps": "0.29",
        "kb_read_s": "7.22",
        "kb_wrtn_s": "1.25",
        "kb_read": "194341",
        "kb_wrtn": "33590",
        "type": "device"
      },
      {
        "device": "dm-0",
        "tps": "0.29",
        "kb_read_s": "5.99",
        "kb_wrtn_s": "1.17",
        "kb_read": "161361",
        "kb_wrtn": "31522",
        "type": "device"
      },
      {
        "device": "dm-1",
        "tps": "0.00",
        "kb_read_s": "0.08",
        "kb_wrtn_s": "0.00",
        "kb_read": "2204",
        "kb_wrtn": "0",
        "type": "device"
      }
    ]
"""
import jc.utils
import jc.parsers.universal


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`iostat` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    magic_commands = ['iostat']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """

    for entry in proc_data:
        float_list = [
            'percent_user', 'percent_nice', 'percent_system', 'percent_iowait',
            'percent_steal', 'percent_idle', 'tps', 'kb_read_s', 'mb_read_s', 'kb_wrtn_s',
            'mb_wrtn_s', 'rrqm_s', 'wrqm_s', 'r_s', 'w_s', 'rmb_s', 'rkb_s', 'wmb_s',
            'wkb_s', 'avgrq_sz', 'avgqu_sz', 'await', 'r_await', 'w_await', 'svctm',
            'percent_util', 'percent_rrqm', 'percent_wrqm', 'aqu_sz', 'rareq_sz', 'wareq_sz',
            'd_s', 'dkb_s', 'dmb_s', 'drqm_s', 'percent_drqm', 'd_await', 'dareq_sz',
            'f_s', 'f_await', 'kb_dscd_s', 'mb_dscd_s'
        ]
        int_list = ['kb_read', 'mb_read', 'kb_wrtn', 'mb_wrtn', 'kb_dscd', 'mb_dscd']
        for key in entry:
            if key in int_list:
                entry[key] = jc.utils.convert_to_int(entry[key])

            if key in float_list:
                entry[key] = jc.utils.convert_to_float(entry[key])

    return proc_data

def _normalize_headers(line):
    return line.replace('%', 'percent_').replace('/', '_').replace('-', '_').lower()

def _create_obj_list(section_list, section_name):
    output_list = jc.parsers.universal.simple_table_parse(section_list)
    for item in output_list:
        item['type'] = section_name
    return output_list

def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = []

    if jc.utils.has_data(data):
        section = ''  # either 'cpu' or 'device'
        headers = ''
        cpu_list = []
        device_list = []

        for line in filter(None, data.splitlines()):
            if line.startswith('avg-cpu:'):
                if cpu_list:
                    raw_output.extend(_create_obj_list(cpu_list, 'cpu'))
                    cpu_list = []

                if device_list:
                    raw_output.extend(_create_obj_list(device_list, 'device'))
                    device_list = []

                section = 'cpu'
                headers = _normalize_headers(line)
                headers = headers.strip().split(':', maxsplit=1)[1:]
                headers = ' '.join(headers)
                cpu_list.append(headers)
                continue

            if line.startswith('Device'):
                if cpu_list:
                    raw_output.extend(_create_obj_list(cpu_list, 'cpu'))
                    cpu_list = []

                if device_list:
                    raw_output.extend(_create_obj_list(device_list, 'device'))
                    device_list = []

                section = 'device'
                headers = _normalize_headers(line)
                headers = headers.replace(':', ' ')
                device_list.append(headers)
                continue

            if section == 'cpu':
                cpu_list.append(line)

            if section == 'device':
                device_list.append(line)

        if cpu_list:
            raw_output.extend(_create_obj_list(cpu_list, 'cpu'))

        if device_list:
            raw_output.extend(_create_obj_list(device_list, 'device'))

    return raw_output if raw else _process(raw_output)
