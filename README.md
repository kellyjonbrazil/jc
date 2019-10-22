# JC
JSON CLI output utility

`jc` is used to JSONify the output of many standard linux cli tools for easier parsing in scripts. Parsers for `ls`, `ifconfig`, `ps`, `route`, and `netstat` are currently included and more can be added via modules.

This allows further command line processing of output with tools like `jq` simply by piping commands:

```
$ ls -l /usr/bin | jc --ls | jq '.[] | select(.bytes > 50000000)'
{
  "filename": "emacs",
  "flags": "-r-xr-xr-x",
  "links": 1,
  "owner": "root",
  "group": "wheel",
  "bytes": 117164432,
  "date": "May 3 22:26"
}
```

The `jc` parsers can also be used as python modules by referencing them via:
```
import jc.parsers.[parser]

data = 'data to parse'
jc.parsers.[parser].parse(data)
```
In this case the output will be a python dictionary instead of JSON.

## Installation
```
$ pip3 install jc
```

## Usage
``` 
jc [parser] [options]
```

`jc` accepts piped input from `STDIN` and outputs a JSON representation of the previous command's output to `STDOUT`. The JSON output can be compact or pretty formatted.

Parsers:
- `--ifconfig` enables the `ifconfig` parser
- `--ls` enables the `ls` parser
- `--netstat` enables the `netstat` parser
- `--ps` enables the `ps` parser
- `--route` enables the `route` parser

Options:
- `-p` specifies whether to pretty format the JSON output

## Examples
### ifconfig
```
$ ifconfig | jc --ifconfig -p
[
  {
    "name": "docker0",
    "flags": "4099",
    "state": "UP,BROADCAST,MULTICAST",
    "mtu": "1500",
    "ipv4_addr": "172.17.0.1",
    "ipv4_mask": "255.255.0.0",
    "ipv4_bcast": "0.0.0.0",
    "mac_addr": "02:42:53:18:31:cc",
    "type": "Ethernet",
    "rx_packets": "0",
    "rx_errors": "0",
    "rx_dropped": "0",
    "rx_overruns": "0",
    "rx_frame": "0",
    "tx_packets": "0",
    "tx_errors": "0",
    "tx_dropped": "0",
    "tx_overruns": "0",
    "tx_carrier": "0",
    "tx_collisions": "0",
    "ipv6_addr": null,
    "ipv6_mask": null,
    "ipv6_scope": null,
    "metric": null
  },
  {
    "name": "ens33",
    "flags": "4163",
    "state": "UP,BROADCAST,RUNNING,MULTICAST",
    "mtu": "1500",
    "ipv4_addr": "192.168.71.135",
    "ipv4_mask": "255.255.255.0",
    "ipv4_bcast": "192.168.71.255",
    "ipv6_addr": "fe80::c1cb:715d:bc3e:b8a0",
    "ipv6_mask": "64",
    "ipv6_scope": "link",
    "mac_addr": "00:0c:29:3b:58:0e",
    "type": "Ethernet",
    "rx_packets": "26348",
    "rx_errors": "0",
    "rx_dropped": "0",
    "rx_overruns": "0",
    "rx_frame": "0",
    "tx_packets": "5308",
    "tx_errors": "0",
    "tx_dropped": "0",
    "tx_overruns": "0",
    "tx_carrier": "0",
    "tx_collisions": "0",
    "metric": null
  },
  {
    "name": "lo",
    "flags": "73",
    "state": "UP,LOOPBACK,RUNNING",
    "mtu": "65536",
    "ipv4_addr": "127.0.0.1",
    "ipv4_mask": "255.0.0.0",
    "ipv4_bcast": null,
    "ipv6_addr": "::1",
    "ipv6_mask": "128",
    "ipv6_scope": "host",
    "mac_addr": null,
    "type": "Local Loopback",
    "rx_packets": "64",
    "rx_errors": "0",
    "rx_dropped": "0",
    "rx_overruns": "0",
    "rx_frame": "0",
    "tx_packets": "64",
    "tx_errors": "0",
    "tx_dropped": "0",
    "tx_overruns": "0",
    "tx_carrier": "0",
    "tx_collisions": "0",
    "metric": null
  }
]
```
### ls
```
$ ls -l /bin | jc --ls -p
[
  {
    "filename": "bash",
    "flags": "-r-xr-xr-x",
    "links": 1,
    "owner": "root",
    "group": "wheel",
    "bytes": 618416,
    "date": "May 3 22:26"
  },
  {
    "filename": "cat",
    "flags": "-rwxr-xr-x",
    "links": 1,
    "owner": "root",
    "group": "wheel",
    "bytes": 23648,
    "date": "May 3 22:26"
  },
  {
    "filename": "chmod",
    "flags": "-rwxr-xr-x",
    "links": 1,
    "owner": "root",
    "group": "wheel",
    "bytes": 30016,
    "date": "May 3 22:26"
  },
  ...
]
```
### netstat
```
$ netstat -p | jc --netstat -p
[
  {
    "transport_protocol": "tcp",
    "network_protocol": "ipv4",
    "local_address": "localhost.localdo",
    "local_port": "34480",
    "foreign_address": "lb-192-30-255-113",
    "foreign_port": "https",
    "state": "ESTABLISHED",
    "pid": 53550,
    "program_name": "git-remote-ht",
    "receive_q": 0,
    "send_q": 0
  },
  {
    "transport_protocol": "tcp",
    "network_protocol": "ipv4",
    "local_address": "localhost.localdo",
    "local_port": "34478",
    "foreign_address": "lb-192-30-255-113",
    "foreign_port": "https",
    "state": "ESTABLISHED",
    "pid": 53550,
    "program_name": "git-remote-ht",
    "receive_q": 0,
    "send_q": 0
  }
]
```
```
$ netstat -lpn | jc --netstat -p
[
  {
    "transport_protocol": "tcp",
    "network_protocol": "ipv4",
    "local_address": "127.0.0.1",
    "local_port": "42351",
    "foreign_address": "0.0.0.0",
    "foreign_port": "*",
    "state": "LISTEN",
    "pid": 1112,
    "program_name": "containerd",
    "receive_q": 0,
    "send_q": 0
  },
  {
    "transport_protocol": "tcp",
    "network_protocol": "ipv4",
    "local_address": "127.0.0.53",
    "local_port": "53",
    "foreign_address": "0.0.0.0",
    "foreign_port": "*",
    "state": "LISTEN",
    "pid": 885,
    "program_name": "systemd-resolve",
    "receive_q": 0,
    "send_q": 0
  },
  {
    "transport_protocol": "tcp",
    "network_protocol": "ipv4",
    "local_address": "0.0.0.0",
    "local_port": "22",
    "foreign_address": "0.0.0.0",
    "foreign_port": "*",
    "state": "LISTEN",
    "pid": 1127,
    "program_name": "sshd",
    "receive_q": 0,
    "send_q": 0
  },
  {
    "transport_protocol": "tcp",
    "network_protocol": "ipv6",
    "local_address": "::",
    "local_port": "22",
    "foreign_address": "::",
    "foreign_port": "*",
    "state": "LISTEN",
    "pid": 1127,
    "program_name": "sshd",
    "receive_q": 0,
    "send_q": 0
  },
  {
    "transport_protocol": "udp",
    "network_protocol": "ipv4",
    "local_address": "127.0.0.53",
    "local_port": "53",
    "foreign_address": "0.0.0.0",
    "foreign_port": "*",
    "pid": 885,
    "program_name": "systemd-resolve",
    "receive_q": 0,
    "send_q": 0
  },
  {
    "transport_protocol": "udp",
    "network_protocol": "ipv4",
    "local_address": "192.168.71.131",
    "local_port": "68",
    "foreign_address": "0.0.0.0",
    "foreign_port": "*",
    "pid": 867,
    "program_name": "systemd-network",
    "receive_q": 0,
    "send_q": 0
  }
]
```
### ps
```
$ ps -ef | jc --ps -p
[
  {
    "UID": "root",
    "PID": "1",
    "PPID": "0",
    "C": "0",
    "STIME": "13:58",
    "TTY": "?",
    "TIME": "00:00:05",
    "CMD": "/lib/systemd/systemd --system --deserialize 35"
  },
  {
    "UID": "root",
    "PID": "2",
    "PPID": "0",
    "C": "0",
    "STIME": "13:58",
    "TTY": "?",
    "TIME": "00:00:00",
    "CMD": "[kthreadd]"
  },
  {
    "UID": "root",
    "PID": "4",
    "PPID": "2",
    "C": "0",
    "STIME": "13:58",
    "TTY": "?",
    "TIME": "00:00:00",
    "CMD": "[kworker/0:0H]"
  },
  {
    "UID": "root",
    "PID": "6",
    "PPID": "2",
    "C": "0",
    "STIME": "13:58",
    "TTY": "?",
    "TIME": "00:00:00",
    "CMD": "[mm_percpu_wq]"
  },
  ...
]
```
### route
```
$ route -n | jc --route -p
[
  {
    "Destination": "0.0.0.0",
    "Gateway": "192.168.71.2",
    "Genmask": "0.0.0.0",
    "Flags": "UG",
    "Metric": "100",
    "Ref": "0",
    "Use": "0",
    "Iface": "ens33"
  },
  {
    "Destination": "172.17.0.0",
    "Gateway": "0.0.0.0",
    "Genmask": "255.255.0.0",
    "Flags": "U",
    "Metric": "0",
    "Ref": "0",
    "Use": "0",
    "Iface": "docker0"
  },
  {
    "Destination": "192.168.71.0",
    "Gateway": "0.0.0.0",
    "Genmask": "255.255.255.0",
    "Flags": "U",
    "Metric": "0",
    "Ref": "0",
    "Use": "0",
    "Iface": "ens33"
  },
  {
    "Destination": "192.168.71.2",
    "Gateway": "0.0.0.0",
    "Genmask": "255.255.255.255",
    "Flags": "UH",
    "Metric": "100",
    "Ref": "0",
    "Use": "0",
    "Iface": "ens33"
  }
]
```

## Contributions
Feel free to add/improve code or parsers!

## Acknowledgments
- `ifconfig-parser` module from https://github.com/KnightWhoSayNi/ifconfig-parser
- Parsing code from Conor Heine at https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501
