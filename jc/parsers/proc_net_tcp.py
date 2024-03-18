r"""jc - JSON Convert `/proc/net/tcp` and `proc/net/tcp6` file parser

IPv4 and IPv6 addresses are converted to standard notation unless the raw
(--raw) option is used.

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

Field names and types gathered from the following:

https://www.kernel.org/doc/Documentation/networking/proc_net_tcp.txt

https://github.com/torvalds/linux/blob/master/net/ipv4/tcp_ipv4.c

https://github.com/torvalds/linux/blob/master/net/ipv6/tcp_ipv6.c

    [
      {
        "entry":                                integer,
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
        "retransmit_timeout":                   integer,
        "soft_clock_tick":                      integer,
        "ack_quick_pingpong":                   integer,
        "sending_congestion_window":            integer,
        "slow_start_size_threshold":            integer,
        "opposite_endian_local_address":        string,    [0]
        "opposite_endian_remote_address":       string     [0]
      }
    ]

    [0] For IPv6 output originating from an opposite endian architecture
        (e.g. s390x vs. x64) You should not need to use this to process
        output originating from the same machine running `jc` or from a
        machine with the same endianness.

Examples:

    $ cat /proc/net/tcp | jc --proc -p
    [
      {
        "entry": "0",
        "local_address": "10.0.0.28",
        "local_port": 42082,
        "remote_address": "64.12.0.108",
        "remote_port": 80,
        "state": "04",
        "tx_queue": "00000001",
        "rx_queue": "00000000",
        "timer_active": 1,
        "jiffies_until_timer_expires": "00000015",
        "unrecovered_rto_timeouts": "00000000",
        "uid": 0,
        "unanswered_0_window_probes": 0,
        "inode": 0,
        "sock_ref_count": 3,
        "sock_mem_loc": "ffff8c7a0de930c0",
        "retransmit_timeout": 21,
        "soft_clock_tick": 4,
        "ack_quick_pingpong": 30,
        "sending_congestion_window": 10,
        "slow_start_size_threshold": -1
      },
      {
        "entry": "1",
        "local_address": "10.0.0.28",
        "local_port": 38864,
        "remote_address": "104.244.42.65",
        "remote_port": 80,
        "state": "06",
        "tx_queue": "00000000",
        "rx_queue": "00000000",
        "timer_active": 3,
        "jiffies_until_timer_expires": "000007C5",
        "unrecovered_rto_timeouts": "00000000",
        "uid": 0,
        "unanswered_0_window_probes": 0,
        "inode": 0,
        "sock_ref_count": 3,
        "sock_mem_loc": "ffff8c7a12d31aa0"
      },
      ...
    ]

    $ cat /proc/net/tcp | jc --proc -p -r
    [
      {
        "entry": "1",
        "local_address": "1C00000A",
        "local_port": "A462",
        "remote_address": "6C000C40",
        "remote_port": "0050",
        "state": "04",
        "tx_queue": "00000001",
        "rx_queue": "00000000",
        "timer_active": "01",
        "jiffies_until_timer_expires": "00000015",
        "unrecovered_rto_timeouts": "00000000",
        "uid": "0",
        "unanswered_0_window_probes": "0",
        "inode": "0",
        "sock_ref_count": "3",
        "sock_mem_loc": "ffff8c7a0de930c0",
        "retransmit_timeout": "21",
        "soft_clock_tick": "4",
        "ack_quick_pingpong": "30",
        "sending_congestion_window": "10",
        "slow_start_size_threshold": "-1"
      },
      {
        "entry": "2",
        "local_address": "1C00000A",
        "local_port": "97D0",
        "remote_address": "412AF468",
        "remote_port": "0050",
        "state": "06",
        "tx_queue": "00000000",
        "rx_queue": "00000000",
        "timer_active": "03",
        "jiffies_until_timer_expires": "000007C5",
        "unrecovered_rto_timeouts": "00000000",
        "uid": "0",
        "unanswered_0_window_probes": "0",
        "inode": "0",
        "sock_ref_count": "3",
        "sock_mem_loc": "ffff8c7a12d31aa0"
      },
      ...
    ]
"""
import socket
import struct
import ipaddress
from typing import List, Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.1'
    description = '`/proc/net/tcp` and `/proc/net/tcp6` file parser'
    author = 'Alvin Solomon'
    author_email = 'alvinms01@gmail.com'
    compatible = ['linux']
    tags = ['file']
    hidden = True


__version__ = info.version


def hex_to_ip(hexaddr: str) -> str:
    if len(hexaddr) == 8:
        addr_long = int(hexaddr, 16)
        return socket.inet_ntop(socket.AF_INET, struct.pack("<L", addr_long))
    elif len(hexaddr) == 32:
        newaddr = ''
        for chunk in range(0, 32, 8):
            chunk_a = hexaddr[chunk + 6:chunk + 8]
            chunk_b = hexaddr[chunk + 4:chunk + 6]
            chunk_c = hexaddr[chunk + 2:chunk + 4]
            chunk_d = hexaddr[chunk + 0:chunk + 2]
            newaddr = newaddr + chunk_a + chunk_b + chunk_c + chunk_d
        full_addr = ':'.join(newaddr[i:i + 4] for i in range(0, 32, 4))
        return ipaddress.IPv6Address(full_addr).compressed

    return ''


def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    int_list = {
        'timer_active', 'uid', 'unanswered_0_window_probes', 'inode',
        'sock_ref_count', 'retransmit_timeout', 'soft_clock_tick',
        'ack_quick_pingpong', 'sending_congestion_window',
        'slow_start_size_threshold'
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

        line_data = data.splitlines()[1:]

        for entry in line_data:
            line = entry.split()
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

            # fields not always included
            if len(line) > 12:
                output_line['retransmit_timeout'] = line[12]
                output_line['soft_clock_tick'] = line[13]
                output_line['ack_quick_pingpong'] = line[14]
                output_line['sending_congestion_window'] = line[15]
                output_line['slow_start_size_threshold'] = line[16]

            raw_output.append(output_line)

    return raw_output if raw else _process(raw_output)
