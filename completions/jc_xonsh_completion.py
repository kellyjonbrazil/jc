"""jc completions for the xonsh shell.

Load this file from your xonsh RC (e.g. ~/.config/xonsh/rc.d/jc.py) or
source it with `exec(compile(open(...).read(), ...))`.
"""
from xonsh.built_ins import XSH
from xonsh.completers.completer import add_one_completer
from xonsh.completers.path import contextual_complete_path
from xonsh.completers.tools import (
    RichCompletion,
    contextual_command_completer_for,
)
from xonsh.parsers.completion_context import CommandContext, CompletionContext

jc_commands = {
    'acpi': 'run "acpi" command with magic syntax.',
    'airport': 'run "airport" command with magic syntax.',
    'amixer': 'run "amixer" command with magic syntax.',
    'apt-cache': 'run "apt-cache" command with magic syntax.',
    'apt-get': 'run "apt-get" command with magic syntax.',
    'arp': 'run "arp" command with magic syntax.',
    'blkid': 'run "blkid" command with magic syntax.',
    'bluetoothctl': 'run "bluetoothctl" command with magic syntax.',
    'cbt': 'run "cbt" command with magic syntax.',
    'certbot': 'run "certbot" command with magic syntax.',
    'chage': 'run "chage" command with magic syntax.',
    'cksum': 'run "cksum" command with magic syntax.',
    'crontab': 'run "crontab" command with magic syntax.',
    'curl': 'run "curl" command with magic syntax.',
    'date': 'run "date" command with magic syntax.',
    'debconf-show': 'run "debconf-show" command with magic syntax.',
    'df': 'run "df" command with magic syntax.',
    'dig': 'run "dig" command with magic syntax.',
    'dmidecode': 'run "dmidecode" command with magic syntax.',
    'dpkg': 'run "dpkg" command with magic syntax.',
    'du': 'run "du" command with magic syntax.',
    'efibootmgr': 'run "efibootmgr" command with magic syntax.',
    'env': 'run "env" command with magic syntax.',
    'ethtool': 'run "ethtool" command with magic syntax.',
    'file': 'run "file" command with magic syntax.',
    'findmnt': 'run "findmnt" command with magic syntax.',
    'finger': 'run "finger" command with magic syntax.',
    'free': 'run "free" command with magic syntax.',
    'git': 'run "git" command with magic syntax.',
    'gpg': 'run "gpg" command with magic syntax.',
    'hciconfig': 'run "hciconfig" command with magic syntax.',
    'host': 'run "host" command with magic syntax.',
    'id': 'run "id" command with magic syntax.',
    'ifconfig': 'run "ifconfig" command with magic syntax.',
    'iostat': 'run "iostat" command with magic syntax.',
    'ip': 'run "ip" command with magic syntax.',
    'ipconfig': 'run "ipconfig" command with magic syntax.',
    'iptables': 'run "iptables" command with magic syntax.',
    'iw': 'run "iw" command with magic syntax.',
    'iwconfig': 'run "iwconfig" command with magic syntax.',
    'jobs': 'run "jobs" command with magic syntax.',
    'last': 'run "last" command with magic syntax.',
    'lastb': 'run "lastb" command with magic syntax.',
    'ls': 'run "ls" command with magic syntax.',
    'lsattr': 'run "lsattr" command with magic syntax.',
    'lsb_release': 'run "lsb_release" command with magic syntax.',
    'lsblk': 'run "lsblk" command with magic syntax.',
    'lsmod': 'run "lsmod" command with magic syntax.',
    'lsof': 'run "lsof" command with magic syntax.',
    'lspci': 'run "lspci" command with magic syntax.',
    'lsusb': 'run "lsusb" command with magic syntax.',
    'md5': 'run "md5" command with magic syntax.',
    'md5sum': 'run "md5sum" command with magic syntax.',
    'mdadm': 'run "mdadm" command with magic syntax.',
    'mount': 'run "mount" command with magic syntax.',
    'mpstat': 'run "mpstat" command with magic syntax.',
    'needrestart': 'run "needrestart" command with magic syntax.',
    'net': 'run "net" command with magic syntax.',
    'netstat': 'run "netstat" command with magic syntax.',
    'nmcli': 'run "nmcli" command with magic syntax.',
    'nsd-control': 'run "nsd-control" command with magic syntax.',
    'ntpq': 'run "ntpq" command with magic syntax.',
    'os-prober': 'run "os-prober" command with magic syntax.',
    'pacman': 'run "pacman" command with magic syntax.',
    'pidstat': 'run "pidstat" command with magic syntax.',
    'ping': 'run "ping" command with magic syntax.',
    'ping6': 'run "ping6" command with magic syntax.',
    'pip': 'run "pip" command with magic syntax.',
    'pip3': 'run "pip3" command with magic syntax.',
    'postconf': 'run "postconf" command with magic syntax.',
    'printenv': 'run "printenv" command with magic syntax.',
    'ps': 'run "ps" command with magic syntax.',
    'route': 'run "route" command with magic syntax.',
    'rpm': 'run "rpm" command with magic syntax.',
    'rsync': 'run "rsync" command with magic syntax.',
    'sfdisk': 'run "sfdisk" command with magic syntax.',
    'sha1sum': 'run "sha1sum" command with magic syntax.',
    'sha224sum': 'run "sha224sum" command with magic syntax.',
    'sha256sum': 'run "sha256sum" command with magic syntax.',
    'sha384sum': 'run "sha384sum" command with magic syntax.',
    'sha512sum': 'run "sha512sum" command with magic syntax.',
    'shasum': 'run "shasum" command with magic syntax.',
    'ss': 'run "ss" command with magic syntax.',
    'ssh': 'run "ssh" command with magic syntax.',
    'sshd': 'run "sshd" command with magic syntax.',
    'stat': 'run "stat" command with magic syntax.',
    'sum': 'run "sum" command with magic syntax.',
    'swapon': 'run "swapon" command with magic syntax.',
    'sysctl': 'run "sysctl" command with magic syntax.',
    'systemctl': 'run "systemctl" command with magic syntax.',
    'systeminfo': 'run "systeminfo" command with magic syntax.',
    'timedatectl': 'run "timedatectl" command with magic syntax.',
    'top': 'run "top" command with magic syntax.',
    'tracepath': 'run "tracepath" command with magic syntax.',
    'tracepath6': 'run "tracepath6" command with magic syntax.',
    'traceroute': 'run "traceroute" command with magic syntax.',
    'traceroute6': 'run "traceroute6" command with magic syntax.',
    'tune2fs': 'run "tune2fs" command with magic syntax.',
    'udevadm': 'run "udevadm" command with magic syntax.',
    'ufw': 'run "ufw" command with magic syntax.',
    'uname': 'run "uname" command with magic syntax.',
    'update-alternatives': 'run "update-alternatives" command with magic syntax.',
    'upower': 'run "upower" command with magic syntax.',
    'upsc': 'run "upsc" command with magic syntax.',
    'uptime': 'run "uptime" command with magic syntax.',
    'vdir': 'run "vdir" command with magic syntax.',
    'veracrypt': 'run "veracrypt" command with magic syntax.',
    'vmstat': 'run "vmstat" command with magic syntax.',
    'w': 'run "w" command with magic syntax.',
    'wc': 'run "wc" command with magic syntax.',
    'wg': 'run "wg" command with magic syntax.',
    'who': 'run "who" command with magic syntax.',
    'xrandr': 'run "xrandr" command with magic syntax.',
    'yay': 'run "yay" command with magic syntax.',
    'zipinfo': 'run "zipinfo" command with magic syntax.',
    'zpool': 'run "zpool" command with magic syntax.',
}
jc_parsers = {
    '--acpi': '`acpi` command parser',
    '--airport': '`airport -I` command parser',
    '--airport-s': '`airport -s` command parser',
    '--amixer': '`amixer` command parser',
    '--apt-cache-show': '`apt-cache show` command parser',
    '--apt-get-sqq': '`apt-get -sqq` command parser',
    '--arp': '`arp` command parser',
    '--asciitable': 'ASCII and Unicode table parser',
    '--asciitable-m': 'multi-line ASCII and Unicode table parser',
    '--blkid': '`blkid` command parser',
    '--bluetoothctl': '`bluetoothctl` command parser',
    '--cbt': '`cbt` (Google Bigtable) command parser',
    '--cef': 'CEF string parser',
    '--cef-s': 'CEF string streaming parser',
    '--certbot': '`certbot` command parser',
    '--chage': '`chage --list` command parser',
    '--cksum': '`cksum` and `sum` command parser',
    '--clf': 'Common and Combined Log Format file parser',
    '--clf-s': 'Common and Combined Log Format file streaming parser',
    '--crontab': '`crontab` command and file parser',
    '--crontab-u': '`crontab` file parser with user support',
    '--csv': 'CSV file parser',
    '--csv-ih': 'CSV implicit header file parser',
    '--csv-s': 'CSV file streaming parser',
    '--csv-ih-s': 'CSV implicit header file streaming parser',
    '--curl-head': '`curl --head` command parser',
    '--date': '`date` command parser',
    '--datetime-iso': 'ISO 8601 Datetime string parser',
    '--debconf-show': '`debconf-show` command parser',
    '--df': '`df` command parser',
    '--dig': '`dig` command parser',
    '--dir': '`dir` command parser',
    '--dmidecode': '`dmidecode` command parser',
    '--dpkg-l': '`dpkg -l` command parser',
    '--du': '`du` command parser',
    '--efibootmgr': '`efibootmgr` command parser',
    '--email-address': 'Email Address string parser',
    '--env': '`env` command parser',
    '--ethtool': '`ethtool` command parser',
    '--file': '`file` command parser',
    '--find': '`find` command parser',
    '--findmnt': '`findmnt` command parser',
    '--finger': '`finger` command parser',
    '--free': '`free` command parser',
    '--fstab': '`/etc/fstab` file parser',
    '--git-diff': '`git diff --name-status` command parser',
    '--git-log': '`git log` command parser',
    '--git-log-s': '`git log` command streaming parser',
    '--git-ls-remote': '`git ls-remote` command parser',
    '--gpg': '`gpg --with-colons` command parser',
    '--group': '`/etc/group` file parser',
    '--gshadow': '`/etc/gshadow` file parser',
    '--hash': '`hash` command parser',
    '--hashsum': 'hashsum command parser (`md5sum`, `shasum`, etc.)',
    '--hciconfig': '`hciconfig` command parser',
    '--history': '`history` command parser',
    '--host': '`host` command parser',
    '--hosts': '`/etc/hosts` file parser',
    '--http-headers': 'HTTP headers parser',
    '--id': '`id` command parser',
    '--ifconfig': '`ifconfig` command parser',
    '--ini': 'INI file parser',
    '--ini-dup': 'INI with duplicate key file parser',
    '--iostat': '`iostat` command parser',
    '--iostat-s': '`iostat` command streaming parser',
    '--ip-address': 'IPv4 and IPv6 Address string parser',
    '--ipconfig': '`ipconfig` Windows command parser',
    '--iptables': '`iptables` command parser',
    '--ip-route': '`ip route` command parser',
    '--iw-scan': '`iw dev [device] scan` command parser',
    '--iwconfig': '`iwconfig` command parser',
    '--jar-manifest': 'Java MANIFEST.MF file parser',
    '--jobs': '`jobs` command parser',
    '--jwt': 'JWT string parser',
    '--kv': 'Key/Value file and string parser',
    '--kv-dup': 'Key/Value with duplicate key file and string parser',
    '--last': '`last` and `lastb` command parser',
    '--ls': '`ls` command parser',
    '--ls-s': '`ls` command streaming parser',
    '--lsattr': '`lsattr` command parser',
    '--lsb-release': '`lsb_release` command parser',
    '--lsblk': '`lsblk` command parser',
    '--lsmod': '`lsmod` command parser',
    '--lsof': '`lsof` command parser',
    '--lspci': '`lspci -mmv` command parser',
    '--lsusb': '`lsusb` command parser',
    '--m3u': 'M3U and M3U8 file parser',
    '--mdadm': '`mdadm` command parser',
    '--mount': '`mount` command parser',
    '--mpstat': '`mpstat` command parser',
    '--mpstat-s': '`mpstat` command streaming parser',
    '--needrestart': '`needrestart -b` command parser',
    '--netstat': '`netstat` command parser',
    '--net-localgroup': '`net localgroup` command parser',
    '--net-user': '`net user` command parser',
    '--nmcli': '`nmcli` command parser',
    '--nsd-control': '`nsd-control` command parser',
    '--ntpq': '`ntpq -p` command parser',
    '--openvpn': 'openvpn-status.log file parser',
    '--os-prober': '`os-prober` command parser',
    '--os-release': '`/etc/os-release` file parser',
    '--pacman': '`pacman` command parser',
    '--passwd': '`/etc/passwd` file parser',
    '--path': 'POSIX path string parser',
    '--path-list': 'POSIX path list string parser',
    '--pci-ids': '`pci.ids` file parser',
    '--pgpass': 'PostgreSQL password file parser',
    '--pidstat': '`pidstat -H` command parser',
    '--pidstat-s': '`pidstat -H` command streaming parser',
    '--ping': '`ping` and `ping6` command parser',
    '--ping-s': '`ping` and `ping6` command streaming parser',
    '--pip-list': '`pip list` command parser',
    '--pip-show': '`pip show` command parser',
    '--pkg-index-apk': 'Alpine Linux Package Index file parser',
    '--pkg-index-deb': 'Debian Package Index file parser',
    '--plist': 'PLIST file parser',
    '--postconf': '`postconf -M` command parser',
    '--proc': '`/proc/` file parser',
    '--proc-buddyinfo': '`/proc/buddyinfo` file parser',
    '--proc-cmdline': '`/proc/cmdline` file parser',
    '--proc-consoles': '`/proc/consoles` file parser',
    '--proc-cpuinfo': '`/proc/cpuinfo` file parser',
    '--proc-crypto': '`/proc/crypto` file parser',
    '--proc-devices': '`/proc/devices` file parser',
    '--proc-diskstats': '`/proc/diskstats` file parser',
    '--proc-filesystems': '`/proc/filesystems` file parser',
    '--proc-interrupts': '`/proc/interrupts` file parser',
    '--proc-iomem': '`/proc/iomem` file parser',
    '--proc-ioports': '`/proc/ioports` file parser',
    '--proc-loadavg': '`/proc/loadavg` file parser',
    '--proc-locks': '`/proc/locks` file parser',
    '--proc-meminfo': '`/proc/meminfo` file parser',
    '--proc-modules': '`/proc/modules` file parser',
    '--proc-mtrr': '`/proc/mtrr` file parser',
    '--proc-pagetypeinfo': '`/proc/pagetypeinfo` file parser',
    '--proc-partitions': '`/proc/partitions` file parser',
    '--proc-slabinfo': '`/proc/slabinfo` file parser',
    '--proc-softirqs': '`/proc/softirqs` file parser',
    '--proc-stat': '`/proc/stat` file parser',
    '--proc-swaps': '`/proc/swaps` file parser',
    '--proc-uptime': '`/proc/uptime` file parser',
    '--proc-version': '`/proc/version` file parser',
    '--proc-vmallocinfo': '`/proc/vmallocinfo` file parser',
    '--proc-vmstat': '`/proc/vmstat` file parser',
    '--proc-zoneinfo': '`/proc/zoneinfo` file parser',
    '--proc-driver-rtc': '`/proc/driver/rtc` file parser',
    '--proc-net-arp': '`/proc/net/arp` file parser',
    '--proc-net-dev': '`/proc/net/dev` file parser',
    '--proc-net-dev-mcast': '`/proc/net/dev_mcast` file parser',
    '--proc-net-if-inet6': '`/proc/net/if_inet6` file parser',
    '--proc-net-igmp': '`/proc/net/igmp` file parser',
    '--proc-net-igmp6': '`/proc/net/igmp6` file parser',
    '--proc-net-ipv6-route': '`/proc/net/ipv6_route` file parser',
    '--proc-net-netlink': '`/proc/net/netlink` file parser',
    '--proc-net-netstat': '`/proc/net/netstat` file parser',
    '--proc-net-packet': '`/proc/net/packet` file parser',
    '--proc-net-protocols': '`/proc/net/protocols` file parser',
    '--proc-net-route': '`/proc/net/route` file parser',
    '--proc-net-tcp': '`/proc/net/tcp` and `/proc/net/tcp6` file parser',
    '--proc-net-unix': '`/proc/net/unix` file parser',
    '--proc-pid-fdinfo': '`/proc/<pid>/fdinfo/<fd>` file parser',
    '--proc-pid-io': '`/proc/<pid>/io` file parser',
    '--proc-pid-maps': '`/proc/<pid>/maps` file parser',
    '--proc-pid-mountinfo': '`/proc/<pid>/mountinfo` file parser',
    '--proc-pid-numa-maps': '`/proc/<pid>/numa_maps` file parser',
    '--proc-pid-smaps': '`/proc/<pid>/smaps` file parser',
    '--proc-pid-stat': '`/proc/<pid>/stat` file parser',
    '--proc-pid-statm': '`/proc/<pid>/statm` file parser',
    '--proc-pid-status': '`/proc/<pid>/status` file parser',
    '--ps': '`ps` command parser',
    '--resolve-conf': '`/etc/resolve.conf` file parser',
    '--route': '`route` command parser',
    '--route-print': '`route print` command parser',
    '--rpm-qi': '`rpm -qi` command parser',
    '--rsync': '`rsync` command parser',
    '--rsync-s': '`rsync` command streaming parser',
    '--semver': 'Semantic Version string parser',
    '--sfdisk': '`sfdisk` command parser',
    '--shadow': '`/etc/shadow` file parser',
    '--srt': 'SRT file parser',
    '--ss': '`ss` command parser',
    '--ssh-conf': '`ssh` config file and `ssh -G` command parser',
    '--sshd-conf': '`sshd` config file and `sshd -T` command parser',
    '--stat': '`stat` command parser',
    '--stat-s': '`stat` command streaming parser',
    '--swapon': '`swapon` command parser',
    '--sysctl': '`sysctl` command parser',
    '--syslog': 'Syslog RFC 5424 string parser',
    '--syslog-s': 'Syslog RFC 5424 string streaming parser',
    '--syslog-bsd': 'Syslog RFC 3164 string parser',
    '--syslog-bsd-s': 'Syslog RFC 3164 string streaming parser',
    '--systemctl': '`systemctl` command parser',
    '--systemctl-lj': '`systemctl list-jobs` command parser',
    '--systemctl-ls': '`systemctl list-sockets` command parser',
    '--systemctl-luf': '`systemctl list-unit-files` command parser',
    '--systeminfo': '`systeminfo` command parser',
    '--time': '`/usr/bin/time` command parser',
    '--timedatectl': '`timedatectl status` command parser',
    '--timestamp': 'Unix Epoch Timestamp string parser',
    '--toml': 'TOML file parser',
    '--top': '`top -b` command parser',
    '--top-s': '`top -b` command streaming parser',
    '--tracepath': '`tracepath` and `tracepath6` command parser',
    '--traceroute': '`traceroute` and `traceroute6` command parser',
    '--traceroute-s': '`traceroute` and `traceroute6` command streaming parser',
    '--tsv': 'TSV file parser',
    '--tsv-ih': 'TSV implicit header file parser',
    '--tsv-s': 'TSV file streaming parser',
    '--tsv-ih-s': 'TSV implicit header file streaming parser',
    '--tune2fs': '`tune2fs -l` command parser',
    '--typeset': '`typeset` and `declare` command parser',
    '--udevadm': '`udevadm info` command parser',
    '--ufw': '`ufw status` command parser',
    '--ufw-appinfo': '`ufw app info [application]` command parser',
    '--uname': '`uname -a` command parser',
    '--update-alt-gs': '`update-alternatives --get-selections` command parser',
    '--update-alt-q': '`update-alternatives --query` command parser',
    '--upower': '`upower` command parser',
    '--upsc': '`upsc` command parser',
    '--uptime': '`uptime` command parser',
    '--url': 'URL string parser',
    '--ver': 'Version string parser',
    '--veracrypt': '`veracrypt` command parser',
    '--vmstat': '`vmstat` command parser',
    '--vmstat-s': '`vmstat` command streaming parser',
    '--w': '`w` command parser',
    '--wc': '`wc` command parser',
    '--wg-show': '`wg show` command parser',
    '--who': '`who` command parser',
    '--x509-cert': 'X.509 PEM and DER certificate file parser',
    '--x509-crl': 'X.509 PEM and DER certificate revocation list file parser',
    '--x509-csr': 'X.509 PEM and DER certificate request file parser',
    '--xml': 'XML file parser',
    '--xrandr': '`xrandr` command parser',
    '--yaml': 'YAML file parser',
    '--zipinfo': '`zipinfo` command parser',
    '--zpool-iostat': '`zpool iostat` command parser',
    '--zpool-status': '`zpool status` command parser',
}
jc_options = {
    '--force-color': 'force color output (overrides -m)',
    '-C': 'force color output (overrides -m)',
    '--debug': 'debug (double for verbose debug)',
    '-d': 'debug (double for verbose debug)',
    '--monochrome': 'monochrome output',
    '-m': 'monochrome output',
    '--meta-out': 'add metadata to output including timestamp, etc.',
    '-M': 'add metadata to output including timestamp, etc.',
    '--pretty': 'pretty print output',
    '-p': 'pretty print output',
    '--quiet': 'suppress warnings (double to ignore streaming errors)',
    '-q': 'suppress warnings (double to ignore streaming errors)',
    '--raw': 'raw output',
    '-r': 'raw output',
    '--slurp': 'slurp multiple lines into an array',
    '-s': 'slurp multiple lines into an array',
    '--unbuffer': 'unbuffer output',
    '-u': 'unbuffer output',
    '--yaml-out': 'YAML output',
    '-y': 'YAML output',
}
jc_about_options = {
    '--about': 'about jc',
    '-a': 'about jc',
}
jc_about_mod_options = {
    '--pretty': 'pretty print output',
    '-p': 'pretty print output',
    '--yaml-out': 'YAML output',
    '-y': 'YAML output',
    '--monochrome': 'monochrome output',
    '-m': 'monochrome output',
    '--force-color': 'force color output (overrides -m)',
    '-C': 'force color output (overrides -m)',
}
jc_help_options = {
    '--help': 'help (--help --parser_name for parser documentation)',
    '-h': 'help (--help --parser_name for parser documentation)',
}
jc_special_options = {
    '--version': 'version info',
    '-v': 'version info',
    '--bash-comp': 'gen Bash completion: jc -B > /etc/bash_completion.d/jc',
    '-B': 'gen Bash completion: jc -B > /etc/bash_completion.d/jc',
    '--zsh-comp': 'gen Zsh completion: jc -Z > "${fpath[1]}/_jc"',
    '-Z': 'gen Zsh completion: jc -Z > "${fpath[1]}/_jc"',
    '--xonsh-comp': 'gen Xonsh completion: jc -X > ~/.config/xonsh/rc.d/jc.py',
    '-X': 'gen Xonsh completion: jc -X > ~/.config/xonsh/rc.d/jc.py',
}


def _completions(prefix, *option_maps):
    """Return RichCompletions matching prefix, with descriptions.

    Matching is by prefix (not xonsh's default substring match) so that
    completion behaves the same way as the Bash and Zsh completions.

    When nothing matches, stop completing instead of returning an empty
    result: Bash and Zsh offer nothing here, while xonsh would otherwise
    fall through to filesystem path completion.
    """
    completions = {
        RichCompletion(opt, description=desc, append_space=True)
        for option_map in option_maps
        for opt, desc in option_map.items()
        if opt.startswith(prefix)
    }

    if not completions:
        return _no_completions()

    return completions


def _no_completions():
    """Stop completing and offer nothing.

    Returning None or an empty set only means "this completer produced
    nothing", which lets xonsh fall through to the remaining completers
    (e.g. path completion). Raising StopIteration tells xonsh to stop
    collecting completions entirely, matching the Bash and Zsh behavior
    of offering nothing at these positions.
    """
    raise StopIteration


@contextual_command_completer_for('jc')
def _jc_completer(command: CommandContext):
    """Completions for the jc command."""
    words = [arg.value for arg in command.args[1:command.arg_index]]
    prefix = command.prefix

    # if jc_about_options are found anywhere in the line, then only complete
    # from jc_about_mod_options
    if any(word in jc_about_options for word in words):
        return _completions(prefix, jc_about_mod_options)

    # if jc_help_options and a parser are found anywhere in the line, then no
    # more completions
    if any(word in jc_help_options for word in words) \
       and any(word in jc_parsers for word in words):
        return _no_completions()

    # if jc_help_options are found anywhere in the line, then only complete
    # with parsers
    if any(word in jc_help_options for word in words):
        return _completions(prefix, jc_parsers)

    # if special options are found anywhere in the line, then no more
    # completions
    if any(word in jc_special_options for word in words):
        return _no_completions()

    # if magic command is found anywhere in the line, use called command's
    # autocompletion
    for index, word in enumerate(words):
        if word in jc_commands:
            # strip jc and its options so the magic command is completed
            magic_context = command._replace(
                args=command.args[index + 1:],
                arg_index=command.arg_index - index - 1
            )
            completer = XSH.shell.shell.completer
            return completer.complete_from_context(
                CompletionContext(magic_context)
            )

    # if "/pr[oc]" (magic for Procfile parsers) is in the current word,
    # complete with files/directories in the path
    if '/pr' in command.prefix:
        return contextual_complete_path(command)

    # if a parser arg is found anywhere in the line, only show options and
    # help options
    if any(word in jc_parsers for word in words):
        return _completions(prefix, jc_options, jc_help_options)

    # default completion
    return _completions(
        prefix, jc_options, jc_about_options, jc_help_options, jc_special_options,
        jc_parsers, jc_commands
    )


add_one_completer('jc', _jc_completer, 'start')

