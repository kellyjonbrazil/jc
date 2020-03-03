# JC
JSON CLI output utility

`jc` is used to JSONify the output of many standard linux cli tools and file types for easier parsing in scripts. See the [**Parsers**](#parsers) section for supported commands and file types.

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
or using the alternative "magic" syntax:
```
$ jc ls -l /usr/bin | jq '.[] | select(.size > 50000000)'
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
The `jc` parsers can also be used as python modules. In this case the output will be a python dictionary, or list of dictionaries, instead of JSON:
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
Two representations of the data are possible. The default representation uses a strict schema per parser and converts known numbers to int/float JSON values. Certain known values of `None` are converted to JSON `null`, known boolean values are converted, and, in some cases, additional semantic context fields are added.

To access the raw, pre-processed JSON, use the `-r` cli option or the `raw=True` function parameter in `parse()`.

Schemas for each parser can be found in the [`docs/parsers`](https://github.com/kellyjonbrazil/jc/tree/master/docs/parsers) folder. 

Release notes can be found [here](https://blog.kellybrazil.com/category/jc-news/).

For more information on the motivations for this project, please see my [blog post](https://blog.kellybrazil.com/2019/11/26/bringing-the-unix-philosophy-to-the-21st-century/).

## Installation
```
$ pip3 install --upgrade jc
```

## Usage
`jc` accepts piped input from `STDIN` and outputs a JSON representation of the previous command's output to `STDOUT`.
``` 
COMMAND | jc PARSER [OPTIONS]
```
Alternatively, the "magic" syntax can be used by prepending `jc` to the command to be converted. Options can be passed to `jc` immediately before the command is given. (Note: command aliases are not supported)
```
jc [OPTIONS] COMMAND
```
The JSON output can be compact (default) or pretty formatted with the `-p` option.

### Parsers
- `--arp` enables the `arp` command parser
- `--blkid` enables the `blkid` command parser
- `--crontab` enables the `crontab` command and file parser
- `--crontab-u` enables the `crontab` file parser with user support
- `--csv` enables the CSV file parser
- `--df` enables the `df` command parser
- `--dig` enables the `dig` command parser
- `--du` enables the `du` command parser
- `--env` enables the `env` command parser
- `--free` enables the `free` command parser
- `--fstab` enables the `/etc/fstab` file parser
- `--group` enables the `/etc/group` file parser
- `--gshadow` enables the `/etc/gshadow` file parser
- `--history` enables the `history` command parser
- `--hosts` enables the `/etc/hosts` file parser
- `--id` enables the `id` command parser
- `--ifconfig` enables the `ifconfig` command parser
- `--ini` enables the `INI` file parser
- `--iptables` enables the `iptables` command parser
- `--jobs` enables the `jobs` command parser
- `--last` enables the `last` and `lastb` command parser
- `--ls` enables the `ls` command parser
- `--lsblk` enables the `lsblk` command parser
- `--lsmod` enables the `lsmod` command parser
- `--lsof` enables the `lsof` command parser
- `--mount` enables the `mount` command parser
- `--netstat` enables the `netstat` command parser
- `--passwd` enables the `/etc/passwd` file parser
- `--pip-list` enables the `pip list` command parser
- `--pip-show` enables the `pip show` command parser
- `--ps` enables the `ps` command parser
- `--route` enables the `route` command parser
- `--shadow` enables the `/etc/shadow` file parser
- `--ss` enables the `ss` command parser
- `--stat` enables the `stat` command parser
- `--systemctl` enables the `systemctl` command parser
- `--systemctl-lj` enables the `systemctl list-jobs` command parser
- `--systemctl-ls` enables the `systemctl list-sockets` command parser
- `--systemctl-luf` enables the `systemctl list-unit-files` command parser
- `--uname` enables the `uname -a` command parser
- `--uptime` enables the `uptime` command parser
- `--w` enables the `w` command parser
- `--who` enables the `who` command parser
- `--xml` enables the `XML` file parser
- `--yaml` enables the `YAML` file parser

### Options
- `-a` about `jc`. Prints information about `jc` and the parsers (in JSON, of course!)
- `-d` debug mode. Prints trace messages if parsing issues encountered
- `-p` pretty format the JSON output
- `-q` quiet mode. Suppresses warning messages
- `-r` raw output. Provides a more literal JSON output with all values as text and no additional sematic processing

## Contributions
Feel free to add/improve code or parsers! You can use the [`jc/parsers/foo.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/foo.py) parser as a template and submit your parser with a pull request.

## Compatibility
Some parsers like `ls`, `ps`, `dig`, etc. will work on any platform. Other parsers that are platform-specific will generate a warning message if they are used on an unsupported platform. To see all parser information, including compatibility, run `jc -ap`.


You may still use a parser on an unsupported platform - for example, you may want to parse a file with linux `lsof` output on an OSX laptop. In that case you can suppress the warning message with the `-q` cli option or the `quiet=True` function parameter in `parse()`:

```
$ cat lsof.out | jc --lsof -q
```

Tested on:
- Centos 7.7
- Ubuntu 18.4
- OSX 10.11.6
- OSX 10.14.6

## Acknowledgments
- `ifconfig-parser` module from https://github.com/KnightWhoSayNi/ifconfig-parser
- `xmltodict` module from https://github.com/martinblech/xmltodict by Martín Blech
- `ruamel.yaml` library from https://pypi.org/project/ruamel.yaml by  Anthon van der Neut
- Parsing code from Conor Heine at https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501 adapted for some parsers
- Excellent constructive feedback from Ilya Sher (https://github.com/ilyash-b)

## Examples
### arp
```
$ arp | jc --arp -p          # or:  jc -p arp
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
$ arp -a | jc --arp -p          # or:  jc -p arp -a
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
### blkid
```
$ blkid | jc --blkid -p          # or:  jc -p blkid
[
  {
    "device": "/dev/sda1",
    "uuid": "05d927ab-5875-49e4-ada1-7f46cb32c932",
    "type": "xfs"
  },
  {
    "device": "/dev/sda2",
    "uuid": "3klkIj-w1kk-DkJi-0XBJ-y3i7-i2Ac-vHqWBM",
    "type": "LVM2_member"
  },
  {
    "device": "/dev/mapper/centos-root",
    "uuid": "07d718ff-950c-4e5b-98f0-42a1147c77d9",
    "type": "xfs"
  },
  {
    "device": "/dev/mapper/centos-swap",
    "uuid": "615eb89a-bcbf-46fd-80e3-c483ff5c931f",
    "type": "swap"
  }
]
```
```
$ sudo blkid -o udev -ip /dev/sda2 | jc --blkid -p          # or:  sudo jc -p blkid -o udev -ip /dev/sda2
[
  {
    "id_fs_uuid": "3klkIj-w1kk-DkJi-0XBJ-y3i7-i2Ac-vHqWBM",
    "id_fs_uuid_enc": "3klkIj-w1kk-DkJi-0XBJ-y3i7-i2Ac-vHqWBM",
    "id_fs_version": "LVM2\x20001",
    "id_fs_type": "LVM2_member",
    "id_fs_usage": "raid",
    "id_iolimit_minimum_io_size": 512,
    "id_iolimit_physical_sector_size": 512,
    "id_iolimit_logical_sector_size": 512,
    "id_part_entry_scheme": "dos",
    "id_part_entry_type": "0x8e",
    "id_part_entry_number": 2,
    "id_part_entry_offset": 2099200,
    "id_part_entry_size": 39843840,
    "id_part_entry_disk": "8:0"
  }
]
```
### crontab
```
$ cat /etc/crontab | jc --crontab -p          # or:  jc -p crontab -l
{
  "variables": [
    {
      "name": "MAILTO",
      "value": "root"
    },
    {
      "name": "PATH",
      "value": "/sbin:/bin:/usr/sbin:/usr/bin"
    },
    {
      "name": "SHELL",
      "value": "/bin/bash"
    }
  ],
  "schedule": [
    {
      "minute": [
        "5"
      ],
      "hour": [
        "10-11",
        "22"
      ],
      "day_of_month": [
        "*"
      ],
      "month": [
        "*"
      ],
      "day_of_week": [
        "*"
      ],
      "command": "/var/www/devdaily.com/bin/mk-new-links.php"
    },
    {
      "minute": [
        "30"
      ],
      "hour": [
        "4/2"
      ],
      "day_of_month": [
        "*"
      ],
      "month": [
        "*"
      ],
      "day_of_week": [
        "*"
      ],
      "command": "/var/www/devdaily.com/bin/create-all-backups.sh"
    },
    {
      "occurrence": "yearly",
      "command": "/home/maverick/bin/annual-maintenance"
    },
    {
      "occurrence": "reboot",
      "command": "/home/cleanup"
    },
    {
      "occurrence": "monthly",
      "command": "/home/maverick/bin/tape-backup"
    }
  ]
}
```
### crontab-u (with user support)
```
$ cat /etc/crontab | jc --crontab-u -p
{
  "variables": [
    {
      "name": "MAILTO",
      "value": "root"
    },
    {
      "name": "PATH",
      "value": "/sbin:/bin:/usr/sbin:/usr/bin"
    },
    {
      "name": "SHELL",
      "value": "/bin/bash"
    }
  ],
  "schedule": [
    {
      "minute": [
        "5"
      ],
      "hour": [
        "10-11",
        "22"
      ],
      "day_of_month": [
        "*"
      ],
      "month": [
        "*"
      ],
      "day_of_week": [
        "*"
      ],
      "user": "root",
      "command": "/var/www/devdaily.com/bin/mk-new-links.php"
    },
    {
      "minute": [
        "30"
      ],
      "hour": [
        "4/2"
      ],
      "day_of_month": [
        "*"
      ],
      "month": [
        "*"
      ],
      "day_of_week": [
        "*"
      ],
      "user": "root",
      "command": "/var/www/devdaily.com/bin/create-all-backups.sh"
    },
    {
      "occurrence": "yearly",
      "user": "root",
      "command": "/home/maverick/bin/annual-maintenance"
    },
    {
      "occurrence": "reboot",
      "user": "root",
      "command": "/home/cleanup"
    },
    {
      "occurrence": "monthly",
      "user": "root",
      "command": "/home/maverick/bin/tape-backup"
    }
  ]
}
```
### CSV files
```
$ cat homes.csv 
"Sell", "List", "Living", "Rooms", "Beds", "Baths", "Age", "Acres", "Taxes"
142, 160, 28, 10, 5, 3,  60, 0.28,  3167
175, 180, 18,  8, 4, 1,  12, 0.43,  4033
129, 132, 13,  6, 3, 1,  41, 0.33,  1471
...

$ cat homes.csv | jc --csv -p
[
  {
    "Sell": "142",
    "List": "160",
    "Living": "28",
    "Rooms": "10",
    "Beds": "5",
    "Baths": "3",
    "Age": "60",
    "Acres": "0.28",
    "Taxes": "3167"
  },
  {
    "Sell": "175",
    "List": "180",
    "Living": "18",
    "Rooms": "8",
    "Beds": "4",
    "Baths": "1",
    "Age": "12",
    "Acres": "0.43",
    "Taxes": "4033"
  },
  {
    "Sell": "129",
    "List": "132",
    "Living": "13",
    "Rooms": "6",
    "Beds": "3",
    "Baths": "1",
    "Age": "41",
    "Acres": "0.33",
    "Taxes": "1471"
  },
  ...
]
```
### df
```
$ df | jc --df -p          # or:  jc -p df
[
  {
    "filesystem": "devtmpfs",
    "1k_blocks": 1918816,
    "used": 0,
    "available": 1918816,
    "use_percent": 0,
    "mounted_on": "/dev"
  },
  {
    "filesystem": "tmpfs",
    "1k_blocks": 1930664,
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
$ dig cnn.com www.cnn.com @205.251.194.64 | jc --dig -p          # or:  jc -p dig cnn.com www.cnn.com @205.251.194.64
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
$ dig -x 1.1.1.1 | jc --dig -p          # or:  jc -p dig -x 1.1.1.1
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
### du
```
$ du /usr | jc --du -p          # or:  jc -p du /usr
[
  {
    "size": 104608,
    "name": "/usr/bin"
  },
  {
    "size": 56,
    "name": "/usr/standalone/firmware/iBridge1_1Customer.bundle/Contents/_CodeSignature"
  },
  {
    "size": 0,
    "name": "/usr/standalone/firmware/iBridge1_1Customer.bundle/Contents/Resources/Firmware/usr/local/standalone"
  },
  {
    "size": 0,
    "name": "/usr/standalone/firmware/iBridge1_1Customer.bundle/Contents/Resources/Firmware/usr/local"
  },
  {
    "size": 0,
    "name": "/usr/standalone/firmware/iBridge1_1Customer.bundle/Contents/Resources/Firmware/usr"
  },
  {
    "size": 1008,
    "name": "/usr/standalone/firmware/iBridge1_1Customer.bundle/Contents/Resources/Firmware/dfu"
  },
  ...
]
```
### env
```
$ env | jc --env -p          # or:  jc -p env
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
$ free | jc --free -p          # or:  jc -p free
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
### /etc/fstab file
```
$ cat /etc/fstab | jc --fstab -p
[
  {
    "fs_spec": "/dev/mapper/centos-root",
    "fs_file": "/",
    "fs_vfstype": "xfs",
    "fs_mntops": "defaults",
    "fs_freq": 0,
    "fs_passno": 0
  },
  {
    "fs_spec": "UUID=05d927bb-5875-49e3-ada1-7f46cb31c932",
    "fs_file": "/boot",
    "fs_vfstype": "xfs",
    "fs_mntops": "defaults",
    "fs_freq": 0,
    "fs_passno": 0
  },
  {
    "fs_spec": "/dev/mapper/centos-swap",
    "fs_file": "swap",
    "fs_vfstype": "swap",
    "fs_mntops": "defaults",
    "fs_freq": 0,
    "fs_passno": 0
  }
]
```
### /etc/group file
```
$ cat /etc/group | jc --group -p
[
  {
    "group_name": "nobody",
    "password": "*",
    "gid": -2,
    "members": []
  },
  {
    "group_name": "nogroup",
    "password": "*",
    "gid": -1,
    "members": []
  },
  {
    "group_name": "wheel",
    "password": "*",
    "gid": 0,
    "members": [
      "root"
    ]
  },
  {
    "group_name": "certusers",
    "password": "*",
    "gid": 29,
    "members": [
      "root",
      "_jabber",
      "_postfix",
      "_cyrus",
      "_calendar",
      "_dovecot"
    ]
  },
  ...
]
```
### /etc/gshadow file
```
$ cat /etc/gshadow | jc --gshadow -p
[
  {
    "group_name": "root",
    "password": "*",
    "administrators": [],
    "members": []
  },
  {
    "group_name": "adm",
    "password": "*",
    "administrators": [],
    "members": [
      "syslog",
      "joeuser"
    ]
  },
  ...
]
```
### history
```
$ history | jc --history -p
[
  {
    "line": 118,
    "command": "sleep 100"
  },
  {
    "line": 119,
    "command": "ls /bin"
  },
  {
    "line": 120,
    "command": "echo \"hello\""
  },
  {
    "line": 121,
    "command": "docker images"
  },
  ...
]
```
### /etc/hosts file
```
$ cat /etc/hosts | jc --hosts -p
[
  {
    "ip": "127.0.0.1",
    "hostname": [
      "localhost"
    ]
  },
  {
    "ip": "127.0.1.1",
    "hostname": [
      "root-ubuntu"
    ]
  },
  {
    "ip": "::1",
    "hostname": [
      "ip6-localhost",
      "ip6-loopback"
    ]
  },
  {
    "ip": "fe00::0",
    "hostname": [
      "ip6-localnet"
    ]
  },
  {
    "ip": "ff00::0",
    "hostname": [
      "ip6-mcastprefix"
    ]
  },
  {
    "ip": "ff02::1",
    "hostname": [
      "ip6-allnodes"
    ]
  },
  {
    "ip": "ff02::2",
    "hostname": [
      "ip6-allrouters"
    ]
  }
]
```
### id
```
$ id | jc --id -p          # or:  jc -p id
{
  "uid": {
    "id": 1000,
    "name": "joeuser"
  },
  "gid": {
    "id": 1000,
    "name": "joeuser"
  },
  "groups": [
    {
      "id": 1000,
      "name": "joeuser"
    },
    {
      "id": 10,
      "name": "wheel"
    }
  ],
  "context": {
    "user": "unconfined_u",
    "role": "unconfined_r",
    "type": "unconfined_t",
    "level": "s0-s0:c0.c1023"
  }
}
```
### ifconfig
```
$ ifconfig | jc --ifconfig -p          # or:  jc -p ifconfig
[
  {
    "name": "ens33",
    "flags": 4163,
    "state": [
      "UP",
      "BROADCAST",
      "RUNNING",
      "MULTICAST"
    ],
    "mtu": 1500,
    "ipv4_addr": "192.168.71.137",
    "ipv4_mask": "255.255.255.0",
    "ipv4_bcast": "192.168.71.255",
    "ipv6_addr": "fe80::c1cb:715d:bc3e:b8a0",
    "ipv6_mask": 64,
    "ipv6_scope": "0x20",
    "mac_addr": "00:0c:29:3b:58:0e",
    "type": "Ethernet",
    "rx_packets": 8061,
    "rx_bytes": 1514413,
    "rx_errors": 0,
    "rx_dropped": 0,
    "rx_overruns": 0,
    "rx_frame": 0,
    "tx_packets": 4502,
    "tx_bytes": 866622,
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
    "state": [
      "UP",
      "LOOPBACK",
      "RUNNING"
    ],
    "mtu": 65536,
    "ipv4_addr": "127.0.0.1",
    "ipv4_mask": "255.0.0.0",
    "ipv4_bcast": null,
    "ipv6_addr": "::1",
    "ipv6_mask": 128,
    "ipv6_scope": "0x10",
    "mac_addr": null,
    "type": "Local Loopback",
    "rx_packets": 73,
    "rx_bytes": 6009,
    "rx_errors": 0,
    "rx_dropped": 0,
    "rx_overruns": 0,
    "rx_frame": 0,
    "tx_packets": 73,
    "tx_bytes": 6009,
    "tx_errors": 0,
    "tx_dropped": 0,
    "tx_overruns": 0,
    "tx_carrier": 0,
    "tx_collisions": 0,
    "metric": null
  }
]
```
### INI files
```
$ cat example.ini
[DEFAULT]
ServerAliveInterval = 45
Compression = yes
CompressionLevel = 9
ForwardX11 = yes

[bitbucket.org]
User = hg

[topsecret.server.com]
Port = 50022
ForwardX11 = no

$ cat example.ini | jc --ini -p
{
  "bitbucket.org": {
    "serveraliveinterval": "45",
    "compression": "yes",
    "compressionlevel": "9",
    "forwardx11": "yes",
    "user": "hg"
  },
  "topsecret.server.com": {
    "serveraliveinterval": "45",
    "compression": "yes",
    "compressionlevel": "9",
    "forwardx11": "no",
    "port": "50022"
  }
}
```
### iptables
```
$ sudo iptables --line-numbers -v -L -t nat | jc --iptables -p          # or:  sudo jc -p iptables --line-numbers -v -L -t nat
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
$ jobs -l | jc --jobs -p          # or:  jc -p jobs
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
### last and lastb
```
$ last | jc --last -p          # or:  jc -p last
[
  {
    "user": "joeuser",
    "tty": "ttys002",
    "hostname": null,
    "login": "Thu Feb 27 14:31",
    "logout": "still logged in"
  },
  {
    "user": "joeuser",
    "tty": "ttys003",
    "hostname": null,
    "login": "Thu Feb 27 10:38",
    "logout": "10:38",
    "duration": "00:00"
  },
  {
    "user": "joeuser",
    "tty": "ttys003",
    "hostname": null,
    "login": "Thu Feb 27 10:18",
    "logout": "10:18",
    "duration": "00:00"
  },
  ...
]
```
### ls
```
$ ls -l /usr/bin | jc --ls -p          # or:  jc -p ls -l /usr/bin
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
$ lsblk | jc --lsblk -p          # or:  jc -p lsblk
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
$ lsmod | jc --lsmod -p          # or:  jc -p lsmod
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
$ sudo lsof | jc --lsof -p          # or:  sudo jc -p lsof
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
$ mount | jc --mount -p          # or:  jc -p mount
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
$ sudo netstat -apee | jc --netstat -p          # or:  sudo jc -p netstat -apee
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
### /etc/passwd file
```
$ cat /etc/passwd | jc --passwd -p
[
  {
    "username": "nobody",
    "password": "*",
    "uid": -2,
    "gid": -2,
    "comment": "Unprivileged User",
    "home": "/var/empty",
    "shell": "/usr/bin/false"
  },
  {
    "username": "root",
    "password": "*",
    "uid": 0,
    "gid": 0,
    "comment": "System Administrator",
    "home": "/var/root",
    "shell": "/bin/sh"
  },
  {
    "username": "daemon",
    "password": "*",
    "uid": 1,
    "gid": 1,
    "comment": "System Services",
    "home": "/var/root",
    "shell": "/usr/bin/false"
  },
  ...
]
```
### pip list
```
$ pip list | jc --pip-list -p          # or:  jc -p pip list          # or:  jc -p pip3 list
[
  {
    "package": "ansible",
    "version": "2.8.5"
  },
  {
    "package": "antlr4-python3-runtime",
    "version": "4.7.2"
  },
  {
    "package": "asn1crypto",
    "version": "0.24.0"
  },
  ...
]

```
### pip show
```
$ pip show wrapt wheel | jc --pip-show -p          # or:  jc -p pip show wrapt wheel          # or:  jc -p pip3 show wrapt wheel
[
  {
    "name": "wrapt",
    "version": "1.11.2",
    "summary": "Module for decorators, wrappers and monkey patching.",
    "home_page": "https://github.com/GrahamDumpleton/wrapt",
    "author": "Graham Dumpleton",
    "author_email": "Graham.Dumpleton@gmail.com",
    "license": "BSD",
    "location": "/usr/local/lib/python3.7/site-packages",
    "requires": null,
    "required_by": "astroid"
  },
  {
    "name": "wheel",
    "version": "0.33.4",
    "summary": "A built-package format for Python.",
    "home_page": "https://github.com/pypa/wheel",
    "author": "Daniel Holth",
    "author_email": "dholth@fastmail.fm",
    "license": "MIT",
    "location": "/usr/local/lib/python3.7/site-packages",
    "requires": null,
    "required_by": null
  }
]
```
### ps
```
$ ps -ef | jc --ps -p          # or:  jc -p ps -ef
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
$ ps axu | jc --ps -p          # or:  jc -p ps axu
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
$ route -ee | jc --route -p          # or:  jc -p route -ee
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
### /etc/shadow file
```
$ sudo cat /etc/shadow | jc --shadow -p
[
  {
    "username": "root",
    "password": "*",
    "last_changed": 18113,
    "minimum": 0,
    "maximum": 99999,
    "warn": 7,
    "inactive": null,
    "expire": null
  },
  {
    "username": "daemon",
    "password": "*",
    "last_changed": 18113,
    "minimum": 0,
    "maximum": 99999,
    "warn": 7,
    "inactive": null,
    "expire": null
  },
  {
    "username": "bin",
    "password": "*",
    "last_changed": 18113,
    "minimum": 0,
    "maximum": 99999,
    "warn": 7,
    "inactive": null,
    "expire": null
  },
  ...
]
```
### ss
```
$ sudo ss -a | jc --ss -p          # or:  sudo jc -p ss -a
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
### stat
```
$ stat /bin/* | jc --stat -p          # or:  jc -p stat /bin/*
[
  {
    "file": "/bin/bash",
    "size": 1113504,
    "blocks": 2176,
    "io_blocks": 4096,
    "type": "regular file",
    "device": "802h/2050d",
    "inode": 131099,
    "links": 1,
    "access": "0755",
    "flags": "-rwxr-xr-x",
    "uid": 0,
    "user": "root",
    "gid": 0,
    "group": "root",
    "access_time": "2019-11-14 08:18:03.509681766 +0000",
    "modify_time": "2019-06-06 22:28:15.000000000 +0000",
    "change_time": "2019-08-12 17:21:29.521945390 +0000",
    "birth_time": null
  },
  {
    "file": "/bin/btrfs",
    "size": 716464,
    "blocks": 1400,
    "io_blocks": 4096,
    "type": "regular file",
    "device": "802h/2050d",
    "inode": 131100,
    "links": 1,
    "access": "0755",
    "flags": "-rwxr-xr-x",
    "uid": 0,
    "user": "root",
    "gid": 0,
    "group": "root",
    "access_time": "2019-11-14 08:18:28.990834276 +0000",
    "modify_time": "2018-03-12 23:04:27.000000000 +0000",
    "change_time": "2019-08-12 17:21:29.545944399 +0000",
    "birth_time": null
  },
  ...
]
```
### systemctl
```
$ systemctl -a | jc --systemctl -p          # or:  jc -p systemctl -a
[
  {
    "unit": "proc-sys-fs-binfmt_misc.automount",
    "load": "loaded",
    "active": "active",
    "sub": "waiting",
    "description": "Arbitrary Executable File Formats File System Automount Point"
  },
  {
    "unit": "dev-block-8:2.device",
    "load": "loaded",
    "active": "active",
    "sub": "plugged",
    "description": "LVM PV 3klkIj-w1qk-DkJi-0XBJ-y3o7-i2Ac-vHqWBM on /dev/sda2 2"
  },
  {
    "unit": "dev-cdrom.device",
    "load": "loaded",
    "active": "active",
    "sub": "plugged",
    "description": "VMware_Virtual_IDE_CDROM_Drive"
  },
  ...
]
```
### systemctl list-jobs
```
$ systemctl list-jobs | jc --systemctl-lj -p          # or:  jc -p systemctl list-jobs
[
  {
    "job": 3543,
    "unit": "nginxAfterGlusterfs.service",
    "type": "start",
    "state": "waiting"
  },
  {
    "job": 3545,
    "unit": "glusterReadyForLocalhostMount.service",
    "type": "start",
    "state": "running"
  },
  {
    "job": 3506,
    "unit": "nginx.service",
    "type": "start",
    "state": "waiting"
  }
]
```
### systemctl list-sockets
```
$ systemctl list-sockets | jc --systemctl-ls -p          # or:  jc -p systemctl list-sockets
[
  {
    "listen": "/dev/log",
    "unit": "systemd-journald.socket",
    "activates": "systemd-journald.service"
  },
  {
    "listen": "/run/dbus/system_bus_socket",
    "unit": "dbus.socket",
    "activates": "dbus.service"
  },
  {
    "listen": "/run/dmeventd-client",
    "unit": "dm-event.socket",
    "activates": "dm-event.service"
  },
  ...
]
```
### systemctl list-unit-files
```
$ systemctl list-unit-files | jc --systemctl-luf -p          # or:  jc -p systemctl list-unit-files
[
  {
    "unit_file": "proc-sys-fs-binfmt_misc.automount",
    "state": "static"
  },
  {
    "unit_file": "dev-hugepages.mount",
    "state": "static"
  },
  {
    "unit_file": "dev-mqueue.mount",
    "state": "static"
  },
  ...
]
```
### uname -a
```
$ uname -a | jc --uname -p          # or:  jc -p uname -a
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
$ uptime | jc --uptime -p          # or:  jc -p uptime
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
$ w | jc --w -p          # or:  jc -p w
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
### who
```
$ who | jc --who -p          # or:  jc -p who
[
  {
    "user": "joeuser",
    "tty": "ttyS0",
    "time": "2020-03-02 02:52"
  },
  {
    "user": "joeuser",
    "tty": "pts/0",
    "time": "2020-03-02 05:15",
    "from": "192.168.71.1"
  }
]
```
```
$ who -a | jc --who -p          # or:  jc -p who -a
[
  {
    "event": "reboot",
    "time": "Feb 7 23:31",
    "pid": 1
  },
  {
    "user": "joeuser",
    "writeable_tty": "-",
    "tty": "console",
    "time": "Feb 7 23:32",
    "idle": "old",
    "pid": 105
  },
  {
    "user": "joeuser",
    "writeable_tty": "+",
    "tty": "ttys000",
    "time": "Feb 13 16:44",
    "idle": ".",
    "pid": 51217,
    "comment": "term=0 exit=0"
  },
  {
    "user": "joeuser",
    "writeable_tty": "?",
    "tty": "ttys003",
    "time": "Feb 28 08:59",
    "idle": "01:36",
    "pid": 41402
  },
  {
    "user": "joeuser",
    "writeable_tty": "+",
    "tty": "ttys004",
    "time": "Mar 1 16:35",
    "idle": ".",
    "pid": 15679,
    "from": "192.168.1.5"
  }
]
```
### XML files
```
$ cat cd_catalog.xml 
<?xml version="1.0" encoding="UTF-8"?>
<CATALOG>
  <CD>
    <TITLE>Empire Burlesque</TITLE>
    <ARTIST>Bob Dylan</ARTIST>
    <COUNTRY>USA</COUNTRY>
    <COMPANY>Columbia</COMPANY>
    <PRICE>10.90</PRICE>
    <YEAR>1985</YEAR>
  </CD>
  <CD>
    <TITLE>Hide your heart</TITLE>
    <ARTIST>Bonnie Tyler</ARTIST>
    <COUNTRY>UK</COUNTRY>
    <COMPANY>CBS Records</COMPANY>
    <PRICE>9.90</PRICE>
    <YEAR>1988</YEAR>
  </CD>
  ...

$ cat cd_catalog.xml | jc --xml -p
{
  "CATALOG": {
    "CD": [
      {
        "TITLE": "Empire Burlesque",
        "ARTIST": "Bob Dylan",
        "COUNTRY": "USA",
        "COMPANY": "Columbia",
        "PRICE": "10.90",
        "YEAR": "1985"
      },
      {
        "TITLE": "Hide your heart",
        "ARTIST": "Bonnie Tyler",
        "COUNTRY": "UK",
        "COMPANY": "CBS Records",
        "PRICE": "9.90",
        "YEAR": "1988"
      },
  ...
}
```
### YAML files
```
$ cat istio.yaml 
apiVersion: "authentication.istio.io/v1alpha1"
kind: "Policy"
metadata:
  name: "default"
  namespace: "default"
spec:
  peers:
  - mtls: {}
---
apiVersion: "networking.istio.io/v1alpha3"
kind: "DestinationRule"
metadata:
  name: "default"
  namespace: "default"
spec:
  host: "*.default.svc.cluster.local"
  trafficPolicy:
    tls:
      mode: ISTIO_MUTUAL

$ cat istio.yaml | jc --yaml -p
[
  {
    "apiVersion": "authentication.istio.io/v1alpha1",
    "kind": "Policy",
    "metadata": {
      "name": "default",
      "namespace": "default"
    },
    "spec": {
      "peers": [
        {
          "mtls": {}
        }
      ]
    }
  },
  {
    "apiVersion": "networking.istio.io/v1alpha3",
    "kind": "DestinationRule",
    "metadata": {
      "name": "default",
      "namespace": "default"
    },
    "spec": {
      "host": "*.default.svc.cluster.local",
      "trafficPolicy": {
        "tls": {
          "mode": "ISTIO_MUTUAL"
        }
      }
    }
  }
]
```