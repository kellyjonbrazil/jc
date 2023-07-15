"""jc - JSON Convert `/proc/net/tcp` file parser

Usage (cli):

    $ cat /proc/net/tcp | jc --proc

or

    $ jc /proc/net/tcp

or

    $ cat /proc/net/tcp | jc --proc-net-tcp

Usage (module):

    import jc
    result = jc.parse('proc', proc_net_tcp_file)

or

    import jc
    result = jc.parse('proc_net_tcp', proc_net_tcp_file)

Schema:

    [
      {
        "sl":                           string,
        "local_address":                string,
        "rem_address":                  string,
        "st":                           string,
        "tx_queue":                     string,
        "rx_queue":                     string,
        "tr":                           string,
        "tm->when":                     string,
        "retrnsmt":                     string,
        "uid":                          string,
        "timeout":                      string,
        "inode":                        string,
        "sock_ref_count":               string,
        "sock_mem_loc":                 string,
        "retransmit_timeout":           string,
        "soft_clock_tick":              string,
        "(ack.quick<<1)|ack.pingpong":  string,
        "sending_congestion_window":    string,
        "slow_start_size_threshold":    string
      }
    ]

Examples:

    $ cat /proc/net/tcp | jc --proc -p
    [
      {
        "sl": "1",
        "local_address": "0100007F:0277",
        "rem_address": "00000000:0000",
        "st": "0A",
        "tx_queue": "00000000",
        "rx_queue": "00000000",
        "tr": "00",
        "tm->when": "00000000",
        "retrnsmt": "00000000",
        "uid": "101",
        "timeout": "0",
        "inode": "57192",
        "sock_ref_count": "1",
        "sock_mem_loc": "0000000000000000",
        "retransmit_timeout": "100",
        "soft_clock_tick": "0",
        "(ack.quick<<1)|ack.pingpong": "0",
        "sending_congestion_window": "10",
        "slow_start_size_threshold": "5"
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
    description = '`/proc/net/tcp` file parser'
    author = 'Alvin Solomon'
    author_email = 'alvinms01@gmail.com'
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

    data = data.splitlines()[1:]

    if jc.utils.has_data(data):

        for line in data:
            line = line.split()
            output_line = {}
            output_line['sl'] = line[0][:-1]
            output_line['local_address'] = line[1]
            output_line['rem_address'] = line[2]
            output_line['st'] = line[3]
            output_line['tx_queue'] = line[4][:8]
            output_line['rx_queue'] = line[4][9:]
            output_line['tr'] = line[5][:2]
            output_line['tm->when'] = line[5][3:]
            output_line['retrnsmt'] = line[6]
            output_line['uid'] = line[7]
            output_line['timeout'] = line[8]
            output_line['inode'] = line[9]
            output_line['sock_ref_count'] = line[10]
            output_line['sock_mem_loc'] = line[11]
            output_line['retransmit_timeout'] = line[12]
            output_line['soft_clock_tick'] = line[13]
            output_line['(ack.quick<<1)|ack.pingpong'] = line[14]
            output_line['sending_congestion_window'] = line[15]
            output_line['slow_start_size_threshold'] = line[16]

            raw_output.append(output_line)

    return raw_output if raw else _process(raw_output)
