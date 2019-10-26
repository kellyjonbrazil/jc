# JC
JSON CLI output utility

`jc` is used to JSONify the output of many standard linux cli tools for easier parsing in scripts. See the **Parsers** section for supported commands.

This allows further command line processing of output with tools like `jq` simply by piping commands:

```
$ ls -l /usr/bin | jc --ls | jq '.[] | select(.size|tonumber > 50000000)'
{
  "filename": "emacs",
  "flags": "-r-xr-xr-x",
  "links": 1,
  "owner": "root",
  "group": "wheel",
  "size": "117164432",
  "date": "May 3 22:26"
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
[{'filename': 'cat', 'flags': '-rwxr-xr-x', 'links': 1, 'owner': 'root', 'group': 'wheel', 'size': '23648', 
'date': 'May 3 22:26'}, {'filename': 'chmod', 'flags': '-rwxr-xr-x', 'links': 1, 'owner': 'root', 
'group': 'wheel', 'size': '30016', 'date': 'May 3 22:26'}, {'filename': 'cp', 'flags': '-rwxr-xr-x', 
'links': 1, 'owner': 'root', 'group': 'wheel', 'size': '29024', 'date': 'May 3 22:26'}, {'filename': 'csh', 
'flags': '-rwxr-xr-x', 'links': 1, 'owner': 'root', 'group': 'wheel', 'size': '375824', 'date': 'May 3 22:26'}, 
{'filename': 'date', 'flags': '-rwxr-xr-x', 'links': 1, 'owner': 'root', 'group': 'wheel', 'size': '28608', 
'date': 'May 3 22:26'}, {'filename': 'dd', 'flags': '-rwxr-xr-x', 'links': 1, 'owner': 'root', 'group': 'wheel', 
'size': '32000', 'date': 'May 3 22:26'}, {'filename': 'df', 'flags': '-rwxr-xr-x', 'links': 1, 'owner': 'root', 
'group': 'wheel', 'size': '23392', 'date': 'May 3 22:26'}, {'filename': 'echo', 'flags': '-rwxr-xr-x', 
'links': 1, 'owner': 'root', 'group': 'wheel', 'size': '18128', 'date': 'May 3 22:26'}]
```

The goal is to keep the resulting JSON as flat and simple as possible. Also, keys have been converted to lowercase and special characters are replaced whenever possible.  Numbers are kept as strings because, depending on context or the output options, numbers can sometimes turn into strings. (e.g 'human readable' options)

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
    "filesystem": "udev",
    "1k-blocks": "977500",
    "used": "0",
    "available": "977500",
    "use_percent": "0%",
    "mounted": "/dev"
  },
  {
    "filesystem": "tmpfs",
    "1k-blocks": "201732",
    "used": "1204",
    "available": "200528",
    "use_percent": "1%",
    "mounted": "/run"
  },
  {
    "filesystem": "/dev/sda2",
    "1k-blocks": "20508240",
    "used": "5748312",
    "available": "13695124",
    "use_percent": "30%",
    "mounted": "/"
  },
  {
    "filesystem": "tmpfs",
    "1k-blocks": "1008648",
    "used": "0",
    "available": "1008648",
    "use_percent": "0%",
    "mounted": "/dev/shm"
  }
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
    "buff_cache": "655744",
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
  "n118": "sleep 100",
  "n119": "ls /bin",
  "n120": "echo \"hello\"",
  "n121": "docker images",
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
    "job_number": "1",
    "pid": "19510",
    "status": "Running",
    "command": "sleep 1000 &"
  },
  {
    "job_number": "2",
    "pid": "19511",
    "status": "Running",
    "command": "sleep 1001 &"
  },
  {
    "job_number": "3",
    "pid": "19512",
    "history": "previous",
    "status": "Running",
    "command": "sleep 1002 &"
  },
  {
    "job_number": "4",
    "pid": "19513",
    "history": "current",
    "status": "Running",
    "command": "sleep 1003 &"
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
    "links": "1",
    "owner": "root",
    "group": "root",
    "size": "6",
    "date": "Aug 15 10:53"
  },
  {
    "filename": "arch",
    "flags": "-rwxr-xr-x.",
    "links": "1",
    "owner": "root",
    "group": "root",
    "size": "33080",
    "date": "Aug 19 23:25"
  },
  {
    "filename": "awk",
    "link_to": "gawk",
    "flags": "lrwxrwxrwx.",
    "links": "1",
    "owner": "root",
    "group": "root",
    "size": "4",
    "date": "Aug 15 10:53"
  },
  {
    "filename": "base64",
    "flags": "-rwxr-xr-x.",
    "links": "1",
    "owner": "root",
    "group": "root",
    "size": "37360",
    "date": "Aug 19 23:25"
  },
  {
    "filename": "basename",
    "flags": "-rwxr-xr-x.",
    "links": "1",
    "owner": "root",
    "group": "root",
    "size": "29032",
    "date": "Aug 19 23:25"
  },
  {
    "filename": "bash",
    "flags": "-rwxr-xr-x.",
    "links": "1",
    "owner": "root",
    "group": "root",
    "size": "964600",
    "date": "Aug 8 05:06"
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
    "rm": "0",
    "size": "20G",
    "ro": "0",
    "type": "disk"
  },
  {
    "name": "sda1",
    "maj_min": "8:1",
    "rm": "0",
    "size": "1G",
    "ro": "0",
    "type": "part",
    "mountpoint": "/boot"
  },
  {
    "name": "sda2",
    "maj_min": "8:2",
    "rm": "0",
    "size": "19G",
    "ro": "0",
    "type": "part"
  },
  {
    "name": "centos-root",
    "maj_min": "253:0",
    "rm": "0",
    "size": "17G",
    "ro": "0",
    "type": "lvm",
    "mountpoint": "/"
  },
  {
    "name": "centos-swap",
    "maj_min": "253:1",
    "rm": "0",
    "size": "2G",
    "ro": "0",
    "type": "lvm",
    "mountpoint": "[SWAP]"
  },
  {
    "name": "sr0",
    "maj_min": "11:0",
    "rm": "1",
    "size": "1024M",
    "ro": "0",
    "type": "rom"
  }
]
```
### lsmod
```
$ lsmod | jc --lsmod -p
[
  ...
  {
    "module": "nf_conntrack",
    "size": "139224",
    "used": "7",
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
  {
    "module": "ip_set",
    "size": "45799",
    "used": "0"
  },
  {
    "module": "nfnetlink",
    "size": "14519",
    "used": "1",
    "by": [
      "ip_set"
    ]
  },
  {
    "module": "ebtable_filter",
    "size": "12827",
    "used": "1"
  },
  {
    "module": "ebtables",
    "size": "35009",
    "used": "2",
    "by": [
      "ebtable_nat",
      "ebtable_filter"
    ]
  },
  ...
]
```
### lsof
```
$ sudo lsof | jc --lsof -p | more
[
  {
    "command": "systemd",
    "pid": "1",
    "tid": null,
    "user": "root",
    "fd": "cwd",
    "type": "DIR",
    "device": "8,2",
    "size_off": "4096",
    "node": "2",
    "name": "/"
  },
  {
    "command": "systemd",
    "pid": "1",
    "tid": null,
    "user": "root",
    "fd": "rtd",
    "type": "DIR",
    "device": "8,2",
    "size_off": "4096",
    "node": "2",
    "name": "/"
  },
  {
    "command": "systemd",
    "pid": "1",
    "tid": null,
    "user": "root",
    "fd": "txt",
    "type": "REG",
    "device": "8,2",
    "size_off": "1595792",
    "node": "668802",
    "name": "/lib/systemd/systemd"
  },
  {
    "command": "systemd",
    "pid": "1",
    "tid": null,
    "user": "root",
    "fd": "mem",
    "type": "REG",
    "device": "8,2",
    "size_off": "1700792",
    "node": "656167",
    "name": "/lib/x86_64-linux-gnu/libm-2.27.so"
  },
  {
    "command": "systemd",
    "pid": "1",
    "tid": null,
    "user": "root",
    "fd": "mem",
    "type": "REG",
    "device": "8,2",
    "size_off": "121016",
    "node": "655394",
    "name": "/lib/x86_64-linux-gnu/libudev.so.1.6.9"
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
    "receive_q": "0",
    "send_q": "0"
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
    "receive_q": "0",
    "send_q": "0"
  }
]
```
```
$ sudo netstat -lpn | jc --netstat -p
[
  {
    "transport_protocol": "tcp",
    "network_protocol": "ipv4",
    "local_address": "127.0.0.1",
    "local_port": "25",
    "foreign_address": "0.0.0.0",
    "foreign_port": "*",
    "state": "LISTEN",
    "pid": "1584",
    "program_name": "master",
    "receive_q": "0",
    "send_q": "0"
  },
  {
    "transport_protocol": "tcp",
    "network_protocol": "ipv4",
    "local_address": "0.0.0.0",
    "local_port": "22",
    "foreign_address": "0.0.0.0",
    "foreign_port": "*",
    "state": "LISTEN",
    "pid": "1213",
    "program_name": "sshd",
    "receive_q": "0",
    "send_q": "0"
  },
  {
    "transport_protocol": "tcp",
    "network_protocol": "ipv6",
    "local_address": "::1",
    "local_port": "25",
    "foreign_address": "::",
    "foreign_port": "*",
    "state": "LISTEN",
    "pid": "1584",
    "program_name": "master",
    "receive_q": "0",
    "send_q": "0"
  },
  {
    "transport_protocol": "udp",
    "network_protocol": "ipv4",
    "local_address": "0.0.0.0",
    "local_port": "68",
    "foreign_address": "0.0.0.0",
    "foreign_port": "*",
    "pid": "19177",
    "program_name": "dhclient",
    "receive_q": "0",
    "send_q": "0"
  },
  ...
]
```
### ps
```
$ ps -ef | jc --ps -p
[
  ...
  {
    "uid": "root",
    "pid": "545",
    "ppid": "1",
    "c": "0",
    "stime": "Oct21",
    "tty": "?",
    "time": "00:00:03",
    "cmd": "/usr/lib/systemd/systemd-journald"
  },
  {
    "uid": "root",
    "pid": "566",
    "ppid": "1",
    "c": "0",
    "stime": "Oct21",
    "tty": "?",
    "time": "00:00:00",
    "cmd": "/usr/sbin/lvmetad -f"
  },
  {
    "uid": "root",
    "pid": "580",
    "ppid": "1",
    "c": "0",
    "stime": "Oct21",
    "tty": "?",
    "time": "00:00:00",
    "cmd": "/usr/lib/systemd/systemd-udevd"
  },
  {
    "uid": "root",
    "pid": "659",
    "ppid": "2",
    "c": "0",
    "stime": "Oct21",
    "tty": "?",
    "time": "00:00:00",
    "cmd": "[kworker/u257:0]"
  },
  {
    "uid": "root",
    "pid": "666",
    "ppid": "2",
    "c": "0",
    "stime": "Oct21",
    "tty": "?",
    "time": "00:00:00",
    "cmd": "[hci0]"
  },
  ...
]
```
### route
```
$ route | jc --route -p
[
  {
    "destination": "default",
    "gateway": "gateway",
    "genmask": "0.0.0.0",
    "flags": "UG",
    "metric": "100",
    "ref": "0",
    "use": "0",
    "iface": "ens33"
  },
  {
    "destination": "172.17.0.0",
    "gateway": "0.0.0.0",
    "genmask": "255.255.0.0",
    "flags": "U",
    "metric": "0",
    "ref": "0",
    "use": "0",
    "iface": "docker0"
  },
  {
    "destination": "192.168.71.0",
    "gateway": "0.0.0.0",
    "genmask": "255.255.255.0",
    "flags": "U",
    "metric": "100",
    "ref": "0",
    "use": "0",
    "iface": "ens33"
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
    "user": "root",
    "tty": "ttyS0",
    "from": "-",
    "login_at": "Mon20",
    "idle": "0.00s",
    "jcpu": "14.70s",
    "pcpu": "0.00s",
    "what": "bash"
  },
  {
    "user": "root",
    "tty": "pts/0",
    "from": "192.168.71.1",
    "login_at": "Thu22",
    "idle": "22:46m",
    "jcpu": "0.05s",
    "pcpu": "0.05s",
    "what": "-bash"
  }
]
```

## Contributions
Feel free to add/improve code or parsers!

## Acknowledgments
- `ifconfig-parser` module from https://github.com/KnightWhoSayNi/ifconfig-parser
- Parsing code from Conor Heine at https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501
