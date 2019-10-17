# JC
JSON CLI output utility

`jc` is used to JSONify the output of many standard linux cli tools for easier parsing in scripts. Parsers for `ls`, `ifconfig`, and `netstat` are currently included and more can be added via modules.

## Usage
`jc` accepts piped input from `STDIN` and outputs a JSON representation of the previous command to `STDOUT`. The JSON output can be compact or pretty formatted.

The first argument is required and identifies the command that is piping output to `jc` input. For example:
- `--ls` enables the `ls` parser
- `--ifconfig` enables the `ifconfig` parser
- `--netstat` enables the `netstat` parser

The second `-p` argument is optional and specifies whether to pretty format the JSON output.

## Examples
```
$ ls -l /bin | jc --ls -p
[
  {
    "filename": "bash",
    "flags": "-r-xr-xr-x",
    "links": 1,
    "owner": "root",
    "group": "wheel",
    "bytes": 618416,
    "date": "May 3 22:26"
  },
  {
    "filename": "cat",
    "flags": "-rwxr-xr-x",
    "links": 1,
    "owner": "root",
    "group": "wheel",
    "bytes": 23648,
    "date": "May 3 22:26"
  },
  {
    "filename": "chmod",
    "flags": "-rwxr-xr-x",
    "links": 1,
    "owner": "root",
    "group": "wheel",
    "bytes": 30016,
    "date": "May 3 22:26"
  },
  ...
]

$ ifconfig | jc --ifconfig -p
[
  {
    "name": "docker0",
    "flags": "4099",
    "state": "UP,BROADCAST,MULTICAST",
    "mtu": "1500",
    "ipv4_addr": "172.17.0.1",
    "ipv4_mask": "255.255.0.0",
    "ipv4_bcast": "0.0.0.0",
    "mac_addr": "02:42:53:18:31:cc",
    "type": "Ethernet",
    "rx_packets": "0",
    "rx_errors": "0",
    "rx_dropped": "0",
    "rx_overruns": "0",
    "rx_frame": "0",
    "tx_packets": "0",
    "tx_errors": "0",
    "tx_dropped": "0",
    "tx_overruns": "0",
    "tx_carrier": "0",
    "tx_collisions": "0",
    "ipv6_addr": null,
    "ipv6_mask": null,
    "ipv6_scope": null,
    "metric": null
  },
  {
    "name": "ens33",
    "flags": "4163",
    "state": "UP,BROADCAST,RUNNING,MULTICAST",
    "mtu": "1500",
    "ipv4_addr": "192.168.71.135",
    "ipv4_mask": "255.255.255.0",
    "ipv4_bcast": "192.168.71.255",
    "ipv6_addr": "fe80::c1cb:715d:bc3e:b8a0",
    "ipv6_mask": "64",
    "ipv6_scope": "link",
    "mac_addr": "00:0c:29:3b:58:0e",
    "type": "Ethernet",
    "rx_packets": "26348",
    "rx_errors": "0",
    "rx_dropped": "0",
    "rx_overruns": "0",
    "rx_frame": "0",
    "tx_packets": "5308",
    "tx_errors": "0",
    "tx_dropped": "0",
    "tx_overruns": "0",
    "tx_carrier": "0",
    "tx_collisions": "0",
    "metric": null
  },
  {
    "name": "lo",
    "flags": "73",
    "state": "UP,LOOPBACK,RUNNING",
    "mtu": "65536",
    "ipv4_addr": "127.0.0.1",
    "ipv4_mask": "255.0.0.0",
    "ipv4_bcast": null,
    "ipv6_addr": "::1",
    "ipv6_mask": "128",
    "ipv6_scope": "host",
    "mac_addr": null,
    "type": "Local Loopback",
    "rx_packets": "64",
    "rx_errors": "0",
    "rx_dropped": "0",
    "rx_overruns": "0",
    "rx_frame": "0",
    "tx_packets": "64",
    "tx_errors": "0",
    "tx_dropped": "0",
    "tx_overruns": "0",
    "tx_carrier": "0",
    "tx_collisions": "0",
    "metric": null
  }
]

$ netstat -p | jc --netstat -p
{
  "client": {
    "tcp": {
      "ipv4": [
        {
          "local_address": "localhost.localdo",
          "local_port": "34480",
          "foreign_address": "lb-192-30-255-113",
          "foreign_port": "https",
          "state": "ESTABLISHED",
          "pid": 53550,
          "program_name": "git-remote-ht",
          "receive_q": 0,
          "send_q": 0
        },
        {
          "local_address": "localhost.localdo",
          "local_port": "34478",
          "foreign_address": "lb-192-30-255-113",
          "foreign_port": "https",
          "state": "ESTABLISHED",
          "pid": 53550,
          "program_name": "git-remote-ht",
          "receive_q": 0,
          "send_q": 0
        }
      ]
    }
  }
}

$ netstat -lp | jc --netstat -p
{
  "server": {
    "tcp": {
      "ipv4": [
        {
          "local_address": "localhost",
          "local_port": "smtp",
          "foreign_address": "0.0.0.0",
          "foreign_port": "*",
          "state": "LISTEN",
          "pid": 1594,
          "program_name": "master",
          "receive_q": 0,
          "send_q": 0
        },
        {
          "local_address": "0.0.0.0",
          "local_port": "ssh",
          "foreign_address": "0.0.0.0",
          "foreign_port": "*",
          "state": "LISTEN",
          "pid": 21918,
          "program_name": "sshd",
          "receive_q": 0,
          "send_q": 0
        }
      ],
      "ipv6": [
        {
          "local_address": "localhost",
          "local_port": "smtp",
          "foreign_address": "[::]",
          "foreign_port": "*",
          "state": "LISTEN",
          "pid": 1594,
          "program_name": "master",
          "receive_q": 0,
          "send_q": 0
        },
        {
          "local_address": "[::]",
          "local_port": "ssh",
          "foreign_address": "[::]",
          "foreign_port": "*",
          "state": "LISTEN",
          "pid": 21918,
          "program_name": "sshd",
          "receive_q": 0,
          "send_q": 0
        }
      ]
    },
    "udp": {
      "ipv4": [
        {
          "local_address": "0.0.0.0",
          "local_port": "bootpc",
          "foreign_address": "0.0.0.0",
          "foreign_port": "*",
          "pid": 13903,
          "program_name": "dhclient",
          "receive_q": 0,
          "send_q": 0
        },
        {
          "local_address": "localhost",
          "local_port": "323",
          "foreign_address": "0.0.0.0",
          "foreign_port": "*",
          "pid": 30926,
          "program_name": "chronyd",
          "receive_q": 0,
          "send_q": 0
        }
      ],
      "ipv6": [
        {
          "local_address": "localhost",
          "local_port": "323",
          "foreign_address": "[::]",
          "foreign_port": "*",
          "pid": 30926,
          "program_name": "chronyd",
          "receive_q": 0,
          "send_q": 0
        }
      ]
    }
  }
}
```



