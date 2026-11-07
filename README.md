[![Pypi](https://img.shields.io/pypi/v/jc.svg)](https://pypi.org/project/jc/)

# JC
JSON Convert

`jc` JSONifies the output of many CLI tools, file-types, and common strings
for easier parsing in scripts. See the [**Parsers**](#parsers) section for
supported commands, file-types, and strings.
```bash
dig example.com | jc --dig
```
```json
[{"id":38052,"opcode":"QUERY","status":"NOERROR","flags":["qr","rd","ra"],
"query_num":1,"answer_num":1,"authority_num":0,"additional_num":1,
"opt_pseudosection":{"edns":{"version":0,"flags":[],"udp":4096}},"question":
{"name":"example.com.","class":"IN","type":"A"},"answer":[{"name":
"example.com.","class":"IN","type":"A","ttl":39049,"data":"93.184.216.34"}],
"query_time":49,"server":"2600:1700:bab0:d40::1#53(2600:1700:bab0:d40::1)",
"when":"Fri Apr 16 16:09:00 PDT 2021","rcvd":56,"when_epoch":1618614540,
"when_epoch_utc":null}]
```

Pipe the output to tools like `jq` or [`jello`](https://github.com/kellyjonbrazil/jello),
or use the "magic" syntax by putting `jc` in front of the command:
```bash
$ dig example.com | jc --dig | jq -r '.[].answer[].data'
93.184.216.34
$ jc dig example.com | jq -r '.[].answer[].data'
93.184.216.34
```

`jc` can also be used as a Python library. It returns a dictionary, a list of
dictionaries, or a
[lazy iterable of dictionaries](#using-streaming-parsers-as-python-modules)
instead of JSON:
```python
>>> import subprocess
>>> import jc
>>>
>>> cmd_output = subprocess.check_output(['dig', 'example.com'], text=True)
>>> data = jc.parse('dig', cmd_output)
>>>
>>> data[0]['answer']
[{'name': 'example.com.', 'class': 'IN', 'type': 'A', 'ttl': 29658, 'data':
'93.184.216.34'}]
```
For library documentation, use `help('jc')` or see the
[online documentation](https://github.com/kellyjonbrazil/jc/tree/master/docs).

By default, output follows a documented schema for each parser: known numbers,
booleans, and `null` values are converted, and some parsers add fields such as
epoch timestamps. Use the `-r` option (or `raw=True` in `parse()`) for raw
output that stays closer to the original text. Each parser's schema is linked
from the [**Parsers**](#parsers) table.

Release notes are in the [Releases section](https://github.com/kellyjonbrazil/jc/releases) on Github.

Try `jc` in the [web demo](https://jc-web.onrender.com/), or run it as a
service with the [REST API](https://github.com/kellyjonbrazil/jc-restapi).

## Further Reading
- [Bringing the Unix Philosophy to the 21st Century](https://blog.kellybrazil.com/2019/11/26/bringing-the-unix-philosophy-to-the-21st-century/)
  (why `jc` exists) and an [interview with Console](https://console.substack.com/p/console-89)
- Use cases:
  [Bash scripting](https://blog.kellybrazil.com/2021/04/12/practical-json-at-the-command-line/),
  [Ansible](https://blog.kellybrazil.com/2020/08/30/parsing-command-output-in-ansible-with-jc/),
  [Saltstack](https://blog.kellybrazil.com/2020/09/15/parsing-command-output-in-saltstack-with-jc/),
  [Nornir](https://blog.kellybrazil.com/2020/12/09/parsing-command-output-in-nornir-with-jc/),
  [FortiSOAR](https://docs.fortinet.com/document/fortisoar/1.0.0/jc-parse-command-output/323/jc-parse-command-output-v1-0-0)
- Related:
  [libxo on FreeBSD](http://juniper.github.io/libxo/libxo-manual.html),
  [PowerShell `ConvertTo-Json`](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/convertto-json?view=powershell-7),
  [Linux CLI apps should have a JSON flag](https://thomashunter.name/posts/2012-06-06-linux-cli-apps-should-have-a-json-flag)

## Installation
Install `jc` with `pip`, an OS package manager, or a precompiled binary that
runs from anywhere on your filesystem.

### Pip (macOS, linux, unix, Windows)
```bash
pip3 install jc
```

### OS Package Repositories

| OS                                   | Command                                                                       |
|--------------------------------------|-------------------------------------------------------------------------------|
| Debian/Ubuntu linux                  | `apt-get install jc`                                                          |
| Fedora linux                         | `dnf install jc`                                                              |
| openSUSE linux                       | `zypper install jc`                                                           |
| Arch linux                           | `pacman -S jc`                                                                |
| NixOS linux                          | `nix-env -iA nixpkgs.jc` or `nix-env -iA nixos.jc`                            |
| Guix System linux                    | `guix install jc`                                                             |
| Gentoo Linux                         | `emerge dev-python/jc`                                                        |
| Photon linux                         | `tdnf install jc`                                                             |
| macOS                                | `brew install jc`                                                             |
| FreeBSD                              | `portsnap fetch update && cd /usr/ports/textproc/py-jc && make install clean` |
| [Ansible filter plugin](https://docs.ansible.com/ansible/latest/collections/community/general/jc_filter.html) | `ansible-galaxy collection install community.general` |
| FortiSOAR connector                  | Install from FortiSOAR Connector Marketplace                                  |

> For more OS Packages, see https://repology.org/project/jc/versions.

### Binaries
For precompiled binaries, see [Releases](https://github.com/kellyjonbrazil/jc/releases)
on Github.

## Usage
`jc` reads command output, a file, or a string from `STDIN` and writes JSON to
`STDOUT`:
```bash
COMMAND | jc [SLICE] [OPTIONS] PARSER
cat FILE | jc [SLICE] [OPTIONS] PARSER
echo STRING | jc [SLICE] [OPTIONS] PARSER
```

With the "magic" syntax, put `jc` and its options in front of the command or
`/proc` file path instead (command aliases and shell builtins are not
supported):
```bash
jc [SLICE] [OPTIONS] COMMAND
jc [SLICE] [OPTIONS] /proc/<path-to-procfile>
```

Output is compact JSON by default. Use `-p` to pretty-print it.

### Parsers

| Argument          | Command or Filetype                                     | Documentation                                                              |
|-------------------|---------------------------------------------------------|----------------------------------------------------------------------------|
|          `--acpi` | `acpi` command parser                                   | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/acpi)           |
|       `--airport` | `airport -I` command parser                             | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/airport)        |
|     `--airport-s` | `airport -s` command parser                             | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/airport_s)      |
|        `--amixer` | `amixer` command parser                                 | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/amixer)         |
|     `--apachectl` | `apachectl -S` command parser                           | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/apachectl)      |
| `--apt-cache-show` | `apt-cache show` command parser                         | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/apt_cache_show) |
|   `--apt-get-sqq` | `apt-get -sqq` command parser                           | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/apt_get_sqq)    |
|           `--arp` | `arp` command parser                                    | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/arp)            |
|    `--asciitable` | ASCII and Unicode table parser                          | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/asciitable)     |
|  `--asciitable-m` | multi-line ASCII and Unicode table parser               | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/asciitable_m)   |
| `--authorized-keys` | `~/.ssh/authorized_keys` file parser                    | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/authorized_keys) |
|         `--blkid` | `blkid` command parser                                  | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/blkid)          |
|  `--bluetoothctl` | `bluetoothctl` command parser                           | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/bluetoothctl)   |
|           `--cbt` | `cbt` (Google Bigtable) command parser                  | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/cbt)            |
|           `--cef` | CEF string parser                                       | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/cef)            |
|         `--cef-s` | CEF string streaming parser                             | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/cef_s)          |
|       `--certbot` | `certbot` command parser                                | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/certbot)        |
|         `--chage` | `chage --list` command parser                           | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/chage)          |
|         `--cksum` | `cksum` and `sum` command parser                        | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/cksum)          |
|           `--clf` | Common and Combined Log Format file parser              | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/clf)            |
|         `--clf-s` | Common and Combined Log Format file streaming parser    | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/clf_s)          |
|     `--conntrack` | `conntrack` command parser                              | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/conntrack)      |
|       `--crontab` | `crontab` command and file parser                       | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/crontab)        |
|     `--crontab-u` | `crontab` file parser with user support                 | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/crontab_u)      |
|           `--csv` | CSV file parser                                         | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/csv)            |
|        `--csv-ih` | CSV implicit header file parser                         | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/csv_ih)         |
|         `--csv-s` | CSV file streaming parser                               | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/csv_s)          |
|      `--csv-ih-s` | CSV implicit header file streaming parser               | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/csv_ih_s)       |
|     `--curl-head` | `curl --head` command parser                            | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/curl_head)      |
|          `--date` | `date` command parser                                   | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/date)           |
|  `--datetime-iso` | ISO 8601 Datetime string parser                         | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/datetime_iso)   |
|  `--debconf-show` | `debconf-show` command parser                           | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/debconf_show)   |
|            `--df` | `df` command parser                                     | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/df)             |
|           `--dig` | `dig` command parser                                    | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/dig)            |
|           `--dir` | `dir` command parser                                    | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/dir)            |
|     `--dmidecode` | `dmidecode` command parser                              | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/dmidecode)      |
|        `--dpkg-l` | `dpkg -l` command parser                                | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/dpkg_l)         |
|            `--du` | `du` command parser                                     | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/du)             |
|    `--efibootmgr` | `efibootmgr` command parser                             | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/efibootmgr)     |
| `--email-address` | Email Address string parser                             | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/email_address)  |
|           `--env` | `env` command parser                                    | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/env)            |
|       `--ethtool` | `ethtool` command parser                                | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/ethtool)        |
|          `--file` | `file` command parser                                   | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/file)           |
|          `--find` | `find` command parser                                   | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/find)           |
|       `--findmnt` | `findmnt` command parser                                | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/findmnt)        |
|        `--finger` | `finger` command parser                                 | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/finger)         |
|          `--free` | `free` command parser                                   | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/free)           |
|         `--fstab` | `/etc/fstab` file parser                                | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/fstab)          |
|       `--getfacl` | `getfacl` command parser                                | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/getfacl)        |
|      `--git-diff` | `git diff --name-status` command parser                 | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/git_diff)       |
|       `--git-log` | `git log` command parser                                | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/git_log)        |
|     `--git-log-s` | `git log` command streaming parser                      | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/git_log_s)      |
| `--git-ls-remote` | `git ls-remote` command parser                          | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/git_ls_remote)  |
|           `--gpg` | `gpg --with-colons` command parser                      | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/gpg)            |
|         `--group` | `/etc/group` file parser                                | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/group)          |
|       `--gshadow` | `/etc/gshadow` file parser                              | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/gshadow)        |
|          `--hash` | `hash` command parser                                   | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/hash)           |
|       `--hashsum` | hashsum command parser (`md5sum`, `shasum`, etc.)       | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/hashsum)        |
|     `--hciconfig` | `hciconfig` command parser                              | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/hciconfig)      |
|       `--history` | `history` command parser                                | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/history)        |
|          `--host` | `host` command parser                                   | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/host)           |
|         `--hosts` | `/etc/hosts` file parser                                | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/hosts)          |
|  `--http-headers` | HTTP headers parser                                     | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/http_headers)   |
|           `--ics` | `ics` file parser                                       | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/ics)            |
|            `--id` | `id` command parser                                     | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/id)             |
|      `--ifconfig` | `ifconfig` command parser                               | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/ifconfig)       |
|         `--iftop` | `iftop` command parser                                  | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/iftop)          |
|           `--ini` | INI file parser                                         | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/ini)            |
|       `--ini-dup` | INI with duplicate key file parser                      | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/ini_dup)        |
|        `--iostat` | `iostat` command parser                                 | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/iostat)         |
|      `--iostat-s` | `iostat` command streaming parser                       | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/iostat_s)       |
|    `--ip-address` | IPv4 and IPv6 Address string parser                     | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/ip_address)     |
|      `--ipconfig` | `ipconfig` Windows command parser                       | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/ipconfig)       |
|      `--iptables` | `iptables` command parser                               | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/iptables)       |
|      `--ip-route` | `ip route` command parser                               | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/ip_route)       |
|       `--iw-scan` | `iw dev [device] scan` command parser                   | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/iw_scan)        |
|      `--iwconfig` | `iwconfig` command parser                               | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/iwconfig)       |
|  `--jar-manifest` | Java MANIFEST.MF file parser                            | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/jar_manifest)   |
|          `--jobs` | `jobs` command parser                                   | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/jobs)           |
|           `--jwt` | JWT string parser                                       | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/jwt)            |
|            `--kv` | Key/Value file and string parser                        | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/kv)             |
|        `--kv-dup` | Key/Value with duplicate key file and string parser     | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/kv_dup)         |
|          `--last` | `last` and `lastb` command parser                       | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/last)           |
|           `--ldd` | `ldd` command parser                                    | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/ldd)            |
|            `--ls` | `ls` command parser                                     | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/ls)             |
|          `--ls-s` | `ls` command streaming parser                           | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/ls_s)           |
|        `--lsattr` | `lsattr` command parser                                 | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/lsattr)         |
|   `--lsb-release` | `lsb_release` command parser                            | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/lsb_release)    |
|         `--lsblk` | `lsblk` command parser                                  | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/lsblk)          |
|         `--lsmod` | `lsmod` command parser                                  | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/lsmod)          |
|          `--lsof` | `lsof` command parser                                   | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/lsof)           |
|         `--lspci` | `lspci -mmv` command parser                             | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/lspci)          |
|         `--lsusb` | `lsusb` command parser                                  | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/lsusb)          |
|           `--m3u` | M3U and M3U8 file parser                                | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/m3u)            |
|         `--mdadm` | `mdadm` command parser                                  | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/mdadm)          |
|         `--mount` | `mount` command parser                                  | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/mount)          |
|        `--mpstat` | `mpstat` command parser                                 | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/mpstat)         |
|      `--mpstat-s` | `mpstat` command streaming parser                       | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/mpstat_s)       |
|   `--needrestart` | `needrestart -b` command parser                         | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/needrestart)    |
|         `--netrc` | `.netrc` file parser                                    | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/netrc)          |
|       `--netstat` | `netstat` command parser                                | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/netstat)        |
| `--net-localgroup` | `net localgroup` command parser                         | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/net_localgroup) |
|      `--net-user` | `net user` command parser                               | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/net_user)       |
|     `--nfsiostat` | `nfsiostat` command parser                              | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/nfsiostat)      |
|   `--nfsiostat-s` | `nfsiostat` command streaming parser                    | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/nfsiostat_s)    |
|      `--nftables` | `nft` command parser                                    | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/nftables)       |
|         `--nmcli` | `nmcli` command parser                                  | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/nmcli)          |
|   `--nsd-control` | `nsd-control` command parser                            | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/nsd_control)    |
|          `--ntpq` | `ntpq -p` command parser                                | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/ntpq)           |
|       `--openvpn` | openvpn-status.log file parser                          | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/openvpn)        |
|     `--os-prober` | `os-prober` command parser                              | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/os_prober)      |
|    `--os-release` | `/etc/os-release` file parser                           | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/os_release)     |
|        `--pacman` | `pacman` command parser                                 | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/pacman)         |
|        `--passwd` | `/etc/passwd` file parser                               | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/passwd)         |
|          `--path` | POSIX path string parser                                | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/path)           |
|     `--path-list` | POSIX path list string parser                           | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/path_list)      |
|       `--pci-ids` | `pci.ids` file parser                                   | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/pci_ids)        |
|        `--pgpass` | PostgreSQL password file parser                         | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/pgpass)         |
|       `--pidstat` | `pidstat -H` command parser                             | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/pidstat)        |
|     `--pidstat-s` | `pidstat -H` command streaming parser                   | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/pidstat_s)      |
|          `--ping` | `ping` and `ping6` command parser                       | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/ping)           |
|        `--ping-s` | `ping` and `ping6` command streaming parser             | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/ping_s)         |
|      `--pip-list` | `pip list` command parser                               | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/pip_list)       |
|      `--pip-show` | `pip show` command parser                               | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/pip_show)       |
| `--pkg-index-apk` | Alpine Linux Package Index file parser                  | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/pkg_index_apk)  |
| `--pkg-index-deb` | Debian Package Index file parser                        | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/pkg_index_deb)  |
|         `--plist` | PLIST file parser                                       | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/plist)          |
|      `--postconf` | `postconf -M` command parser                            | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/postconf)       |
|          `--proc` | `/proc/` file parser                                    | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/proc)           |
|            `--ps` | `ps` command parser                                     | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/ps)             |
|  `--resolve-conf` | `/etc/resolve.conf` file parser                         | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/resolve_conf)   |
|         `--route` | `route` command parser                                  | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/route)          |
|   `--route-print` | `route print` command parser                            | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/route_print)    |
|        `--rpm-qi` | `rpm -qi` command parser                                | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/rpm_qi)         |
|         `--rsync` | `rsync` command parser                                  | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/rsync)          |
|       `--rsync-s` | `rsync` command streaming parser                        | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/rsync_s)        |
|        `--semver` | Semantic Version string parser                          | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/semver)         |
|        `--sfdisk` | `sfdisk` command parser                                 | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/sfdisk)         |
|        `--shadow` | `/etc/shadow` file parser                               | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/shadow)         |
|           `--srt` | SRT file parser                                         | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/srt)            |
|            `--ss` | `ss` command parser                                     | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/ss)             |
|      `--ssh-conf` | `ssh` config file and `ssh -G` command parser           | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/ssh_conf)       |
|     `--sshd-conf` | `sshd` config file and `sshd -T` command parser         | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/sshd_conf)      |
|          `--stat` | `stat` command parser                                   | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/stat)           |
|        `--stat-s` | `stat` command streaming parser                         | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/stat_s)         |
|        `--swapon` | `swapon` command parser                                 | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/swapon)         |
|        `--sysctl` | `sysctl` command parser                                 | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/sysctl)         |
|        `--syslog` | Syslog RFC 5424 string parser                           | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/syslog)         |
|      `--syslog-s` | Syslog RFC 5424 string streaming parser                 | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/syslog_s)       |
|    `--syslog-bsd` | Syslog RFC 3164 string parser                           | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/syslog_bsd)     |
|  `--syslog-bsd-s` | Syslog RFC 3164 string streaming parser                 | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/syslog_bsd_s)   |
|     `--systemctl` | `systemctl` command parser                              | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/systemctl)      |
|  `--systemctl-lj` | `systemctl list-jobs` command parser                    | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/systemctl_lj)   |
|  `--systemctl-ls` | `systemctl list-sockets` command parser                 | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/systemctl_ls)   |
| `--systemctl-luf` | `systemctl list-unit-files` command parser              | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/systemctl_luf)  |
|    `--systeminfo` | `systeminfo` command parser                             | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/systeminfo)     |
|          `--time` | `/usr/bin/time` command parser                          | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/time)           |
|   `--timedatectl` | `timedatectl status` command parser                     | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/timedatectl)    |
|     `--timestamp` | Unix Epoch Timestamp string parser                      | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/timestamp)      |
|          `--toml` | TOML file parser                                        | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/toml)           |
|           `--top` | `top -b` command parser                                 | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/top)            |
|         `--top-s` | `top -b` command streaming parser                       | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/top_s)          |
|     `--tracepath` | `tracepath` and `tracepath6` command parser             | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/tracepath)      |
|    `--traceroute` | `traceroute` and `traceroute6` command parser           | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/traceroute)     |
|  `--traceroute-s` | `traceroute` and `traceroute6` command streaming parser | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/traceroute_s)   |
|           `--tsv` | TSV file parser                                         | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/tsv)            |
|        `--tsv-ih` | TSV implicit header file parser                         | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/tsv_ih)         |
|         `--tsv-s` | TSV file streaming parser                               | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/tsv_s)          |
|      `--tsv-ih-s` | TSV implicit header file streaming parser               | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/tsv_ih_s)       |
|       `--tune2fs` | `tune2fs -l` command parser                             | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/tune2fs)        |
|       `--typeset` | `typeset` and `declare` command parser                  | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/typeset)        |
|       `--udevadm` | `udevadm info` command parser                           | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/udevadm)        |
|           `--ufw` | `ufw status` command parser                             | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/ufw)            |
|   `--ufw-appinfo` | `ufw app info [application]` command parser             | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/ufw_appinfo)    |
|         `--uname` | `uname -a` command parser                               | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/uname)          |
| `--update-alt-gs` | `update-alternatives --get-selections` command parser   | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/update_alt_gs)  |
|  `--update-alt-q` | `update-alternatives --query` command parser            | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/update_alt_q)   |
|        `--upower` | `upower` command parser                                 | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/upower)         |
|          `--upsc` | `upsc` command parser                                   | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/upsc)           |
|        `--uptime` | `uptime` command parser                                 | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/uptime)         |
|           `--url` | URL string parser                                       | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/url)            |
|           `--ver` | Version string parser                                   | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/ver)            |
|     `--veracrypt` | `veracrypt` command parser                              | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/veracrypt)      |
|        `--vmstat` | `vmstat` command parser                                 | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/vmstat)         |
|      `--vmstat-s` | `vmstat` command streaming parser                       | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/vmstat_s)       |
|             `--w` | `w` command parser                                      | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/w)              |
|            `--wc` | `wc` command parser                                     | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/wc)             |
|       `--wg-show` | `wg show` command parser                                | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/wg_show)        |
|           `--who` | `who` command parser                                    | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/who)            |
|     `--x509-cert` | X.509 PEM and DER certificate file parser               | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/x509_cert)      |
|      `--x509-crl` | X.509 PEM and DER certificate revocation list file parser | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/x509_crl)       |
|      `--x509-csr` | X.509 PEM and DER certificate request file parser       | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/x509_csr)       |
|           `--xml` | XML file parser                                         | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/xml)            |
|        `--xrandr` | `xrandr` command parser                                 | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/xrandr)         |
|          `--yaml` | YAML file parser                                        | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/yaml)           |
|       `--zipinfo` | `zipinfo` command parser                                | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/zipinfo)        |
|  `--zpool-iostat` | `zpool iostat` command parser                           | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/zpool_iostat)   |
|  `--zpool-status` | `zpool status` command parser                           | [details](https://kellyjonbrazil.github.io/jc/docs/parsers/zpool_status)   |

### Options

| Short | Long            | Description                                                                                                                                                  |
|-------|-----------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `-a`  | `--about`       | About `jc`. Prints information about `jc` and the parsers (in JSON or YAML, of course!)                                                                      |
| `-C`  | `--force-color` | Force color output even when using pipes (overrides `-m` and the `NO_COLOR` env variable)                                                                    |
| `-d`  | `--debug`       | Debug mode. Prints trace messages if parsing issues are encountered (use`-dd` for verbose debugging)                                                         |
| `-h`  | `--help`        | Help. Use `jc -h --parser_name` for parser documentation. Use twice to show hidden parsers (e.g. `-hh`). Use thrice to show parser categories (e.g. `-hhh`). |
| `-m`  | `--monochrome`  | Monochrome output                                                                                                                                            |
| `-M`  | `--meta-out`    | Add metadata to output including timestamp, parser name, magic command, magic command exit code, etc.                                                        |
| `-p`  | `--pretty`      | Pretty format the JSON output                                                                                                                                |
| `-q`  | `--quiet`       | Quiet mode. Suppresses parser warning messages (use `-qq` to ignore streaming parser errors)                                                                 |
| `-r`  | `--raw`         | Raw output. Provides more literal output, typically with string values and no additional semantic processing                                                 |
| `-s`  | `--slurp`       | Slurp multiple lines into an array. (use `-hhh` to find compatible parsers)                                                                                  |
| `-u`  | `--unbuffer`    | Unbuffer output                                                                                                                                              |
| `-v`  | `--version`     | Version information                                                                                                                                          |
| `-y`  | `--yaml-out`    | YAML output                                                                                                                                                  |
| `-B`  | `--bash-comp`   | Generate Bash shell completion script ([more info](https://github.com/kellyjonbrazil/jc/wiki/Shell-Completions))                                             |
| `-Z`  | `--zsh-comp`    | Generate Zsh shell completion script ([more info](https://github.com/kellyjonbrazil/jc/wiki/Shell-Completions))                                              |
| `-X`  | `--xonsh-comp`  | Generate Xonsh shell completion script ([more info](https://github.com/kellyjonbrazil/jc/wiki/Shell-Completions))                                            |


### Slice
A `START:STOP` line slice selects which lines of the input to convert, like
[Python's slicing](https://stackoverflow.com/questions/509211/understanding-slicing).
Lines are numbered from `0` at the start or from `-1` at the end, and `STOP`
is not included. Lines are counted at LF and CRLF line endings; a lone CR does
not start a new line. Slices with negative numbers use more memory.

For example, both of these slices skip the first and last lines:
```bash
$ cat table.txt
      ### We want to skip this header ###
          col1       col2
          foo        1
          bar        2
      ### We want to skip this footer ###
$ cat table.txt | jc 1:-1 --asciitable
[{"col1":"foo","col2":"1"},{"col1":"bar","col2":"2"}]
$ cat table.txt | jc 1:4 --asciitable
[{"col1":"foo","col2":"1"},{"col1":"bar","col2":"2"}]
```

| Slice Notation | Input Lines Processed                                        |
|----------------|--------------------------------------------------------------|
| `START:STOP`   | lines `START` through `STOP - 1`                             |
| `START:`       | lines `START` through the rest of the output                 |
| `:STOP`        | lines from the beginning through `STOP - 1`                  |
| `-START:STOP`  | `START` lines from the end through `STOP - 1`                |
| `START:-STOP`  | lines `START` through `STOP` lines from the end              |
| `-START:-STOP` | `START` lines from the end through `STOP` lines from the end |
| `-START:`      | `START` lines from the end through the rest of the output    |
| `:-STOP`       | lines from the beginning through `STOP` lines from the end   |
| `:`            | all lines                                                    |

### Slurp
String parsers that read a single line (e.g. `url` and `ip-address`) can read
many lines with the `--slurp` option and output an array of results. Use
`jc -hhh` to see which parsers support it.
```bash
$ cat ip-addresses.txt | jc --slurp --ip-address
[<multiple output objects>]
```

The `/proc` magic syntax slurps multiple files automatically and adds a `_file`
field to each output object:
```bash
$ jc /proc/*/status
[<multiple output objects>]
```

With `--meta-out`, slurped output is wrapped in an object, and `input_list`
holds the input strings or `/proc` filenames so you can match each result to
its input:
```json
{
  "result": [<multiple output objects>],
  "_jc_meta": {
    "parser": "url",
    "timestamp": 1706235558.654576,
    "slice_start": null,
    "slice_end": null,
    "input_list": [
      "http://www.google.com",
      "https://www.apple.com",
      "https://www.microsoft.com"
    ]
  }
}
```

### Exit Codes
`jc` exits with `100` on a fatal error, otherwise `0`. With the "magic" syntax
(e.g. `jc ifconfig eth0`), the exit code of the parsed program is added to the
`jc` exit code, so you can tell where an error came from:

| `ifconfig` exit code | `jc` exit code | Combined exit code | Interpretation                     |
|----------------------|----------------|--------------------|------------------------------------|
| `0`                  | `0`            | `0`                | No errors                          |
| `1`                  | `0`            | `1`                | Error in  `ifconfig`               |
| `0`                  | `100`          | `100`              | Error in  `jc`                     |
| `1`                  | `100`          | `101`              | Error in  both `ifconfig` and `jc` |

The `-M` (`--meta-out`) option also adds the program's exit code to the
output in the `_jc_meta` object:
```bash
$ jc --meta-out -p ping -c2 192.168.1.252
{
  "destination_ip": "192.168.1.252",
  "data_bytes": 56,
  "pattern": null,
  "destination": "192.168.1.252",
  "packets_transmitted": 2,
  "packets_received": 0,
  "packet_loss_percent": 100.0,
  "duplicates": 0,
  "responses": [
    {
      "type": "timeout",
      "icmp_seq": 0,
      "duplicate": false
    }
  ],
  "_jc_meta": {
    "parser": "ping",
    "timestamp": 1661357115.27949,
    "magic_command": [
      "ping",
      "-c2",
      "192.168.1.252"
    ],
    "magic_command_exit": 2
  }
}
$ echo $?
2
```

### Colors
Set custom colors with the `JC_COLORS` environment variable, as four
comma-separated values:
```bash
JC_COLORS=<keyname_color>,<keyword_color>,<number_color>,<string_color>
```

Colors are: `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`,
`gray`, `brightblack`, `brightred`, `brightgreen`, `brightyellow`, `brightblue`,
`brightmagenta`, `brightcyan`, `white`, or `default`. For example, the default
colors are `JC_COLORS=blue,brightblack,magenta,green` (the same as
`JC_COLORS=default,default,default,default`).

Set the [`NO_COLOR`](http://no-color.org/) environment variable to any value
to disable colors. The `-C` option forces color output and overrides both
`NO_COLOR` and `-m`.

### Streaming Parsers
Streaming parsers (e.g. `ls-s` and `ping-s`) output
[JSON Lines](https://jsonlines.org/) as the input arrives instead of waiting
for all of it. This uses much less memory on large inputs (e.g. `ls -lR /`).

> Note: Streaming parsers cannot be used with the "magic" syntax

#### Ignoring Errors
To keep a long-running pipeline going when a line can't be parsed, use the
`-qq` option (or `ignore_exceptions=True` in `parse()`). Each output object
then gets a `_jc_meta` object with a `success` field. Lines that failed also
get `error` and `line` fields.

Successfully parsed line with `-qq` option:
```json
{
  "command_data": "data",
  "_jc_meta": {
    "success": true
  }
}
```

Unsuccessfully parsed line with `-qq` option:
```json
{
  "_jc_meta": {
    "success": false,
    "error": "error message",
    "line": "original line data"
  }
}
```

#### Unbuffering Output
When `jc` output is piped to another program, the OS buffers it (usually about
4KB), so slow input like `ping` can look stuck. Use the `-u` option to unbuffer
the output:
```
$ ping 1.1.1.1 | jc --ping-s -u | jq
{"type":"reply","pattern":null,"timestamp":null,"bytes":"64","response...}
{"type":"reply","pattern":null,"timestamp":null,"bytes":"64","response...}
...
```

> Note: Unbuffered output can be slower for large data streams.

#### Using Streaming Parsers as Python Modules
Streaming parsers take any iterable of lines (e.g. `sys.stdin` or
`str.split('\n')`) and return a lazy iterable. Loop through it or use
[next()](https://docs.python.org/3/library/functions.html#next):
```python
import jc

result = jc.parse('ls_s', ls_command_output.split('\n'))
for item in result:
    print(item["filename"])
```

### Parser Plugins
Parser plugins go in the `jcparsers` folder of your local app data directory:

- Linux/unix: `$HOME/.local/share/jc/jcparsers`
- macOS: `$HOME/Library/Application Support/jc/jcparsers`
- Windows: `$LOCALAPPDATA\jc\jc\jcparsers`

A plugin is a standard Python module. Use
[`jc/parsers/foo.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/foo.py)
or [`jc/parsers/foo_s.py (streaming)`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/foo_s.py)
as a template. Plugin filenames must be valid Python module names (starting
with a letter, and only letters, digits, and underscores). Dependencies can be
placed in the `jc` folder above `jcparsers`. Local plugins may override
built-in parsers.

> Note: The application data directory follows the
[XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html)

### Caveats

#### Locale

For best results set the locale environment variables to `C` or
`en_US.UTF-8` by modifying the `LC_ALL` variable:
```
$ LC_ALL=C date | jc --date
```

You can also set the locale variables individually:
```
$ export LANG=C
$ export LC_NUMERIC=C
```

On some older systems UTF-8 output will be downgraded to ASCII with `\u`
escape sequences if the `C` locale does not support UTF-8 encoding.

#### Timezones

Some parsers have calculated epoch timestamp fields added to the output. Unless
a timestamp field name has a `_utc` suffix it is considered naive. (i.e. based
on the local timezone of the system the `jc` parser was run on).

If a UTC timezone can be detected in the text of the command output, the
timestamp will be timezone aware and have a `_utc` suffix on the key name.
(e.g. `epoch_utc`) No other timezones are supported for aware timestamps.

#### Line Endings

`jc` passes input to the parser without translating line endings, whether it
comes from `STDIN`, a "magic" command, or a `/proc` file. All line-based
parsers split lines at LF and CRLF line endings only, so other characters that
can appear inside a value, such as a lone CR, form feed, or Unicode line separator, stay
part of that line. Parsers for file formats that can use CR-only line endings (`csv`,
`hosts`, `jar-manifest`, and `m3u`) also accept a lone CR as a line ending.

Streaming parsers split `STDIN` lines the same way (LF and CRLF only). Bytes
in `STDIN` that are not valid UTF-8 are shown as backslash escapes (e.g.
`\xff`) instead of stopping the parser.

## Use In Other Shells
`jc` works in most shells, and some modern shells can load JSON directly. For
example, in [NGS](https://ngs-lang.org/) (Next Generation Shell):
```bash
myvar = ``jc dig www.google.com``[0].answer[0].data
```

For other shells, see this
[wiki page](https://github.com/kellyjonbrazil/jc/wiki/Using-jc-With-Different-Shells).

## Compatibility
`jc` requires Python 3.6 or newer. Some parsers (e.g. `dig`, `xml`, `csv`) work
on any platform. Parsers for platform-specific output print a warning on an
unsupported platform. Run `jc -ap` to see each parser's compatibility.

You can still use a parser on another platform, for example to parse a saved
Linux `lsof` output on macOS or Windows. Use the `-q` option (or `quiet=True`
in `parse()`) to hide the warning:
```bash
cat lsof.out | jc -q --lsof      # Windows: type lsof.out | jc -q --lsof
```

## Contributions
Contributions are welcome! Use the
[`jc/parsers/foo.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/foo.py)
or [`jc/parsers/foo_s.py (streaming)`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/foo_s.py)
parser as a template and submit a pull request. See the
[Contributing Guidelines](https://github.com/kellyjonbrazil/jc/blob/master/CONTRIBUTING.md)
for more information.

## Examples
Here is an example of `jc` output. See [EXAMPLES](https://kellyjonbrazil.github.io/jc/EXAMPLES)
or the parser documentation for many more.

### ps
```bash
ps axu | jc -p --ps          # or:  jc -p ps axu
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
    "command": "/usr/lib/systemd/systemd --switched-root --system --deseria..."
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

© 2019-2026 Kelly Brazil