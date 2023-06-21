## JC Examples
### acpi
```bash
acpi -V | jc --acpi -p          # or:  jc -p acpi -V
```
```json
[
  {
    "type": "Battery",
    "id": 0,
    "state": "Charging",
    "charge_percent": 71,
    "until_charged": "00:29:20",
    "design_capacity_mah": 2110,
    "last_full_capacity": 2271,
    "last_full_capacity_percent": 100,
    "until_charged_hours": 0,
    "until_charged_minutes": 29,
    "until_charged_seconds": 20,
    "until_charged_total_seconds": 1760
  },
  {
    "type": "Adapter",
    "id": 0,
    "on-line": true
  },
  {
    "type": "Thermal",
    "id": 0,
    "mode": "ok",
    "temperature": 46.0,
    "temperature_unit": "C",
    "trip_points": [
      {
        "id": 0,
        "switches_to_mode": "critical",
        "temperature": 127.0,
        "temperature_unit": "C"
      },
      {
        "id": 1,
        "switches_to_mode": "hot",
        "temperature": 127.0,
        "temperature_unit": "C"
      }
    ]
  },
  {
    "type": "Cooling",
    "id": 0,
    "messages": [
      "Processor 0 of 10"
    ]
  },
  {
    "type": "Cooling",
    "id": 1,
    "messages": [
      "Processor 0 of 10"
    ]
  },
  {
    "type": "Cooling",
    "id": 2,
    "messages": [
      "x86_pkg_temp no state information available"
    ]
  },
  {
    "type": "Cooling",
    "id": 3,
    "messages": [
      "Processor 0 of 10"
    ]
  },
  {
    "type": "Cooling",
    "id": 4,
    "messages": [
      "intel_powerclamp no state information available"
    ]
  },
  {
    "type": "Cooling",
    "id": 5,
    "messages": [
      "Processor 0 of 10"
    ]
  }
]
```
### airport -I
```bash
airport -I | jc --airport -p          # or:  jc -p airport -I
```
```json
{
  "agrctlrssi": -66,
  "agrextrssi": 0,
  "agrctlnoise": -90,
  "agrextnoise": 0,
  "state": "running",
  "op_mode": "station",
  "lasttxrate": 195,
  "maxrate": 867,
  "lastassocstatus": 0,
  "802_11_auth": "open",
  "link_auth": "wpa2-psk",
  "bssid": "3c:37:86:15:ad:f9",
  "ssid": "SnazzleDazzle",
  "mcs": 0,
  "channel": "48,80"
}
```
### airport -s
```bash
airport -s | jc --airport-s -p          # or:  jc -p airport -s
```
```json
[
  {
    "ssid": "DIRECT-4A-HP OfficeJet 3830",
    "bssid": "00:67:eb:2a:a7:3b",
    "rssi": -90,
    "channel": "6",
    "ht": true,
    "cc": "--",
    "security": [
      "WPA2(PSK/AES/AES)"
    ]
  },
  {
    "ssid": "Latitude38",
    "bssid": "c0:ff:d5:d2:7a:f3",
    "rssi": -85,
    "channel": "11",
    "ht": true,
    "cc": "US",
    "security": [
      "WPA2(PSK/AES/AES)"
    ]
  },
  {
    "ssid": "xfinitywifi",
    "bssid": "6e:e3:0e:b8:45:99",
    "rssi": -83,
    "channel": "11",
    "ht": true,
    "cc": "US",
    "security": [
      "NONE"
    ]
  }
]
```
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
```bash
arp -a | jc --arp -p          # or:  jc -p arp -a
```
```json
[
  {
    "name": null,
    "address": "192.168.71.1",
    "hwtype": "ether",
    "hwaddress": "00:50:56:c0:00:08",
    "iface": "ens33",
    "permanent": true
  },
  {
    "name": null,
    "address": "192.168.71.254",
    "hwtype": "ether",
    "hwaddress": "00:50:56:fe:7a:b4",
    "iface": "ens33",
    "permanent": true
  },
  {
    "name": "_gateway",
    "address": "192.168.71.2",
    "hwtype": "ether",
    "hwaddress": "00:50:56:f7:4a:fc",
    "iface": "ens33",
    "permanent": false,
    "expires": 110
  }
]
```
### blkid
```bash
blkid | jc --blkid -p          # or:  jc -p blkid
```
```json
[
  {
    "device": "/dev/sda1",
    "uuid": "05d927ab-5875-49e4-ada1-7f46cb32c932",
    "type": "xfs"
  },
  {
    "device": "/dev/sda2",
    "uuid": "3klkIj-w1kk-DkJi-0XBJ-y3i7-i2Ac-vHqWBM",
    "type": "LVM2_member"
  },
  {
    "device": "/dev/mapper/centos-root",
    "uuid": "07d718ff-950c-4e5b-98f0-42a1147c77d9",
    "type": "xfs"
  },
  {
    "device": "/dev/mapper/centos-swap",
    "uuid": "615eb89a-bcbf-46fd-80e3-c483ff5c931f",
    "type": "swap"
  }
]
```
```bash
blkid -o udev -ip /dev/sda2 | jc --blkid -p          # or:  jc -p blkid -o udev -ip /dev/sda2
```
```json
[
  {
    "id_fs_uuid": "3klkIj-w1kk-DkJi-0XBJ-y3i7-i2Ac-vHqWBM",
    "id_fs_uuid_enc": "3klkIj-w1kk-DkJi-0XBJ-y3i7-i2Ac-vHqWBM",
    "id_fs_version": "LVM220001",
    "id_fs_type": "LVM2_member",
    "id_fs_usage": "raid",
    "id_iolimit_minimum_io_size": 512,
    "id_iolimit_physical_sector_size": 512,
    "id_iolimit_logical_sector_size": 512,
    "id_part_entry_scheme": "dos",
    "id_part_entry_type": "0x8e",
    "id_part_entry_number": 2,
    "id_part_entry_offset": 2099200,
    "id_part_entry_size": 39843840,
    "id_part_entry_disk": "8:0"
  }
]
```
### CEF strings
```bash
cat cef.log | jc --cef -p
```
```json
[
  {
    "deviceVendor": "Trend Micro",
    "deviceProduct": "Deep Security Agent",
    "deviceVersion": "<DSA version>",
    "deviceEventClassId": "4000000",
    "name": "Eicar_test_file",
    "agentSeverity": 6,
    "CEFVersion": 0,
    "dvchost": "hostname",
    "string": "hello \"world\"!",
    "start": "Nov 08 2020 12:30:00.111 UTC",
    "start_epoch": 1604867400,
    "start_epoch_utc": 1604838600,
    "Host_ID": 1,
    "Quarantine": 205,
    "myDate": "Nov 08 2022 12:30:00.111",
    "myDate_epoch": 1667939400,
    "myDate_epoch_utc": null,
    "myFloat": 3.14,
    "deviceEventClassIdNum": 4000000,
    "agentSeverityString": "Medium",
    "agentSeverityNum": 6
  }
]
```
### chage --list
```bash
chage --list joeuser | jc --chage -p          # or:  jc -p chage --list joeuser
```
```json
{
  "password_last_changed": "never",
  "password_expires": "never",
  "password_inactive": "never",
  "account_expires": "never",
  "min_days_between_password_change": 0,
  "max_days_between_password_change": 99999,
  "warning_days_before_password_expires": 7
}
```
### cksum
```bash
cksum * | jc --cksum -p          # or:  jc -p cksum *
```
```json
[
  {
    "filename": "__init__.py",
    "checksum": 4294967295,
    "blocks": 0
  },
  {
    "filename": "airport.py",
    "checksum": 2208551092,
    "blocks": 3745
  },
  {
    "filename": "airport_s.py",
    "checksum": 1113817598,
    "blocks": 4572
  }
]
```
### crontab
```bash
cat /etc/crontab | jc --crontab -p          # or:  jc -p crontab -l
```
```json
{
  "variables": [
    {
      "name": "MAILTO",
      "value": "root"
    },
    {
      "name": "PATH",
      "value": "/sbin:/bin:/usr/sbin:/usr/bin"
    },
    {
      "name": "SHELL",
      "value": "/bin/bash"
    }
  ],
  "schedule": [
    {
      "minute": [
        "5"
      ],
      "hour": [
        "10-11",
        "22"
      ],
      "day_of_month": [
        "*"
      ],
      "month": [
        "*"
      ],
      "day_of_week": [
        "*"
      ],
      "command": "/var/www/devdaily.com/bin/mk-new-links.php"
    },
    {
      "minute": [
        "30"
      ],
      "hour": [
        "4/2"
      ],
      "day_of_month": [
        "*"
      ],
      "month": [
        "*"
      ],
      "day_of_week": [
        "*"
      ],
      "command": "/var/www/devdaily.com/bin/create-all-backups.sh"
    },
    {
      "occurrence": "yearly",
      "command": "/home/maverick/bin/annual-maintenance"
    },
    {
      "occurrence": "reboot",
      "command": "/home/cleanup"
    },
    {
      "occurrence": "monthly",
      "command": "/home/maverick/bin/tape-backup"
    }
  ]
}
```
### crontab-u (with user support)
```bash
cat /etc/crontab | jc --crontab-u -p
```
```json
{
  "variables": [
    {
      "name": "MAILTO",
      "value": "root"
    },
    {
      "name": "PATH",
      "value": "/sbin:/bin:/usr/sbin:/usr/bin"
    },
    {
      "name": "SHELL",
      "value": "/bin/bash"
    }
  ],
  "schedule": [
    {
      "minute": [
        "5"
      ],
      "hour": [
        "10-11",
        "22"
      ],
      "day_of_month": [
        "*"
      ],
      "month": [
        "*"
      ],
      "day_of_week": [
        "*"
      ],
      "user": "root",
      "command": "/var/www/devdaily.com/bin/mk-new-links.php"
    },
    {
      "minute": [
        "30"
      ],
      "hour": [
        "4/2"
      ],
      "day_of_month": [
        "*"
      ],
      "month": [
        "*"
      ],
      "day_of_week": [
        "*"
      ],
      "user": "root",
      "command": "/var/www/devdaily.com/bin/create-all-backups.sh"
    },
    {
      "occurrence": "yearly",
      "user": "root",
      "command": "/home/maverick/bin/annual-maintenance"
    },
    {
      "occurrence": "reboot",
      "user": "root",
      "command": "/home/cleanup"
    },
    {
      "occurrence": "monthly",
      "user": "root",
      "command": "/home/maverick/bin/tape-backup"
    }
  ]
}
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
### date
```bash
date | jc --date -p          # or:  jc -p date
```
```json
{
  "year": 2021,
  "month": "Mar",
  "month_num": 3,
  "day": 25,
  "weekday": "Thu",
  "weekday_num": 4,
  "hour": 2,
  "hour_24": 2,
  "minute": 2,
  "second": 26,
  "period": "AM",
  "timezone": "UTC",
  "utc_offset": "+0000",
  "day_of_year": 84,
  "week_of_year": 12,
  "iso": "2021-03-25T02:02:26+00:00",
  "epoch": 1616662946,
  "epoch_utc": 1616637746,
  "timezone_aware": true
}
```
### df
```bash
df | jc --df -p          # or:  jc -p df
```
```json
[
  {
    "filesystem": "devtmpfs",
    "1k_blocks": 1918816,
    "used": 0,
    "available": 1918816,
    "use_percent": 0,
    "mounted_on": "/dev"
  },
  {
    "filesystem": "tmpfs",
    "1k_blocks": 1930664,
    "used": 0,
    "available": 1930664,
    "use_percent": 0,
    "mounted_on": "/dev/shm"
  }
]
```
### dig
```bash
dig cnn.com www.cnn.com @205.251.194.64 | jc --dig -p          # or:  jc -p dig cnn.com www.cnn.com @205.251.194.64
```
```json
[
  {
    "id": 10267,
    "opcode": "QUERY",
    "status": "NOERROR",
    "flags": [
      "qr",
      "rd",
      "ra"
    ],
    "query_num": 1,
    "answer_num": 4,
    "authority_num": 0,
    "additional_num": 1,
    "opt_pseudosection": {
      "edns": {
        "version": 0,
        "flags": [],
        "udp": 4096
      }
    },
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
        "ttl": 17,
        "data": "151.101.65.67"
      },
      {
        "name": "cnn.com.",
        "class": "IN",
        "type": "A",
        "ttl": 17,
        "data": "151.101.129.67"
      },
      {
        "name": "cnn.com.",
        "class": "IN",
        "type": "A",
        "ttl": 17,
        "data": "151.101.1.67"
      },
      {
        "name": "cnn.com.",
        "class": "IN",
        "type": "A",
        "ttl": 17,
        "data": "151.101.193.67"
      }
    ],
    "query_time": 51,
    "server": "2600:1700:bab0:d40::1#53(2600:1700:bab0:d40::1)",
    "when": "Fri Apr 16 16:24:32 PDT 2021",
    "rcvd": 100,
    "when_epoch": 1618615472,
    "when_epoch_utc": null
  },
  {
    "id": 56207,
    "opcode": "QUERY",
    "status": "NOERROR",
    "flags": [
      "qr",
      "aa",
      "rd"
    ],
    "query_num": 1,
    "answer_num": 1,
    "authority_num": 4,
    "additional_num": 1,
    "opt_pseudosection": {
      "edns": {
        "version": 0,
        "flags": [],
        "udp": 4096
      }
    },
    "question": {
      "name": "www.cnn.com.",
      "class": "IN",
      "type": "A"
    },
    "answer": [
      {
        "name": "www.cnn.com.",
        "class": "IN",
        "type": "CNAME",
        "ttl": 300,
        "data": "turner-tls.map.fastly.net."
      }
    ],
    "authority": [
      {
        "name": "cnn.com.",
        "class": "IN",
        "type": "NS",
        "ttl": 3600,
        "data": "ns-1086.awsdns-07.org."
      },
      {
        "name": "cnn.com.",
        "class": "IN",
        "type": "NS",
        "ttl": 3600,
        "data": "ns-1630.awsdns-11.co.uk."
      },
      {
        "name": "cnn.com.",
        "class": "IN",
        "type": "NS",
        "ttl": 3600,
        "data": "ns-47.awsdns-05.com."
      },
      {
        "name": "cnn.com.",
        "class": "IN",
        "type": "NS",
        "ttl": 3600,
        "data": "ns-576.awsdns-08.net."
      }
    ],
    "query_time": 22,
    "server": "205.251.194.64#53(205.251.194.64)",
    "when": "Fri Apr 16 16:24:32 PDT 2021",
    "rcvd": 212,
    "when_epoch": 1618615472,
    "when_epoch_utc": null
  }
]
```
```bash
dig -x 1.1.1.1 | jc --dig -p          # or:  jc -p dig -x 1.1.1.1
```
```json
[
  {
    "id": 20785,
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
    "opt_pseudosection": {
      "edns": {
        "version": 0,
        "flags": [],
        "udp": 4096
      }
    },
    "question": {
      "name": "1.1.1.1.in-addr.arpa.",
      "class": "IN",
      "type": "PTR"
    },
    "answer": [
      {
        "name": "1.1.1.1.in-addr.arpa.",
        "class": "IN",
        "type": "PTR",
        "ttl": 1800,
        "data": "one.one.one.one."
      }
    ],
    "query_time": 40,
    "server": "2600:1700:bab0:d40::1#53(2600:1700:bab0:d40::1)",
    "when": "Sat Apr 17 14:50:50 PDT 2021",
    "rcvd": 78,
    "when_epoch": 1618696250,
    "when_epoch_utc": null
  }
]
```
### dir
```bash
dir | jc --dir -p
```
```json
[
  {
    "date": "03/24/2021",
    "time": "03:15 PM",
    "dir": true,
    "size": null,
    "filename": ".",
    "parent": "C:\\Program Files\\Internet Explorer",
    "epoch": 1616624100
  },
  {
    "date": "03/24/2021",
    "time": "03:15 PM",
    "dir": true,
    "size": null,
    "filename": "..",
    "parent": "C:\\Program Files\\Internet Explorer",
    "epoch": 1616624100
  },
  {
    "date": "12/07/2019",
    "time": "02:49 AM",
    "dir": true,
    "size": null,
    "filename": "en-US",
    "parent": "C:\\Program Files\\Internet Explorer",
    "epoch": 1575715740
  },
  {
    "date": "12/07/2019",
    "time": "02:09 AM",
    "dir": false,
    "size": 54784,
    "filename": "ExtExport.exe",
    "parent": "C:\\Program Files\\Internet Explorer",
    "epoch": 1575713340
  }
]
```
### dmidecode
```bash
dmidecode | jc --dmidecode -p          # or:  jc -p dmidecode
```
```json
[
  {
    "handle": "0x0000",
    "type": 0,
    "bytes": 24,
    "description": "BIOS Information",
    "values": {
      "vendor": "Phoenix Technologies LTD",
      "version": "6.00",
      "release_date": "04/13/2018",
      "address": "0xEA490",
      "runtime_size": "88944 bytes",
      "rom_size": "64 kB",
      "characteristics": [
        "ISA is supported",
        "PCI is supported",
        "PC Card (PCMCIA) is supported",
        "PNP is supported",
        "APM is supported",
        "BIOS is upgradeable",
        "BIOS shadowing is allowed",
        "ESCD support is available",
        "Boot from CD is supported",
        "Selectable boot is supported",
        "EDD is supported",
        "Print screen service is supported (int 5h)",
        "8042 keyboard services are supported (int 9h)",
        "Serial services are supported (int 14h)",
        "Printer services are supported (int 17h)",
        "CGA/mono video services are supported (int 10h)",
        "ACPI is supported",
        "Smart battery is supported",
        "BIOS boot specification is supported",
        "Function key-initiated network boot is supported",
        "Targeted content distribution is supported"
      ],
      "bios_revision": "4.6",
      "firmware_revision": "0.0"
    }
  }
]
```
### dpkg -l
```bash
dpkg -l | jc --dpkg-l -p          # or:  jc -p dpkg -l
```
```json
[
  {
    "codes": "ii",
    "name": "accountsservice",
    "version": "0.6.45-1ubuntu1.3",
    "architecture": "amd64",
    "description": "query and manipulate user account information",
    "desired": "install",
    "status": "installed"
  },
  {
    "codes": "rc",
    "name": "acl",
    "version": "2.2.52-3build1",
    "architecture": "amd64",
    "description": "Access control list utilities",
    "desired": "remove",
    "status": "config-files"
  },
  {
    "codes": "uWR",
    "name": "acpi",
    "version": "1.7-1.1",
    "architecture": "amd64",
    "description": "displays information on ACPI devices",
    "desired": "unknown",
    "status": "trigger await",
    "error": "reinstall required"
  },
  {
    "codes": "rh",
    "name": "acpid",
    "version": "1:2.0.28-1ubuntu1",
    "architecture": "amd64",
    "description": "Advanced Configuration and Power Interface event daemon",
    "desired": "remove",
    "status": "half installed"
  },
  {
    "codes": "pn",
    "name": "adduser",
    "version": "3.116ubuntu1",
    "architecture": "all",
    "description": "add and remove users and groups",
    "desired": "purge",
    "status": "not installed"
  }
]
```
### du
```bash
du /usr | jc --du -p          # or:  jc -p du /usr
```
```json
[
  {
    "size": 104608,
    "name": "/usr/bin"
  },
  {
    "size": 56,
    "name": "/usr/standalone/firmware/iBridge1_1Customer.bundle/Contents/_CodeSignature"
  },
  {
    "size": 0,
    "name": "/usr/standalone/firmware/iBridge1_1Customer.bundle/Contents/Resources/Firmware/usr/local/standalone"
  },
  {
    "size": 0,
    "name": "/usr/standalone/firmware/iBridge1_1Customer.bundle/Contents/Resources/Firmware/usr/local"
  },
  {
    "size": 0,
    "name": "/usr/standalone/firmware/iBridge1_1Customer.bundle/Contents/Resources/Firmware/usr"
  },
  {
    "size": 1008,
    "name": "/usr/standalone/firmware/iBridge1_1Customer.bundle/Contents/Resources/Firmware/dfu"
  }
]
```
### Email Address string
```bash
echo 'joe.user@gmail.com' | jc --email-address -p
```
```json
{
  "username": "joe.user",
  "domain": "gmail.com",
  "local": "joe.user",
  "local_plus_suffix": null
}
```
### env
```bash
env | jc --env -p          # or:  jc -p env
```
```json
[
  {
    "name": "XDG_SESSION_ID",
    "value": "1"
  },
  {
    "name": "HOSTNAME",
    "value": "localhost.localdomain"
  },
  {
    "name": "TERM",
    "value": "vt220"
  },
  {
    "name": "SHELL",
    "value": "/bin/bash"
  },
  {
    "name": "HISTSIZE",
    "value": "1000"
  }
]
```
### file
```bash
file * | jc --file -p          # or:  jc -p file *
```
```json
[
  {
    "filename": "Applications",
    "type": "directory"
  },
  {
    "filename": "another file with spaces",
    "type": "empty"
  },
  {
    "filename": "argstest.py",
    "type": "Python script text executable, ASCII text"
  },
  {
    "filename": "blkid-p.out",
    "type": "ASCII text"
  },
  {
    "filename": "blkid-pi.out",
    "type": "ASCII text, with very long lines"
  },
  {
    "filename": "cd_catalog.xml",
    "type": "XML 1.0 document text, ASCII text, with CRLF line terminators"
  },
  {
    "filename": "centosserial.sh",
    "type": "Bourne-Again shell script text executable, UTF-8 Unicode text"
  }
]
```
### finger
```bash
finger | jc --finger -p          # or:  jc -p finger
```
```json
[
  {
    "login": "jdoe",
    "name": "John Doe",
    "tty": "tty1",
    "idle": "14d",
    "login_time": "Mar 22 21:14",
    "tty_writeable": false,
    "idle_minutes": 0,
    "idle_hours": 0,
    "idle_days": 14,
    "total_idle_minutes": 20160
  },
  {
    "login": "jdoe",
    "name": "John Doe",
    "tty": "pts/0",
    "idle": null,
    "login_time": "Apr  5 15:33",
    "details": "(192.168.1.22)",
    "tty_writeable": true,
    "idle_minutes": 0,
    "idle_hours": 0,
    "idle_days": 0,
    "total_idle_minutes": 0
  }
]
```
### free
```bash
free | jc --free -p          # or:  jc -p free
```
```json
[
  {
    "type": "Mem",
    "total": 3861340,
    "used": 220508,
    "free": 3381972,
    "shared": 11800,
    "buff_cache": 258860,
    "available": 3397784
  },
  {
    "type": "Swap",
    "total": 2097148,
    "used": 0,
    "free": 2097148
  }
]
```
### /etc/fstab file
```bash
cat /etc/fstab | jc --fstab -p
```
```json
[
  {
    "fs_spec": "/dev/mapper/centos-root",
    "fs_file": "/",
    "fs_vfstype": "xfs",
    "fs_mntops": "defaults",
    "fs_freq": 0,
    "fs_passno": 0
  },
  {
    "fs_spec": "UUID=05d927bb-5875-49e3-ada1-7f46cb31c932",
    "fs_file": "/boot",
    "fs_vfstype": "xfs",
    "fs_mntops": "defaults",
    "fs_freq": 0,
    "fs_passno": 0
  },
  {
    "fs_spec": "/dev/mapper/centos-swap",
    "fs_file": "swap",
    "fs_vfstype": "swap",
    "fs_mntops": "defaults",
    "fs_freq": 0,
    "fs_passno": 0
  }
]
```
### git log
```bash
git log --stat | jc --git-log -p          or:  jc -p git log --stat
```
```json
[
  {
    "commit": "728d882ed007b3c8b785018874a0eb06e1143b66",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "date": "Wed Apr 20 09:50:19 2022 -0400",
    "stats": {
      "files_changed": 2,
      "insertions": 90,
      "deletions": 12,
      "files": [
        "docs/parsers/git_log.md",
        "jc/parsers/git_log.py"
      ]
    },
    "message": "add timestamp docs and examples",
    "epoch": 1650462619,
    "epoch_utc": null
  },
  {
    "commit": "b53e42aca623181aa9bc72194e6eeef1e9a3a237",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "date": "Wed Apr 20 09:44:42 2022 -0400",
    "stats": {
      "files_changed": 5,
      "insertions": 29,
      "deletions": 6,
      "files": [
        "docs/parsers/git_log.md",
        "docs/utils.md",
        "jc/parsers/git_log.py",
        "jc/utils.py",
        "man/jc.1"
      ]
    },
    "message": "add calculated timestamp",
    "epoch": 1650462282,
    "epoch_utc": null
  }
]
```
### gpg --with-colons
```bash
gpg --with-colons --show-keys file.gpg | jc --gpg -p          # or  jc -p gpg --with-colons --show-keys file.gpg
```
```json
[
  {
    "type": "pub",
    "validity": "f",
    "key_length": "1024",
    "pub_key_alg": "17",
    "key_id": "6C7EE1B8621CC013",
    "creation_date": "899817715",
    "expiration_date": "1055898235",
    "certsn_uidhash_trustinfo": null,
    "owner_trust": "m",
    "user_id": null,
    "signature_class": null,
    "key_capabilities": "scESC",
    "cert_fingerprint_other": null,
    "flag": null,
    "token_sn": null,
    "hash_alg": null,
    "curve_name": null,
    "compliance_flags": null,
    "last_update_date": null,
    "origin": null,
    "comment": null
  }
]
```
### /etc/group file
```bash
cat /etc/group | jc --group -p
```
```json
[
  {
    "group_name": "nobody",
    "password": "*",
    "gid": -2,
    "members": []
  },
  {
    "group_name": "nogroup",
    "password": "*",
    "gid": -1,
    "members": []
  },
  {
    "group_name": "wheel",
    "password": "*",
    "gid": 0,
    "members": [
      "root"
    ]
  },
  {
    "group_name": "certusers",
    "password": "*",
    "gid": 29,
    "members": [
      "root",
      "_jabber",
      "_postfix",
      "_cyrus",
      "_calendar",
      "_dovecot"
    ]
  }
]
```
### /etc/gshadow file
```bash
cat /etc/gshadow | jc --gshadow -p
```
```json
[
  {
    "group_name": "root",
    "password": "*",
    "administrators": [],
    "members": []
  },
  {
    "group_name": "adm",
    "password": "*",
    "administrators": [],
    "members": [
      "syslog",
      "joeuser"
    ]
  }
]
```
### hash
```bash
hash | jc --hash -p
```
```json
[
  {
    "hits": 2,
    "command": "/bin/cat"
  },
  {
    "hits": 1,
    "command": "/bin/ls"
  }
]
```
### hashsum
```bash
md5sum * | jc --hashsum -p           # or:  jc -p md5sum *
```
```json
[
  {
    "filename": "devtoolset-3-gcc-4.9.2-6.el7.x86_64.rpm",
    "hash": "65fc958c1add637ec23c4b137aecf3d3"
  },
  {
    "filename": "digout",
    "hash": "5b9312ee5aff080927753c63a347707d"
  },
  {
    "filename": "dmidecode.out",
    "hash": "716fd11c2ac00db109281f7110b8fb9d"
  },
  {
    "filename": "file with spaces in the name",
    "hash": "d41d8cd98f00b204e9800998ecf8427e"
  },
  {
    "filename": "id-centos.out",
    "hash": "4295be239a14ad77ef3253103de976d2"
  },
  {
    "filename": "ifcfg.json",
    "hash": "01fda0d9ba9a75618b072e64ff512b43"
  }
]
```
### hciconfig
```bash
hciconfig -a | jc --hciconfig -p           # or:  jc -p hciconfig -a
```
```json
[
  {
    "device": "hci0",
    "type": "Primary",
    "bus": "USB",
    "bd_address": "00:1A:7D:DA:71:13",
    "acl_mtu": 310,
    "acl_mtu_packets": 10,
    "sco_mtu": 64,
    "sco_mtu_packets": 8,
    "state": [
      "UP",
      "RUNNING"
    ],
    "rx_bytes": 13905869,
    "rx_acl": 0,
    "rx_sco": 0,
    "rx_events": 393300,
    "rx_errors": 0,
    "tx_bytes": 62629,
    "tx_acl": 0,
    "tx_sco": 0,
    "tx_commands": 3893,
    "tx_errors": 0,
    "features": [
      "0xff",
      "0xff",
      "0x8f",
      "0xfe",
      "0xdb",
      "0xff",
      "0x5b",
      "0x87"
    ],
    "packet_type": [
      "DM1",
      "DM3",
      "DM5",
      "DH1",
      "DH3",
      "DH5",
      "HV1",
      "HV2",
      "HV3"
    ],
    "link_policy": [
      "RSWITCH",
      "HOLD",
      "SNIFF",
      "PARK"
    ],
    "link_mode": [
      "SLAVE",
      "ACCEPT"
    ],
    "name": "CSR8510 A10",
    "class": "0x000000",
    "service_classes": null,
    "device_class": "Miscellaneous",
    "hci_version": "4.0 (0x6)",
    "hci_revision": "0x22bb",
    "lmp_version": "4.0 (0x6)",
    "lmp_subversion": "0x22bb",
    "manufacturer": "Cambridge Silicon Radio (10)"
  },
  {
    "device": "hci1",
    "type": "Primary",
    "bus": "USB",
    "bd_address": "00:1A:7D:DA:71:13",
    "acl_mtu": 310,
    "acl_mtu_packets": 10,
    "sco_mtu": 64,
    "sco_mtu_packets": 8,
    "state": [
      "DOWN"
    ],
    "rx_bytes": 4388363,
    "rx_acl": 0,
    "rx_sco": 0,
    "rx_events": 122021,
    "rx_errors": 0,
    "tx_bytes": 52350,
    "tx_acl": 0,
    "tx_sco": 0,
    "tx_commands": 3480,
    "tx_errors": 2,
    "features": [
      "0xff",
      "0xff",
      "0x8f",
      "0xfe",
      "0xdb",
      "0xff",
      "0x5b",
      "0x87"
    ],
    "packet_type": [
      "DM1",
      "DM3",
      "DM5",
      "DH1",
      "DH3",
      "DH5",
      "HV1",
      "HV2",
      "HV3"
    ],
    "link_policy": [
      "RSWITCH",
      "HOLD",
      "SNIFF",
      "PARK"
    ],
    "link_mode": [
      "SLAVE",
      "ACCEPT"
    ]
  }
]
```
### history
```bash
history | jc --history -p
```
```json
[
  {
    "line": 118,
    "command": "sleep 100"
  },
  {
    "line": 119,
    "command": "ls /bin"
  },
  {
    "line": 120,
    "command": "echo \"hello\""
  },
  {
    "line": 121,
    "command": "docker images"
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
    "ip": "127.0.1.1",
    "hostname": [
      "root-ubuntu"
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
  },
  {
    "ip": "ff00::0",
    "hostname": [
      "ip6-mcastprefix"
    ]
  },
  {
    "ip": "ff02::1",
    "hostname": [
      "ip6-allnodes"
    ]
  },
  {
    "ip": "ff02::2",
    "hostname": [
      "ip6-allrouters"
    ]
  }
]
```
### id
```bash
id | jc --id -p          # or:  jc -p id
```
```json
{
  "uid": {
    "id": 1000,
    "name": "joeuser"
  },
  "gid": {
    "id": 1000,
    "name": "joeuser"
  },
  "groups": [
    {
      "id": 1000,
      "name": "joeuser"
    },
    {
      "id": 10,
      "name": "wheel"
    }
  ],
  "context": {
    "user": "unconfined_u",
    "role": "unconfined_r",
    "type": "unconfined_t",
    "level": "s0-s0:c0.c1023"
  }
}
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
  },
  {
    "name": "lo",
    "flags": 73,
    "state": [
      "UP",
      "LOOPBACK",
      "RUNNING"
    ],
    "mtu": 65536,
    "ipv4_addr": "127.0.0.1",
    "ipv4_mask": "255.0.0.0",
    "ipv4_bcast": null,
    "ipv6_addr": "::1",
    "ipv6_mask": 128,
    "ipv6_scope": "0x10",
    "mac_addr": null,
    "type": "Local Loopback",
    "rx_packets": 73,
    "rx_bytes": 6009,
    "rx_errors": 0,
    "rx_dropped": 0,
    "rx_overruns": 0,
    "rx_frame": 0,
    "tx_packets": 73,
    "tx_bytes": 6009,
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
  "DEFAULT": {
    "ServerAliveInterval": "45",
    "Compression": "yes",
    "CompressionLevel": "9",
    "ForwardX11": "yes"
  },
  "bitbucket.org": {
    "User": "hg"
  },
  "topsecret.server.com": {
    "Port": "50022",
    "ForwardX11": "no"
  }
}

```
### iostat
```bash
$ iostat | jc --iostat -p          # or:  jc -p iostat
```
```json
[
  {
      "percent_user": 0.15,
      "percent_nice": 0.0,
      "percent_system": 0.18,
      "percent_iowait": 0.0,
      "percent_steal": 0.0,
      "percent_idle": 99.67,
      "type": "cpu"
  },
  {
      "device": "sda",
      "tps": 0.29,
      "kb_read_s": 7.22,
      "kb_wrtn_s": 1.25,
      "kb_read": 194341,
      "kb_wrtn": 33590,
      "type": "device"
  },
  {
      "device": "dm-0",
      "tps": 0.29,
      "kb_read_s": 5.99,
      "kb_wrtn_s": 1.17,
      "kb_read": 161361,
      "kb_wrtn": 31522,
      "type": "device"
  },
  {
      "device": "dm-1",
      "tps": 0.0,
      "kb_read_s": 0.08,
      "kb_wrtn_s": 0.0,
      "kb_read": 2204,
      "kb_wrtn": 0,
      "type": "device"
  }
]
```
### IP Address strings
```bash
echo 192.168.2.10/24 | jc --ip-address -p
```
```json
{
  "version": 4,
  "max_prefix_length": 32,
  "ip": "192.168.2.10",
  "ip_compressed": "192.168.2.10",
  "ip_exploded": "192.168.2.10",
  "ip_split": [
    "192",
    "168",
    "2",
    "10"
  ],
  "scope_id": null,
  "ipv4_mapped": null,
  "six_to_four": null,
  "teredo_client": null,
  "teredo_server": null,
  "dns_ptr": "10.2.168.192.in-addr.arpa",
  "network": "192.168.2.0",
  "broadcast": "192.168.2.255",
  "hostmask": "0.0.0.255",
  "netmask": "255.255.255.0",
  "cidr_netmask": 24,
  "hosts": 254,
  "first_host": "192.168.2.1",
  "last_host": "192.168.2.254",
  "is_multicast": false,
  "is_private": true,
  "is_global": false,
  "is_link_local": false,
  "is_loopback": false,
  "is_reserved": false,
  "is_unspecified": false,
  "int": {
    "ip": 3232236042,
    "network": 3232236032,
    "broadcast": 3232236287,
    "first_host": 3232236033,
    "last_host": 3232236286
  },
  "hex": {
    "ip": "c0:a8:02:0a",
    "network": "c0:a8:02:00",
    "broadcast": "c0:a8:02:ff",
    "hostmask": "00:00:00:ff",
    "netmask": "ff:ff:ff:00",
    "first_host": "c0:a8:02:01",
    "last_host": "c0:a8:02:fe"
  },
  "bin": {
    "ip": "11000000101010000000001000001010",
    "network": "11000000101010000000001000000000",
    "broadcast": "11000000101010000000001011111111",
    "hostmask": "00000000000000000000000011111111",
    "netmask": "11111111111111111111111100000000",
    "first_host": "11000000101010000000001000000001",
    "last_host": "11000000101010000000001011111110"
  }
}
```
### iptables
```bash
iptables --line-numbers -v -L -t nat | jc --iptables -p          # or:  jc -p iptables --line-numbers -v -L -t nat
```
```json
[
  {
    "chain": "PREROUTING",
    "rules": [
      {
        "num": 1,
        "pkts": 2183,
        "bytes": 186000,
        "target": "PREROUTING_direct",
        "prot": "all",
        "opt": null,
        "in": "any",
        "out": "any",
        "source": "anywhere",
        "destination": "anywhere"
      },
      {
        "num": 2,
        "pkts": 2183,
        "bytes": 186000,
        "target": "PREROUTING_ZONES_SOURCE",
        "prot": "all",
        "opt": null,
        "in": "any",
        "out": "any",
        "source": "anywhere",
        "destination": "anywhere"
      },
      {
        "num": 3,
        "pkts": 2183,
        "bytes": 186000,
        "target": "PREROUTING_ZONES",
        "prot": "all",
        "opt": null,
        "in": "any",
        "out": "any",
        "source": "anywhere",
        "destination": "anywhere"
      },
      {
        "num": 4,
        "pkts": 0,
        "bytes": 0,
        "target": "DOCKER",
        "prot": "all",
        "opt": null,
        "in": "any",
        "out": "any",
        "source": "anywhere",
        "destination": "anywhere",
        "options": "ADDRTYPE match dst-type LOCAL"
      }
    ]
  }
]
```
### ISO Datetime string
```bash
echo "2022-07-20T14:52:45Z" | jc --datetime-iso -p
```
```json
{
  "year": 2022,
  "month": "Jul",
  "month_num": 7,
  "day": 20,
  "weekday": "Wed",
  "weekday_num": 3,
  "hour": 2,
  "hour_24": 14,
  "minute": 52,
  "second": 45,
  "microsecond": 0,
  "period": "PM",
  "utc_offset": "+0000",
  "day_of_year": 201,
  "week_of_year": 29,
  "iso": "2022-07-20T14:52:45+00:00",
  "timestamp": 1658328765
}
```
### iw dev `device` scan
```bash
iw dev wlan0 scan | jc --iw-scan -p          # or:  jc -p iw dev wlan0 scan
```
```json
[
  {
    "bssid": "71:31:72:65:e1:a2",
    "interface": "wlan0",
    "freq": 2462,
    "capability": "ESS Privacy ShortSlotTime (0x0411)",
    "ssid": "WLAN-1234",
    "supported_rates": [
      1.0,
      2.0,
      5.5,
      11.0,
      18.0,
      24.0,
      36.0,
      54.0
    ],
    "erp": "<no flags>",
    "erp_d4.0": "<no flags>",
    "rsn": "Version: 1",
    "group_cipher": "CCMP",
    "pairwise_ciphers": "CCMP",
    "authentication_suites": "PSK",
    "capabilities": "0x186c",
    "extended_supported_rates": [
      6.0,
      9.0,
      12.0,
      48.0
    ],
    "ht_rx_mcs_rate_indexes_supported": "0-15",
    "primary_channel": 11,
    "secondary_channel_offset": "no secondary",
    "rifs": 1,
    "ht_protection": "no",
    "non-gf_present": 1,
    "obss_non-gf_present": 0,
    "dual_beacon": 0,
    "dual_cts_protection": 0,
    "stbc_beacon": 0,
    "l-sig_txop_prot": 0,
    "pco_active": 0,
    "pco_phase": 0,
    "bss_width_channel_transition_delay_factor": 5,
    "extended_capabilities": "HT Information Exchange Supported",
    "wmm": "Parameter version 1",
    "be": "CW 15-1023, AIFSN 3",
    "bk": "CW 15-1023, AIFSN 7",
    "vi": "CW 7-15, AIFSN 2, TXOP 3008 usec",
    "vo": "CW 3-7, AIFSN 2, TXOP 1504 usec",
    "wps": "Version: 1.0",
    "wi-fi_protected_setup_state": "2 (Configured)",
    "selected_registrar": "0x0",
    "response_type": "3 (AP)",
    "uuid": "00000000-0000-0003-0000-75317074f1a2",
    "manufacturer": "Corporation",
    "model": "VGV8539JW",
    "model_number": "1.47.000",
    "serial_number": "J144024542",
    "primary_device_type": "6-0050f204-1",
    "device_name": "Wireless Router(WFA)",
    "config_methods": "Label, PBC",
    "rf_bands": "0x3",
    "tsf_usec": 212098649788,
    "sta_channel_width_mhz": 20,
    "passive_dwell_tus": 20,
    "active_dwell_tus": 10,
    "channel_width_trigger_scan_interval_s": 300,
    "scan_passive_total_per_channel_tus": 200,
    "scan_active_total_per_channel_tus": 20,
    "beacon_interval_tus": 100,
    "signal_dbm": -80.0,
    "last_seen_ms": 11420,
    "selected_rates": [
      1.0,
      2.0,
      5.5,
      11.0
    ],
    "obss_scan_activity_threshold_percent": 0.25,
    "ds_parameter_set_channel": 11,
    "max_amsdu_length_bytes": 7935,
    "minimum_rx_ampdu_time_spacing_usec": 16
  }
]
```
### jar-manifest
```bash
cat MANIFEST.MF | jc --jar-manifest -p
```
```json
[
  {
    "Import_Package": "com.conversantmedia.util.concurrent;resolution:=optional,com.fasterxml.jackson.annotation;version=\"[2.12,3)\";resolution:=optional,com.fasterxml.jackson.core;version=\"[2.12,3)\";resolution:=optional,com.fasterxml.jackson.core.type;version=\"[2.12,3)\";resolution:=optional,com.fasterxml.jackson.cor...",
    "Export_Package": "org.apache.logging.log4j.core;uses:=\"org.apache.logging.log4j,org.apache.logging.log4j.core.config,org.apache.logging.log4j.core.impl,org.apache.logging.log4j.core.layout,org.apache.logging.log4j.core.time,org.apache.logging.log4j.message,org.apache.logging.log4j.spi,org.apache.logging.log4j.status...",
    "Manifest_Version": "1.0",
    "Bundle_License": "https://www.apache.org/licenses/LICENSE-2.0.txt",
    "Bundle_SymbolicName": "org.apache.logging.log4j.core",
    "Built_By": "matt",
    "Bnd_LastModified": "1639373735804",
    "Implementation_Vendor_Id": "org.apache.logging.log4j",
    "Specification_Title": "Apache Log4j Core",
    "Log4jReleaseManager": "Matt Sicker",
    ...
  }
]
```
### jobs
```bash
jobs -l | jc --jobs -p
```
```json
[
  {
    "job_number": 1,
    "pid": 5283,
    "status": "Running",
    "command": "sleep 10000 &"
  },
  {
    "job_number": 2,
    "pid": 5284,
    "status": "Running",
    "command": "sleep 10100 &"
  },
  {
    "job_number": 3,
    "pid": 5285,
    "history": "previous",
    "status": "Running",
    "command": "sleep 10001 &"
  },
  {
    "job_number": 4,
    "pid": 5286,
    "history": "current",
    "status": "Running",
    "command": "sleep 10112 &"
  }
]
```
### JWT string
```bash
echo 'eyJhbGciOiJIUzI1N...' | jc --jwt -p
```
```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "1234567890",
    "name": "John Doe",
    "iat": 1516239022
  },
  "signature": "49:f9:4a:c7:04:49:48:c7:8a:28:5d:90:4f:87:f0:a4:c7..."
}
```
### Key/Value files
```bash
cat keyvalue.txt
```
```
# this file contains key/value pairs
name = John Doe
address=555 California Drive
age: 34
; comments can include # or ;
# delimiter can be = or :
# quoted values have quotation marks stripped by default
# but can be preserved with the -r argument
occupation:"Engineer"
```
```bash
cat keyvalue.txt | jc --kv -p
```
```json
{
  "name": "John Doe",
  "address": "555 California Drive",
  "age": "34",
  "occupation": "Engineer"
}
```
### last and lastb
```bash
last -F | jc --last -p          # or:  jc -p last -F
```
```json
[
  {
    "user": "kbrazil",
    "tty": "pts/0",
    "hostname": "kbrazil-mac.attlocal.net",
    "login": "Tue Jan 5 14:29:24 2021",
    "logout": "still logged in",
    "login_epoch": 1609885764
  },
  {
    "user": "kbrazil",
    "tty": "tty1",
    "hostname": null,
    "login": "Tue Jan 5 14:28:41 2021",
    "logout": "still logged in",
    "login_epoch": 1609885721
  },
  {
    "user": "reboot",
    "tty": "system boot",
    "hostname": "3.10.0-1062.1.2.el7.x86_64",
    "login": "Tue Jan 5 14:28:28 2021",
    "logout": "Tue Jan 5 14:29:36 2021",
    "duration": "00:01",
    "login_epoch": 1609885708,
    "logout_epoch": 1609885776,
    "duration_seconds": 68
  }
]
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
### lsblk
```bash
lsblk | jc --lsblk -p          # or:  jc -p lsblk
```
```json
[
  {
    "name": "sda",
    "maj_min": "8:0",
    "rm": false,
    "size": "20G",
    "ro": false,
    "type": "disk",
    "mountpoint": null
  },
  {
    "name": "sda1",
    "maj_min": "8:1",
    "rm": false,
    "size": "1G",
    "ro": false,
    "type": "part",
    "mountpoint": "/boot"
  }
]
```
### lsmod
```bash
lsmod | jc --lsmod -p          # or:  jc -p lsmod
```
```json
[
  {
    "module": "nf_nat",
    "size": 26583,
    "used": 3,
    "by": [
      "nf_nat_ipv4",
      "nf_nat_ipv6",
      "nf_nat_masquerade_ipv4"
    ]
  },
  {
    "module": "iptable_mangle",
    "size": 12695,
    "used": 1
  },
  {
    "module": "iptable_security",
    "size": 12705,
    "used": 1
  },
  {
    "module": "iptable_raw",
    "size": 12678,
    "used": 1
  },
  {
    "module": "nf_conntrack",
    "size": 139224,
    "used": 7,
    "by": [
      "nf_nat",
      "nf_nat_ipv4",
      "nf_nat_ipv6",
      "xt_conntrack",
      "nf_nat_masquerade_ipv4",
      "nf_conntrack_ipv4",
      "nf_conntrack_ipv6"
    ]
  }
]
```
### lsof
```bash
lsof | jc --lsof -p          # or:  jc -p lsof
```
```json
[
  {
    "command": "systemd",
    "pid": 1,
    "tid": null,
    "user": "root",
    "fd": "cwd",
    "type": "DIR",
    "device": "253,0",
    "size_off": 224,
    "node": 64,
    "name": "/"
  },
  {
    "command": "systemd",
    "pid": 1,
    "tid": null,
    "user": "root",
    "fd": "rtd",
    "type": "DIR",
    "device": "253,0",
    "size_off": 224,
    "node": 64,
    "name": "/"
  },
  {
    "command": "systemd",
    "pid": 1,
    "tid": null,
    "user": "root",
    "fd": "txt",
    "type": "REG",
    "device": "253,0",
    "size_off": 1624520,
    "node": 50360451,
    "name": "/usr/lib/systemd/systemd"
  }
]
```
### lsusb
```bash
lsusb -v | jc --lsusb -p          # or: jc -p lsusb -v
```
```json
[
  {
    "bus": "002",
    "device": "001",
    "id": "1d6b:0001",
    "description": "Linux Foundation 1.1 root hub",
    "device_descriptor": {
      "bLength": {
        "value": "18"
      },
      "bDescriptorType": {
        "value": "1"
      },
      "bcdUSB": {
        "value": "1.10"
      },
      ...
      "bNumConfigurations": {
        "value": "1"
      },
      "configuration_descriptor": {
        "bLength": {
          "value": "9"
        },
        ...
        "iConfiguration": {
          "value": "0"
        },
        "bmAttributes": {
          "value": "0xe0",
          "attributes": [
            "Self Powered",
            "Remote Wakeup"
          ]
        },
        "MaxPower": {
          "description": "0mA"
        },
        "interface_descriptors": [
          {
            "bLength": {
              "value": "9"
            },
            ...
            "bInterfaceProtocol": {
              "value": "0",
              "description": "Full speed (or root) hub"
            },
            "iInterface": {
              "value": "0"
            },
            "endpoint_descriptors": [
              {
                "bLength": {
                  "value": "7"
                },
                ...
                "bmAttributes": {
                  "value": "3",
                  "attributes": [
                    "Transfer Type  Interrupt",
                    "Synch Type  None",
                    "Usage Type  Data"
                  ]
                },
                "wMaxPacketSize": {
                  "value": "0x0002",
                  "description": "1x 2 bytes"
                },
                "bInterval": {
                  "value": "255"
                }
              }
            ]
          }
        ]
      }
    },
    "hub_descriptor": {
      "bLength": {
        "value": "9"
      },
      ...
      "wHubCharacteristic": {
        "value": "0x000a",
        "attributes": [
          "No power switching (usb 1.0)",
          "Per-port overcurrent protection"
        ]
      },
      ...
      "hub_port_status": {
        "Port 1": {
          "value": "0000.0103",
          "attributes": [
            "power",
            "enable",
            "connect"
          ]
        },
        "Port 2": {
          "value": "0000.0103",
          "attributes": [
            "power",
            "enable",
            "connect"
          ]
        }
      }
    },
    "device_status": {
      "value": "0x0001",
      "description": "Self Powered"
    }
  }
]
```
### M3U and M3U8 files
```bash
cat playlist.m3u | jc --m3u -p
```
```json
[
  {
    "runtime": 105,
    "display": "Example artist - Example title",
    "path": "C:\\Files\\My Music\\Example.mp3"
  },
  {
    "runtime": 321,
    "display": "Example Artist2 - Example title2",
    "path": "C:\\Files\\My Music\\Favorites\\Example2.ogg"
  }
]
```
### mount
```bash
mount | jc --mount -p          # or:  jc -p mount
```
```json
[
  {
    "filesystem": "sysfs",
    "mount_point": "/sys",
    "type": "sysfs",
    "options": [
      "rw",
      "nosuid",
      "nodev",
      "noexec",
      "relatime"
    ]
  },
  {
    "filesystem": "proc",
    "mount_point": "/proc",
    "type": "proc",
    "options": [
      "rw",
      "nosuid",
      "nodev",
      "noexec",
      "relatime"
    ]
  },
  {
    "filesystem": "udev",
    "mount_point": "/dev",
    "type": "devtmpfs",
    "options": [
      "rw",
      "nosuid",
      "relatime",
      "size=977500k",
      "nr_inodes=244375",
      "mode=755"
    ]
  }
]
```
### mpstat
```bash
mpstat | jc --mpstat -p          # or  jc -p mpstat
```
```json
[
  {
    "cpu": "all",
    "percent_usr": 12.94,
    "percent_nice": 0.0,
    "percent_sys": 26.42,
    "percent_iowait": 0.43,
    "percent_irq": 0.0,
    "percent_soft": 0.16,
    "percent_steal": 0.0,
    "percent_guest": 0.0,
    "percent_gnice": 0.0,
    "percent_idle": 60.05,
    "type": "cpu",
    "time": "01:58:14 PM"
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
    "proto": "tcp",
    "recv_q": 0,
    "send_q": 0,
    "local_address": "0.0.0.0",
    "foreign_address": "0.0.0.0",
    "state": "LISTEN",
    "user": "root",
    "inode": 30499,
    "program_name": "sshd",
    "kind": "network",
    "pid": 1186,
    "local_port": "ssh",
    "foreign_port": "*",
    "transport_protocol": "tcp",
    "network_protocol": "ipv4"
  },
  {
    "proto": "tcp",
    "recv_q": 0,
    "send_q": 0,
    "local_address": "localhost",
    "foreign_address": "localhost",
    "state": "ESTABLISHED",
    "user": "root",
    "inode": 46829,
    "program_name": "sshd: root",
    "kind": "network",
    "pid": 2242,
    "local_port": "ssh",
    "foreign_port": "52186",
    "transport_protocol": "tcp",
    "network_protocol": "ipv4",
    "foreign_port_num": 52186
  },
  {
    "proto": "tcp",
    "recv_q": 0,
    "send_q": 0,
    "local_address": "localhost",
    "foreign_address": "localhost",
    "state": "ESTABLISHED",
    "user": "root",
    "inode": 46828,
    "program_name": "ssh",
    "kind": "network",
    "pid": 2241,
    "local_port": "52186",
    "foreign_port": "ssh",
    "transport_protocol": "tcp",
    "network_protocol": "ipv4",
    "local_port_num": 52186
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
  },
  {
    "proto": "unix",
    "refcnt": 2,
    "flags": "ACC",
    "type": "SEQPACKET",
    "state": "LISTENING",
    "inode": 20835,
    "program_name": "init",
    "path": "/run/udev/control",
    "kind": "socket",
    "pid": 1
  }
]
```
```bash
netstat -r | jc --netstat -p          # or:  jc -p netstat -r
```
```json
[
  {
    "destination": "default",
    "gateway": "gateway",
    "genmask": "0.0.0.0",
    "route_flags": "UG",
    "mss": 0,
    "window": 0,
    "irtt": 0,
    "iface": "ens33",
    "kind": "route",
    "route_flags_pretty": [
      "UP",
      "GATEWAY"
    ]
  },
  {
    "destination": "172.17.0.0",
    "gateway": "0.0.0.0",
    "genmask": "255.255.0.0",
    "route_flags": "U",
    "mss": 0,
    "window": 0,
    "irtt": 0,
    "iface": "docker0",
    "kind": "route",
    "route_flags_pretty": [
      "UP"
    ]
  },
  {
    "destination": "192.168.71.0",
    "gateway": "0.0.0.0",
    "genmask": "255.255.255.0",
    "route_flags": "U",
    "mss": 0,
    "window": 0,
    "irtt": 0,
    "iface": "ens33",
    "kind": "route",
    "route_flags_pretty": [
      "UP"
    ]
  }
]
```
```bash
netstat -i | jc --netstat -p          # or:  jc -p netstat -i
```
```json
[
  {
    "iface": "ens33",
    "mtu": 1500,
    "rx_ok": 476,
    "rx_err": 0,
    "rx_drp": 0,
    "rx_ovr": 0,
    "tx_ok": 312,
    "tx_err": 0,
    "tx_drp": 0,
    "tx_ovr": 0,
    "flg": "BMRU",
    "kind": "interface"
  },
  {
    "iface": "lo",
    "mtu": 65536,
    "rx_ok": 0,
    "rx_err": 0,
    "rx_drp": 0,
    "rx_ovr": 0,
    "tx_ok": 0,
    "tx_err": 0,
    "tx_drp": 0,
    "tx_ovr": 0,
    "flg": "LRU",
    "kind": "interface"
  }
]
```
### nmcli
```bash
nmcli connection show ens33 | jc --nmcli -p          # or jc -p nmcli connection show ens33
```
```json
[
  {
    "connection_id": "ens33",
    "connection_uuid": "d92ece08-9e02-47d5-b2d2-92c80e155744",
    "connection_stable_id": null,
    "connection_type": "802-3-ethernet",
    "connection_interface_name": "ens33",
    "connection_autoconnect": "yes",
    "ip4_address_1": "192.168.71.180/24",
    "ip4_gateway": "192.168.71.2",
    "ip4_route_1": {
      "dst": "0.0.0.0/0",
      "nh": "192.168.71.2",
      "mt": 100
    },
    "ip4_route_2": {
      "dst": "192.168.71.0/24",
      "nh": "0.0.0.0",
      "mt": 100
    },
    "ip4_dns_1": "192.168.71.2",
    "ip4_domain_1": "localdomain",
    "dhcp4_option_1": {
      "name": "broadcast_address",
      "value": "192.168.71.255"
    },
    "ip6_address_1": "fe80::c1cb:715d:bc3e:b8a0/64",
    "ip6_gateway": null,
    "ip6_route_1": {
      "dst": "fe80::/64",
      "nh": "::",
      "mt": 100
    }
  }
]
```
### ntpq
```bash
ntpq -p | jc --ntpq -p          # or:  jc -p ntpq -p
```
```json
[
  {
    "remote": "44.190.6.254",
    "refid": "127.67.113.92",
    "st": 2,
    "t": "u",
    "when": 1,
    "poll": 64,
    "reach": 1,
    "delay": 23.399,
    "offset": -2.805,
    "jitter": 2.131,
    "state": null
  },
  {
    "remote": "mirror1.sjc02.s",
    "refid": "216.218.254.202",
    "st": 2,
    "t": "u",
    "when": 2,
    "poll": 64,
    "reach": 1,
    "delay": 29.325,
    "offset": 1.044,
    "jitter": 4.069,
    "state": null
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
    "username": "nobody",
    "password": "*",
    "uid": -2,
    "gid": -2,
    "comment": "Unprivileged User",
    "home": "/var/empty",
    "shell": "/usr/bin/false"
  },
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
### pidstat
```bash
pidstat -hl | jc --pidstat -p          # or  jc -p pidstat -hl
```
```json
[
  {
    "time": 1646859134,
    "uid": 0,
    "pid": 1,
    "percent_usr": 0.0,
    "percent_system": 0.03,
    "percent_guest": 0.0,
    "percent_cpu": 0.03,
    "cpu": 0,
    "command": "/usr/lib/systemd/systemd --switched-root --system..."
  },
  {
    "time": 1646859134,
    "uid": 0,
    "pid": 6,
    "percent_usr": 0.0,
    "percent_system": 0.0,
    "percent_guest": 0.0,
    "percent_cpu": 0.0,
    "cpu": 0,
    "command": "ksoftirqd/0"
  },
  {
    "time": 1646859134,
    "uid": 0,
    "pid": 2263,
    "percent_usr": 0.0,
    "percent_system": 0.0,
    "percent_guest": 0.0,
    "percent_cpu": 0.0,
    "cpu": 0,
    "command": "kworker/0:0"
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
### pip list
```bash
pip list | jc --pip-list -p          # or:  jc -p pip list          # or:  jc -p pip3 list
```
```json
[
  {
    "package": "ansible",
    "version": "2.8.5"
  },
  {
    "package": "antlr4-python3-runtime",
    "version": "4.7.2"
  },
  {
    "package": "asn1crypto",
    "version": "0.24.0"
  }
]
```
### pip show
```bash
pip show wrapt wheel | jc --pip-show -p          # or:  jc -p pip show wrapt wheel          # or:  jc -p pip3 show wrapt wheel
```
```json
[
  {
    "name": "wrapt",
    "version": "1.11.2",
    "summary": "Module for decorators, wrappers and monkey patching.",
    "home_page": "https://github.com/GrahamDumpleton/wrapt",
    "author": "Graham Dumpleton",
    "author_email": "Graham.Dumpleton@gmail.com",
    "license": "BSD",
    "location": "/usr/local/lib/python3.7/site-packages",
    "requires": null,
    "required_by": "astroid"
  },
  {
    "name": "wheel",
    "version": "0.33.4",
    "summary": "A built-package format for Python.",
    "home_page": "https://github.com/pypa/wheel",
    "author": "Daniel Holth",
    "author_email": "dholth@fastmail.fm",
    "license": "MIT",
    "location": "/usr/local/lib/python3.7/site-packages",
    "requires": null,
    "required_by": null
  }
]
```
### PLIST files
```bash
cat info.plist | jc --plist -p
```
```json
{
  "NSAppleScriptEnabled": true,
  "LSMultipleInstancesProhibited": true,
  "CFBundleInfoDictionaryVersion": "6.0",
  "DTPlatformVersion": "GM",
  "CFBundleIconFile": "GarageBand.icns",
  "CFBundleName": "GarageBand",
  "DTSDKName": "macosx10.13internal",
  "NSSupportsAutomaticGraphicsSwitching": true,
  "RevisionDate": "2018-12-03_14:10:56",
  "UTImportedTypeDeclarations": [
    {
      "UTTypeConformsTo": [
        "public.data",
        "public.content"
      ]
    }
  ]
}
```
### postconf -M
```bash
postconf -M | jc --postconf -p          # or jc -p postconf -M
```
```json
[
  {
    "service_name": "smtp",
    "service_type": "inet",
    "private": false,
    "unprivileged": null,
    "chroot": true,
    "wake_up_time": null,
    "process_limit": null,
    "command": "smtpd",
    "no_wake_up_before_first_use": null
  },
  {
    "service_name": "pickup",
    "service_type": "unix",
    "private": false,
    "unprivileged": null,
    "chroot": true,
    "wake_up_time": 60,
    "process_limit": 1,
    "command": "pickup",
    "no_wake_up_before_first_use": false
  }
]
```
### ps
```bash
ps -ef | jc --ps -p          # or:  jc -p ps -ef
```
```json
[
  {
    "uid": "root",
    "pid": 1,
    "ppid": 0,
    "c": 0,
    "stime": "Nov01",
    "tty": null,
    "time": "00:00:11",
    "cmd": "/usr/lib/systemd/systemd --switched-root --system --deserialize 22"
  },
  {
    "uid": "root",
    "pid": 2,
    "ppid": 0,
    "c": 0,
    "stime": "Nov01",
    "tty": null,
    "time": "00:00:00",
    "cmd": "[kthreadd]"
  },
  {
    "uid": "root",
    "pid": 4,
    "ppid": 2,
    "c": 0,
    "stime": "Nov01",
    "tty": null,
    "time": "00:00:00",
    "cmd": "[kworker/0:0H]"
  }
]
```
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
### route
```bash
route -ee | jc --route -p          # or:  jc -p route -ee
```
```json
[
  {
    "destination": "default",
    "gateway": "_gateway",
    "genmask": "0.0.0.0",
    "flags": "UG",
    "metric": 202,
    "ref": 0,
    "use": 0,
    "iface": "ens33",
    "mss": 0,
    "window": 0,
    "irtt": 0,
    "flags_pretty": [
      "UP",
      "GATEWAY"
    ]
  },
  {
    "destination": "192.168.71.0",
    "gateway": "0.0.0.0",
    "genmask": "255.255.255.0",
    "flags": "U",
    "metric": 202,
    "ref": 0,
    "use": 0,
    "iface": "ens33",
    "mss": 0,
    "window": 0,
    "irtt": 0,
    "flags_pretty": [
      "UP"
    ]
  }
]
```
### rpm -qi
```bash
rpm_qia | jc --rpm_qi -p          # or:  jc -p rpm -qia
```
```json
[
  {
    "name": "make",
    "epoch": 1,
    "version": "3.82",
    "release": "24.el7",
    "architecture": "x86_64",
    "install_date": "Wed 16 Oct 2019 09:21:42 AM PDT",
    "group": "Development/Tools",
    "size": 1160660,
    "license": "GPLv2+",
    "signature": "RSA/SHA256, Thu 22 Aug 2019 02:34:59 PM PDT, Key ID 24c6a8a7f4a80eb5",
    "source_rpm": "make-3.82-24.el7.src.rpm",
    "build_date": "Thu 08 Aug 2019 05:47:25 PM PDT",
    "build_host": "x86-01.bsys.centos.org",
    "relocations": "(not relocatable)",
    "packager": "CentOS BuildSystem <http://bugs.centos.org>",
    "vendor": "CentOS",
    "url": "http://www.gnu.org/software/make/",
    "summary": "A GNU tool which simplifies the build process for users",
    "description": "A GNU tool for controlling the generation of executables and other...",
    "build_epoch": 1565311645,
    "build_epoch_utc": null,
    "install_date_epoch": 1571242902,
    "install_date_epoch_utc": null
  },
  {
    "name": "kbd-legacy",
    "version": "1.15.5",
    "release": "15.el7",
    "architecture": "noarch",
    "install_date": "Thu 15 Aug 2019 10:53:08 AM PDT",
    "group": "System Environment/Base",
    "size": 503608,
    "license": "GPLv2+",
    "signature": "RSA/SHA256, Mon 12 Nov 2018 07:17:49 AM PST, Key ID 24c6a8a7f4a80eb5",
    "source_rpm": "kbd-1.15.5-15.el7.src.rpm",
    "build_date": "Tue 30 Oct 2018 03:40:00 PM PDT",
    "build_host": "x86-01.bsys.centos.org",
    "relocations": "(not relocatable)",
    "packager": "CentOS BuildSystem <http://bugs.centos.org>",
    "vendor": "CentOS",
    "url": "http://ftp.altlinux.org/pub/people/legion/kbd",
    "summary": "Legacy data for kbd package",
    "description": "The kbd-legacy package contains original keymaps for kbd package...",
    "build_epoch": 1540939200,
    "build_epoch_utc": null,
    "install_date_epoch": 1565891588,
    "install_date_epoch_utc": null
  }
]
```
### rsync
```bash
rsync -i -a source/ dest | jc --rsync -p          # or jc -p rsync -i -a source/ dest
```
```json
[
  {
    "summary": {
      "sent": 1708,
      "received": 8209,
      "bytes_sec": 19834.0,
      "total_size": 235,
      "speedup": 0.02
    },
    "files": [
      {
        "filename": "./",
        "metadata": ".d..t......",
        "update_type": "not updated",
        "file_type": "directory",
        "checksum_or_value_different": false,
        "size_different": false,
        "modification_time_different": true,
        "permissions_different": false,
        "owner_different": false,
        "group_different": false,
        "acl_different": false,
        "extended_attribute_different": false
      }
    ]
  }
]
```
### sfdisk
```bash
sfdisk -l | jc --sfdisk -p          # or jc -p sfdisk -l
```
```json
[
  {
    "disk": "/dev/sda",
    "cylinders": 2610,
    "heads": 255,
    "sectors_per_track": 63,
    "units": "cylinders of 8225280 bytes, blocks of 1024 bytes, counting from 0",
    "partitions": [
      {
        "device": "/dev/sda1",
        "boot": true,
        "start": 0,
        "end": 130,
        "cyls": 131,
        "blocks": 1048576,
        "id": "83",
        "system": "Linux"
      },
      {
        "device": "/dev/sda2",
        "boot": false,
        "start": 130,
        "end": 2610,
        "cyls": 2481,
        "blocks": 19921920,
        "id": "8e",
        "system": "Linux LVM"
      },
      {
        "device": "/dev/sda3",
        "boot": false,
        "start": 0,
        "end": null,
        "cyls": 0,
        "blocks": 0,
        "id": "0",
        "system": "Empty"
      },
      {
        "device": "/dev/sda4",
        "boot": false,
        "start": 0,
        "end": null,
        "cyls": 0,
        "blocks": 0,
        "id": "0",
        "system": "Empty"
      }
    ]
  },
  {
    "disk": "/dev/mapper/centos-root",
    "cylinders": 2218,
    "heads": 255,
    "sectors_per_track": 63
  },
  {
    "disk": "/dev/mapper/centos-swap",
    "cylinders": 261,
    "heads": 255,
    "sectors_per_track": 63
  }
]
```
### /etc/shadow file
```bash
cat /etc/shadow | jc --shadow -p
```
```json
[
  {
    "username": "root",
    "password": "*",
    "last_changed": 18113,
    "minimum": 0,
    "maximum": 99999,
    "warn": 7,
    "inactive": null,
    "expire": null
  },
  {
    "username": "daemon",
    "password": "*",
    "last_changed": 18113,
    "minimum": 0,
    "maximum": 99999,
    "warn": 7,
    "inactive": null,
    "expire": null
  },
  {
    "username": "bin",
    "password": "*",
    "last_changed": 18113,
    "minimum": 0,
    "maximum": 99999,
    "warn": 7,
    "inactive": null,
    "expire": null
  }
]
```
### ss
```bash
ss -a | jc --ss -p          # or:  jc -p ss -a
```
```json
[
  {
    "netid": "nl",
    "state": "UNCONN",
    "recv_q": 0,
    "send_q": 0,
    "peer_address": "*",
    "channel": "rtnl:kernel"
  },
  {
    "netid": "nl",
    "state": "UNCONN",
    "recv_q": 0,
    "send_q": 0,
    "peer_address": "*",
    "pid": 893,
    "channel": "rtnl:systemd-resolve"
  },
  {
    "netid": "p_raw",
    "state": "UNCONN",
    "recv_q": 0,
    "send_q": 0,
    "peer_address": "*",
    "link_layer": "LLDP",
    "interface": "ens33"
  },
  {
    "netid": "u_dgr",
    "state": "UNCONN",
    "recv_q": 0,
    "send_q": 0,
    "local_port": "93066",
    "peer_address": "*",
    "peer_port": "0",
    "path": "/run/user/1000/systemd/notify"
  },
  {
    "netid": "u_seq",
    "state": "LISTEN",
    "recv_q": 0,
    "send_q": 128,
    "local_port": "20699",
    "peer_address": "*",
    "peer_port": "0",
    "path": "/run/udev/control"
  },
  {
    "netid": "icmp6",
    "state": "UNCONN",
    "recv_q": 0,
    "send_q": 0,
    "local_address": "*",
    "local_port": "ipv6-icmp",
    "peer_address": "*",
    "peer_port": "*",
    "interface": "ens33"
  },
  {
    "netid": "udp",
    "state": "UNCONN",
    "recv_q": 0,
    "send_q": 0,
    "local_address": "127.0.0.53",
    "local_port": "domain",
    "peer_address": "0.0.0.0",
    "peer_port": "*",
    "interface": "lo"
  },
  {
    "netid": "tcp",
    "state": "LISTEN",
    "recv_q": 0,
    "send_q": 128,
    "local_address": "127.0.0.53",
    "local_port": "domain",
    "peer_address": "0.0.0.0",
    "peer_port": "*",
    "interface": "lo"
  },
  {
    "netid": "tcp",
    "state": "LISTEN",
    "recv_q": 0,
    "send_q": 128,
    "local_address": "0.0.0.0",
    "local_port": "ssh",
    "peer_address": "0.0.0.0",
    "peer_port": "*"
  },
  {
    "netid": "tcp",
    "state": "LISTEN",
    "recv_q": 0,
    "send_q": 128,
    "local_address": "[::]",
    "local_port": "ssh",
    "peer_address": "[::]",
    "peer_port": "*"
  },
  {
    "netid": "v_str",
    "state": "ESTAB",
    "recv_q": 0,
    "send_q": 0,
    "local_address": "999900439",
    "local_port": "1023",
    "peer_address": "0",
    "peer_port": "976",
    "local_port_num": 1023,
    "peer_port_num": 976
  }
]
```
### stat
```bash
stat /bin/* | jc --stat -p          # or:  jc -p stat /bin/*
```
```json
[
  {
    "file": "/bin/bash",
    "size": 1113504,
    "blocks": 2176,
    "io_blocks": 4096,
    "type": "regular file",
    "device": "802h/2050d",
    "inode": 131099,
    "links": 1,
    "access": "0755",
    "flags": "-rwxr-xr-x",
    "uid": 0,
    "user": "root",
    "gid": 0,
    "group": "root",
    "access_time": "2019-11-14 08:18:03.509681766 +0000",
    "modify_time": "2019-06-06 22:28:15.000000000 +0000",
    "change_time": "2019-08-12 17:21:29.521945390 +0000",
    "birth_time": null,
    "access_time_epoch": 1573748283,
    "access_time_epoch_utc": 1573719483,
    "modify_time_epoch": 1559885295,
    "modify_time_epoch_utc": 1559860095,
    "change_time_epoch": 1565655689,
    "change_time_epoch_utc": 1565630489,
    "birth_time_epoch": null,
    "birth_time_epoch_utc": null
  },
  {
    "file": "/bin/btrfs",
    "size": 716464,
    "blocks": 1400,
    "io_blocks": 4096,
    "type": "regular file",
    "device": "802h/2050d",
    "inode": 131100,
    "links": 1,
    "access": "0755",
    "flags": "-rwxr-xr-x",
    "uid": 0,
    "user": "root",
    "gid": 0,
    "group": "root",
    "access_time": "2019-11-14 08:18:28.990834276 +0000",
    "modify_time": "2018-03-12 23:04:27.000000000 +0000",
    "change_time": "2019-08-12 17:21:29.545944399 +0000",
    "birth_time": null,
    "access_time_epoch": 1573748308,
    "access_time_epoch_utc": 1573719508,
    "modify_time_epoch": 1520921067,
    "modify_time_epoch_utc": 1520895867,
    "change_time_epoch": 1565655689,
    "change_time_epoch_utc": 1565630489,
    "birth_time_epoch": null,
    "birth_time_epoch_utc": null
  }
]
```
### sysctl
```bash
sysctl -a | jc --sysctl -p          # or:  jc -p sysctl -a
```
```json
{
  "user.cs_path": "/usr/bin:/bin:/usr/sbin:/sbin",
  "user.bc_base_max": 99,
  "user.bc_dim_max": 2048,
  "user.bc_scale_max": 99,
  "user.bc_string_max": 1000,
  "user.coll_weights_max": 2,
  "user.expr_nest_max": 32
}
```
### Syslog strings (RFC 5424)
```bash
cat syslog.txt | jc --syslog -p
```
```json
[
  {
    "priority": 35,
    "version": 1,
    "timestamp": "2003-10-11T22:14:15.003Z",
    "hostname": "mymachine.example.com",
    "appname": "evntslog",
    "proc_id": null,
    "msg_id": "ID47",
    "structured_data": [
      {
        "identity": "exampleSDID@32473",
        "parameters": {
          "iut": "3",
          "eventSource": "Application",
          "eventID": "1011"
        }
      },
      {
        "identity": "examplePriority@32473",
        "parameters": {
          "class": "high"
        }
      }
    ],
    "message": "unauthorized attempt",
    "timestamp_epoch": 1065935655,
    "timestamp_epoch_utc": 1065910455
  }
]
```
### Syslog strings (RFC 3164)
```bash
cat syslog.txt | jc --syslog-bsd -p
```
```json
[
  {
    "priority": 34,
    "date": "Oct 11 22:14:15",
    "hostname": "mymachine",
    "tag": "su",
    "content": "'su root' failed for lonvick on /dev/pts/8"
  }
]
```
### systemctl
```bash
systemctl -a | jc --systemctl -p          # or:  jc -p systemctl -a
```
```json
[
  {
    "unit": "proc-sys-fs-binfmt_misc.automount",
    "load": "loaded",
    "active": "active",
    "sub": "waiting",
    "description": "Arbitrary Executable File Formats File System Automount Point"
  },
  {
    "unit": "dev-block-8:2.device",
    "load": "loaded",
    "active": "active",
    "sub": "plugged",
    "description": "LVM PV 3klkIj-w1qk-DkJi-0XBJ-y3o7-i2Ac-vHqWBM on /dev/sda2 2"
  },
  {
    "unit": "dev-cdrom.device",
    "load": "loaded",
    "active": "active",
    "sub": "plugged",
    "description": "VMware_Virtual_IDE_CDROM_Drive"
  }
]
```
### systemctl list-jobs
```bash
systemctl list-jobs | jc --systemctl-lj -p          # or:  jc -p systemctl list-jobs
```
```json
[
  {
    "job": 3543,
    "unit": "nginxAfterGlusterfs.service",
    "type": "start",
    "state": "waiting"
  },
  {
    "job": 3545,
    "unit": "glusterReadyForLocalhostMount.service",
    "type": "start",
    "state": "running"
  },
  {
    "job": 3506,
    "unit": "nginx.service",
    "type": "start",
    "state": "waiting"
  }
]
```
### systemctl list-sockets
```bash
systemctl list-sockets | jc --systemctl-ls -p          # or:  jc -p systemctl list-sockets
```
```json
[
  {
    "listen": "/dev/log",
    "unit": "systemd-journald.socket",
    "activates": "systemd-journald.service"
  },
  {
    "listen": "/run/dbus/system_bus_socket",
    "unit": "dbus.socket",
    "activates": "dbus.service"
  },
  {
    "listen": "/run/dmeventd-client",
    "unit": "dm-event.socket",
    "activates": "dm-event.service"
  }
]
```
### systemctl list-unit-files
```bash
systemctl list-unit-files | jc --systemctl-luf -p          # or:  jc -p systemctl list-unit-files
```
```json
[
  {
    "unit_file": "proc-sys-fs-binfmt_misc.automount",
    "state": "static"
  },
  {
    "unit_file": "dev-hugepages.mount",
    "state": "static"
  },
  {
    "unit_file": "dev-mqueue.mount",
    "state": "static"
  }
]
```
### systeminfo
```bash
systeminfo | jc --systeminfo -p          # or:  jc -p systeminfo
```
```json
{
  "host_name": "TESTLAPTOP",
  "os_name": "Microsoft Windows 10 Enterprise",
  "os_version": "10.0.17134 N/A Build 17134",
  "os_manufacturer": "Microsoft Corporation",
  "os_configuration": "Member Workstation",
  "os_build_type": "Multiprocessor Free",
  "registered_owner": "Test, Inc.",
  "registered_organization": "Test, Inc.",
  "product_id": "11111-11111-11111-AA111",
  "original_install_date": "3/26/2019, 3:51:30 PM",
  "system_boot_time": "3/30/2021, 6:13:59 AM",
  "system_manufacturer": "Dell Inc.",
  "system_model": "Precision 5530",
  "system_type": "x64-based PC",
  "processors": [
    "Intel64 Family 6 Model 158 Stepping 10 GenuineIntel ~2592 Mhz"
  ],
  "bios_version": "Dell Inc. 1.16.2, 4/21/2020",
  "windows_directory": "C:\\WINDOWS",
  "system_directory": "C:\\WINDOWS\\system32",
  "boot_device": "\\Device\\HarddiskVolume2",
  "system_locale": "en-us;English (United States)",
  "input_locale": "en-us;English (United States)",
  "time_zone": "(UTC+00:00) UTC",
  "total_physical_memory_mb": 32503,
  "available_physical_memory_mb": 19743,
  "virtual_memory_max_size_mb": 37367,
  "virtual_memory_available_mb": 22266,
  "virtual_memory_in_use_mb": 15101,
  "page_file_locations": "C:\\pagefile.sys",
  "domain": "test.com",
  "logon_server": "\\\\TESTDC01",
  "hotfixs": [
    "KB2693643",
    "KB4601054"
  ],
  "network_cards": [
    {
      "name": "Intel(R) Wireless-AC 9260 160MHz",
      "connection_name": "Wi-Fi",
      "status": null,
      "dhcp_enabled": true,
      "dhcp_server": "192.168.2.1",
      "ip_addresses": [
        "192.168.2.219"
      ]
    }
  ],
  "hyperv_requirements": {
    "vm_monitor_mode_extensions": true,
    "virtualization_enabled_in_firmware": true,
    "second_level_address_translation": false,
    "data_execution_prevention_available": true
  },
  "original_install_date_epoch": 1553640690,
  "original_install_date_epoch_utc": 1553615490,
  "system_boot_time_epoch": 1617110039,
  "system_boot_time_epoch_utc": 1617084839
}
```
### /usr/bin/time
```bash
/usr/bin/time --verbose -o timefile.out sleep 2.5; cat timefile.out | jc --time -p
```
```json
{
  "command_being_timed": "sleep 2.5",
  "user_time": 0.0,
  "system_time": 0.0,
  "cpu_percent": 0,
  "elapsed_time": "0:02.50",
  "average_shared_text_size": 0,
  "average_unshared_data_size": 0,
  "average_stack_size": 0,
  "average_total_size": 0,
  "maximum_resident_set_size": 2084,
  "average_resident_set_size": 0,
  "major_pagefaults": 0,
  "minor_pagefaults": 72,
  "voluntary_context_switches": 2,
  "involuntary_context_switches": 1,
  "swaps": 0,
  "block_input_operations": 0,
  "block_output_operations": 0,
  "messages_sent": 0,
  "messages_received": 0,
  "signals_delivered": 0,
  "page_size": 4096,
  "exit_status": 0,
  "elapsed_time_hours": 0,
  "elapsed_time_minutes": 0,
  "elapsed_time_seconds": 2,
  "elapsed_time_centiseconds": 50,
  "elapsed_time_total_seconds": 2.5
}
```
### timedatectl status
```bash
timedatectl | jc --timedatectl -p          # or: jc -p timedatectl
```
```json
{
  "local_time": "Tue 2020-03-10 17:53:21 PDT",
  "universal_time": "Wed 2020-03-11 00:53:21 UTC",
  "rtc_time": "Wed 2020-03-11 00:53:21",
  "time_zone": "America/Los_Angeles (PDT, -0700)",
  "ntp_enabled": true,
  "ntp_synchronized": true,
  "rtc_in_local_tz": false,
  "dst_active": true,
  "epoch_utc": 1583888001
}
```
### Timestamp strings (UNIX Epoch)
```bash
echo '1658599410' | jc --timestamp -p
```
```json
{
  "naive": {
    "year": 2022,
    "month": "Jul",
    "month_num": 7,
    "day": 23,
    "weekday": "Sat",
    "weekday_num": 6,
    "hour": 11,
    "hour_24": 11,
    "minute": 3,
    "second": 30,
    "period": "AM",
    "day_of_year": 204,
    "week_of_year": 29,
    "iso": "2022-07-23T11:03:30"
  },
  "utc": {
    "year": 2022,
    "month": "Jul",
    "month_num": 7,
    "day": 23,
    "weekday": "Sat",
    "weekday_num": 6,
    "hour": 6,
    "hour_24": 18,
    "minute": 3,
    "second": 30,
    "period": "PM",
    "utc_offset": "+0000",
    "day_of_year": 204,
    "week_of_year": 29,
    "iso": "2022-07-23T18:03:30+00:00"
  }
}
```
### tob -b
```bash
top -b -n 1 | jc --top -p          # or jc -p tob -b -n 1
```
```json
[
  {
    "time": "11:20:43",
    "uptime": 118,
    "users": 2,
    "load_1m": 0.0,
    "load_5m": 0.01,
    "load_15m": 0.05,
    "tasks_total": 108,
    "tasks_running": 2,
    "tasks_sleeping": 106,
    "tasks_stopped": 0,
    "tasks_zombie": 0,
    "cpu_user": 5.6,
    "cpu_sys": 11.1,
    "cpu_nice": 0.0,
    "cpu_idle": 83.3,
    "cpu_wait": 0.0,
    "cpu_hardware": 0.0,
    "cpu_software": 0.0,
    "cpu_steal": 0.0,
    "mem_total": 3.7,
    "mem_free": 3.3,
    "mem_used": 0.2,
    "mem_buff_cache": 0.2,
    "swap_total": 2.0,
    "swap_free": 2.0,
    "swap_used": 0.0,
    "mem_available": 3.3,
    "processes": [
      {
        "pid": 2225,
        "user": "kbrazil",
        "priority": 20,
        "nice": 0,
        "virtual_mem": 158.1,
        "resident_mem": 2.2,
        "shared_mem": 1.6,
        "status": "running",
        "percent_cpu": 12.5,
        "percent_mem": 0.1,
        "time_hundredths": "0:00.02",
        "command": "top",
        "parent_pid": 1884,
        "uid": 1000,
        "real_uid": 1000,
        "real_user": "kbrazil",
        "saved_uid": 1000,
        "saved_user": "kbrazil",
        "gid": 1000,
        "group": "kbrazil",
        "pgrp": 2225,
        "tty": "pts/0",
        "tty_process_gid": 2225,
        "session_id": 1884,
        "thread_count": 1,
        "last_used_processor": 0,
        "time": "0:00",
        "swap": 0.0,
        "code": 0.1,
        "data": 1.0,
        "major_page_fault_count": 0,
        "minor_page_fault_count": 736,
        "dirty_pages_count": 0,
        "sleeping_in_function": null,
        "flags": "..4.2...",
        "cgroups": "1:name=systemd:/user.slice/user-1000.+",
        "supplementary_gids": [
          10,
          1000
        ],
        "supplementary_groups": [
          "wheel",
          "kbrazil"
        ],
        "thread_gid": 2225,
        "environment_variables": [
          "XDG_SESSION_ID=2",
          "HOSTNAME=localhost"
        ],
        "major_page_fault_count_delta": 0,
        "minor_page_fault_count_delta": 4,
        "used": 2.2,
        "ipc_namespace_inode": 4026531839,
        "mount_namespace_inode": 4026531840,
        "net_namespace_inode": 4026531956,
        "pid_namespace_inode": 4026531836,
        "user_namespace_inode": 4026531837,
        "nts_namespace_inode": 4026531838
      }
    ]
  }
]
```
### tracepath
```bash
tracepath6 3ffe:2400:0:109::2 | jc --tracepath -p
```
```json
{
  "pmtu": 1480,
  "forward_hops": 2,
  "return_hops": 2,
  "hops": [
    {
      "ttl": 1,
      "guess": true,
      "host": "[LOCALHOST]",
      "reply_ms": null,
      "pmtu": 1500,
      "asymmetric_difference": null,
      "reached": false
    },
    {
      "ttl": 1,
      "guess": false,
      "host": "dust.inr.ac.ru",
      "reply_ms": 0.411,
      "pmtu": null,
      "asymmetric_difference": null,
      "reached": false
    },
    {
      "ttl": 2,
      "guess": false,
      "host": "dust.inr.ac.ru",
      "reply_ms": 0.39,
      "pmtu": 1480,
      "asymmetric_difference": 1,
      "reached": false
    },
    {
      "ttl": 2,
      "guess": false,
      "host": "3ffe:2400:0:109::2",
      "reply_ms": 463.514,
      "pmtu": null,
      "asymmetric_difference": null,
      "reached": true
    }
  ]
}
```
### traceroute
```bash
traceroute -m 3 8.8.8.8 | jc --traceroute -p          # or:  jc -p traceroute -m 3 8.8.8.8
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
    },
    {
      "hop": 3,
      "probes": []
    }
  ]
}
```
### ufw status
```bash
ufw status verbose  | jc --ufw -p          # or jc -p ufw status verbose
```
```json
{
  "status": "active",
  "logging": "on",
  "logging_level": "low",
  "default": "deny (incoming), allow (outgoing), disabled (routed)",
  "new_profiles": "skip",
  "rules": [
    {
      "action": "ALLOW",
      "action_direction": "IN",
      "index": null,
      "network_protocol": "ipv4",
      "to_interface": "any",
      "to_transport": "any",
      "to_service": null,
      "to_ports": [
        22
      ],
      "to_ip": "0.0.0.0",
      "to_ip_prefix": 0,
      "comment": null,
      "from_ip": "0.0.0.0",
      "from_ip_prefix": 0,
      "from_interface": "any",
      "from_transport": "any",
      "from_port_ranges": [
        {
          "start": 0,
          "end": 65535
        }
      ],
      "from_service": null
    },
    {
      "action": "ALLOW",
      "action_direction": "IN",
      "index": null,
      "network_protocol": "ipv4",
      "to_interface": "any",
      "to_transport": "tcp",
      "to_service": null,
      "to_ports": [
        80,
        443
      ],
      "to_ip": "0.0.0.0",
      "to_ip_prefix": 0,
      "comment": null,
      "from_ip": "0.0.0.0",
      "from_ip_prefix": 0,
      "from_interface": "any",
      "from_transport": "any",
      "from_port_ranges": [
        {
          "start": 0,
          "end": 65535
        }
      ],
      "from_service": null
    }
  ]
}
```
### ufw app info [application]
```bash
ufw app info MSN | jc --ufw-appinfo -p          # or:  jc -p ufw app info MSN
```
```json
[
  {
    "profile": "MSN",
    "title": "MSN Chat",
    "description": "MSN chat protocol (with file transfer and voice)",
    "tcp_list": [
      1863,
      6901
    ],
    "udp_list": [
      1863,
      6901
    ],
    "tcp_ranges": [
      {
        "start": 6891,
        "end": 6900
      }
    ],
    "normalized_tcp_list": [
      1863,
      6901
    ],
    "normalized_tcp_ranges": [
      {
        "start": 6891,
        "end": 6900
      }
    ],
    "normalized_udp_list": [
      1863,
      6901
    ]
  }
]
```
### uname -a
```bash
uname -a | jc --uname -p          # or:  jc -p uname -a
```
```json
{
  "kernel_name": "Linux",
  "node_name": "user-ubuntu",
  "kernel_release": "4.15.0-65-generic",
  "operating_system": "GNU/Linux",
  "hardware_platform": "x86_64",
  "processor": "x86_64",
  "machine": "x86_64",
  "kernel_version": "#74-Ubuntu SMP Tue Sep 17 17:06:04 UTC 2019"
}
```
### update-alternatives --get-selections
```bash
update-alternatives --get-selections | jc --update-alt-gs -p          # or:  jc -p update-alternatives --get-selections
```
```json
[
  {
    "name": "arptables",
    "status": "auto",
    "current": "/usr/sbin/arptables-nft"
  },
  {
    "name": "awk",
    "status": "auto",
    "current": "/usr/bin/gawk"
  }
]
```
### update-alternatives --query
```bash
update-alternatives --query editor | jc --update-alt-q -p          # or:  jc -p update-alternatives --query editor
```
```json
{
  "name": "editor",
  "link": "/usr/bin/editor",
  "slaves": [
    {
      "name": "editor.1.gz",
      "path": "/usr/share/man/man1/editor.1.gz"
    },
    {
      "name": "editor.da.1.gz",
      "path": "/usr/share/man/da/man1/editor.1.gz"
    }
  ],
  "status": "auto",
  "best": "/bin/nano",
  "value": "/bin/nano",
  "alternatives": [
    {
      "name": "/bin/ed",
      "priority": -100,
      "slaves": [
        {
          "name": "editor.1.gz",
          "path": "/usr/share/man/man1/ed.1.gz"
        }
      ]
    },
    {
      "name": "/bin/nano",
      "priority": 40,
      "slaves": [
        {
          "name": "editor.1.gz",
          "path": "/usr/share/man/man1/nano.1.gz"
        }
      ]
    }
  ]
}
```
### upower
```bash
upower -i /org/freedesktop/UPower/devices/battery | jc --upower -p          # or jc -p upower -i /org/freedesktop/UPower/devices/battery
```
```json
[
  {
    "native_path": "/sys/devices/LNXSYSTM:00/device:00/PNP0C0A:00/power_supply/BAT0",
    "vendor": "NOTEBOOK",
    "model": "BAT",
    "serial": "0001",
    "power_supply": true,
    "updated": "Thu 11 Mar 2021 06:28:08 PM UTC",
    "has_history": true,
    "has_statistics": true,
    "detail": {
      "type": "battery",
      "present": true,
      "rechargeable": true,
      "state": "charging",
      "energy": 22.3998,
      "energy_empty": 0.0,
      "energy_full": 52.6473,
      "energy_full_design": 62.16,
      "energy_rate": 31.6905,
      "voltage": 12.191,
      "time_to_full": 57.3,
      "percentage": 42.5469,
      "capacity": 84.6964,
      "technology": "lithium-ion",
      "energy_unit": "Wh",
      "energy_empty_unit": "Wh",
      "energy_full_unit": "Wh",
      "energy_full_design_unit": "Wh",
      "energy_rate_unit": "W",
      "voltage_unit": "V",
      "time_to_full_unit": "minutes"
    },
    "history_charge": [
      {
        "time": 1328809335,
        "percent_charged": 42.547,
        "status": "charging"
      },
      {
        "time": 1328809305,
        "percent_charged": 42.02,
        "status": "charging"
      }
    ],
    "history_rate": [
      {
        "time": 1328809335,
        "percent_charged": 31.691,
        "status": "charging"
      }
    ],
    "updated_seconds_ago": 441975,
    "updated_epoch": 1615516088,
    "updated_epoch_utc": 1615487288
  }
]
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
### URL string
```bash
echo "http://example.com/test/path?q1=foo&q1=bar&q2=baz#frag" \\
     | jc --url -p
```
```json
{
  "url": "http://example.com/test/path?q1=foo&q1=bar&q2=baz#frag",
  "scheme": "http",
  "netloc": "example.com",
  "path": "/test/path",
  "path_list": [
    "test",
    "path"
  ],
  "query": "q1=foo&q1=bar&q2=baz",
  "query_obj": {
    "q1": [
      "foo",
      "bar"
    ],
    "q2": [
      "baz"
    ]
  },
  "fragment": "frag",
  "username": null,
  "password": null,
  "hostname": "example.com",
  "port": null,
  "encoded": {
    "url": "http://example.com/test/path?q1=foo&q1=bar&q2=baz#frag",
    "scheme": "http",
    "netloc": "example.com",
    "path": "/test/path",
    "path_list": [
      "test",
      "path"
    ],
    "query": "q1=foo&q1=bar&q2=baz",
    "fragment": "frag",
    "username": null,
    "password": null,
    "hostname": "example.com",
    "port": null
  },
  "decoded": {
    "url": "http://example.com/test/path?q1=foo&q1=bar&q2=baz#frag",
    "scheme": "http",
    "netloc": "example.com",
    "path": "/test/path",
    "path_list": [
      "test",
      "path"
    ],
    "query": "q1=foo&q1=bar&q2=baz",
    "fragment": "frag",
    "username": null,
    "password": null,
    "hostname": "example.com",
    "port": null
  }
}
```
### w
```bash
w | jc --w -p          # or:  jc -p w
```
```json
[
  {
    "user": "root",
    "tty": "tty1",
    "from": null,
    "login_at": "07:49",
    "idle": "1:15m",
    "jcpu": "0.00s",
    "pcpu": "0.00s",
    "what": "-bash"
  },
  {
    "user": "root",
    "tty": "ttyS0",
    "from": null,
    "login_at": "06:24",
    "idle": "0.00s",
    "jcpu": "0.43s",
    "pcpu": "0.00s",
    "what": "w"
  },
  {
    "user": "root",
    "tty": "pts/0",
    "from": "192.168.71.1",
    "login_at": "06:29",
    "idle": "2:35m",
    "jcpu": "0.00s",
    "pcpu": "0.00s",
    "what": "-bash"
  }
]
```
### wc
```bash
wc * | jc --wc -p          # or:  jc -p wc *
```
```json
[
      {
        "filename": "airport-I.json",
        "lines": 1,
        "words": 30,
        "characters": 307
      },
      {
        "filename": "airport-I.out",
        "lines": 15,
        "words": 33,
        "characters": 348
      },
      {
        "filename": "airport-s.json",
        "lines": 1,
        "words": 202,
        "characters": 2152
      }
    ]
```
### who
```bash
who | jc --who -p          # or:  jc -p who
```
```json
[
  {
    "user": "joeuser",
    "tty": "ttyS0",
    "time": "2020-03-02 02:52",
    "epoch": 1583146320
  },
  {
    "user": "joeuser",
    "tty": "pts/0",
    "time": "2020-03-02 05:15",
    "from": "192.168.71.1",
    "epoch": 1583154900
  }
]
```
```bash
who -a | jc --who -p          # or:  jc -p who -a
```
```json
[
  {
    "event": "reboot",
    "time": "Feb 7 23:31",
    "pid": 1,
    "epoch": null
  },
  {
    "user": "joeuser",
    "writeable_tty": "+",
    "tty": "ttys004",
    "time": "Mar 1 16:35",
    "idle": ".",
    "pid": 15679,
    "from": "192.168.1.5",
    "epoch": null
  }
]
```
### X.509 PEM and DER certificate files
```bash
cat entrust.pem | jc --x509-cert -p
```
```json
[
  {
    "tbs_certificate": {
      "version": "v3",
      "serial_number": "a6:8b:79:29:00:00:00:00:50:d0:91:f9",
      "signature": {
        "algorithm": "sha384_ecdsa",
        "parameters": null
      },
      "issuer": {
        "country_name": "US",
        "organization_name": "Entrust, Inc.",
        "organizational_unit_name": [
          "See www.entrust.net/legal-terms",
          "(c) 2012 Entrust, Inc. - for authorized use only"
        ],
        "common_name": "Entrust Root Certification Authority - EC1"
      },
      "validity": {
        "not_before": 1355844336,
        "not_after": 2144764536,
        "not_before_iso": "2012-12-18T15:25:36+00:00",
        "not_after_iso": "2037-12-18T15:55:36+00:00"
      },
      "subject": {
        "country_name": "US",
        "organization_name": "Entrust, Inc.",
        "organizational_unit_name": [
          "See www.entrust.net/legal-terms",
          "(c) 2012 Entrust, Inc. - for authorized use only"
        ],
        "common_name": "Entrust Root Certification Authority - EC1"
      },
      "subject_public_key_info": {
        "algorithm": {
          "algorithm": "ec",
          "parameters": "secp384r1"
        },
        "public_key": "04:84:13:c9:d0:ba:6d:41:7b:e2:6c:d0:eb:55:5f:66:02:1a:24:f4:5b:89:69:47:e3:b8:c2:7d:f1:f2:02:c5:9f:a0:f6:5b:d5:8b:06:19:86:4f:53:10:6d:07:24:27:a1:a0:f8:d5:47:19:61:4c:7d:ca:93:27:ea:74:0c:ef:6f:96:09:fe:63:ec:70:5d:36:ad:67:77:ae:c9:9d:7c:55:44:3a:a2:63:51:1f:f5:e3:62:d4:a9:47:07:3e:cc:20"
      },
      "issuer_unique_id": null,
      "subject_unique_id": null,
      "extensions": [
        {
          "extn_id": "key_usage",
          "critical": true,
          "extn_value": [
            "key_cert_sign",
            "crl_sign"
          ]
        },
        {
          "extn_id": "basic_constraints",
          "critical": true,
          "extn_value": {
            "ca": true,
            "path_len_constraint": null
          }
        },
        {
          "extn_id": "key_identifier",
          "critical": false,
          "extn_value": "b7:63:e7:1a:dd:8d:e9:08:a6:55:83:a4:e0:6a:50:41:65:11:42:49"
        }
      ]
    },
    "signature_algorithm": {
      "algorithm": "sha384_ecdsa",
      "parameters": null
    },
    "signature_value": "30:64:02:30:61:79:d8:e5:42:47:df:1c:ae:53:99:17:b6:6f:1c:7d:e1:bf:11:94:d1:03:88:75:e4:8d:89:a4:8a:77:46:de:6d:61:ef:02:f5:fb:b5:df:cc:fe:4e:ff:fe:a9:e6:a7:02:30:5b:99:d7:85:37:06:b5:7b:08:fd:eb:27:8b:4a:94:f9:e1:fa:a7:8e:26:08:e8:7c:92:68:6d:73:d8:6f:26:ac:21:02:b8:99:b7:26:41:5b:25:60:ae:d0:48:1a:ee:06"
  }
]
```
### X.509 PEM and DER certificate request files
```bash
cat myserver.csr | jc --x509-csr -p
```
```json
[
  {
    "certification_request_info": {
      "version": "v1",
      "subject": {
        "common_name": "myserver.for.example"
      },
      "subject_pk_info": {
        "algorithm": {
          "algorithm": "ec",
          "parameters": "secp256r1"
        },
        "public_key": "04:40:33:c0:91:8f:e9:46:ea:d0:dc:d0:f9:63:2c:a4:35:1f:0f:54:c8:a9:9b:e3:9e:d4:f3:64:b8:60:cc:7f:39:75:dd:a7:61:31:02:7c:9e:89:c6:db:45:15:f2:5f:b0:65:29:0b:42:d2:6e:c2:ea:a6:23:bd:fc:65:e5:7d:4e"
      },
      "attributes": [
        {
          "type": "extension_request",
          "values": [
            [
              {
                "extn_id": "extended_key_usage",
                "critical": false,
                "extn_value": [
                  "server_auth"
                ]
              },
              {
                "extn_id": "subject_alt_name",
                "critical": false,
                "extn_value": [
                  "myserver.for.example"
                ]
              }
            ]
          ]
        }
      ]
    },
    "signature_algorithm": {
      "algorithm": "sha384_ecdsa",
      "parameters": null
    },
    "signature": "30:45:02:20:77:ac:5b:51:bf:c5:f5:43:02:52:ae:66:8a:fe:95:98:98:98:a9:45:34:31:08:ff:2c:cc:92:d9:1c:70:28:74:02:21:00:97:79:7b:e7:45:18:76:cf:d7:3b:79:34:56:d2:69:b5:73:41:9b:8a:b7:ad:ec:80:23:c1:2f:64:da:e5:28:19"
  }
]
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
### xrandr
```bash
$ xrandr | jc --xrandr -p          # or  jc -p xrandr
```
```json
{
  "screens": [
    {
      "screen_number": 0,
      "minimum_width": 8,
      "minimum_height": 8,
      "current_width": 1920,
      "current_height": 1080,
      "maximum_width": 32767,
      "maximum_height": 32767,
      "associated_device": {
        "associated_modes": [
          {
            "resolution_width": 1920,
            "resolution_height": 1080,
            "is_high_resolution": false,
            "frequencies": [
              {
                "frequency": 60.03,
                "is_current": true,
                "is_preferred": true
              },
              {
                "frequency": 59.93,
                "is_current": false,
                "is_preferred": false
              }
            ]
          },
          {
            "resolution_width": 1680,
            "resolution_height": 1050,
            "is_high_resolution": false,
            "frequencies": [
              {
                "frequency": 59.88,
                "is_current": false,
                "is_preferred": false
              }
            ]
          }
        ],
        "is_connected": true,
        "is_primary": true,
        "device_name": "eDP1",
        "resolution_width": 1920,
        "resolution_height": 1080,
        "offset_width": 0,
        "offset_height": 0,
        "dimension_width": 310,
        "dimension_height": 170
      }
    }
  ],
  "unassociated_devices": []
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
### zipinfo
```bash
zipinfo file.zip | jc --zipinfo -p          # or:  jc -p zipinfo file.zip
```
```json
[
  {
    "archive": "file.zip",
    "size": 4116,
    "size_unit": "bytes",
    "number_entries": 1,
    "number_files": 1,
    "bytes_uncompressed": 11837,
    "bytes_compressed": 3966,
    "percent_compressed": 66.5,
    "files": [
      {
        "flags": "-rw-r--r--",
        "zipversion": "2.1",
        "zipunder": "unx",
        "filesize": 11837,
        "type": "bX",
        "method": "defN",
        "date": "21-Dec-08",
        "time": "20:50",
        "filename": "compressed_file"
      }
    ]
  }
]
```

© 2019-2021 Kelly Brazil
