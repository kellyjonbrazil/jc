![Tests](https://github.com/kellyjonbrazil/jc/workflows/Tests/badge.svg?branch=master)
![Pypi](https://img.shields.io/pypi/v/jc.svg)

> Try the new `jc` [web demo](https://jc-web-demo.herokuapp.com/)!

> JC is [now available](https://galaxy.ansible.com/community/general) as an Ansible filter plugin in the `community.general` collection! See this [blog post](https://blog.kellybrazil.com/2020/08/30/parsing-command-output-in-ansible-with-jc/) for an example.

# JC
JSON CLI output utility

`jc` JSONifies the output of many CLI tools and file-types for easier parsing in scripts. See the [**Parsers**](#parsers) section for supported commands and file-types.

This allows further command-line processing of output with tools like `jq` by piping commands:
```bash
ls -l /usr/bin | jc --ls | jq '.[] | select(.size > 50000000)'
```
```json
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
```bash
jc ls -l /usr/bin | jq '.[] | select(.size > 50000000)'
```
```json
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
```python
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

## Why Would Anyone Do This!?
For more information on the motivations for this project, please see my [blog post](https://blog.kellybrazil.com/2019/11/26/bringing-the-unix-philosophy-to-the-21st-century/).

See also:
- [libxo on FreeBSD](http://juniper.github.io/libxo/libxo-manual.html)
- [powershell](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/convertto-json?view=powershell-7)
- [blog: linux apps should have a json flag](https://thomashunter.name/posts/2012-06-06-linux-cli-apps-should-have-a-json-flag)

## Installation
There are several ways to get `jc`. You can install via `pip`; other OS package repositories like `apt-get`, `dnf`, `zypper`, `pacman`, `nix-env`, `guix`, `brew`, or `portsnap`; via DEB/RPM packages; or by downloading the correct binary for your architecture and running it anywhere on your filesystem.

### Pip (macOS, linux, unix, Windows)
```bash
pip3 install jc
```

### OS Package Repositories

| OS                    | Command                                                                       | 
|-----------------------|-------------------------------------------------------------------------------|
| Debian/Ubuntu linux   | `apt-get install jc`                                                          |
| Fedora linux          | `dnf install jc`                                                              |
| openSUSE linux        | `zypper install jc`                                                           |
| Arch linux            | `pacman -S jc`                                                                |
| NixOS linux           | `nix-env -iA nixpkgs.jc`                                                      |
| Guix System linux     | `guix install jc`                                                             |
| MacOS                 | `brew install jc`                                                             |
| FreeBSD               | `portsnap fetch update && cd /usr/ports/textproc/py-jc && make install clean` |
| Ansible filter plugin | `ansible-galaxy collection install community.general`                         |

> For more packages and binaries, see https://kellyjonbrazil.github.io/jc-packaging/.

## Usage
`jc` accepts piped input from `STDIN` and outputs a JSON representation of the previous command's output to `STDOUT`.
```bash
COMMAND | jc PARSER [OPTIONS]
```
Alternatively, the "magic" syntax can be used by prepending `jc` to the command to be converted. Options can be passed to `jc` immediately before the command is given. (Note: command aliases are not supported)
```bash
jc [OPTIONS] COMMAND
```
The JSON output can be compact (default) or pretty formatted with the `-p` option.

### Parsers
- `--airport` enables the `airport -I` command parser (OSX)
- `--airport-s` enables the `airport -s` command parser (OSX)
- `--arp` enables the `arp` command parser
- `--blkid` enables the `blkid` command parser
- `--cksum` enables the `cksum` and `sum` command parser
- `--crontab` enables the `crontab` command and file parser
- `--crontab-u` enables the `crontab` file parser with user support
- `--csv` enables the `CSV` file parser
- `--date` enables the `date` command parser
- `--df` enables the `df` command parser
- `--dig` enables the `dig` command parser
- `--dmidecode` enables the `dmidecode` command parser
- `--du` enables the `du` command parser
- `--env` enables the `env` and `printenv` command parser
- `--file` enables the `file` command parser
- `--free` enables the `free` command parser
- `--fstab` enables the `/etc/fstab` file parser
- `--group` enables the `/etc/group` file parser
- `--gshadow` enables the `/etc/gshadow` file parser
- `--hash` enables the `hash` command parser
- `--hashsum` enables the `hashsum` command parser (`md5`, `md5sum`, `shasum`, `sha1sum`, `sha224sum`, `sha256sum`, `sha384sum`, `sha512sum`)
- `--history` enables the `history` command parser
- `--hosts` enables the `/etc/hosts` file parser
- `--id` enables the `id` command parser
- `--ifconfig` enables the `ifconfig` command parser
- `--ini` enables the `INI` file parser
- `--iptables` enables the `iptables` command parser
- `--iw-scan` enables the `iw dev <device> scan` command parser (beta)
- `--jobs` enables the `jobs` command parser
- `--kv` enables the `Key/Value` file parser
- `--last` enables the `last` and `lastb` command parser
- `--ls` enables the `ls` and `vdir` command parser
- `--lsblk` enables the `lsblk` command parser
- `--lsmod` enables the `lsmod` command parser
- `--lsof` enables the `lsof` command parser
- `--mount` enables the `mount` command parser
- `--netstat` enables the `netstat` command parser
- `--ntpq` enables the `ntpq -p` command parser
- `--passwd` enables the `/etc/passwd` file parser
- `--ping` enables the `ping` and `ping6` command parser
- `--pip-list` enables the `pip list` command parser
- `--pip-show` enables the `pip show` command parser
- `--ps` enables the `ps` command parser
- `--route` enables the `route` command parser
- `--shadow` enables the `/etc/shadow` file parser
- `--ss` enables the `ss` command parser
- `--stat` enables the `stat` command parser
- `--sysctl` enables the `sysctl -a` command parser
- `--systemctl` enables the `systemctl` command parser
- `--systemctl-lj` enables the `systemctl list-jobs` command parser
- `--systemctl-ls` enables the `systemctl list-sockets` command parser
- `--systemctl-luf` enables the `systemctl list-unit-files` command parser
- `--timedatectl` enables the `timedatectl status` command parser
- `--tracepath` enables the `tracepath` and `tracepath6` command parser
- `--traceroute` enables the `traceroute` and `traceroute6` command parser
- `--uname` enables the `uname -a` command parser
- `--uptime` enables the `uptime` command parser
- `--w` enables the `w` command parser
- `--wc` enables the `wc` command parser
- `--who` enables the `who` command parser
- `--xml` enables the `XML` file parser
- `--yaml` enables the `YAML` file parser

### Options
- `-a` about `jc`. Prints information about `jc` and the parsers (in JSON, of course!)
- `-d` debug mode. Prints trace messages if parsing issues encountered (use `-dd` for verbose debugging)
- `-m` monochrome JSON output
- `-p` pretty format the JSON output
- `-q` quiet mode. Suppresses warning messages
- `-r` raw output. Provides a more literal JSON output with all values as strings and no additional semantic processing

### Setting Custom Colors via Environment Variable
You can specify custom colors via the `JC_COLORS` environment variable. The `JC_COLORS` environment variable takes four comma separated string values in the following format:
```bash
JC_COLORS=<keyname_color>,<keyword_color>,<number_color>,<string_color>
```
Where colors are: `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `gray`, `brightblack`, `brightred`, `brightgreen`, `brightyellow`, `brightblue`, `brightmagenta`, `brightcyan`, `white`, or  `default`

For example, to set to the default colors:
```bash
JC_COLORS=blue,brightblack,magenta,green
```
or
```bash
JC_COLORS=default,default,default,default
```

### Custom Parsers
Custom local parser plugins may be placed in a `jc/jcparsers` folder in your local **"App data directory"**:

- Linux/unix: `$HOME/.local/share/jc/jcparsers`
- macOS: `$HOME/Library/Application Support/jc/jcparsers`
- Windows: `$LOCALAPPDATA\jc\jc\jcparsers`

Local parser plugins are standard python module files. Use the [`jc/parsers/foo.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/foo.py) parser as a template and simply place a `.py` file in the `jcparsers` subfolder.

Local plugin filenames must be valid python module names, therefore must consist entirely of alphanumerics and start with a letter. Local plugins may override default plugins.

> Note: The application data directory follows the [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html)

## Compatibility
Some parsers like `ls`, `ps`, `dig`, etc. will work on any platform. Other parsers that are platform-specific will generate a warning message if they are used on an unsupported platform. To see all parser information, including compatibility, run `jc -ap`.

You may still use a parser on an unsupported platform - for example, you may want to parse a file with linux `lsof` output on an OSX laptop. In that case you can suppress the warning message with the `-q` cli option or the `quiet=True` function parameter in `parse()`:

```bash
cat lsof.out | jc --lsof -q
```

Tested on:
- Centos 7.7
- Ubuntu 18.04
- Ubuntu 20.04
- Fedora32
- OSX 10.11.6
- OSX 10.14.6
- NixOS
- FreeBSD12

## Contributions
Feel free to add/improve code or parsers! You can use the [`jc/parsers/foo.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/foo.py) parser as a template and submit your parser with a pull request.

## Acknowledgments
- Local parser plugin feature contributed by [Dean Serenevy](https://github.com/duelafn)
- CI automation and code optimizations by [philippeitis](https://github.com/philippeitis)
- [`ifconfig-parser`](https://github.com/KnightWhoSayNi/ifconfig-parser) module by KnightWhoSayNi
- [`xmltodict`](https://github.com/martinblech/xmltodict) module by Martín Blech
- [`ruamel.yaml`](https://pypi.org/project/ruamel.yaml) module by Anthon van der Neut
- [`trparse`](https://github.com/lbenitez000/trparse) module by Luis Benitez
- Parsing [code](https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501) from Conor Heine adapted for some parsers
- Excellent constructive feedback from [Ilya Sher](https://github.com/ilyash-b)

## Examples
Here are some examples of `jc` output. For more examples, see [EXAMPLES.md](https://github.com/kellyjonbrazil/jc/blob/master/EXAMPLES.md) or the [parser documentation](https://github.com/kellyjonbrazil/jc/tree/master/docs/parsers).
### arp
```bash
arp | jc --arp -p          # or:  jc -p arp
```
```json
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
### CSV files
```bash
cat homes.csv
```
```
"Sell", "List", "Living", "Rooms", "Beds", "Baths", "Age", "Acres", "Taxes"
142, 160, 28, 10, 5, 3,  60, 0.28,  3167
175, 180, 18,  8, 4, 1,  12, 0.43,  4033
129, 132, 13,  6, 3, 1,  41, 0.33,  1471
...
```
```bash
cat homes.csv | jc --csv -p
```
```json
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
  }
]
```
### dig
```bash
dig cnn.com @205.251.194.64 | jc --dig -p          # or:  jc -p dig cnn.com @205.251.194.64
```
```json
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
    "answer_num": 1,
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
      }
    ],
    "query_time": 28,
    "server": "2600",
    "when": "Tue Nov 12 07:13:03 PST 2019",
    "rcvd": 100
  }
]
```
### /etc/hosts file
```bash
cat /etc/hosts | jc --hosts -p
```
```json
[
  {
    "ip": "127.0.0.1",
    "hostname": [
      "localhost"
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
  }
]
```
### ifconfig
```bash
ifconfig | jc --ifconfig -p          # or:  jc -p ifconfig
```
```json
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
  }
]
```
### INI files
```bash
cat example.ini
```
```
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
```
```bash
cat example.ini | jc --ini -p
```
```json
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
### ls
```bash
$ ls -l /usr/bin | jc --ls -p          # or:  jc -p ls -l /usr/bin
```
```json
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
  }
]
```
### netstat
```bash
netstat -apee | jc --netstat -p          # or:  jc -p netstat -apee
```
```json
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
  }
]
```
### /etc/passwd file
```bash
cat /etc/passwd | jc --passwd -p
```
```json
[
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
  }
]
```
### ping
```bash
ping 8.8.8.8 -c 3 | jc --ping -p          # or:  jc -p ping 8.8.8.8 -c 3
```
```json
{
  "destination_ip": "8.8.8.8",
  "data_bytes": 56,
  "pattern": null,
  "destination": "8.8.8.8",
  "packets_transmitted": 3,
  "packets_received": 3,
  "packet_loss_percent": 0.0,
  "duplicates": 0,
  "time_ms": 2005.0,
  "round_trip_ms_min": 23.835,
  "round_trip_ms_avg": 30.46,
  "round_trip_ms_max": 34.838,
  "round_trip_ms_stddev": 4.766,
  "responses": [
    {
      "type": "reply",
      "timestamp": null,
      "bytes": 64,
      "response_ip": "8.8.8.8",
      "icmp_seq": 1,
      "ttl": 118,
      "time_ms": 23.8,
      "duplicate": false
    },
    {
      "type": "reply",
      "timestamp": null,
      "bytes": 64,
      "response_ip": "8.8.8.8",
      "icmp_seq": 2,
      "ttl": 118,
      "time_ms": 34.8,
      "duplicate": false
    },
    {
      "type": "reply",
      "timestamp": null,
      "bytes": 64,
      "response_ip": "8.8.8.8",
      "icmp_seq": 3,
      "ttl": 118,
      "time_ms": 32.7,
      "duplicate": false
    }
  ]
}
```
### ps
```bash
ps axu | jc --ps -p          # or:  jc -p ps axu
```
```json
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
  }
]
```
### traceroute
```bash
traceroute -m 2 8.8.8.8 | jc --traceroute -p          # or:  jc -p traceroute -m 2 8.8.8.8
```
```json
{
  "destination_ip": "8.8.8.8",
  "destination_name": "8.8.8.8",
  "hops": [
    {
      "hop": 1,
      "probes": [
        {
          "annotation": null,
          "asn": null,
          "ip": "192.168.1.254",
          "name": "dsldevice.local.net",
          "rtt": 6.616
        },
        {
          "annotation": null,
          "asn": null,
          "ip": "192.168.1.254",
          "name": "dsldevice.local.net",
          "rtt": 6.413
        },
        {
          "annotation": null,
          "asn": null,
          "ip": "192.168.1.254",
          "name": "dsldevice.local.net",
          "rtt": 6.308
        }
      ]
    },
    {
      "hop": 2,
      "probes": [
        {
          "annotation": null,
          "asn": null,
          "ip": "76.220.24.1",
          "name": "76-220-24-1.lightspeed.sntcca.sbcglobal.net",
          "rtt": 29.367
        },
        {
          "annotation": null,
          "asn": null,
          "ip": "76.220.24.1",
          "name": "76-220-24-1.lightspeed.sntcca.sbcglobal.net",
          "rtt": 40.197
        },
        {
          "annotation": null,
          "asn": null,
          "ip": "76.220.24.1",
          "name": "76-220-24-1.lightspeed.sntcca.sbcglobal.net",
          "rtt": 29.162
        }
      ]
    }
  ]
}
```
### uptime
```bash
uptime | jc --uptime -p          # or:  jc -p uptime
```
```json
{
  "time": "11:30:44",
  "uptime": "1 day, 21:17",
  "users": 1,
  "load_1m": 0.01,
  "load_5m": 0.04,
  "load_15m": 0.05
}
```
### XML files
```bash
cat cd_catalog.xml
```
```xml
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
```
```bash
cat cd_catalog.xml | jc --xml -p
```
```json
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
      }
    ]
  }
}
```
### YAML files
```bash
cat istio.yaml 
```
```yaml
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
```
```bash
cat istio.yaml | jc --yaml -p
```
```json
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