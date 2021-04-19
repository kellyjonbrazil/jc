![Tests](https://github.com/kellyjonbrazil/jc/workflows/Tests/badge.svg?branch=master)
![Pypi](https://img.shields.io/pypi/v/jc.svg)

> Try the new `jc` [web demo](https://jc-web-demo.herokuapp.com/)!

> JC is [now available](https://galaxy.ansible.com/community/general) as an Ansible filter plugin in the `community.general` collection! See this [blog post](https://blog.kellybrazil.com/2020/08/30/parsing-command-output-in-ansible-with-jc/) for an example.

# JC
JSON CLI output utility

`jc` JSONifies the output of many CLI tools and file-types for easier parsing in scripts. See the [**Parsers**](#parsers) section for supported commands and file-types.
```bash
dig example.com | jc --dig
```
```json
[{"id":38052,"opcode":"QUERY","status":"NOERROR","flags":["qr","rd","ra"],"query_num":1,"answer_num":1,
"authority_num":0,"additional_num":1,"opt_pseudosection":{"edns":{"version":0,"flags":[],"udp":4096}},"question":
{"name":"example.com.","class":"IN","type":"A"},"answer":[{"name":"example.com.","class":"IN","type":"A","ttl":
39049,"data":"93.184.216.34"}],"query_time":49,"server":"2600:1700:bab0:d40::1#53(2600:1700:bab0:d40::1)","when":
"Fri Apr 16 16:09:00 PDT 2021","rcvd":56,"when_epoch":1618614540,"when_epoch_utc":null}]
```
This allows further command-line processing of output with tools like `jq` by piping commands:
```bash
$ dig example.com | jc --dig | jq -r '.[].answer[].data'
93.184.216.34
```
or using the alternative "magic" syntax:
```bash
$ jc dig example.com | jq -r '.[].answer[].data'
93.184.216.34
```
The `jc` parsers can also be used as python modules. In this case the output will be a python dictionary, or list of dictionaries, instead of JSON:
```python
>>> import jc.parsers.dig
>>> 
>>> data = '''; <<>> DiG 9.10.6 <<>> example.com
... ;; global options: +cmd
... ;; Got answer:
... ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 64612
... ;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1
... 
... ;; OPT PSEUDOSECTION:
... ; EDNS: version: 0, flags:; udp: 4096
... ;; QUESTION SECTION:
... ;example.com.           IN  A
... 
... ;; ANSWER SECTION:
... example.com.        29658   IN  A   93.184.216.34
... 
... ;; Query time: 52 msec
... ;; SERVER: 2600:1700:bab0:d40::1#53(2600:1700:bab0:d40::1)
... ;; WHEN: Fri Apr 16 16:13:00 PDT 2021
... ;; MSG SIZE  rcvd: 56'''
>>>
>>> jc.parsers.dig.parse(data)
[{'id': 64612, 'opcode': 'QUERY', 'status': 'NOERROR', 'flags': ['qr', 'rd', 'ra'], 'query_num': 1, 'answer_num':
1, 'authority_num': 0, 'additional_num': 1, 'opt_pseudosection': {'edns': {'version': 0, 'flags': [], 'udp':
4096}}, 'question': {'name': 'example.com.', 'class': 'IN', 'type': 'A'}, 'answer': [{'name': 'example.com.',
'class': 'IN', 'type': 'A', 'ttl': 29658, 'data': '93.184.216.34'}], 'query_time': 52, 'server':
'2600:1700:bab0:d40::1#53(2600:1700:bab0:d40::1)', 'when': 'Fri Apr 16 16:13:00 PDT 2021', 'rcvd': 56,
'when_epoch': 1618614780, 'when_epoch_utc': None}]
```
Two representations of the data are possible. The default representation uses a strict schema per parser and converts known numbers to int/float JSON values. Certain known values of `None` are converted to JSON `null`, known boolean values are converted, and, in some cases, additional semantic context fields are added.

> Note: Some parsers have calculated epoch timestamp fields added to the output. Unless a timestamp field name has a `_utc` suffix it is considered naive. (i.e. based on the local timezone of the system the `jc` parser was run on). 
>
> If a UTC timezone can be detected in the text of the command output, the timestamp will be timezone aware and have a `_utc` suffix on the key name. (e.g. `epoch_utc`) No other timezones are supported for aware timestamps.

To access the raw, pre-processed JSON, use the `-r` cli option or the `raw=True` function parameter in `parse()`.

Schemas for each parser can be found at the documentation link beside each parser below.

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
| NixOS linux           | `nix-env -iA nixpkgs.jc` or `nix-env -iA nixos.jc`                            |
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
Alternatively, the "magic" syntax can be used by prepending `jc` to the command to be converted. Options can be passed to `jc` immediately before the command is given. (Note: command aliases and shell builtins are not supported)
```bash
jc [OPTIONS] COMMAND
```
The JSON output can be compact (default) or pretty formatted with the `-p` option.

> Note: For best results set the `LANG` locale environment variable to `C`. For example, either by setting directly on the command-line: `$ LANG=C date | jc --date`, or by exporting to the environment before running commands: `$ export LANG=C`.

### Parsers

- `--acpi` enables the `acpi` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/acpi))
- `--airport` enables the `airport -I` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/airport))
- `--airport-s` enables the `airport -s` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/airport_s))
- `--arp` enables the `arp` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/arp))
- `--blkid` enables the `blkid` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/blkid))
- `--cksum` enables the `cksum` and `sum` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/cksum))
- `--crontab` enables the `crontab` command and file parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/crontab))
- `--crontab-u` enables the `crontab` file parser with user support ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/crontab_u))
- `--csv` enables the CSV file parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/csv))
- `--date` enables the `date` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/date))
- `--df` enables the `df` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/df))
- `--dig` enables the `dig` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/dig))
- `--dir` enables the `dir` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/dir))
- `--dmidecode` enables the `dmidecode` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/dmidecode))
- `--dpkg-l` enables the `dpkg -l` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/dpkg_l))
- `--du` enables the `du` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/du))
- `--env` enables the `env` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/env))
- `--file` enables the `file` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/file))
- `--finger` enables the `finger` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/finger))
- `--free` enables the `free` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/free))
- `--fstab` enables the `/etc/fstab` file parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/fstab))
- `--group` enables the `/etc/group` file parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/group))
- `--gshadow` enables the `/etc/gshadow` file parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/gshadow))
- `--hash` enables the `hash` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/hash))
- `--hashsum` enables the hashsum command parser (`md5sum`, `shasum`, etc.) ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/hashsum))
- `--hciconfig` enables the `hciconfig` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/hciconfig))
- `--history` enables the `history` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/history))
- `--hosts` enables the `/etc/hosts` file parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/hosts))
- `--id` enables the `id` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/id))
- `--ifconfig` enables the `ifconfig` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/ifconfig))
- `--ini` enables the INI file parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/ini))
- `--iptables` enables the `iptables` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/iptables))
- `--iw-scan` enables the `iw dev [device] scan` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/iw_scan))
- `--jobs` enables the `jobs` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/jobs))
- `--kv` enables the Key/Value file parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/kv))
- `--last` enables the `last` and `lastb` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/last))
- `--ls` enables the `ls` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/ls))
- `--lsblk` enables the `lsblk` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/lsblk))
- `--lsmod` enables the `lsmod` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/lsmod))
- `--lsof` enables the `lsof` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/lsof))
- `--mount` enables the `mount` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/mount))
- `--netstat` enables the `netstat` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/netstat))
- `--ntpq` enables the `ntpq -p` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/ntpq))
- `--passwd` enables the `/etc/passwd` file parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/passwd))
- `--ping` enables the `ping` and `ping6` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/ping))
- `--pip-list` enables the `pip list` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/pip_list))
- `--pip-show` enables the `pip show` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/pip_show))
- `--ps` enables the `ps` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/ps))
- `--route` enables the `route` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/route))
- `--rpm-qi` enables the `rpm -qi` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/rpm_qi))
- `--shadow` enables the `/etc/shadow` file parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/shadow))
- `--ss` enables the `ss` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/ss))
- `--stat` enables the `stat` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/stat))
- `--sysctl` enables the `sysctl` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/sysctl))
- `--systemctl` enables the `systemctl` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/systemctl))
- `--systemctl-lj` enables the `systemctl list-jobs` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/systemctl_lj))
- `--systemctl-ls` enables the `systemctl list-sockets` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/systemctl_ls))
- `--systemctl-luf` enables the `systemctl list-unit-files` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/systemctl_luf))
- `--systeminfo` enables the `systeminfo` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/systeminfo))
- `--time` enables the `/usr/bin/time` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/time))
- `--timedatectl` enables the `timedatectl status` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/timedatectl))
- `--tracepath` enables the `tracepath` and `tracepath6` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/tracepath))
- `--traceroute` enables the `traceroute` and `traceroute6` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/traceroute))
- `--uname` enables the `uname -a` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/uname))
- `--upower` enables the `upower` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/upower))
- `--uptime` enables the `uptime` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/uptime))
- `--w` enables the `w` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/w))
- `--wc` enables the `wc` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/wc))
- `--who` enables the `who` command parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/who))
- `--xml` enables the XML file parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/xml))
- `--yaml` enables the YAML file parser ([documentation](https://kellyjonbrazil.github.io/jc/docs/parsers/yaml))

### Options
- `-a` about `jc`. Prints information about `jc` and the parsers (in JSON, of course!)
- `-d` debug mode. Prints trace messages if parsing issues are encountered (use `-dd` for verbose debugging)
- `-h` `jc` help. Use `jc -h --parser_name` for parser documentation
- `-m` monochrome JSON output
- `-p` pretty format the JSON output
- `-q` quiet mode. Suppresses parser warning messages
- `-r` raw output. Provides a more literal JSON output, typically with string values and no additional semantic processing
- `-v` version information

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

You may still use a parser on an unsupported platform - for example, you may want to parse a file with linux `lsof` output on an macOS laptop. In that case you can suppress the warning message with the `-q` cli option or the `quiet=True` function parameter in `parse()`:

```bash
cat lsof.out | jc --lsof -q
```

Tested on:
- Centos 7.7
- Ubuntu 18.04
- Ubuntu 20.04
- Fedora32
- macOS 10.11.6
- macOS 10.14.6
- NixOS
- FreeBSD12
- Windows 10

## Contributions
Feel free to add/improve code or parsers! You can use the [`jc/parsers/foo.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/foo.py) parser as a template and submit your parser with a pull request.

Please see the [Contributing Guidelines](https://github.com/kellyjonbrazil/jc/blob/master/CONTRIBUTING.md) for more information.

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
Here are some examples of `jc` output. For more examples, see [here](https://kellyjonbrazil.github.io/jc/EXAMPLES) or the parser documentation.
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
  "time": "11:35",
  "uptime": "3 days, 4:03",
  "users": 5,
  "load_1m": 1.88,
  "load_5m": 2.0,
  "load_15m": 1.94,
  "time_hour": 11,
  "time_minute": 35,
  "time_second": null,
  "uptime_days": 3,
  "uptime_hours": 4,
  "uptime_minutes": 3,
  "uptime_total_seconds": 273780
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

© 2019-2021 Kelly Brazil