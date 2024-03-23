#compdef jc

_jc() {
    local -a jc_commands jc_commands_describe \
             jc_parsers jc_parsers_describe \
             jc_options jc_options_describe \
             jc_about_options jc_about_options_describe \
             jc_about_mod_options jc_about_mod_options_describe \
             jc_help_options jc_help_options_describe \
             jc_special_options jc_special_options_describe

    jc_commands=(acpi airport apt-cache apt-get arp blkid bluetoothctl cbt certbot chage cksum crontab curl date debconf-show df dig dmidecode dpkg du efibootmgr env ethtool file findmnt finger free git gpg hciconfig host id ifconfig iostat ip iptables iw iwconfig jobs last lastb ls lsattr lsb_release lsblk lsmod lsof lspci lsusb md5 md5sum mdadm mount mpstat needrestart netstat nmcli nsd-control ntpq os-prober pidstat ping ping6 pip pip3 postconf printenv ps route rpm rsync sfdisk sha1sum sha224sum sha256sum sha384sum sha512sum shasum ss ssh sshd stat sum swapon sysctl systemctl systeminfo timedatectl top tracepath tracepath6 traceroute traceroute6 tune2fs udevadm ufw uname update-alternatives upower uptime vdir veracrypt vmstat w wc who xrandr zipinfo zpool)
    jc_commands_describe=(
        'acpi:run "acpi" command with magic syntax.'
        'airport:run "airport" command with magic syntax.'
        'apt-cache:run "apt-cache" command with magic syntax.'
        'apt-get:run "apt-get" command with magic syntax.'
        'arp:run "arp" command with magic syntax.'
        'blkid:run "blkid" command with magic syntax.'
        'bluetoothctl:run "bluetoothctl" command with magic syntax.'
        'cbt:run "cbt" command with magic syntax.'
        'certbot:run "certbot" command with magic syntax.'
        'chage:run "chage" command with magic syntax.'
        'cksum:run "cksum" command with magic syntax.'
        'crontab:run "crontab" command with magic syntax.'
        'curl:run "curl" command with magic syntax.'
        'date:run "date" command with magic syntax.'
        'debconf-show:run "debconf-show" command with magic syntax.'
        'df:run "df" command with magic syntax.'
        'dig:run "dig" command with magic syntax.'
        'dmidecode:run "dmidecode" command with magic syntax.'
        'dpkg:run "dpkg" command with magic syntax.'
        'du:run "du" command with magic syntax.'
        'efibootmgr:run "efibootmgr" command with magic syntax.'
        'env:run "env" command with magic syntax.'
        'ethtool:run "ethtool" command with magic syntax.'
        'file:run "file" command with magic syntax.'
        'findmnt:run "findmnt" command with magic syntax.'
        'finger:run "finger" command with magic syntax.'
        'free:run "free" command with magic syntax.'
        'git:run "git" command with magic syntax.'
        'gpg:run "gpg" command with magic syntax.'
        'hciconfig:run "hciconfig" command with magic syntax.'
        'host:run "host" command with magic syntax.'
        'id:run "id" command with magic syntax.'
        'ifconfig:run "ifconfig" command with magic syntax.'
        'iostat:run "iostat" command with magic syntax.'
        'ip:run "ip" command with magic syntax.'
        'iptables:run "iptables" command with magic syntax.'
        'iw:run "iw" command with magic syntax.'
        'iwconfig:run "iwconfig" command with magic syntax.'
        'jobs:run "jobs" command with magic syntax.'
        'last:run "last" command with magic syntax.'
        'lastb:run "lastb" command with magic syntax.'
        'ls:run "ls" command with magic syntax.'
        'lsattr:run "lsattr" command with magic syntax.'
        'lsb_release:run "lsb_release" command with magic syntax.'
        'lsblk:run "lsblk" command with magic syntax.'
        'lsmod:run "lsmod" command with magic syntax.'
        'lsof:run "lsof" command with magic syntax.'
        'lspci:run "lspci" command with magic syntax.'
        'lsusb:run "lsusb" command with magic syntax.'
        'md5:run "md5" command with magic syntax.'
        'md5sum:run "md5sum" command with magic syntax.'
        'mdadm:run "mdadm" command with magic syntax.'
        'mount:run "mount" command with magic syntax.'
        'mpstat:run "mpstat" command with magic syntax.'
        'needrestart:run "needrestart" command with magic syntax.'
        'netstat:run "netstat" command with magic syntax.'
        'nmcli:run "nmcli" command with magic syntax.'
        'nsd-control:run "nsd-control" command with magic syntax.'
        'ntpq:run "ntpq" command with magic syntax.'
        'os-prober:run "os-prober" command with magic syntax.'
        'pidstat:run "pidstat" command with magic syntax.'
        'ping:run "ping" command with magic syntax.'
        'ping6:run "ping6" command with magic syntax.'
        'pip:run "pip" command with magic syntax.'
        'pip3:run "pip3" command with magic syntax.'
        'postconf:run "postconf" command with magic syntax.'
        'printenv:run "printenv" command with magic syntax.'
        'ps:run "ps" command with magic syntax.'
        'route:run "route" command with magic syntax.'
        'rpm:run "rpm" command with magic syntax.'
        'rsync:run "rsync" command with magic syntax.'
        'sfdisk:run "sfdisk" command with magic syntax.'
        'sha1sum:run "sha1sum" command with magic syntax.'
        'sha224sum:run "sha224sum" command with magic syntax.'
        'sha256sum:run "sha256sum" command with magic syntax.'
        'sha384sum:run "sha384sum" command with magic syntax.'
        'sha512sum:run "sha512sum" command with magic syntax.'
        'shasum:run "shasum" command with magic syntax.'
        'ss:run "ss" command with magic syntax.'
        'ssh:run "ssh" command with magic syntax.'
        'sshd:run "sshd" command with magic syntax.'
        'stat:run "stat" command with magic syntax.'
        'sum:run "sum" command with magic syntax.'
        'swapon:run "swapon" command with magic syntax.'
        'sysctl:run "sysctl" command with magic syntax.'
        'systemctl:run "systemctl" command with magic syntax.'
        'systeminfo:run "systeminfo" command with magic syntax.'
        'timedatectl:run "timedatectl" command with magic syntax.'
        'top:run "top" command with magic syntax.'
        'tracepath:run "tracepath" command with magic syntax.'
        'tracepath6:run "tracepath6" command with magic syntax.'
        'traceroute:run "traceroute" command with magic syntax.'
        'traceroute6:run "traceroute6" command with magic syntax.'
        'tune2fs:run "tune2fs" command with magic syntax.'
        'udevadm:run "udevadm" command with magic syntax.'
        'ufw:run "ufw" command with magic syntax.'
        'uname:run "uname" command with magic syntax.'
        'update-alternatives:run "update-alternatives" command with magic syntax.'
        'upower:run "upower" command with magic syntax.'
        'uptime:run "uptime" command with magic syntax.'
        'vdir:run "vdir" command with magic syntax.'
        'veracrypt:run "veracrypt" command with magic syntax.'
        'vmstat:run "vmstat" command with magic syntax.'
        'w:run "w" command with magic syntax.'
        'wc:run "wc" command with magic syntax.'
        'who:run "who" command with magic syntax.'
        'xrandr:run "xrandr" command with magic syntax.'
        'zipinfo:run "zipinfo" command with magic syntax.'
        'zpool:run "zpool" command with magic syntax.'
    )
    jc_parsers=(--acpi --airport --airport-s --apt-cache-show --apt-get-sqq --arp --asciitable --asciitable-m --blkid --bluetoothctl --cbt --cef --cef-s --certbot --chage --cksum --clf --clf-s --crontab --crontab-u --csv --csv-s --curl-head --date --datetime-iso --debconf-show --df --dig --dir --dmidecode --dpkg-l --du --efibootmgr --email-address --env --ethtool --file --find --findmnt --finger --free --fstab --git-log --git-log-s --git-ls-remote --gpg --group --gshadow --hash --hashsum --hciconfig --history --host --hosts --http-headers --id --ifconfig --ini --ini-dup --iostat --iostat-s --ip-address --iptables --ip-route --iw-scan --iwconfig --jar-manifest --jobs --jwt --kv --kv-dup --last --ls --ls-s --lsattr --lsb-release --lsblk --lsmod --lsof --lspci --lsusb --m3u --mdadm --mount --mpstat --mpstat-s --needrestart --netstat --nmcli --nsd-control --ntpq --openvpn --os-prober --os-release --passwd --path --path-list --pci-ids --pgpass --pidstat --pidstat-s --ping --ping-s --pip-list --pip-show --pkg-index-apk --pkg-index-deb --plist --postconf --proc --proc-buddyinfo --proc-cmdline --proc-consoles --proc-cpuinfo --proc-crypto --proc-devices --proc-diskstats --proc-filesystems --proc-interrupts --proc-iomem --proc-ioports --proc-loadavg --proc-locks --proc-meminfo --proc-modules --proc-mtrr --proc-pagetypeinfo --proc-partitions --proc-slabinfo --proc-softirqs --proc-stat --proc-swaps --proc-uptime --proc-version --proc-vmallocinfo --proc-vmstat --proc-zoneinfo --proc-driver-rtc --proc-net-arp --proc-net-dev --proc-net-dev-mcast --proc-net-if-inet6 --proc-net-igmp --proc-net-igmp6 --proc-net-ipv6-route --proc-net-netlink --proc-net-netstat --proc-net-packet --proc-net-protocols --proc-net-route --proc-net-tcp --proc-net-unix --proc-pid-fdinfo --proc-pid-io --proc-pid-maps --proc-pid-mountinfo --proc-pid-numa-maps --proc-pid-smaps --proc-pid-stat --proc-pid-statm --proc-pid-status --ps --resolve-conf --route --rpm-qi --rsync --rsync-s --semver --sfdisk --shadow --srt --ss --ssh-conf --sshd-conf --stat --stat-s --swapon --sysctl --syslog --syslog-s --syslog-bsd --syslog-bsd-s --systemctl --systemctl-lj --systemctl-ls --systemctl-luf --systeminfo --time --timedatectl --timestamp --toml --top --top-s --tracepath --traceroute --tune2fs --udevadm --ufw --ufw-appinfo --uname --update-alt-gs --update-alt-q --upower --uptime --url --ver --veracrypt --vmstat --vmstat-s --w --wc --who --x509-cert --x509-csr --xml --xrandr --yaml --zipinfo --zpool-iostat --zpool-status)
    jc_parsers_describe=(
        '--acpi:`acpi` command parser'
        '--airport:`airport -I` command parser'
        '--airport-s:`airport -s` command parser'
        '--apt-cache-show:`apt-cache show` command parser'
        '--apt-get-sqq:`apt-get -sqq` command parser'
        '--arp:`arp` command parser'
        '--asciitable:ASCII and Unicode table parser'
        '--asciitable-m:multi-line ASCII and Unicode table parser'
        '--blkid:`blkid` command parser'
        '--bluetoothctl:`bluetoothctl` command parser'
        '--cbt:`cbt` (Google Bigtable) command parser'
        '--cef:CEF string parser'
        '--cef-s:CEF string streaming parser'
        '--certbot:`certbot` command parser'
        '--chage:`chage --list` command parser'
        '--cksum:`cksum` and `sum` command parser'
        '--clf:Common and Combined Log Format file parser'
        '--clf-s:Common and Combined Log Format file streaming parser'
        '--crontab:`crontab` command and file parser'
        '--crontab-u:`crontab` file parser with user support'
        '--csv:CSV file parser'
        '--csv-s:CSV file streaming parser'
        '--curl-head:`curl --head` command parser'
        '--date:`date` command parser'
        '--datetime-iso:ISO 8601 Datetime string parser'
        '--debconf-show:`debconf-show` command parser'
        '--df:`df` command parser'
        '--dig:`dig` command parser'
        '--dir:`dir` command parser'
        '--dmidecode:`dmidecode` command parser'
        '--dpkg-l:`dpkg -l` command parser'
        '--du:`du` command parser'
        '--efibootmgr:`efibootmgr` command parser'
        '--email-address:Email Address string parser'
        '--env:`env` command parser'
        '--ethtool:`ethtool` command parser'
        '--file:`file` command parser'
        '--find:`find` command parser'
        '--findmnt:`findmnt` command parser'
        '--finger:`finger` command parser'
        '--free:`free` command parser'
        '--fstab:`/etc/fstab` file parser'
        '--git-log:`git log` command parser'
        '--git-log-s:`git log` command streaming parser'
        '--git-ls-remote:`git ls-remote` command parser'
        '--gpg:`gpg --with-colons` command parser'
        '--group:`/etc/group` file parser'
        '--gshadow:`/etc/gshadow` file parser'
        '--hash:`hash` command parser'
        '--hashsum:hashsum command parser (`md5sum`, `shasum`, etc.)'
        '--hciconfig:`hciconfig` command parser'
        '--history:`history` command parser'
        '--host:`host` command parser'
        '--hosts:`/etc/hosts` file parser'
        '--http-headers:HTTP headers parser'
        '--id:`id` command parser'
        '--ifconfig:`ifconfig` command parser'
        '--ini:INI file parser'
        '--ini-dup:INI with duplicate key file parser'
        '--iostat:`iostat` command parser'
        '--iostat-s:`iostat` command streaming parser'
        '--ip-address:IPv4 and IPv6 Address string parser'
        '--iptables:`iptables` command parser'
        '--ip-route:`ip route` command parser'
        '--iw-scan:`iw dev [device] scan` command parser'
        '--iwconfig:`iwconfig` command parser'
        '--jar-manifest:Java MANIFEST.MF file parser'
        '--jobs:`jobs` command parser'
        '--jwt:JWT string parser'
        '--kv:Key/Value file and string parser'
        '--kv-dup:Key/Value with duplicate key file and string parser'
        '--last:`last` and `lastb` command parser'
        '--ls:`ls` command parser'
        '--ls-s:`ls` command streaming parser'
        '--lsattr:`lsattr` command parser'
        '--lsb-release:`lsb_release` command parser'
        '--lsblk:`lsblk` command parser'
        '--lsmod:`lsmod` command parser'
        '--lsof:`lsof` command parser'
        '--lspci:`lspci -mmv` command parser'
        '--lsusb:`lsusb` command parser'
        '--m3u:M3U and M3U8 file parser'
        '--mdadm:`mdadm` command parser'
        '--mount:`mount` command parser'
        '--mpstat:`mpstat` command parser'
        '--mpstat-s:`mpstat` command streaming parser'
        '--needrestart:`needrestart -b` command parser'
        '--netstat:`netstat` command parser'
        '--nmcli:`nmcli` command parser'
        '--nsd-control:`nsd-control` command parser'
        '--ntpq:`ntpq -p` command parser'
        '--openvpn:openvpn-status.log file parser'
        '--os-prober:`os-prober` command parser'
        '--os-release:`/etc/os-release` file parser'
        '--passwd:`/etc/passwd` file parser'
        '--path:POSIX path string parser'
        '--path-list:POSIX path list string parser'
        '--pci-ids:`pci.ids` file parser'
        '--pgpass:PostgreSQL password file parser'
        '--pidstat:`pidstat -H` command parser'
        '--pidstat-s:`pidstat -H` command streaming parser'
        '--ping:`ping` and `ping6` command parser'
        '--ping-s:`ping` and `ping6` command streaming parser'
        '--pip-list:`pip list` command parser'
        '--pip-show:`pip show` command parser'
        '--pkg-index-apk:Alpine Linux Package Index file parser'
        '--pkg-index-deb:Debian Package Index file parser'
        '--plist:PLIST file parser'
        '--postconf:`postconf -M` command parser'
        '--proc:`/proc/` file parser'
        '--proc-buddyinfo:`/proc/buddyinfo` file parser'
        '--proc-cmdline:`/proc/cmdline` file parser'
        '--proc-consoles:`/proc/consoles` file parser'
        '--proc-cpuinfo:`/proc/cpuinfo` file parser'
        '--proc-crypto:`/proc/crypto` file parser'
        '--proc-devices:`/proc/devices` file parser'
        '--proc-diskstats:`/proc/diskstats` file parser'
        '--proc-filesystems:`/proc/filesystems` file parser'
        '--proc-interrupts:`/proc/interrupts` file parser'
        '--proc-iomem:`/proc/iomem` file parser'
        '--proc-ioports:`/proc/ioports` file parser'
        '--proc-loadavg:`/proc/loadavg` file parser'
        '--proc-locks:`/proc/locks` file parser'
        '--proc-meminfo:`/proc/meminfo` file parser'
        '--proc-modules:`/proc/modules` file parser'
        '--proc-mtrr:`/proc/mtrr` file parser'
        '--proc-pagetypeinfo:`/proc/pagetypeinfo` file parser'
        '--proc-partitions:`/proc/partitions` file parser'
        '--proc-slabinfo:`/proc/slabinfo` file parser'
        '--proc-softirqs:`/proc/softirqs` file parser'
        '--proc-stat:`/proc/stat` file parser'
        '--proc-swaps:`/proc/swaps` file parser'
        '--proc-uptime:`/proc/uptime` file parser'
        '--proc-version:`/proc/version` file parser'
        '--proc-vmallocinfo:`/proc/vmallocinfo` file parser'
        '--proc-vmstat:`/proc/vmstat` file parser'
        '--proc-zoneinfo:`/proc/zoneinfo` file parser'
        '--proc-driver-rtc:`/proc/driver/rtc` file parser'
        '--proc-net-arp:`/proc/net/arp` file parser'
        '--proc-net-dev:`/proc/net/dev` file parser'
        '--proc-net-dev-mcast:`/proc/net/dev_mcast` file parser'
        '--proc-net-if-inet6:`/proc/net/if_inet6` file parser'
        '--proc-net-igmp:`/proc/net/igmp` file parser'
        '--proc-net-igmp6:`/proc/net/igmp6` file parser'
        '--proc-net-ipv6-route:`/proc/net/ipv6_route` file parser'
        '--proc-net-netlink:`/proc/net/netlink` file parser'
        '--proc-net-netstat:`/proc/net/netstat` file parser'
        '--proc-net-packet:`/proc/net/packet` file parser'
        '--proc-net-protocols:`/proc/net/protocols` file parser'
        '--proc-net-route:`/proc/net/route` file parser'
        '--proc-net-tcp:`/proc/net/tcp` and `/proc/net/tcp6` file parser'
        '--proc-net-unix:`/proc/net/unix` file parser'
        '--proc-pid-fdinfo:`/proc/<pid>/fdinfo/<fd>` file parser'
        '--proc-pid-io:`/proc/<pid>/io` file parser'
        '--proc-pid-maps:`/proc/<pid>/maps` file parser'
        '--proc-pid-mountinfo:`/proc/<pid>/mountinfo` file parser'
        '--proc-pid-numa-maps:`/proc/<pid>/numa_maps` file parser'
        '--proc-pid-smaps:`/proc/<pid>/smaps` file parser'
        '--proc-pid-stat:`/proc/<pid>/stat` file parser'
        '--proc-pid-statm:`/proc/<pid>/statm` file parser'
        '--proc-pid-status:`/proc/<pid>/status` file parser'
        '--ps:`ps` command parser'
        '--resolve-conf:`/etc/resolve.conf` file parser'
        '--route:`route` command parser'
        '--rpm-qi:`rpm -qi` command parser'
        '--rsync:`rsync` command parser'
        '--rsync-s:`rsync` command streaming parser'
        '--semver:Semantic Version string parser'
        '--sfdisk:`sfdisk` command parser'
        '--shadow:`/etc/shadow` file parser'
        '--srt:SRT file parser'
        '--ss:`ss` command parser'
        '--ssh-conf:`ssh` config file and `ssh -G` command parser'
        '--sshd-conf:`sshd` config file and `sshd -T` command parser'
        '--stat:`stat` command parser'
        '--stat-s:`stat` command streaming parser'
        '--swapon:`swapon` command parser'
        '--sysctl:`sysctl` command parser'
        '--syslog:Syslog RFC 5424 string parser'
        '--syslog-s:Syslog RFC 5424 string streaming parser'
        '--syslog-bsd:Syslog RFC 3164 string parser'
        '--syslog-bsd-s:Syslog RFC 3164 string streaming parser'
        '--systemctl:`systemctl` command parser'
        '--systemctl-lj:`systemctl list-jobs` command parser'
        '--systemctl-ls:`systemctl list-sockets` command parser'
        '--systemctl-luf:`systemctl list-unit-files` command parser'
        '--systeminfo:`systeminfo` command parser'
        '--time:`/usr/bin/time` command parser'
        '--timedatectl:`timedatectl status` command parser'
        '--timestamp:Unix Epoch Timestamp string parser'
        '--toml:TOML file parser'
        '--top:`top -b` command parser'
        '--top-s:`top -b` command streaming parser'
        '--tracepath:`tracepath` and `tracepath6` command parser'
        '--traceroute:`traceroute` and `traceroute6` command parser'
        '--tune2fs:`tune2fs -l` command parser'
        '--udevadm:`udevadm info` command parser'
        '--ufw:`ufw status` command parser'
        '--ufw-appinfo:`ufw app info [application]` command parser'
        '--uname:`uname -a` command parser'
        '--update-alt-gs:`update-alternatives --get-selections` command parser'
        '--update-alt-q:`update-alternatives --query` command parser'
        '--upower:`upower` command parser'
        '--uptime:`uptime` command parser'
        '--url:URL string parser'
        '--ver:Version string parser'
        '--veracrypt:`veracrypt` command parser'
        '--vmstat:`vmstat` command parser'
        '--vmstat-s:`vmstat` command streaming parser'
        '--w:`w` command parser'
        '--wc:`wc` command parser'
        '--who:`who` command parser'
        '--x509-cert:X.509 PEM and DER certificate file parser'
        '--x509-csr:X.509 PEM and DER certificate request file parser'
        '--xml:XML file parser'
        '--xrandr:`xrandr` command parser'
        '--yaml:YAML file parser'
        '--zipinfo:`zipinfo` command parser'
        '--zpool-iostat:`zpool iostat` command parser'
        '--zpool-status:`zpool status` command parser'
    )
    jc_options=(--force-color -C --debug -d --monochrome -m --meta-out -M --pretty -p --quiet -q --raw -r --slurp -s --unbuffer -u --yaml-out -y)
    jc_options_describe=(
        '--force-color:force color output (overrides -m)'
        '-C:force color output (overrides -m)'
        '--debug:debug (double for verbose debug)'
        '-d:debug (double for verbose debug)'
        '--monochrome:monochrome output'
        '-m:monochrome output'
        '--meta-out:add metadata to output including timestamp, etc.'
        '-M:add metadata to output including timestamp, etc.'
        '--pretty:pretty print output'
        '-p:pretty print output'
        '--quiet:suppress warnings (double to ignore streaming errors)'
        '-q:suppress warnings (double to ignore streaming errors)'
        '--raw:raw output'
        '-r:raw output'
        '--slurp:slurp multiple lines into an array'
        '-s:slurp multiple lines into an array'
        '--unbuffer:unbuffer output'
        '-u:unbuffer output'
        '--yaml-out:YAML output'
        '-y:YAML output'
    )
    jc_about_options=(--about -a)
    jc_about_options_describe=(
        '--about:about jc'
        '-a:about jc'
    )
    jc_about_mod_options=(--pretty -p --yaml-out -y --monochrome -m --force-color -C)
    jc_about_mod_options_describe=(
        '--pretty:pretty print output'
        '-p:pretty print output'
        '--yaml-out:YAML output'
        '-y:YAML output'
        '--monochrome:monochrome output'
        '-m:monochrome output'
        '--force-color:force color output (overrides -m)'
        '-C:force color output (overrides -m)'
    )
    jc_help_options=(--help -h)
    jc_help_options_describe=(
        '--help:help (--help --parser_name for parser documentation)'
        '-h:help (--help --parser_name for parser documentation)'
    )
    jc_special_options=(--version -v --bash-comp -B --zsh-comp -Z)
    jc_special_options_describe=(
        '--version:version info'
        '-v:version info'
        '--bash-comp:gen Bash completion: jc -B > /etc/bash_completion.d/jc'
        '-B:gen Bash completion: jc -B > /etc/bash_completion.d/jc'
        '--zsh-comp:gen Zsh completion: jc -Z > "${fpath[1]}/_jc"'
        '-Z:gen Zsh completion: jc -Z > "${fpath[1]}/_jc"'
    )

    # if jc_about_options are found anywhere in the line, then only complete from jc_about_mod_options
    for i in ${words:0:-1}; do
        if (( $jc_about_options[(Ie)${i}] )); then
            _describe 'commands' jc_about_mod_options_describe
            return 0
        fi
    done

    # if jc_help_options and a parser are found anywhere in the line, then no more completions
     if
        (
            for i in ${words:0:-1}; do
                if (( $jc_help_options[(Ie)${i}] )); then
                    return 0
                fi
            done
            return 1
        ) && (
            for i in ${words:0:-1}; do
                if (( $jc_parsers[(Ie)${i}] )); then
                    return 0
                fi
            done
            return 1
        ); then
        return 0
    fi

    # if jc_help_options are found anywhere in the line, then only complete with parsers
    for i in ${words:0:-1}; do
        if (( $jc_help_options[(Ie)${i}] )); then
            _describe 'commands' jc_parsers_describe
            return 0
        fi
    done

    # if special options are found anywhere in the line, then no more completions
    for i in ${words:0:-1}; do
        if (( $jc_special_options[(Ie)${i}] )); then
            return 0
        fi
    done

    # if magic command is found anywhere in the line, use called command's autocompletion
    for i in ${words:0:-1}; do
        if (( $jc_commands[(Ie)${i}] )); then
            # hack to remove options between jc and the magic command
            shift $(( ${#words} - 2 )) words
            words[1,0]=(jc)
            CURRENT=${#words}

            # run the magic command's completions
            _arguments '*::arguments:_normal'
            return 0
        fi
    done

    # if "/pr[oc]" (magic for Procfile parsers) is in the current word, complete with files/directories in the path
    if [[ "${words[-1]}" =~ "/pr" ]]; then
        # run files completion
        _files
        return 0
    fi

    # if a parser arg is found anywhere in the line, only show options and help options
    for i in ${words:0:-1}; do
        if (( $jc_parsers[(Ie)${i}] )); then
            _describe 'commands' jc_options_describe -- jc_help_options_describe
            return 0
        fi
    done

    # default completion
    _describe 'commands' jc_options_describe -- jc_about_options_describe -- jc_help_options_describe -- jc_special_options_describe -- jc_parsers_describe -- jc_commands_describe
}

_jc

