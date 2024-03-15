[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_net_tcp"></a>

# jc.parsers.proc_net_tcp

jc - JSON Convert `/proc/net/tcp` and `proc/net/tcp6` file parser

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

<a id="jc.parsers.proc_net_tcp.parse"></a>

### parse

```python
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[Dict]
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

### Parser Information
Compatibility:  linux

Source: [`jc/parsers/proc_net_tcp.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_net_tcp.py)

Version 1.1 by Alvin Solomon (alvinms01@gmail.com)
