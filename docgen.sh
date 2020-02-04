#!/bin/bash
# Generate docs.md

cd jc
pydocmd simple jc+ > ../docs/readme.md
pydocmd simple utils+ > ../docs/utils.md
pydocmd simple jc.parsers.arp+ > ../docs/parsers/arp.md
pydocmd simple jc.parsers.crontab+ > ../docs/parsers/crontab.md
pydocmd simple jc.parsers.df+ > ../docs/parsers/df.md
pydocmd simple jc.parsers.dig+ > ../docs/parsers/dig.md
pydocmd simple jc.parsers.du+ > ../docs/parsers/du.md
pydocmd simple jc.parsers.env+ > ../docs/parsers/env.md
pydocmd simple jc.parsers.free+ > ../docs/parsers/free.md
pydocmd simple jc.parsers.fstab+ > ../docs/parsers/fstab.md
pydocmd simple jc.parsers.history+ > ../docs/parsers/history.md
pydocmd simple jc.parsers.hosts+ > ../docs/parsers/hosts.md
pydocmd simple jc.parsers.ifconfig+ > ../docs/parsers/ifconfig.md
pydocmd simple jc.parsers.ini+ > ../docs/parsers/ini.md
pydocmd simple jc.parsers.iptables+ > ../docs/parsers/iptables.md
pydocmd simple jc.parsers.jobs+ > ../docs/parsers/jobs.md
pydocmd simple jc.parsers.ls+ > ../docs/parsers/ls.md
pydocmd simple jc.parsers.lsblk+ > ../docs/parsers/lsblk.md
pydocmd simple jc.parsers.lsmod+ > ../docs/parsers/lsmod.md
pydocmd simple jc.parsers.lsof+ > ../docs/parsers/lsof.md
pydocmd simple jc.parsers.mount+ > ../docs/parsers/mount.md
pydocmd simple jc.parsers.netstat+ > ../docs/parsers/netstat.md
pydocmd simple jc.parsers.pip_list+ > ../docs/parsers/pip_list.md
pydocmd simple jc.parsers.pip_show+ > ../docs/parsers/pip_show.md
pydocmd simple jc.parsers.ps+ > ../docs/parsers/ps.md
pydocmd simple jc.parsers.route+ > ../docs/parsers/route.md
pydocmd simple jc.parsers.ss+ > ../docs/parsers/ss.md
pydocmd simple jc.parsers.stat+ > ../docs/parsers/stat.md
pydocmd simple jc.parsers.systemctl+ > ../docs/parsers/systemctl.md
pydocmd simple jc.parsers.systemctl_lj+ > ../docs/parsers/systemctl_lj.md
pydocmd simple jc.parsers.systemctl_ls+ > ../docs/parsers/systemctl_ls.md
pydocmd simple jc.parsers.systemctl_luf+ > ../docs/parsers/systemctl_luf.md
pydocmd simple jc.parsers.uname+ > ../docs/parsers/uname.md
pydocmd simple jc.parsers.uptime+ > ../docs/parsers/uptime.md
pydocmd simple jc.parsers.w+ > ../docs/parsers/w.md
pydocmd simple jc.parsers.xml+ > ../docs/parsers/xml.md
pydocmd simple jc.parsers.yaml+ > ../docs/parsers/yaml.md
