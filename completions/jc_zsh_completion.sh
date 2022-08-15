#compdef jc

_jc() {
    local -a jc_commands jc_commands_describe \
             jc_parsers jc_parsers_describe \
             jc_options jc_options_describe \
             jc_about_options jc_about_options_describe \
             jc_about_mod_options jc_about_mod_options_describe \
             jc_help_options jc_help_options_describe \
             jc_special_options jc_special_options_describe

    jc_commands=(acpi airport arp blkid chage cksum crontab date df dig dmidecode dpkg du env file finger free git gpg hciconfig id ifconfig iostat iptables iw jobs last lastb ls lsblk lsmod lsof lsusb md5 md5sum mdadm mount mpstat netstat nmcli ntpq pidstat ping ping6 pip pip3 postconf printenv ps route rpm rsync sfdisk sha1sum sha224sum sha256sum sha384sum sha512sum shasum ss stat sum sysctl systemctl systeminfo timedatectl top tracepath tracepath6 traceroute traceroute6 ufw uname update-alternatives upower uptime vdir vmstat w wc who xrandr zipinfo)
    jc_commands_describe=(
        'acpi:run "acpi" command with magic syntax.'
        'airport:run "airport" command with magic syntax.'
        'arp:run "arp" command with magic syntax.'
        'blkid:run "blkid" command with magic syntax.'
        'chage:run "chage" command with magic syntax.'
        'cksum:run "cksum" command with magic syntax.'
        'crontab:run "crontab" command with magic syntax.'
        'date:run "date" command with magic syntax.'
        'df:run "df" command with magic syntax.'
        'dig:run "dig" command with magic syntax.'
        'dmidecode:run "dmidecode" command with magic syntax.'
        'dpkg:run "dpkg" command with magic syntax.'
        'du:run "du" command with magic syntax.'
        'env:run "env" command with magic syntax.'
        'file:run "file" command with magic syntax.'
        'finger:run "finger" command with magic syntax.'
        'free:run "free" command with magic syntax.'
        'git:run "git" command with magic syntax.'
        'gpg:run "gpg" command with magic syntax.'
        'hciconfig:run "hciconfig" command with magic syntax.'
        'id:run "id" command with magic syntax.'
        'ifconfig:run "ifconfig" command with magic syntax.'
        'iostat:run "iostat" command with magic syntax.'
        'iptables:run "iptables" command with magic syntax.'
        'iw:run "iw" command with magic syntax.'
        'jobs:run "jobs" command with magic syntax.'
        'last:run "last" command with magic syntax.'
        'lastb:run "lastb" command with magic syntax.'
        'ls:run "ls" command with magic syntax.'
        'lsblk:run "lsblk" command with magic syntax.'
        'lsmod:run "lsmod" command with magic syntax.'
        'lsof:run "lsof" command with magic syntax.'
        'lsusb:run "lsusb" command with magic syntax.'
        'md5:run "md5" command with magic syntax.'
        'md5sum:run "md5sum" command with magic syntax.'
        'mdadm:run "mdadm" command with magic syntax.'
        'mount:run "mount" command with magic syntax.'
        'mpstat:run "mpstat" command with magic syntax.'
        'netstat:run "netstat" command with magic syntax.'
        'nmcli:run "nmcli" command with magic syntax.'
        'ntpq:run "ntpq" command with magic syntax.'
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
        'stat:run "stat" command with magic syntax.'
        'sum:run "sum" command with magic syntax.'
        'sysctl:run "sysctl" command with magic syntax.'
        'systemctl:run "systemctl" command with magic syntax.'
        'systeminfo:run "systeminfo" command with magic syntax.'
        'timedatectl:run "timedatectl" command with magic syntax.'
        'top:run "top" command with magic syntax.'
        'tracepath:run "tracepath" command with magic syntax.'
        'tracepath6:run "tracepath6" command with magic syntax.'
        'traceroute:run "traceroute" command with magic syntax.'
        'traceroute6:run "traceroute6" command with magic syntax.'
        'ufw:run "ufw" command with magic syntax.'
        'uname:run "uname" command with magic syntax.'
        'update-alternatives:run "update-alternatives" command with magic syntax.'
        'upower:run "upower" command with magic syntax.'
        'uptime:run "uptime" command with magic syntax.'
        'vdir:run "vdir" command with magic syntax.'
        'vmstat:run "vmstat" command with magic syntax.'
        'w:run "w" command with magic syntax.'
        'wc:run "wc" command with magic syntax.'
        'who:run "who" command with magic syntax.'
        'xrandr:run "xrandr" command with magic syntax.'
        'zipinfo:run "zipinfo" command with magic syntax.'
    )
    jc_parsers=(--acpi --airport --airport-s --arp --asciitable --asciitable-m --blkid --cef --chage --cksum --crontab --crontab-u --csv --csv-s --date --df --dig --dir --dmidecode --dpkg-l --du --email-address --env --file --finger --free --fstab --git-log --git-log-s --gpg --group --gshadow --hash --hashsum --hciconfig --history --hosts --id --ifconfig --ini --iostat --iostat-s --ip-address --iptables --iso-datetime --iw-scan --jar-manifest --jobs --jwt --kv --last --ls --ls-s --lsblk --lsmod --lsof --lsusb --m3u --mdadm --mount --mpstat --mpstat-s --netstat --nmcli --ntpq --passwd --pidstat --pidstat-s --ping --ping-s --pip-list --pip-show --plist --postconf --ps --route --rpm-qi --rsync --rsync-s --sfdisk --shadow --ss --stat --stat-s --sysctl --syslog-bsd --syslog --systemctl --systemctl-lj --systemctl-ls --systemctl-luf --systeminfo --time --timedatectl --timestamp --top --top-s --tracepath --traceroute --ufw --ufw-appinfo --uname --update-alt-gs --update-alt-q --upower --uptime --url --vmstat --vmstat-s --w --wc --who --x509-cert --xml --xrandr --yaml --zipinfo)
    jc_parsers_describe=(
        '--acpi:`acpi` command parser'
        '--airport:`airport -I` command parser'
        '--airport-s:`airport -s` command parser'
        '--arp:`arp` command parser'
        '--asciitable:ASCII and Unicode table parser'
        '--asciitable-m:multi-line ASCII and Unicode table parser'
        '--blkid:`blkid` command parser'
        '--cef:CEF string parser'
        '--chage:`chage --list` command parser'
        '--cksum:`cksum` and `sum` command parser'
        '--crontab:`crontab` command and file parser'
        '--crontab-u:`crontab` file parser with user support'
        '--csv:CSV file parser'
        '--csv-s:CSV file streaming parser'
        '--date:`date` command parser'
        '--df:`df` command parser'
        '--dig:`dig` command parser'
        '--dir:`dir` command parser'
        '--dmidecode:`dmidecode` command parser'
        '--dpkg-l:`dpkg -l` command parser'
        '--du:`du` command parser'
        '--email-address:Email Address string parser'
        '--env:`env` command parser'
        '--file:`file` command parser'
        '--finger:`finger` command parser'
        '--free:`free` command parser'
        '--fstab:`/etc/fstab` file parser'
        '--git-log:`git log` command parser'
        '--git-log-s:`git log` command streaming parser'
        '--gpg:`gpg --with-colons` command parser'
        '--group:`/etc/group` file parser'
        '--gshadow:`/etc/gshadow` file parser'
        '--hash:`hash` command parser'
        '--hashsum:hashsum command parser (`md5sum`, `shasum`, etc.)'
        '--hciconfig:`hciconfig` command parser'
        '--history:`history` command parser'
        '--hosts:`/etc/hosts` file parser'
        '--id:`id` command parser'
        '--ifconfig:`ifconfig` command parser'
        '--ini:INI file parser'
        '--iostat:`iostat` command parser'
        '--iostat-s:`iostat` command streaming parser'
        '--ip-address:IPv4 and IPv6 Address string parser'
        '--iptables:`iptables` command parser'
        '--iso-datetime:ISO 8601 Datetime string parser'
        '--iw-scan:`iw dev [device] scan` command parser'
        '--jar-manifest:Java MANIFEST.MF file parser'
        '--jobs:`jobs` command parser'
        '--jwt:JWT string parser'
        '--kv:Key/Value file parser'
        '--last:`last` and `lastb` command parser'
        '--ls:`ls` command parser'
        '--ls-s:`ls` command streaming parser'
        '--lsblk:`lsblk` command parser'
        '--lsmod:`lsmod` command parser'
        '--lsof:`lsof` command parser'
        '--lsusb:`lsusb` command parser'
        '--m3u:M3U and M3U8 file parser'
        '--mdadm:`mdadm` command parser'
        '--mount:`mount` command parser'
        '--mpstat:`mpstat` command parser'
        '--mpstat-s:`mpstat` command streaming parser'
        '--netstat:`netstat` command parser'
        '--nmcli:`nmcli` command parser'
        '--ntpq:`ntpq -p` command parser'
        '--passwd:`/etc/passwd` file parser'
        '--pidstat:`pidstat -h` command parser'
        '--pidstat-s:`pidstat -h` command streaming parser'
        '--ping:`ping` and `ping6` command parser'
        '--ping-s:`ping` and `ping6` command streaming parser'
        '--pip-list:`pip list` command parser'
        '--pip-show:`pip show` command parser'
        '--plist:PLIST file parser'
        '--postconf:`postconf -M` command parser'
        '--ps:`ps` command parser'
        '--route:`route` command parser'
        '--rpm-qi:`rpm -qi` command parser'
        '--rsync:`rsync` command parser'
        '--rsync-s:`rsync` command streaming parser'
        '--sfdisk:`sfdisk` command parser'
        '--shadow:`/etc/shadow` file parser'
        '--ss:`ss` command parser'
        '--stat:`stat` command parser'
        '--stat-s:`stat` command streaming parser'
        '--sysctl:`sysctl` command parser'
        '--syslog-bsd:Syslog RFC 3164 string parser'
        '--syslog:Syslog RFC 5424 string parser'
        '--systemctl:`systemctl` command parser'
        '--systemctl-lj:`systemctl list-jobs` command parser'
        '--systemctl-ls:`systemctl list-sockets` command parser'
        '--systemctl-luf:`systemctl list-unit-files` command parser'
        '--systeminfo:`systeminfo` command parser'
        '--time:`/usr/bin/time` command parser'
        '--timedatectl:`timedatectl status` command parser'
        '--timestamp:Unix Epoch Timestamp string parser'
        '--top:`top -b` command parser'
        '--top-s:`top -b` command streaming parser'
        '--tracepath:`tracepath` and `tracepath6` command parser'
        '--traceroute:`traceroute` and `traceroute6` command parser'
        '--ufw:`ufw status` command parser'
        '--ufw-appinfo:`ufw app info [application]` command parser'
        '--uname:`uname -a` command parser'
        '--update-alt-gs:`update-alternatives --get-selections` command parser'
        '--update-alt-q:`update-alternatives --query` command parser'
        '--upower:`upower` command parser'
        '--uptime:`uptime` command parser'
        '--url:URL string parser'
        '--vmstat:`vmstat` command parser'
        '--vmstat-s:`vmstat` command streaming parser'
        '--w:`w` command parser'
        '--wc:`wc` command parser'
        '--who:`who` command parser'
        '--x509-cert:X.509 PEM and DER certificate file parser'
        '--xml:XML file parser'
        '--xrandr:`xrandr` command parser'
        '--yaml:YAML file parser'
        '--zipinfo:`zipinfo` command parser'
    )
    jc_options=(--force-color -C --debug -d --monochrome -m --pretty -p --quiet -q --raw -r --time-out -t --unbuffer -u --yaml-out -y)
    jc_options_describe=(
        '--force-color:force color output even when using pipes (overrides -m)'
        '-C:force color output even when using pipes (overrides -m)'
        '--debug:debug (double for verbose debug)'
        '-d:debug (double for verbose debug)'
        '--monochrome:monochrome output'
        '-m:monochrome output'
        '--pretty:pretty print output'
        '-p:pretty print output'
        '--quiet:suppress warnings (double to ignore streaming errors)'
        '-q:suppress warnings (double to ignore streaming errors)'
        '--raw:raw output'
        '-r:raw output'
        '--time-out:add UTC Unix timestamp information to output'
        '-t:add UTC Unix timestamp information to output'
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
        '--force-color:force color output even when using pipes (overrides -m)'
        '-C:force color output even when using pipes (overrides -m)'
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

