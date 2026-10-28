r"""jc - JSON Convert `/proc/net/udp` and `/proc/net/udp6` file parser

Usage (cli):

    $ cat /proc/net/udp | jc --proc

or

    $ jc /proc/net/udp

or

    $ cat /proc/net/udp | jc --proc-net-udp

Usage (module):

    import jc
    result = jc.parse('proc', proc_net_udp_file)

or

    import jc
    result = jc.parse('proc_net_udp', proc_net_udp_file)

Schema:

Field names and types gathered from the following:

https://github.com/torvalds/linux/blob/master/net/ipv4/udp.c

https://github.com/torvalds/linux/blob/master/net/ipv6/datagram.c

    [
      {
        "entry":                                string,
        "local_address":                        string,
        "local_port":                           integer,
        "remote_address":                       string,
        "remote_port":                          integer,
        "state":                                string,
        "tx_queue":                             string,
        "rx_queue":                             string,
        "timer_active":                         integer,
        "jiffies_until_timer_expires":          string,
        "unrecovered_rto_timeouts":             string,
        "uid":                                  integer,
        "unanswered_0_window_probes":           integer,
        "inode":                                integer,
        "sock_ref_count":                       integer,
        "sock_mem_loc":                         string,
        "drops":                                integer,
        "opposite_endian_local_address":        string,    [0]
        "opposite_endian_remote_address":       string     [0]
      }
    ]

    [0] For IPv6 output originating from an opposite endian architecture
        (e.g. s390x vs. x64) You should not need to use this to process
        output originating from the same machine running `jc` or from a
        machine with the same endianness.

Examples:

    $ cat /proc/net/udp | jc --proc -p
    [
      {
        "entry": "1465",
        "local_address": "127.0.0.54",
        "local_port": 53,
        "remote_address": "0.0.0.0",
        "remote_port": 0,
        "state": "07",
        "tx_queue": "00000000",
        "rx_queue": "00000000",
        "timer_active": 0,
        "jiffies_until_timer_expires": "00000000",
        "unrecovered_rto_timeouts": "00000000",
        "uid": 193,
        "unanswered_0_window_probes": 0,
        "inode": 11301,
        "sock_ref_count": 2,
        "sock_mem_loc": "00000000188b1206",
        "drops": 0
      },
      {
        "entry": "1465",
        "local_address": "127.0.0.53",
        "local_port": 53,
        "remote_address": "0.0.0.0",
        "remote_port": 0,
        "state": "07",
        "tx_queue": "00000000",
        "rx_queue": "00000000",
        "timer_active": 0,
        "jiffies_until_timer_expires": "00000000",
        "unrecovered_rto_timeouts": "00000000",
        "uid": 193,
        "unanswered_0_window_probes": 0,
        "inode": 11299,
        "sock_ref_count": 2,
        "sock_mem_loc": "00000000a7f8edaa",
        "drops": 0
      },
      {
        "entry": "1480",
        "local_address": "192.0.2.10",
        "local_port": 68,
        "remote_address": "192.0.2.1",
        "remote_port": 67,
        "state": "01",
        "tx_queue": "00000000",
        "rx_queue": "00000000",
        "timer_active": 0,
        "jiffies_until_timer_expires": "00000000",
        "unrecovered_rto_timeouts": "00000000",
        "uid": 0,
        "unanswered_0_window_probes": 0,
        "inode": 2764719,
        "sock_ref_count": 2,
        "sock_mem_loc": "000000008eb56d17",
        "drops": 0
      },
      ...
    ]

    $ cat /proc/net/udp | jc --proc -p -r
    [
      {
        "entry": "1465",
        "local_address": "3600007F",
        "local_port": "0035",
        "remote_address": "00000000",
        "remote_port": "0000",
        "state": "07",
        "tx_queue": "00000000",
        "rx_queue": "00000000",
        "timer_active": "00",
        "jiffies_until_timer_expires": "00000000",
        "unrecovered_rto_timeouts": "00000000",
        "uid": "193",
        "unanswered_0_window_probes": "0",
        "inode": "11301",
        "sock_ref_count": "2",
        "sock_mem_loc": "00000000188b1206",
        "drops": "0"
      },
      {
        "entry": "1465",
        "local_address": "3500007F",
        "local_port": "0035",
        "remote_address": "00000000",
        "remote_port": "0000",
        "state": "07",
        "tx_queue": "00000000",
        "rx_queue": "00000000",
        "timer_active": "00",
        "jiffies_until_timer_expires": "00000000",
        "unrecovered_rto_timeouts": "00000000",
        "uid": "193",
        "unanswered_0_window_probes": "0",
        "inode": "11299",
        "sock_ref_count": "2",
        "sock_mem_loc": "00000000a7f8edaa",
        "drops": "0"
      },
      {
        "entry": "1480",
        "local_address": "0A0200C0",
        "local_port": "0044",
        "remote_address": "010200C0",
        "remote_port": "0043",
        "state": "01",
        "tx_queue": "00000000",
        "rx_queue": "00000000",
        "timer_active": "00",
        "jiffies_until_timer_expires": "00000000",
        "unrecovered_rto_timeouts": "00000000",
        "uid": "0",
        "unanswered_0_window_probes": "0",
        "inode": "2764719",
        "sock_ref_count": "2",
        "sock_mem_loc": "000000008eb56d17",
        "drops": "0"
      },
      ...
    ]
"""
import ipaddress
from typing import List, Dict
import jc.utils
from jc.parsers.proc_net_tcp import hex_to_ip


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`/proc/net/udp` and `/proc/net/udp6` file parser'
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
    int_list = {
        'timer_active', 'uid', 'unanswered_0_window_probes', 'inode', 'sock_ref_count',
        'drops'
    }

    for entry in proc_data:
        if 'local_address' in entry:
            local_addr = entry['local_address']
            remote_addr = entry['remote_address']

            entry['local_address'] = hex_to_ip(local_addr)
            entry['local_port'] = int(entry['local_port'], 16)
            entry['remote_address'] = hex_to_ip(remote_addr)
            entry['remote_port'] = int(entry['remote_port'], 16)

            if len(local_addr) == 32:
                opp_endian_local_addr = ':'.join(local_addr[i:i + 4] for i in range(0, 32, 4))
                opp_endian_local_addr = ipaddress.IPv6Address(opp_endian_local_addr).compressed
                opp_endian_remote_addr = ':'.join(remote_addr[i:i + 4] for i in range(0, 32, 4))
                opp_endian_remote_addr = ipaddress.IPv6Address(opp_endian_remote_addr).compressed

                entry['opposite_endian_local_address'] = opp_endian_local_addr
                entry['opposite_endian_remote_address'] = opp_endian_remote_addr

        for item in int_list:
            if item in entry:
                entry[item] = jc.utils.convert_to_int(entry[item])

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

        line_data = jc.utils.splitlines(data)[1:]

        for entry in line_data:
            line = entry.split()

            if not line:
                continue

            output_line = {}
            output_line['entry'] = line[0][:-1]

            local_ip_port = line[1]
            local_ip = local_ip_port.split(':')[0]
            local_port = local_ip_port.split(':')[1]

            output_line['local_address'] = local_ip
            output_line['local_port'] = local_port

            remote_ip_port = line[2]
            remote_ip = remote_ip_port.split(':')[0]
            remote_port = remote_ip_port.split(':')[1]

            output_line['remote_address'] = remote_ip
            output_line['remote_port'] = remote_port

            output_line['state'] = line[3]
            output_line['tx_queue'] = line[4][:8]
            output_line['rx_queue'] = line[4][9:]
            output_line['timer_active'] = line[5][:2]
            output_line['jiffies_until_timer_expires'] = line[5][3:]
            output_line['unrecovered_rto_timeouts'] = line[6]
            output_line['uid'] = line[7]
            output_line['unanswered_0_window_probes'] = line[8]
            output_line['inode'] = line[9]
            output_line['sock_ref_count'] = line[10]
            output_line['sock_mem_loc'] = line[11]
            output_line['drops'] = line[12]

            raw_output.append(output_line)

    return raw_output if raw else _process(raw_output)
