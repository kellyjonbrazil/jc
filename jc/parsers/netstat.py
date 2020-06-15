"""jc - JSON CLI output utility netstat Parser

Usage:

    Specify --netstat as the first argument if the piped input is coming from netstat

Caveats:

    - Use of multiple 'l' options is not supported on OSX (e.g. 'netstat -rlll')
    - Use of the 'A' option is not supported on OSX when using the 'r' option (e.g. netstat -rA)

Compatibility:

    'linux', 'darwin', 'freebsd'

Examples:

    # netstat -apee | jc --netstat -p
    [
      {
        "proto": "tcp",
        "recv_q": 0,
        "send_q": 0,
        "local_address": "localhost",
        "foreign_address": "0.0.0.0",
        "state": "LISTEN",
        "user": "systemd-resolve",
        "inode": 26958,
        "program_name": "systemd-resolve",
        "kind": "network",
        "pid": 887,
        "local_port": "domain",
        "foreign_port": "*",
        "transport_protocol": "tcp",
        "network_protocol": "ipv4"
      },
      {
        "proto": "tcp",
        "recv_q": 0,
        "send_q": 0,
        "local_address": "0.0.0.0",
        "foreign_address": "0.0.0.0",
        "state": "LISTEN",
        "user": "root",
        "inode": 30499,
        "program_name": "sshd",
        "kind": "network",
        "pid": 1186,
        "local_port": "ssh",
        "foreign_port": "*",
        "transport_protocol": "tcp",
        "network_protocol": "ipv4"
      },
      {
        "proto": "tcp",
        "recv_q": 0,
        "send_q": 0,
        "local_address": "localhost",
        "foreign_address": "localhost",
        "state": "ESTABLISHED",
        "user": "root",
        "inode": 46829,
        "program_name": "sshd: root",
        "kind": "network",
        "pid": 2242,
        "local_port": "ssh",
        "foreign_port": "52186",
        "transport_protocol": "tcp",
        "network_protocol": "ipv4",
        "foreign_port_num": 52186
      },
      {
        "proto": "tcp",
        "recv_q": 0,
        "send_q": 0,
        "local_address": "localhost",
        "foreign_address": "localhost",
        "state": "ESTABLISHED",
        "user": "root",
        "inode": 46828,
        "program_name": "ssh",
        "kind": "network",
        "pid": 2241,
        "local_port": "52186",
        "foreign_port": "ssh",
        "transport_protocol": "tcp",
        "network_protocol": "ipv4",
        "local_port_num": 52186
      },
      {
        "proto": "tcp6",
        "recv_q": 0,
        "send_q": 0,
        "local_address": "[::]",
        "foreign_address": "[::]",
        "state": "LISTEN",
        "user": "root",
        "inode": 30510,
        "program_name": "sshd",
        "kind": "network",
        "pid": 1186,
        "local_port": "ssh",
        "foreign_port": "*",
        "transport_protocol": "tcp",
        "network_protocol": "ipv6"
      },
      {
        "proto": "udp",
        "recv_q": 0,
        "send_q": 0,
        "local_address": "localhost",
        "foreign_address": "0.0.0.0",
        "state": null,
        "user": "systemd-resolve",
        "inode": 26957,
        "program_name": "systemd-resolve",
        "kind": "network",
        "pid": 887,
        "local_port": "domain",
        "foreign_port": "*",
        "transport_protocol": "udp",
        "network_protocol": "ipv4"
      },
      {
        "proto": "raw6",
        "recv_q": 0,
        "send_q": 0,
        "local_address": "[::]",
        "foreign_address": "[::]",
        "state": "7",
        "user": "systemd-network",
        "inode": 27001,
        "program_name": "systemd-network",
        "kind": "network",
        "pid": 867,
        "local_port": "ipv6-icmp",
        "foreign_port": "*",
        "transport_protocol": null,
        "network_protocol": "ipv6"
      },
      {
        "proto": "unix",
        "refcnt": 2,
        "flags": null,
        "type": "DGRAM",
        "state": null,
        "inode": 33322,
        "program_name": "systemd",
        "path": "/run/user/1000/systemd/notify",
        "kind": "socket",
        "pid": 1607
      },
      {
        "proto": "unix",
        "refcnt": 2,
        "flags": "ACC",
        "type": "SEQPACKET",
        "state": "LISTENING",
        "inode": 20835,
        "program_name": "init",
        "path": "/run/udev/control",
        "kind": "socket",
        "pid": 1
      },
      ...
    ]

    $ netstat -r | jc --netstat -p
    [
      {
        "destination": "default",
        "gateway": "gateway",
        "genmask": "0.0.0.0",
        "route_flags": "UG",
        "mss": 0,
        "window": 0,
        "irtt": 0,
        "iface": "ens33",
        "kind": "route",
        "route_flags_pretty": [
          "UP",
          "GATEWAY"
        ]
      },
      {
        "destination": "172.17.0.0",
        "gateway": "0.0.0.0",
        "genmask": "255.255.0.0",
        "route_flags": "U",
        "mss": 0,
        "window": 0,
        "irtt": 0,
        "iface": "docker0",
        "kind": "route",
        "route_flags_pretty": [
          "UP"
        ]
      },
      {
        "destination": "192.168.71.0",
        "gateway": "0.0.0.0",
        "genmask": "255.255.255.0",
        "route_flags": "U",
        "mss": 0,
        "window": 0,
        "irtt": 0,
        "iface": "ens33",
        "kind": "route",
        "route_flags_pretty": [
          "UP"
        ]
      }
    ]

    $ netstat -i | jc --netstat -p
    [
      {
        "iface": "ens33",
        "mtu": 1500,
        "rx_ok": 476,
        "rx_err": 0,
        "rx_drp": 0,
        "rx_ovr": 0,
        "tx_ok": 312,
        "tx_err": 0,
        "tx_drp": 0,
        "tx_ovr": 0,
        "flg": "BMRU",
        "kind": "interface"
      },
      {
        "iface": "lo",
        "mtu": 65536,
        "rx_ok": 0,
        "rx_err": 0,
        "rx_drp": 0,
        "rx_ovr": 0,
        "tx_ok": 0,
        "tx_err": 0,
        "tx_drp": 0,
        "tx_ovr": 0,
        "flg": "LRU",
        "kind": "interface"
      }
    ]
"""


class info():
    version = '1.8'
    description = 'netstat command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'freebsd']
    magic_commands = ['netstat']


__version__ = info.version


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (dictionary) raw structured data to process

    Returns:

        List of dictionaries. Structured data with the following schema:

        [
          {
            "proto":                  string,
            "recv_q":                 integer,
            "send_q":                 integer,
            "transport_protocol"      string,
            "network_protocol":       string,
            "local_address":          string,
            "local_port":             string,
            "local_port_num":         integer,
            "foreign_address":        string,
            "foreign_port":           string,
            "foreign_port_num":       integer,
            "state":                  string,
            "program_name":           string,
            "pid":                    integer,
            "user":                   string,
            "security_context":       string,
            "refcnt":                 integer,
            "flags":                  string,
            "type":                   string,
            "inode":                  integer,
            "path":                   string,
            "kind":                   string,
            "address":                string,
            "unix_inode":             string,
            "conn":                   string,
            "refs":                   string,
            "nextref":                string,
            "name":                   string,
            "unit":                   integer,
            "vendor":                 integer,
            "class":                  integer,
            "subcla":                 integer,
            "unix_flags":             integer,
            "pcbcount":               integer,
            "rcvbuf":                 integer,
            "sndbuf":                 integer,
            "rxbytes":                integer,
            "txbytes":                integer,
            "destination":            string,
            "gateway":                string,
            "route_flags":            string,
            "route_flags_pretty": [
                                      string,
            ]
            "route_refs":             integer,
            "use":                    integer,
            "mtu":                    integer,
            "expire":                 string,
            "genmask":                string,
            "mss":                    integer,
            "window":                 integer,
            "irtt":                   integer,
            "iface":                  string,
            "metric":                 integer,
            "network":                string,
            "address":                string,
            "ipkts":                  integer,    - = null
            "ierrs":                  integer,    - = null
            "idrop":                  integer,    - = null
            "opkts":                  integer,    - = null
            "oerrs":                  integer,    - = null
            "coll":                   integer,    - = null
            "rx_ok":                  integer,
            "rx_err":                 integer,
            "rx_drp":                 integer,
            "rx_ovr":                 integer,
            "tx_ok":                  integer,
            "tx_err":                 integer,
            "tx_drp":                 integer,
            "tx_ovr":                 integer,
            "flg":                    string,
            "ibytes":                 integer,
            "obytes":                 integer,
            "r_mbuf":                 integer,
            "s_mbuf":                 integer,
            "r_clus":                 integer,
            "s_clus":                 integer,
            "r_hiwa":                 integer,
            "s_hiwa":                 integer,
            "r_lowa":                 integer,
            "s_lowa":                 integer,
            "r_bcnt":                 integer,
            "s_bcnt":                 integer,
            "r_bmax":                 integer,
            "s_bmax":                 integer,
            "rexmit":                 integer,
            "ooorcv":                 integer,
            "0_win":                  integer,
            "rexmt":                  float,
            "persist":                float,
            "keep":                   float,
            "2msl":                   float,
            "delack":                 float,
            "rcvtime":                float,
          }
        ]
    """
    for entry in proc_data:
        # integer changes
        int_list = ['recv_q', 'send_q', 'pid', 'refcnt', 'inode', 'unit', 'vendor', 'class',
                    'osx_flags', 'subcla', 'pcbcount', 'rcvbuf', 'sndbuf', 'rxbytes', 'txbytes',
                    'route_refs', 'use', 'mtu', 'mss', 'window', 'irtt', 'metric', 'ipkts',
                    'ierrs', 'opkts', 'oerrs', 'coll', 'rx_ok', 'rx_err', 'rx_drp', 'rx_ovr',
                    'tx_ok', 'tx_err', 'tx_drp', 'tx_ovr', 'idrop', 'ibytes', 'obytes', 'r_mbuf',
                    's_mbuf', 'r_clus', 's_clus', 'r_hiwa', 's_hiwa', 'r_lowa', 's_lowa', 'r_bcnt',
                    's_bcnt', 'r_bmax', 's_bmax', 'rexmit', 'ooorcv', '0_win']
        for key in int_list:
            if key in entry:
                try:
                    key_int = int(entry[key])
                    entry[key] = key_int
                except (ValueError):
                    entry[key] = None

        # float changes
        float_list = ['rexmt', 'persist', 'keep', '2msl', 'delack', 'rcvtime']
        for key in float_list:
            if key in entry:
                try:
                    key_float = float(entry[key])
                    entry[key] = key_float
                except (ValueError):
                    entry[key] = None

        if 'local_port' in entry:
            try:
                entry['local_port_num'] = int(entry['local_port'])
            except (ValueError):
                pass

        if 'foreign_port' in entry:
            try:
                entry['foreign_port_num'] = int(entry['foreign_port'])
            except (ValueError):
                pass

    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of dictionaries. Raw or processed structured data.
    """
    import jc.utils
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    cleandata = list(filter(None, data.splitlines()))
    raw_output = []

    if jc.utils.has_data(data):

        # check for FreeBSD/OSX vs Linux
        # is this from FreeBSD/OSX?
        if cleandata[0] == 'Active Internet connections' \
           or cleandata[0] == 'Active Internet connections (including servers)' \
           or cleandata[0] == 'Active Multipath Internet connections' \
           or cleandata[0] == 'Active LOCAL (UNIX) domain sockets' \
           or cleandata[0] == 'Registered kernel control modules' \
           or cleandata[0] == 'Active kernel event sockets' \
           or cleandata[0] == 'Active kernel control sockets' \
           or cleandata[0] == 'Routing tables' \
           or cleandata[0].startswith('Name  '):

            import jc.parsers.netstat_freebsd_osx
            raw_output = jc.parsers.netstat_freebsd_osx.parse(cleandata)

        # use linux parser
        else:
            import jc.parsers.netstat_linux
            raw_output = jc.parsers.netstat_linux.parse(cleandata)

    if raw:
        return raw_output
    else:
        return process(raw_output)
