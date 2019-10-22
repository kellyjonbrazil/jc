# JC
JSON CLI output utility

`jc` is used to JSONify the output of many standard linux cli tools for easier parsing in scripts. See the **Parsers** section for supported commands.

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

The `jc` parsers can also be used as python modules:
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
[{'filename': 'cat', 'flags': '-rwxr-xr-x', 'links': 1, 'owner': 'root', 'group': 'wheel', 
'bytes': 23648, 'date': 'May 3 22:26'}, {'filename': 'chmod', 'flags': '-rwxr-xr-x', 'links': 1, 
'owner': 'root', 'group': 'wheel', 'bytes': 30016, 'date': 'May 3 22:26'}, {'filename': 'cp', 
'flags': '-rwxr-xr-x', 'links': 1, 'owner': 'root', 'group': 'wheel', 'bytes': 29024, 
'date': 'May 3 22:26'}, {'filename': 'csh', 'flags': '-rwxr-xr-x', 'links': 1, 'owner': 'root', 
'group': 'wheel', 'bytes': 375824, 'date': 'May 3 22:26'}, {'filename': 'date', 
'flags': '-rwxr-xr-x', 'links': 1, 'owner': 'root', 'group': 'wheel', 'bytes': 28608, 
'date': 'May 3 22:26'}, {'filename': 'dd', 'flags': '-rwxr-xr-x', 'links': 1, 'owner': 'root', 
'group': 'wheel', 'bytes': 32000, 'date': 'May 3 22:26'}, {'filename': 'df', 'flags': '-rwxr-xr-x', 
'links': 1, 'owner': 'root', 'group': 'wheel', 'bytes': 23392, 'date': 'May 3 22:26'}, 
{'filename': 'echo', 'flags': '-rwxr-xr-x', 'links': 1, 'owner': 'root', 'group': 'wheel', 
'bytes': 18128, 'date': 'May 3 22:26'}]
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

### Parsers
- `--df` enables the `df` parser
- `--env` enables the `env` parser
- `--free` enables the `free` parser
- `--ifconfig` enables the `ifconfig` parser
- `--ls` enables the `ls` parser
- `--lsblk` enables the `lsblk` parser
- `--mount` enables the `mount` parser
- `--netstat` enables the `netstat` parser
- `--ps` enables the `ps` parser
- `--route` enables the `route` parser

### Options
- `-p` specifies whether to pretty format the JSON output

## Examples
### df
```
$ df | jc --df -p
[
  {
    "Filesystem": "/dev/disk1s1",
    "512-blocks": "976490576",
    "Used": "268326664",
    "Available": "702568152",
    "Capacity": "28%",
    "iused": "1395740",
    "ifree": "9223372036853380067",
    "%iused": "0%",
    "Mounted": "/"
  },
  {
    "Filesystem": "devfs",
    "512-blocks": "680",
    "Used": "680",
    "Available": "0",
    "Capacity": "100%",
    "iused": "1178",
    "ifree": "0",
    "%iused": "100%",
    "Mounted": "/dev"
  },
  {
    "Filesystem": "map",
    "512-blocks": "auto_home",
    "Used": "0",
    "Available": "0",
    "Capacity": "0",
    "iused": "100%",
    "ifree": "0",
    "%iused": "0",
    "Mounted": "100%",
    "on": "/home"
  }
]
```
### env
```
$ env | jc --env -p
[
  {
    "TERM": "xterm-256color"
  },
  {
    "SHELL": "/bin/bash"
  },
  {
    "USER": "root"
  },
  {
    "PATH": "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
  },
  {
    "PWD": "/bin"
  },
  {
    "LANG": "en_US.UTF-8"
  },
  {
    "HOME": "/root"
  },
  {
    "_": "/usr/bin/env"
  }
]
```
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
### lsblk
```
$ lsblk | jc --lsblk -p
[
  {
    "NAME": "loop0",
    "MAJ:MIN": "7:0",
    "RM": "0",
    "SIZE": "54.5M",
    "RO": "1",
    "TYPE": "loop",
    "MOUNTPOINT": "/snap/core18/1223"
  },
  {
    "NAME": "sda",
    "MAJ:MIN": "8:0",
    "RM": "0",
    "SIZE": "20G",
    "RO": "0",
    "TYPE": "disk"
  },
  {
    "NAME": "sda1",
    "MAJ:MIN": "8:1",
    "RM": "0",
    "SIZE": "1M",
    "RO": "0",
    "TYPE": "part"
  },
  {
    "NAME": "sda2",
    "MAJ:MIN": "8:2",
    "RM": "0",
    "SIZE": "20G",
    "RO": "0",
    "TYPE": "part",
    "MOUNTPOINT": "/"
  },
  {
    "NAME": "sr0",
    "MAJ:MIN": "11:0",
    "RM": "1",
    "SIZE": "64.8M",
    "RO": "0",
    "TYPE": "rom"
  }
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
    "access": [
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
    "access": [
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
    "access": [
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
