# jc.parsers.netstat
jc - JSON CLI output utility netstat Parser

Usage:

    Specify --netstat as the first argument if the piped input is coming from netstat

Compatibility:

    'linux', 'darwin'

Examples:

    $ sudo netstat -apee | jc --netstat -p
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

    $ sudo netstat -apee | jc --netstat -p -r
    [
      {
        "proto": "tcp",
        "recv_q": "0",
        "send_q": "0",
        "local_address": "localhost",
        "foreign_address": "0.0.0.0",
        "state": "LISTEN",
        "user": "systemd-resolve",
        "inode": "26958",
        "program_name": "systemd-resolve",
        "kind": "network",
        "pid": "887",
        "local_port": "domain",
        "foreign_port": "*",
        "transport_protocol": "tcp",
        "network_protocol": "ipv4"
      },
      {
        "proto": "tcp",
        "recv_q": "0",
        "send_q": "0",
        "local_address": "0.0.0.0",
        "foreign_address": "0.0.0.0",
        "state": "LISTEN",
        "user": "root",
        "inode": "30499",
        "program_name": "sshd",
        "kind": "network",
        "pid": "1186",
        "local_port": "ssh",
        "foreign_port": "*",
        "transport_protocol": "tcp",
        "network_protocol": "ipv4"
      },
      {
        "proto": "tcp",
        "recv_q": "0",
        "send_q": "0",
        "local_address": "localhost",
        "foreign_address": "localhost",
        "state": "ESTABLISHED",
        "user": "root",
        "inode": "46829",
        "program_name": "sshd: root",
        "kind": "network",
        "pid": "2242",
        "local_port": "ssh",
        "foreign_port": "52186",
        "transport_protocol": "tcp",
        "network_protocol": "ipv4"
      },
      {
        "proto": "tcp",
        "recv_q": "0",
        "send_q": "0",
        "local_address": "localhost",
        "foreign_address": "localhost",
        "state": "ESTABLISHED",
        "user": "root",
        "inode": "46828",
        "program_name": "ssh",
        "kind": "network",
        "pid": "2241",
        "local_port": "52186",
        "foreign_port": "ssh",
        "transport_protocol": "tcp",
        "network_protocol": "ipv4"
      },
      {
        "proto": "tcp6",
        "recv_q": "0",
        "send_q": "0",
        "local_address": "[::]",
        "foreign_address": "[::]",
        "state": "LISTEN",
        "user": "root",
        "inode": "30510",
        "program_name": "sshd",
        "kind": "network",
        "pid": "1186",
        "local_port": "ssh",
        "foreign_port": "*",
        "transport_protocol": "tcp",
        "network_protocol": "ipv6"
      },
      {
        "proto": "udp",
        "recv_q": "0",
        "send_q": "0",
        "local_address": "localhost",
        "foreign_address": "0.0.0.0",
        "state": null,
        "user": "systemd-resolve",
        "inode": "26957",
        "program_name": "systemd-resolve",
        "kind": "network",
        "pid": "887",
        "local_port": "domain",
        "foreign_port": "*",
        "transport_protocol": "udp",
        "network_protocol": "ipv4"
      },
      {
        "proto": "raw6",
        "recv_q": "0",
        "send_q": "0",
        "local_address": "[::]",
        "foreign_address": "[::]",
        "state": "7",
        "user": "systemd-network",
        "inode": "27001",
        "program_name": "systemd-network",
        "kind": "network",
        "pid": "867",
        "local_port": "ipv6-icmp",
        "foreign_port": "*",
        "transport_protocol": null,
        "network_protocol": "ipv6"
      },
      {
        "proto": "unix",
        "refcnt": "2",
        "flags": null,
        "type": "DGRAM",
        "state": null,
        "inode": "33322",
        "program_name": "systemd",
        "path": "/run/user/1000/systemd/notify",
        "kind": "socket",
        "pid": " 1607"
      },
      {
        "proto": "unix",
        "refcnt": "2",
        "flags": "ACC",
        "type": "SEQPACKET",
        "state": "LISTENING",
        "inode": "20835",
        "program_name": "init",
        "path": "/run/udev/control",
        "kind": "socket",
        "pid": " 1"
      },
      ...
    ]

## info
```python
info(self, /, *args, **kwargs)
```

## process
```python
process(proc_data)
```

Final processing to conform to the schema.

Parameters:

    proc_data:   (dictionary) raw structured data to process

Returns:

    List of dictionaries. Structured data with the following schema:

    [
      {
        "proto":             string,
        "recv_q":            integer,
        "send_q":            integer,
        "transport_protocol" string,
        "network_protocol":  string,
        "local_address":     string,
        "local_port":        string,
        "local_port_num":    integer,
        "foreign_address":   string,
        "foreign_port":      string,
        "foreign_port_num":  integer,
        "state":             string,
        "program_name":      string,
        "pid":               integer,
        "user":              string,
        "security_context":  string,
        "refcnt":            integer,
        "flags":             string,
        "type":              string,
        "inode":             integer,
        "path":              string,
        "kind":              string,
        "address":           string,
        "osx_inode":         string,
        "conn":              string,
        "refs":              string,
        "nextref":           string,
        "name":              string,
        "unit":              integer,
        "vendor":            integer,
        "class":             integer,
        "subcla":            integer,
        "osx_flags":         integer,
        "pcbcount":          integer,
        "rcvbuf":            integer,
        "sndbuf":            integer,
        "rxbytes":           integer,
        "txbytes":           integer
      }
    ]

## parse
```python
parse(data, raw=False, quiet=False)
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) output preprocessed JSON if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of dictionaries. Raw or processed structured data.

