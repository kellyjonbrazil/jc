"""jc - JSON CLI output utility ipables Parser

Usage:
    Specify --iptables as the first argument if the piped input is coming from iptables

    Supports -vLn for all tables

Examples:

$ sudo iptables -L -t nat | jc --iptables -p
[
  {
    "chain": "PREROUTING",
    "rules": [
      {
        "target": "PREROUTING_direct",
        "prot": "all",
        "opt": "--",
        "source": "anywhere",
        "destination": "anywhere"
      },
      {
        "target": "PREROUTING_ZONES_SOURCE",
        "prot": "all",
        "opt": "--",
        "source": "anywhere",
        "destination": "anywhere"
      },
      {
        "target": "PREROUTING_ZONES",
        "prot": "all",
        "opt": "--",
        "source": "anywhere",
        "destination": "anywhere"
      },
      {
        "target": "DOCKER",
        "prot": "all",
        "opt": "--",
        "source": "anywhere",
        "destination": "anywhere",
        "options": "ADDRTYPE match dst-type LOCAL"
      }
    ]
  },
  {
    "chain": "INPUT",
    "rules": []
  },
  {
    "chain": "OUTPUT",
    "rules": [
      {
        "target": "OUTPUT_direct",
        "prot": "all",
        "opt": "--",
        "source": "anywhere",
        "destination": "anywhere"
      },
      {
        "target": "DOCKER",
        "prot": "all",
        "opt": "--",
        "source": "anywhere",
        "destination": "!loopback/8",
        "options": "ADDRTYPE match dst-type LOCAL"
      }
    ]
  },
  ...
]

$ sudo iptables -vnL -t filter | jc --iptables -p
[
  {
    "chain": "INPUT",
    "rules": [
      {
        "pkts": "1571",
        "bytes": "3394K",
        "target": "ACCEPT",
        "prot": "all",
        "opt": "--",
        "in": "*",
        "out": "*",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0",
        "options": "ctstate RELATED,ESTABLISHED"
      },
      {
        "pkts": "0",
        "bytes": "0",
        "target": "ACCEPT",
        "prot": "all",
        "opt": "--",
        "in": "lo",
        "out": "*",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0"
      },
      {
        "pkts": "711",
        "bytes": "60126",
        "target": "INPUT_direct",
        "prot": "all",
        "opt": "--",
        "in": "*",
        "out": "*",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0"
      },
      {
        "pkts": "711",
        "bytes": "60126",
        "target": "INPUT_ZONES_SOURCE",
        "prot": "all",
        "opt": "--",
        "in": "*",
        "out": "*",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0"
      },
      {
        "pkts": "711",
        "bytes": "60126",
        "target": "INPUT_ZONES",
        "prot": "all",
        "opt": "--",
        "in": "*",
        "out": "*",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0"
      },
      {
        "pkts": "0",
        "bytes": "0",
        "target": "DROP",
        "prot": "all",
        "opt": "--",
        "in": "*",
        "out": "*",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0",
        "options": "ctstate INVALID"
      },
      {
        "pkts": "710",
        "bytes": "60078",
        "target": "REJECT",
        "prot": "all",
        "opt": "--",
        "in": "*",
        "out": "*",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0",
        "options": "reject-with icmp-host-prohibited"
      }
    ]
  },
  {
    "chain": "FORWARD",
    "rules": [
      {
        "pkts": "0",
        "bytes": "0",
        "target": "DOCKER-ISOLATION",
        "prot": "all",
        "opt": "--",
        "in": "*",
        "out": "*",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0"
      },
      {
        "pkts": "0",
        "bytes": "0",
        "target": "DOCKER",
        "prot": "all",
        "opt": "--",
        "in": "*",
        "out": "docker0",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0"
      },
      {
        "pkts": "0",
        "bytes": "0",
        "target": "ACCEPT",
        "prot": "all",
        "opt": "--",
        "in": "*",
        "out": "docker0",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0",
        "options": "ctstate RELATED,ESTABLISHED"
      },
      {
        "pkts": "0",
        "bytes": "0",
        "target": "ACCEPT",
        "prot": "all",
        "opt": "--",
        "in": "docker0",
        "out": "!docker0",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0"
      },
      {
        "pkts": "0",
        "bytes": "0",
        "target": "ACCEPT",
        "prot": "all",
        "opt": "--",
        "in": "docker0",
        "out": "docker0",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0"
      },
      {
        "pkts": "0",
        "bytes": "0",
        "target": "ACCEPT",
        "prot": "all",
        "opt": "--",
        "in": "*",
        "out": "*",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0",
        "options": "ctstate RELATED,ESTABLISHED"
      },
      {
        "pkts": "0",
        "bytes": "0",
        "target": "ACCEPT",
        "prot": "all",
        "opt": "--",
        "in": "lo",
        "out": "*",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0"
      },
      {
        "pkts": "0",
        "bytes": "0",
        "target": "FORWARD_direct",
        "prot": "all",
        "opt": "--",
        "in": "*",
        "out": "*",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0"
      },
      {
        "pkts": "0",
        "bytes": "0",
        "target": "FORWARD_IN_ZONES_SOURCE",
        "prot": "all",
        "opt": "--",
        "in": "*",
        "out": "*",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0"
      },
      {
        "pkts": "0",
        "bytes": "0",
        "target": "FORWARD_IN_ZONES",
        "prot": "all",
        "opt": "--",
        "in": "*",
        "out": "*",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0"
      },
      {
        "pkts": "0",
        "bytes": "0",
        "target": "FORWARD_OUT_ZONES_SOURCE",
        "prot": "all",
        "opt": "--",
        "in": "*",
        "out": "*",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0"
      },
      {
        "pkts": "0",
        "bytes": "0",
        "target": "FORWARD_OUT_ZONES",
        "prot": "all",
        "opt": "--",
        "in": "*",
        "out": "*",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0"
      },
      {
        "pkts": "0",
        "bytes": "0",
        "target": "DROP",
        "prot": "all",
        "opt": "--",
        "in": "*",
        "out": "*",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0",
        "options": "ctstate INVALID"
      },
      {
        "pkts": "0",
        "bytes": "0",
        "target": "REJECT",
        "prot": "all",
        "opt": "--",
        "in": "*",
        "out": "*",
        "source": "0.0.0.0/0",
        "destination": "0.0.0.0/0",
        "options": "reject-with icmp-host-prohibited"
      }
    ]
  },
  ...
]
"""


def parse(data):
    output = []
    chain = {}
    headers = []

    cleandata = data.splitlines()

    for line in cleandata:

        if line.find('Chain') == 0:
            output.append(chain)
            chain = {}
            headers = []

            parsed_line = line.split()

            chain['chain'] = parsed_line[1]
            chain['rules'] = []

            continue

        elif line.find('target') == 0 or line.find('pkts') == 1:
            headers = []
            headers = [h for h in ' '.join(line.lower().strip().split()).split() if h]
            headers.append("options")

            continue

        else:
            rule = line.split(maxsplit=len(headers) - 1)
            temp_rule = dict(zip(headers, rule))
            if temp_rule:
                chain['rules'].append(temp_rule)

    output = list(filter(None, output))

    return output
