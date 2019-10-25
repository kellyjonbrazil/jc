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
- `--uname` enables the `uname -a` parser
- `--uptime` enables the `uptime` parser
- `--w` enables the `w` parser

### Options
- `-p` specifies whether to pretty format the JSON output

## Examples
### df
```
$ df | jc --df -p
[
  {
    "Filesystem": "udev",
    "1K-blocks": "977500",
    "Used": "0",
    "Available": "977500",
    "Use%": "0%",
    "Mounted": "/dev"
  },
  {
    "Filesystem": "tmpfs",
    "1K-blocks": "201732",
    "Used": "1180",
    "Available": "200552",
    "Use%": "1%",
    "Mounted": "/run"
  },
  {
    "Filesystem": "/dev/sda2",
    "1K-blocks": "20508240",
    "Used": "5747284",
    "Available": "13696152",
    "Use%": "30%",
    "Mounted": "/"
  },
  {
    "Filesystem": "tmpfs",
    "1K-blocks": "1008648",
    "Used": "0",
    "Available": "1008648",
    "Use%": "0%",
    "Mounted": "/dev/shm"
  },
  ...
]
```
### env
```
$ env | jc --env -p
{
  "TERM": "xterm-256color",
  "SHELL": "/bin/bash",
  "USER": "root",
  "PATH": "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin",
  "PWD": "/root",
  "LANG": "en_US.UTF-8",
  "HOME": "/root",
  "LOGNAME": "root",
  "_": "/usr/bin/env"
}
```
### free
```
$ free | jc --free -p
[
  {
    "type": "Mem",
    "total": "2017300",
    "used": "213104",
    "free": "1148452",
    "shared": "1176",
    "buff/cache": "655744",
    "available": "1622204"
  },
  {
    "type": "Swap",
    "total": "2097148",
    "used": "0",
    "free": "2097148"
  }
]
```
### history
```
$ history | jc --history -p
{
  "118": "sleep 100",
  "119": "ls /bin",
  "120": "echo \"hello\"",
  "121": "docker images",
  ...
}
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
### iptables
```
$ sudo iptables -L -t nat | jc --iptables -p
[
  {
    "chain": "PREROUTING",
    "rules": [
      {
        "target": "PREROUTING_direct",
        "prot": "all",
        "opt": "--",
        "source": "anywhere",
        "destination": "anywhere"
      },
      {
        "target": "PREROUTING_ZONES_SOURCE",
        "prot": "all",
        "opt": "--",
        "source": "anywhere",
        "destination": "anywhere"
      },
      {
        "target": "PREROUTING_ZONES",
        "prot": "all",
        "opt": "--",
        "source": "anywhere",
        "destination": "anywhere"
      },
      {
        "target": "DOCKER",
        "prot": "all",
        "opt": "--",
        "source": "anywhere",
        "destination": "anywhere",
        "options": "ADDRTYPE match dst-type LOCAL"
      }
    ]
  },
  {
    "chain": "INPUT",
    "rules": []
  },
  {
    "chain": "OUTPUT",
    "rules": [
      {
        "target": "OUTPUT_direct",
        "prot": "all",
        "opt": "--",
        "source": "anywhere",
        "destination": "anywhere"
      },
      {
        "target": "DOCKER",
        "prot": "all",
        "opt": "--",
        "source": "anywhere",
        "destination": "!loopback/8",
        "options": "ADDRTYPE match dst-type LOCAL"
      }
    ]
  },
  ...
]
```
```
$ sudo iptables -vnL -t filter | jc --iptables -p
[
  {
    "chain": "INPUT",
    "rules": [
      {
        "pkts": "1571",
        "bytes": "3394K",
        "target": "ACCEPT",
        "prot": "all",
        "opt": "--",
        "in": "*",
        "out": "*",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0",
        "options": "ctstate RELATED,ESTABLISHED"
      },
      {
        "pkts": "0",
        "bytes": "0",
        "target": "ACCEPT",
        "prot": "all",
        "opt": "--",
        "in": "lo",
        "out": "*",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0"
      },
      {
        "pkts": "711",
        "bytes": "60126",
        "target": "INPUT_direct",
        "prot": "all",
        "opt": "--",
        "in": "*",
        "out": "*",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0"
      },
      {
        "pkts": "711",
        "bytes": "60126",
        "target": "INPUT_ZONES_SOURCE",
        "prot": "all",
        "opt": "--",
        "in": "*",
        "out": "*",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0"
      },
      {
        "pkts": "711",
        "bytes": "60126",
        "target": "INPUT_ZONES",
        "prot": "all",
        "opt": "--",
        "in": "*",
        "out": "*",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0"
      },
      {
        "pkts": "0",
        "bytes": "0",
        "target": "DROP",
        "prot": "all",
        "opt": "--",
        "in": "*",
        "out": "*",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0",
        "options": "ctstate INVALID"
      },
      {
        "pkts": "710",
        "bytes": "60078",
        "target": "REJECT",
        "prot": "all",
        "opt": "--",
        "in": "*",
        "out": "*",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0",
        "options": "reject-with icmp-host-prohibited"
      }
    ]
  },
  {
    "chain": "FORWARD",
    "rules": [
      {
        "pkts": "0",
        "bytes": "0",
        "target": "DOCKER-ISOLATION",
        "prot": "all",
        "opt": "--",
        "in": "*",
        "out": "*",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0"
      },
      {
        "pkts": "0",
        "bytes": "0",
        "target": "DOCKER",
        "prot": "all",
        "opt": "--",
        "in": "*",
        "out": "docker0",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0"
      },
      {
        "pkts": "0",
        "bytes": "0",
        "target": "ACCEPT",
        "prot": "all",
        "opt": "--",
        "in": "*",
        "out": "docker0",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0",
        "options": "ctstate RELATED,ESTABLISHED"
      },
      {
        "pkts": "0",
        "bytes": "0",
        "target": "ACCEPT",
        "prot": "all",
        "opt": "--",
        "in": "docker0",
        "out": "!docker0",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0"
      },
      {
        "pkts": "0",
        "bytes": "0",
        "target": "ACCEPT",
        "prot": "all",
        "opt": "--",
        "in": "docker0",
        "out": "docker0",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0"
      },
      {
        "pkts": "0",
        "bytes": "0",
        "target": "ACCEPT",
        "prot": "all",
        "opt": "--",
        "in": "*",
        "out": "*",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0",
        "options": "ctstate RELATED,ESTABLISHED"
      },
      {
        "pkts": "0",
        "bytes": "0",
        "target": "ACCEPT",
        "prot": "all",
        "opt": "--",
        "in": "lo",
        "out": "*",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0"
      },
      {
        "pkts": "0",
        "bytes": "0",
        "target": "FORWARD_direct",
        "prot": "all",
        "opt": "--",
        "in": "*",
        "out": "*",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0"
      },
      {
        "pkts": "0",
        "bytes": "0",
        "target": "FORWARD_IN_ZONES_SOURCE",
        "prot": "all",
        "opt": "--",
        "in": "*",
        "out": "*",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0"
      },
      {
        "pkts": "0",
        "bytes": "0",
        "target": "FORWARD_IN_ZONES",
        "prot": "all",
        "opt": "--",
        "in": "*",
        "out": "*",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0"
      },
      {
        "pkts": "0",
        "bytes": "0",
        "target": "FORWARD_OUT_ZONES_SOURCE",
        "prot": "all",
        "opt": "--",
        "in": "*",
        "out": "*",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0"
      },
      {
        "pkts": "0",
        "bytes": "0",
        "target": "FORWARD_OUT_ZONES",
        "prot": "all",
        "opt": "--",
        "in": "*",
        "out": "*",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0"
      },
      {
        "pkts": "0",
        "bytes": "0",
        "target": "DROP",
        "prot": "all",
        "opt": "--",
        "in": "*",
        "out": "*",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0",
        "options": "ctstate INVALID"
      },
      {
        "pkts": "0",
        "bytes": "0",
        "target": "REJECT",
        "prot": "all",
        "opt": "--",
        "in": "*",
        "out": "*",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0",
        "options": "reject-with icmp-host-prohibited"
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
    "pid": 14798,
    "status": "Running",
    "command": "sleep 10000 &"
  },
  {
    "job_number": 2,
    "pid": 14799,
    "status": "Running",
    "command": "sleep 10001 &"
  },
  {
    "job_number": 3,
    "pid": 14800,
    "status": "Running",
    "command": "sleep 10002 &"
  },
  {
    "job_number": 4,
    "pid": 14814,
    "history": "previous",
    "status": "Running",
    "command": "sleep 10003 &"
  },
  {
    "job_number": 5,
    "pid": 14815,
    "history": "current",
    "status": "Running",
    "command": "sleep 10004 &"
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
### lsmod
```
$ lsmod | jc --lsmod -p
[
 {
    "Module": "nf_nat_ipv4",
    "Size": "14115",
    "Used": "1",
    "By": [
      "iptable_nat"
    ]
  },
  {
    "Module": "nf_nat",
    "Size": "26583",
    "Used": "3",
    "By": [
      "nf_nat_ipv4",
      "nf_nat_ipv6",
      "nf_nat_masquerade_ipv4"
    ]
  },
  {
    "Module": "iptable_mangle",
    "Size": "12695",
    "Used": "1"
  },
  {
    "Module": "iptable_security",
    "Size": "12705",
    "Used": "1"
  },
  {
    "Module": "iptable_raw",
    "Size": "12678",
    "Used": "1"
  },
  {
    "Module": "nf_conntrack",
    "Size": "139224",
    "Used": "7",
    "By": [
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
    "COMMAND": "systemd",
    "PID": "1",
    "TID": null,
    "USER": "root",
    "FD": "cwd",
    "TYPE": "DIR",
    "DEVICE": "253,0",
    "SIZE/OFF": "224",
    "NODE": "64",
    "NAME": "/"
  },
  {
    "COMMAND": "systemd",
    "PID": "1",
    "TID": null,
    "USER": "root",
    "FD": "rtd",
    "TYPE": "DIR",
    "DEVICE": "253,0",
    "SIZE/OFF": "224",
    "NODE": "64",
    "NAME": "/"
  },
  {
    "COMMAND": "systemd",
    "PID": "1",
    "TID": null,
    "USER": "root",
    "FD": "txt",
    "TYPE": "REG",
    "DEVICE": "253,0",
    "SIZE/OFF": "1624520",
    "NODE": "50360451",
    "NAME": "/usr/lib/systemd/systemd"
  },
  {
    "COMMAND": "systemd",
    "PID": "1",
    "TID": null,
    "USER": "root",
    "FD": "mem",
    "TYPE": "REG",
    "DEVICE": "253,0",
    "SIZE/OFF": "20064",
    "NODE": "8146",
    "NAME": "/usr/lib64/libuuid.so.1.3.0"
  },
  {
    "COMMAND": "systemd",
    "PID": "1",
    "TID": null,
    "USER": "root",
    "FD": "mem",
    "TYPE": "REG",
    "DEVICE": "253,0",
    "SIZE/OFF": "265600",
    "NODE": "8147",
    "NAME": "/usr/lib64/libblkid.so.1.1.0"
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
  "time": "16:52",
  "uptime": "3 days, 4:49",
  "users": "5",
  "load_1m": "1.85",
  "load_5m": "1.90",
  "load_15m": "1.91"
}
```
### w
```
$ w | jc --w -p
[
  {
    "USER": "root",
    "TTY": "ttyS0",
    "FROM": "-",
    "LOGIN@": "Mon20",
    "IDLE": "2:27",
    "JCPU": "10.61s",
    "PCPU": "10.53s",
    "WHAT": "-bash"
  },
  {
    "USER": "root",
    "TTY": "pts/0",
    "FROM": "192.168.71.1",
    "LOGIN@": "22:58",
    "IDLE": "2.00s",
    "JCPU": "0.04s",
    "PCPU": "0.00s",
    "WHAT": "w"
  }
]
```

## Contributions
Feel free to add/improve code or parsers!

## Acknowledgments
- `ifconfig-parser` module from https://github.com/KnightWhoSayNi/ifconfig-parser
- Parsing code from Conor Heine at https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501
