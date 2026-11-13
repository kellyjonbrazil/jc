[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_net_udp"></a>

# jc.parsers.proc_net_udp

jc - JSON Convert `/proc/net/udp` and `/proc/net/udp6` file parser

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

<a id="jc.parsers.proc_net_udp.parse"></a>

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

Source: [`jc/parsers/proc_net_udp.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_net_udp.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
