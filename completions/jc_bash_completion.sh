_jc()
{
    local cur prev words cword jc_commands jc_parsers jc_options \
          jc_about_options jc_about_mod_options jc_help_options jc_special_options

    jc_commands=(acpi airport arp blkid bluetoothctl cbt certbot chage cksum crontab date df dig dmidecode dpkg du env file findmnt finger free git gpg hciconfig id ifconfig iostat iptables iw iwconfig jobs last lastb ls lsattr lsblk lsmod lsof lspci lsusb md5 md5sum mdadm mount mpstat netstat nmcli ntpq os-prober pidstat ping ping6 pip pip3 postconf printenv ps route rpm rsync sfdisk sha1sum sha224sum sha256sum sha384sum sha512sum shasum ss ssh sshd stat sum sysctl systemctl systeminfo timedatectl top tracepath tracepath6 traceroute traceroute6 udevadm ufw uname update-alternatives upower uptime vdir veracrypt vmstat w wc who xrandr zipinfo zpool)
    jc_parsers=(--acpi --airport --airport-s --arp --asciitable --asciitable-m --blkid --bluetoothctl --cbt --cef --cef-s --certbot --chage --cksum --clf --clf-s --crontab --crontab-u --csv --csv-s --date --datetime-iso --df --dig --dir --dmidecode --dpkg-l --du --email-address --env --file --findmnt --finger --free --fstab --git-log --git-log-s --git-ls-remote --gpg --group --gshadow --hash --hashsum --hciconfig --history --hosts --id --ifconfig --ini --ini-dup --iostat --iostat-s --ip-address --iptables --iw-scan --iwconfig --jar-manifest --jobs --jwt --kv --last --ls --ls-s --lsattr --lsblk --lsmod --lsof --lspci --lsusb --m3u --mdadm --mount --mpstat --mpstat-s --netstat --nmcli --ntpq --openvpn --os-prober --passwd --pci-ids --pgpass --pidstat --pidstat-s --ping --ping-s --pip-list --pip-show --plist --postconf --proc --proc-buddyinfo --proc-consoles --proc-cpuinfo --proc-crypto --proc-devices --proc-diskstats --proc-filesystems --proc-interrupts --proc-iomem --proc-ioports --proc-loadavg --proc-locks --proc-meminfo --proc-modules --proc-mtrr --proc-pagetypeinfo --proc-partitions --proc-slabinfo --proc-softirqs --proc-stat --proc-swaps --proc-uptime --proc-version --proc-vmallocinfo --proc-vmstat --proc-zoneinfo --proc-driver-rtc --proc-net-arp --proc-net-dev --proc-net-dev-mcast --proc-net-if-inet6 --proc-net-igmp --proc-net-igmp6 --proc-net-ipv6-route --proc-net-netlink --proc-net-netstat --proc-net-packet --proc-net-protocols --proc-net-route --proc-net-unix --proc-pid-fdinfo --proc-pid-io --proc-pid-maps --proc-pid-mountinfo --proc-pid-numa-maps --proc-pid-smaps --proc-pid-stat --proc-pid-statm --proc-pid-status --ps --route --rpm-qi --rsync --rsync-s --semver --sfdisk --shadow --srt --ss --ssh-conf --sshd-conf --stat --stat-s --sysctl --syslog --syslog-s --syslog-bsd --syslog-bsd-s --systemctl --systemctl-lj --systemctl-ls --systemctl-luf --systeminfo --time --timedatectl --timestamp --toml --top --top-s --tracepath --traceroute --udevadm --ufw --ufw-appinfo --uname --update-alt-gs --update-alt-q --upower --uptime --url --ver --veracrypt --vmstat --vmstat-s --w --wc --who --x509-cert --x509-csr --xml --xrandr --yaml --zipinfo --zpool-iostat --zpool-status)
    jc_options=(--force-color -C --debug -d --monochrome -m --meta-out -M --pretty -p --quiet -q --raw -r --unbuffer -u --yaml-out -y)
    jc_about_options=(--about -a)
    jc_about_mod_options=(--pretty -p --yaml-out -y --monochrome -m --force-color -C)
    jc_help_options=(--help -h)
    jc_special_options=(--version -v --bash-comp -B --zsh-comp -Z)

    COMPREPLY=()
    _get_comp_words_by_ref cur prev words cword

    # if jc_about_options are found anywhere in the line, then only complete from jc_about_mod_options
    for i in "${words[@]::${#words[@]}-1}"; do
        if [[ " ${jc_about_options[*]} " =~ " ${i} " ]]; then
            COMPREPLY=( $( compgen -W "${jc_about_mod_options[*]}" \
            -- "${cur}" ) )
            return 0
        fi
    done

    # if jc_help_options and a parser are found anywhere in the line, then no more completions
    if
        (
            for i in "${words[@]::${#words[@]}-1}"; do
                if [[ " ${jc_help_options[*]} " =~ " ${i} " ]]; then
                    return 0
                fi
            done
            return 1
        ) && (
            for i in "${words[@]::${#words[@]}-1}"; do
                if [[ " ${jc_parsers[*]} " =~ " ${i} " ]]; then
                    return 0
                fi
            done
            return 1
        ); then
        return 0
    fi

    # if jc_help_options are found anywhere in the line, then only complete with parsers
    for i in "${words[@]::${#words[@]}-1}"; do
        if [[ " ${jc_help_options[*]} " =~ " ${i} " ]]; then
            COMPREPLY=( $( compgen -W "${jc_parsers[*]}" \
            -- "${cur}" ) )
            return 0
        fi
    done

    # if special options are found anywhere in the line, then no more completions
    for i in "${words[@]::${#words[@]}-1}"; do
        if [[ " ${jc_special_options[*]} " =~ " ${i} " ]]; then
            return 0
        fi
    done

    # if magic command is found anywhere in the line, use called command's autocompletion
    for i in "${words[@]::${#words[@]}-1}"; do
        if [[ " ${jc_commands[*]} " =~ " ${i} " ]]; then
            _command
            return 0
        fi
    done

    # if "/pr[oc]" (magic for Procfile parsers) is in the current word, complete with files/directories in the path
    if [[ "${cur}" =~ "/pr" ]]; then
        _filedir
        return 0
    fi

    # if a parser arg is found anywhere in the line, only show options and help options
    for i in "${words[@]::${#words[@]}-1}"; do
        if [[ " ${jc_parsers[*]} " =~ " ${i} " ]]; then
            COMPREPLY=( $( compgen -W "${jc_options[*]} ${jc_help_options[*]}" \
            -- "${cur}" ) )
            return 0
        fi
    done

    # default completion
    COMPREPLY=( $( compgen -W "${jc_options[*]} ${jc_about_options[*]} ${jc_help_options[*]} ${jc_special_options[*]} ${jc_parsers[*]} ${jc_commands[*]}" \
        -- "${cur}" ) )
} &&
complete -F _jc jc

