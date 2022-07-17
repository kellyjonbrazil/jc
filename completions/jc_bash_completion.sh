_jc()
{
    local cur prev words cword jc_commands jc_parsers jc_options \
          jc_about_options jc_about_mod_options jc_help_options jc_special_options

    jc_commands=(acpi airport arp blkid chage cksum crontab date df dig dmidecode dpkg du env file finger free git gpg hciconfig id ifconfig iostat iptables iw jobs last lastb ls lsblk lsmod lsof lsusb md5 md5sum mount mpstat netstat nmcli ntpq pidstat ping ping6 pip pip3 postconf printenv ps route rpm rsync sfdisk sha1sum sha224sum sha256sum sha384sum sha512sum shasum ss stat sum sysctl systemctl systeminfo timedatectl top tracepath tracepath6 traceroute traceroute6 ufw uname update-alternatives upower uptime vdir vmstat w wc who xrandr zipinfo)
    jc_parsers=(--acpi --airport --airport-s --arp --asciitable --asciitable-m --blkid --chage --cksum --crontab --crontab-u --csv --csv-s --date --df --dig --dir --dmidecode --dpkg-l --du --env --file --finger --free --fstab --git-log --git-log-s --gpg --group --gshadow --hash --hashsum --hciconfig --history --hosts --id --ifconfig --ini --iostat --iostat-s --iptables --iw-scan --jar-manifest --jobs --kv --last --ls --ls-s --lsblk --lsmod --lsof --lsusb --m3u --mount --mpstat --mpstat-s --netstat --nmcli --ntpq --passwd --pidstat --pidstat-s --ping --ping-s --pip-list --pip-show --postconf --ps --route --rpm-qi --rsync --rsync-s --sfdisk --shadow --ss --stat --stat-s --sysctl --systemctl --systemctl-lj --systemctl-ls --systemctl-luf --systeminfo --time --timedatectl --top --top-s --tracepath --traceroute --ufw --ufw-appinfo --uname --update-alt-gs --update-alt-q --upower --uptime --vmstat --vmstat-s --w --wc --who --x509-cert --xml --xrandr --yaml --zipinfo)
    jc_options=(--force-color -C --debug -d --monochrome -m --pretty -p --quiet -q --raw -r --unbuffer -u --yaml-out -y)
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

