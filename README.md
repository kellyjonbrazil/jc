# JC
JSON CLI output utility

`jc` is used to JSONify the output of many standard linux cli tools for easier parsing in scripts. See the **Parsers** section for supported commands.

This allows further command line processing of output with tools like `jq` simply by piping commands:

```
$ ls -l /usr/bin | jc --ls | jq '.[] | select(.size > 50000000)'
{
  "filename": "docker",
  "flags": "-rwxr-xr-x",
  "links": 1,
  "owner": "root",
  "group": "root",
  "size": 68677120,
  "date": "Aug 14 19:41"
}
```

The `jc` parsers can also be used as python modules. In this case the output will be a python dictionary instead of JSON:
```
>>> import jc.parsers.ls
>>> 
>>> data='''-rwxr-xr-x  1 root  wheel    23648 May  3 22:26 cat
... -rwxr-xr-x  1 root  wheel    30016 May  3 22:26 chmod
... -rwxr-xr-x  1 root  wheel    29024 May  3 22:26 cp
... -rwxr-xr-x  1 root  wheel   375824 May  3 22:26 csh
... -rwxr-xr-x  1 root  wheel    28608 May  3 22:26 date
... -rwxr-xr-x  1 root  wheel    32000 May  3 22:26 dd
... -rwxr-xr-x  1 root  wheel    23392 May  3 22:26 df
... -rwxr-xr-x  1 root  wheel    18128 May  3 22:26 echo'''
>>>
>>> jc.parsers.ls.parse(data)
[{'filename': 'cat', 'flags': '-rwxr-xr-x', 'links': 1, 'owner': 'root', 'group': 'wheel', 'size': 23648,
'date': 'May 3 22:26'}, {'filename': 'chmod', 'flags': '-rwxr-xr-x', 'links': 1, 'owner': 'root',
'group': 'wheel', 'size': 30016, 'date': 'May 3 22:26'}, {'filename': 'cp', 'flags': '-rwxr-xr-x',
'links': 1, 'owner': 'root', 'group': 'wheel', 'size': 29024, 'date': 'May 3 22:26'}, {'filename': 'csh',
'flags': '-rwxr-xr-x', 'links': 1, 'owner': 'root', 'group': 'wheel', 'size': 375824, 'date': 'May 3
22:26'}, {'filename': 'date', 'flags': '-rwxr-xr-x', 'links': 1, 'owner': 'root', 'group': 'wheel',
'size': 28608, 'date': 'May 3 22:26'}, {'filename': 'dd', 'flags': '-rwxr-xr-x', 'links': 1, 'owner':
'root', 'group': 'wheel', 'size': 32000, 'date': 'May 3 22:26'}, {'filename': 'df', 'flags':
'-rwxr-xr-x', 'links': 1, 'owner': 'root', 'group': 'wheel', 'size': 23392, 'date': 'May 3 22:26'},
{'filename': 'echo', 'flags': '-rwxr-xr-x', 'links': 1, 'owner': 'root', 'group': 'wheel', 'size': 18128,
'date': 'May 3 22:26'}]
```
Two representations of the data are possible. The default representation uses a strict schema per parser and converts known numbers to int/float JSON values. Certain known values of None are converted to JSON Null, known boolean values are converted, and, in some cases, additional semantic context fields are added.

To access the raw, pre-processed JSON, use the `-r` cli option or the `raw=True` function parameter in `parse()`.

Schemas for each parser can be found in the `docs/parsers` folder.

> ***Note:** Due to the introduction of schemas in version `1.5.1` the output for some parsers will be different than in versions `1.1.1` and below.  Now that schemas are defined, the output will be stable for future versions. You can still get similar output to prior versions with the `-r` or `raw=true` options. Though the goal is to keep all output stable, raw output is not guaranteed to stay the same in future releases.*

## Installation
```
$ pip3 install --upgrade jc
```

## Usage
``` 
jc PARSER [OPTIONS]
```

`jc` accepts piped input from `STDIN` and outputs a JSON representation of the previous command's output to `STDOUT`. The JSON output can be compact or pretty formatted.

### Parsers
- `--arp` enables the `arp` parser
- `--df` enables the `df` parser
- `--dig` enables the `dig` parser
- `--env` enables the `env` parser
- `--free` enables the `free` parser
- `--history` enables the `history` parser
- `--ifconfig` enables the `ifconfig` parser
- `--iptables` enables the `iptables` parser
- `--jobs` enables the `jobs` parser
- `--ls` enables the `ls` parser
- `--lsblk` enables the `lsblk` parser
- `--lsmod` enables the `lsmod` parser
- `--lsof` enables the `lsof` parser
- `--mount` enables the `mount` parser
- `--netstat` enables the `netstat` parser
- `--ps` enables the `ps` parser
- `--route` enables the `route` parser
- `--ss` enables the `ss` parser
- `--uname` enables the `uname -a` parser
- `--uptime` enables the `uptime` parser
- `--w` enables the `w` parser

### Options
- `-d` debug mode. Prints trace messages if parsing issues encountered
- `-p` pretty format the JSON output
- `-q` quiet mode. Suppresses warning messages
- `-r` raw output. Provides a more literal JSON output with all values as text and no additional sematic processing

## Examples
### arp
```
$ arp | jc --arp -p
[
  {
    "address": "gateway",
    "hwtype": "ether",
    "hwaddress": "00:50:56:f7:4a:fc",
    "flags_mask": "C",
    "iface": "ens33"
  },
  {
    "address": "192.168.71.1",
    "hwtype": "ether",
    "hwaddress": "00:50:56:c0:00:08",
    "flags_mask": "C",
    "iface": "ens33"
  },
  {
    "address": "192.168.71.254",
    "hwtype": "ether",
    "hwaddress": "00:50:56:fe:7a:b4",
    "flags_mask": "C",
    "iface": "ens33"
  }
]
```
```
$ arp -a | jc --arp -p
[
  {
    "name": null,
    "address": "192.168.71.1",
    "hwtype": "ether",
    "hwaddress": "00:50:56:c0:00:08",
    "iface": "ens33"
  },
  {
    "name": null,
    "address": "192.168.71.254",
    "hwtype": "ether",
    "hwaddress": "00:50:56:fe:7a:b4",
    "iface": "ens33"
  },
  {
    "name": "_gateway",
    "address": "192.168.71.2",
    "hwtype": "ether",
    "hwaddress": "00:50:56:f7:4a:fc",
    "iface": "ens33"
  }
]
```
### df
```
$ df | jc --df -p
[
  {
    "filesystem": "devtmpfs",
    "1k-blocks": 1918816,
    "used": 0,
    "available": 1918816,
    "use_percent": 0,
    "mounted_on": "/dev"
  },
  {
    "filesystem": "tmpfs",
    "1k-blocks": 1930664,
    "used": 0,
    "available": 1930664,
    "use_percent": 0,
    "mounted_on": "/dev/shm"
  },
  ...
]
```
### dig
```
$ dig cnn.com www.cnn.com @205.251.194.64 | jc --dig -p
[
  {
    "id": 5509,
    "opcode": "QUERY",
    "status": "NOERROR",
    "flags": [
      "qr",
      "rd",
      "ra"
    ],
    "query_num": 1,
    "answer_num": 4,
    "authority_num": 0,
    "additional_num": 1,
    "question": {
      "name": "cnn.com.",
      "class": "IN",
      "type": "A"
    },
    "answer": [
      {
        "name": "cnn.com.",
        "class": "IN",
        "type": "A",
        "ttl": 60,
        "data": "151.101.129.67"
      },
      {
        "name": "cnn.com.",
        "class": "IN",
        "type": "A",
        "ttl": 60,
        "data": "151.101.193.67"
      },
      {
        "name": "cnn.com.",
        "class": "IN",
        "type": "A",
        "ttl": 60,
        "data": "151.101.1.67"
      },
      {
        "name": "cnn.com.",
        "class": "IN",
        "type": "A",
        "ttl": 60,
        "data": "151.101.65.67"
      }
    ],
    "query_time": 28,
    "server": "2600",
    "when": "Tue Nov 12 07:13:03 PST 2019",
    "rcvd": 100
  },
  {
    "id": 62696,
    "opcode": "QUERY",
    "status": "NOERROR",
    "flags": [
      "qr",
      "aa",
      "rd"
    ],
    "query_num": 1,
    "answer_num": 1,
    "authority_num": 4,
    "additional_num": 1,
    "question": {
      "name": "www.cnn.com.",
      "class": "IN",
      "type": "A"
    },
    "answer": [
      {
        "name": "www.cnn.com.",
        "class": "IN",
        "type": "CNAME",
        "ttl": 300,
        "data": "turner-tls.map.fastly.net."
      }
    ],
    "authority": [
      {
        "name": "cnn.com.",
        "class": "IN",
        "type": "NS",
        "ttl": 3600,
        "data": "ns-1086.awsdns-07.org."
      },
      {
        "name": "cnn.com.",
        "class": "IN",
        "type": "NS",
        "ttl": 3600,
        "data": "ns-1630.awsdns-11.co.uk."
      },
      {
        "name": "cnn.com.",
        "class": "IN",
        "type": "NS",
        "ttl": 3600,
        "data": "ns-47.awsdns-05.com."
      },
      {
        "name": "cnn.com.",
        "class": "IN",
        "type": "NS",
        "ttl": 3600,
        "data": "ns-576.awsdns-08.net."
      }
    ],
    "query_time": 29,
    "server": "205.251.194.64#53(205.251.194.64)",
    "when": "Tue Nov 12 07:13:03 PST 2019",
    "rcvd": 212
  }
]
```
```
$ dig -x 1.1.1.1 | jc --dig -p
[
  {
    "id": 50324,
    "opcode": "QUERY",
    "status": "NOERROR",
    "flags": [
      "qr",
      "rd",
      "ra"
    ],
    "query_num": 1,
    "answer_num": 1,
    "authority_num": 0,
    "additional_num": 1,
    "question": {
      "name": "1.1.1.1.in-addr.arpa.",
      "class": "IN",
      "type": "PTR"
    },
    "answer": [
      {
        "name": "1.1.1.1.in-addr.arpa.",
        "class": "IN",
        "type": "PTR",
        "ttl": 1634,
        "data": "one.one.one.one."
      }
    ],
    "query_time": 36,
    "server": "2600",
    "when": "Tue Nov 12 07:13:49 PST 2019",
    "rcvd": 78
  }
]
```
### env
```
$ env | jc --env -p
[
  {
    "name": "XDG_SESSION_ID",
    "value": "1"
  },
  {
    "name": "HOSTNAME",
    "value": "localhost.localdomain"
  },
  {
    "name": "TERM",
    "value": "vt220"
  },
  {
    "name": "SHELL",
    "value": "/bin/bash"
  },
  {
    "name": "HISTSIZE",
    "value": "1000"
  },
  ...
]
```
### free
```
$ free | jc --free -p
[
  {
    "type": "Mem",
    "total": 3861340,
    "used": 220508,
    "free": 3381972,
    "shared": 11800,
    "buff_cache": 258860,
    "available": 3397784
  },
  {
    "type": "Swap",
    "total": 2097148,
    "used": 0,
    "free": 2097148
  }
]
```
### history
```
$ history | jc --history -p
[
  {
    "line": "118",
    "command": "sleep 100"
  },
  {
    "line": "119",
    "command": "ls /bin"
  },
  {
    "line": "120",
    "command": "echo \"hello\""
  },
  {
    "line": "121",
    "command": "docker images"
  },
  ...
]
```
### ifconfig
```
$ ifconfig | jc --ifconfig -p
[
  {
    "name": "ens33",
    "flags": 4163,
    "state": "UP,BROADCAST,RUNNING,MULTICAST",
    "mtu": 1500,
    "ipv4_addr": "192.168.71.138",
    "ipv4_mask": "255.255.255.0",
    "ipv4_bcast": "192.168.71.255",
    "ipv6_addr": "fe80::c1cb:715d:bc3e:b8a0",
    "ipv6_mask": 64,
    "ipv6_scope": "link",
    "mac_addr": "00:0c:29:3b:58:0e",
    "type": "Ethernet",
    "rx_packets": 6374,
    "rx_errors": 0,
    "rx_dropped": 0,
    "rx_overruns": 0,
    "rx_frame": 0,
    "tx_packets": 3707,
    "tx_errors": 0,
    "tx_dropped": 0,
    "tx_overruns": 0,
    "tx_carrier": 0,
    "tx_collisions": 0,
    "metric": null
  },
  {
    "name": "lo",
    "flags": 73,
    "state": "UP,LOOPBACK,RUNNING",
    "mtu": 65536,
    "ipv4_addr": "127.0.0.1",
    "ipv4_mask": "255.0.0.0",
    "ipv4_bcast": null,
    "ipv6_addr": "::1",
    "ipv6_mask": 128,
    "ipv6_scope": "host",
    "mac_addr": null,
    "type": "Local Loopback",
    "rx_packets": 81,
    "rx_errors": 0,
    "rx_dropped": 0,
    "rx_overruns": 0,
    "rx_frame": 0,
    "tx_packets": 81,
    "tx_errors": 0,
    "tx_dropped": 0,
    "tx_overruns": 0,
    "tx_carrier": 0,
    "tx_collisions": 0,
    "metric": null
  }
]
```
### iptables
```
$ sudo iptables --line-numbers -v -L -t nat | jc --iptables -p
[
  {
    "chain": "PREROUTING",
    "rules": [
      {
        "num": 1,
        "pkts": 2183,
        "bytes": 186000,
        "target": "PREROUTING_direct",
        "prot": "all",
        "opt": null,
        "in": "any",
        "out": "any",
        "source": "anywhere",
        "destination": "anywhere"
      },
      {
        "num": 2,
        "pkts": 2183,
        "bytes": 186000,
        "target": "PREROUTING_ZONES_SOURCE",
        "prot": "all",
        "opt": null,
        "in": "any",
        "out": "any",
        "source": "anywhere",
        "destination": "anywhere"
      },
      {
        "num": 3,
        "pkts": 2183,
        "bytes": 186000,
        "target": "PREROUTING_ZONES",
        "prot": "all",
        "opt": null,
        "in": "any",
        "out": "any",
        "source": "anywhere",
        "destination": "anywhere"
      },
      {
        "num": 4,
        "pkts": 0,
        "bytes": 0,
        "target": "DOCKER",
        "prot": "all",
        "opt": null,
        "in": "any",
        "out": "any",
        "source": "anywhere",
        "destination": "anywhere",
        "options": "ADDRTYPE match dst-type LOCAL"
      }
    ]
  },
  ...
]
```
### jobs
```
$ jobs -l | jc --jobs -p
[
  {
    "job_number": 1,
    "pid": 5283,
    "status": "Running",
    "command": "sleep 10000 &"
  },
  {
    "job_number": 2,
    "pid": 5284,
    "status": "Running",
    "command": "sleep 10100 &"
  },
  {
    "job_number": 3,
    "pid": 5285,
    "history": "previous",
    "status": "Running",
    "command": "sleep 10001 &"
  },
  {
    "job_number": 4,
    "pid": 5286,
    "history": "current",
    "status": "Running",
    "command": "sleep 10112 &"
  }
]
```
### ls
```
$ ls -l /usr/bin | jc --ls -p
[
  {
    "filename": "apropos",
    "link_to": "whatis",
    "flags": "lrwxrwxrwx.",
    "links": 1,
    "owner": "root",
    "group": "root",
    "size": 6,
    "date": "Aug 15 10:53"
  },
  {
    "filename": "ar",
    "flags": "-rwxr-xr-x.",
    "links": 1,
    "owner": "root",
    "group": "root",
    "size": 62744,
    "date": "Aug 8 16:14"
  },
  {
    "filename": "arch",
    "flags": "-rwxr-xr-x.",
    "links": 1,
    "owner": "root",
    "group": "root",
    "size": 33080,
    "date": "Aug 19 23:25"
  },
  ...
]
```
### lsblk
```
$ lsblk | jc --lsblk -p
[
  {
    "name": "sda",
    "maj_min": "8:0",
    "rm": false,
    "size": "20G",
    "ro": false,
    "type": "disk",
    "mountpoint": null
  },
  {
    "name": "sda1",
    "maj_min": "8:1",
    "rm": false,
    "size": "1G",
    "ro": false,
    "type": "part",
    "mountpoint": "/boot"
  },
  ...
]
```
### lsmod
```
$ lsmod | jc --lsmod -p
[
  ...
  {
    "module": "nf_nat",
    "size": 26583,
    "used": 3,
    "by": [
      "nf_nat_ipv4",
      "nf_nat_ipv6",
      "nf_nat_masquerade_ipv4"
    ]
  },
  {
    "module": "iptable_mangle",
    "size": 12695,
    "used": 1
  },
  {
    "module": "iptable_security",
    "size": 12705,
    "used": 1
  },
  {
    "module": "iptable_raw",
    "size": 12678,
    "used": 1
  },
  {
    "module": "nf_conntrack",
    "size": 139224,
    "used": 7,
    "by": [
      "nf_nat",
      "nf_nat_ipv4",
      "nf_nat_ipv6",
      "xt_conntrack",
      "nf_nat_masquerade_ipv4",
      "nf_conntrack_ipv4",
      "nf_conntrack_ipv6"
    ]
  },
  ...
]
```
### lsof
```
$ sudo lsof | jc --lsof -p
[
  {
    "command": "systemd",
    "pid": 1,
    "tid": null,
    "user": "root",
    "fd": "cwd",
    "type": "DIR",
    "device": "253,0",
    "size_off": 224,
    "node": 64,
    "name": "/"
  },
  {
    "command": "systemd",
    "pid": 1,
    "tid": null,
    "user": "root",
    "fd": "rtd",
    "type": "DIR",
    "device": "253,0",
    "size_off": 224,
    "node": 64,
    "name": "/"
  },
  {
    "command": "systemd",
    "pid": 1,
    "tid": null,
    "user": "root",
    "fd": "txt",
    "type": "REG",
    "device": "253,0",
    "size_off": 1624520,
    "node": 50360451,
    "name": "/usr/lib/systemd/systemd"
  },
  ...
]
```
### mount
```
$ mount | jc --mount -p
[
  {
    "filesystem": "sysfs",
    "mount_point": "/sys",
    "type": "sysfs",
    "options": [
      "rw",
      "nosuid",
      "nodev",
      "noexec",
      "relatime"
    ]
  },
  {
    "filesystem": "proc",
    "mount_point": "/proc",
    "type": "proc",
    "options": [
      "rw",
      "nosuid",
      "nodev",
      "noexec",
      "relatime"
    ]
  },
  {
    "filesystem": "udev",
    "mount_point": "/dev",
    "type": "devtmpfs",
    "options": [
      "rw",
      "nosuid",
      "relatime",
      "size=977500k",
      "nr_inodes=244375",
      "mode=755"
    ]
  },
  ...
]
```
### netstat
```
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
```
### ps
```
$ ps -ef | jc --ps -p
[
  {
    "uid": "root",
    "pid": 1,
    "ppid": 0,
    "c": 0,
    "stime": "Nov01",
    "tty": null,
    "time": "00:00:11",
    "cmd": "/usr/lib/systemd/systemd --switched-root --system --deserialize 22"
  },
  {
    "uid": "root",
    "pid": 2,
    "ppid": 0,
    "c": 0,
    "stime": "Nov01",
    "tty": null,
    "time": "00:00:00",
    "cmd": "[kthreadd]"
  },
  {
    "uid": "root",
    "pid": 4,
    "ppid": 2,
    "c": 0,
    "stime": "Nov01",
    "tty": null,
    "time": "00:00:00",
    "cmd": "[kworker/0:0H]"
  },
  ...
]
```
```
$ ps axu | jc --ps -p
[
  {
    "user": "root",
    "pid": 1,
    "cpu_percent": 0.0,
    "mem_percent": 0.1,
    "vsz": 128072,
    "rss": 6784,
    "tty": null,
    "stat": "Ss",
    "start": "Nov09",
    "time": "0:08",
    "command": "/usr/lib/systemd/systemd --switched-root --system --deserialize 22"
  },
  {
    "user": "root",
    "pid": 2,
    "cpu_percent": 0.0,
    "mem_percent": 0.0,
    "vsz": 0,
    "rss": 0,
    "tty": null,
    "stat": "S",
    "start": "Nov09",
    "time": "0:00",
    "command": "[kthreadd]"
  },
  {
    "user": "root",
    "pid": 4,
    "cpu_percent": 0.0,
    "mem_percent": 0.0,
    "vsz": 0,
    "rss": 0,
    "tty": null,
    "stat": "S<",
    "start": "Nov09",
    "time": "0:00",
    "command": "[kworker/0:0H]"
  },
  ...
]
```
### route
```
$ route -ee | jc --route -p
[
  {
    "destination": "default",
    "gateway": "gateway",
    "genmask": "0.0.0.0",
    "flags": "UG",
    "metric": 100,
    "ref": 0,
    "use": 0,
    "iface": "ens33",
    "mss": 0,
    "window": 0,
    "irtt": 0
  },
  {
    "destination": "172.17.0.0",
    "gateway": "0.0.0.0",
    "genmask": "255.255.0.0",
    "flags": "U",
    "metric": 0,
    "ref": 0,
    "use": 0,
    "iface": "docker",
    "mss": 0,
    "window": 0,
    "irtt": 0
  },
  {
    "destination": "192.168.71.0",
    "gateway": "0.0.0.0",
    "genmask": "255.255.255.0",
    "flags": "U",
    "metric": 100,
    "ref": 0,
    "use": 0,
    "iface": "ens33",
    "mss": 0,
    "window": 0,
    "irtt": 0
  }
]
```
### ss
```
$ sudo ss -a | jc --ss -p
[
  {
    "netid": "nl",
    "state": "UNCONN",
    "recv_q": 0,
    "send_q": 0,
    "peer_address": "*",
    "channel": "rtnl:kernel"
  },
  {
    "netid": "nl",
    "state": "UNCONN",
    "recv_q": 0,
    "send_q": 0,
    "peer_address": "*",
    "pid": 893,
    "channel": "rtnl:systemd-resolve"
  },
  ...
  {
    "netid": "p_raw",
    "state": "UNCONN",
    "recv_q": 0,
    "send_q": 0,
    "peer_address": "*",
    "link_layer": "LLDP",
    "interface": "ens33"
  },
  {
    "netid": "u_dgr",
    "state": "UNCONN",
    "recv_q": 0,
    "send_q": 0,
    "local_port": "93066",
    "peer_address": "*",
    "peer_port": "0",
    "path": "/run/user/1000/systemd/notify"
  },
  {
    "netid": "u_seq",
    "state": "LISTEN",
    "recv_q": 0,
    "send_q": 128,
    "local_port": "20699",
    "peer_address": "*",
    "peer_port": "0",
    "path": "/run/udev/control"
  },
  ...
  {
    "netid": "icmp6",
    "state": "UNCONN",
    "recv_q": 0,
    "send_q": 0,
    "local_address": "*",
    "local_port": "ipv6-icmp",
    "peer_address": "*",
    "peer_port": "*",
    "interface": "ens33"
  },
  {
    "netid": "udp",
    "state": "UNCONN",
    "recv_q": 0,
    "send_q": 0,
    "local_address": "127.0.0.53",
    "local_port": "domain",
    "peer_address": "0.0.0.0",
    "peer_port": "*",
    "interface": "lo"
  },
  {
    "netid": "tcp",
    "state": "LISTEN",
    "recv_q": 0,
    "send_q": 128,
    "local_address": "127.0.0.53",
    "local_port": "domain",
    "peer_address": "0.0.0.0",
    "peer_port": "*",
    "interface": "lo"
  },
  {
    "netid": "tcp",
    "state": "LISTEN",
    "recv_q": 0,
    "send_q": 128,
    "local_address": "0.0.0.0",
    "local_port": "ssh",
    "peer_address": "0.0.0.0",
    "peer_port": "*"
  },
  {
    "netid": "tcp",
    "state": "LISTEN",
    "recv_q": 0,
    "send_q": 128,
    "local_address": "[::]",
    "local_port": "ssh",
    "peer_address": "[::]",
    "peer_port": "*"
  },
  {
    "netid": "v_str",
    "state": "ESTAB",
    "recv_q": 0,
    "send_q": 0,
    "local_address": "999900439",
    "local_port": "1023",
    "peer_address": "0",
    "peer_port": "976",
    "local_port_num": 1023,
    "peer_port_num": 976
  }
]
```
### uname -a
```
$ uname -a | jc --uname -p
{
  "kernel_name": "Linux",
  "node_name": "user-ubuntu",
  "kernel_release": "4.15.0-65-generic",
  "operating_system": "GNU/Linux",
  "hardware_platform": "x86_64",
  "processor": "x86_64",
  "machine": "x86_64",
  "kernel_version": "#74-Ubuntu SMP Tue Sep 17 17:06:04 UTC 2019"
}
```
### uptime
```
$ uptime | jc --uptime -p
{
  "time": "11:30:44",
  "uptime": "1 day, 21:17",
  "users": 1,
  "load_1m": 0.01,
  "load_5m": 0.04,
  "load_15m": 0.05
}
```
### w
```
$ w | jc --w -p
[
  {
    "user": "root",
    "tty": "tty1",
    "from": null,
    "login_at": "07:49",
    "idle": "1:15m",
    "jcpu": "0.00s",
    "pcpu": "0.00s",
    "what": "-bash"
  },
  {
    "user": "root",
    "tty": "ttyS0",
    "from": null,
    "login_at": "06:24",
    "idle": "0.00s",
    "jcpu": "0.43s",
    "pcpu": "0.00s",
    "what": "w"
  },
  {
    "user": "root",
    "tty": "pts/0",
    "from": "192.168.71.1",
    "login_at": "06:29",
    "idle": "2:35m",
    "jcpu": "0.00s",
    "pcpu": "0.00s",
    "what": "-bash"
  }
]
```
## TODO
Future parsers:
- nslookup
- stat
- sar
- sadf
- systemctl
- journalctl
- hosts file
- fstab file
- crontab files
- /proc files
- /sys files

## Contributions
Feel free to add/improve code or parsers! You can use the `jc/parsers/foo.py` parser as a template and submit your parser with a pull request.

## Compatibility
Some parsers like `ls`, `ps`, `dig`, etc. will work on any platform. Other parsers that are platform-specific will generate a warning message if they are used on an unsupported platform. You may still use a parser on an unsupported platform - for example, you may want to parse a file with linux `lsof` output on an OSX laptop. In that case you can suppress the warning message with the `-q` cli option or the `quiet=True` function parameter in `parse()`:

```
$ cat lsof.out | jc --lsof -q
```

Tested on:
- Centos 7.7
- Ubuntu 18.4

## Acknowledgments
- `ifconfig-parser` module from https://github.com/KnightWhoSayNi/ifconfig-parser
- Parsing code from Conor Heine at https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501 adapted for some parsers
