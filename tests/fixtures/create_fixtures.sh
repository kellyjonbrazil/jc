#!/bin/bash

arp      > arp.out
arp -v   > arp-v.out
arp -a   > arp-a.out
df       > df.out
df -h    > df-h.out
dig www.google.com AAAA        > dig-aaaa.out
dig www.cnn.com www.google.com > dig.out
dig -x 1.1.1.1                 > dig-x.out
env      > env.out
free     > free.out
free -h  > free-h.out
history  > history.out
ifconfig > ifconfig.out

sudo iptables -A INPUT -i lo -j ACCEPT
sudo iptables -A OUTPUT -o lo -j ACCEPT
sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A OUTPUT -m conntrack --ctstate ESTABLISHED -j ACCEPT
sudo iptables -A INPUT -m conntrack --ctstate INVALID -j DROP
sudo iptables -A INPUT -i lo -s 15.15.15.51 -j DROP
sudo iptables -A INPUT -p tcp -s 15.15.15.0/24 --dport 22 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
sudo iptables -A OUTPUT -p tcp --sport 22 -m conntrack --ctstate ESTABLISHED -j ACCEPT
sudo iptables -L -t filter   > iptables-filter.out
sudo iptables --line-numbers -L -t filter   > iptables-filter-line-numbers.out
sudo iptables -L -t nat      > iptables-nat.out
sudo iptables -L -t mangle   > iptables-mangle.out
sudo iptables -L -t raw      > iptables-raw.out
sudo iptables -nvL -t filter > iptables-filter-nv.out

sleep 11 & sleep 12 & sleep 13 & sleep 14 &
jobs       > jobs.out

ls /       > ls.out
ls -al /   > ls-al.out
ls -alh /  > ls-alh.out

ls -R /usr     > ls-R.out
ls -alR /usr   > ls-alR.out
ls /usr/*      > ls-glob.out

cd /tmp/lstest
touch 'a regular filename'
touch $'\nthis file starts with one newline'
touch $'\n\n\n\nthis file starts with four newlines'
touch $'this file has\na newline inside'
touch $'this file has\n\n\n\nfour contiguous newlines inside'
touch $'this file\nhas\nsix\n\nnewlines\n\nwithin'
touch $'\n\nthis file has\na combination\n\n\nof everything\n\n\n\n'
cd /tmp
ls -R > ~/utils/ls-R-newlines.out
ls -lR > ~/utils/ls-lR-newlines.out
cd lstest
ls > ~/utils/ls-newlines.out
ls -l > ~/utils/ls-l-newlines.out

lsblk      > lsblk.out
lsblk -o +KNAME,FSTYPE,LABEL,UUID,PARTLABEL,PARTUUID,RA,MODEL,SERIAL,STATE,OWNER,GROUP,MODE,ALIGNMENT,MIN-IO,OPT-IO,PHY-SEC,LOG-SEC,ROTA,SCHED,RQ-SIZE,DISC-ALN,DISC-GRAN,DISC-MAX,DISC-ZERO,WSAME,WWN,RAND,PKNAME,HCTL,TRAN,REV,VENDOR > lsblk-allcols.out
lsmod      > lsmod.out
lsof       > lsof.out
sudo lsof  > lsof-sudo.out
mount      > mount.out

rm -rf /tmp/jc
git clone https://github.com/kellyjonbrazil/jc.git /tmp/jc & sleep 1; netstat    > netstat.out
netstat -p > netstat-p.out
netstat -l > netstat-l.out
sudo netstat -lnp > netstat-sudo-lnp.out
sudo netstat -aeep > netstat-sudo-aeep.out

ps -ef     > ps-ef.out
ps axu     > ps-axu.out
route      > route.out
route -vn  > route-vn.out
uname -a   > uname-a.out
uptime     > uptime.out
w          > w.out

cat /etc/hosts > hosts.out
cat /etc/fstab > fstab.out

systemctl -a > systemctl.out
systemctl -a list-unit-files > systemctl-luf.out
systemctl -a list-sockets > systemctl-ls.out
systemctl -a list-jobs > systemctl-jobs.out

du /usr > du.out
pip3 list > pip-list.out
pip3 show wheel pip jc > pip-show.out

blkid > blkid.out
blkid /dev/sda2 > blkid-sda2.out
sudo blkid -ip /dev/sda2 /dev/sda1 > blkid-ip-multi.out
sudo blkid -o udev -ip /dev/sr0 > blkid-ip-udev.out
sudo blkid -o udev -ip /dev/sda2 /dev/sda1 > blkid-ip-udev-multi.out

last > last.out
last -w | cat > last-w.out
sudo lastb > lastb.out

cat /etc/group > group.out
sudo cat /etc/gshadow > gshadow.out
