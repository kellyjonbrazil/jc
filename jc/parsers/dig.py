"""jc - JSON CLI output utility dig Parser

Usage:

    Specify --dig as the first argument if the piped input is coming from dig

Compatibility:

    'linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd'

Examples:

    $ dig cnn.com www.cnn.com @205.251.194.64 | jc --dig -p
    [
      {
        "id": 34128,
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
            "ttl": 60,
            "data": "151.101.65.67"
          },
          {
            "name": "cnn.com.",
            "class": "IN",
            "type": "A",
            "ttl": 60,
            "data": "151.101.193.67"
          },
          {
            "name": "cnn.com.",
            "class": "IN",
            "type": "A",
            "ttl": 60,
            "data": "151.101.1.67"
          },
          {
            "name": "cnn.com.",
            "class": "IN",
            "type": "A",
            "ttl": 60,
            "data": "151.101.129.67"
          }
        ],
        "query_time": 37,
        "server": "2600",
        "when": "Tue Nov 12 07:14:42 PST 2019",
        "rcvd": 100
      },
      {
        "id": 15273,
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
        "query_time": 23,
        "server": "205.251.194.64#53(205.251.194.64)",
        "when": "Tue Nov 12 07:14:42 PST 2019",
        "rcvd": 212
      }
    ]

    $ dig cnn.com www.cnn.com @205.251.194.64 | jc --dig -p -r
    [
      {
        "id": "23843",
        "opcode": "QUERY",
        "status": "NOERROR",
        "flags": [
          "qr",
          "rd",
          "ra"
        ],
        "query_num": "1",
        "answer_num": "4",
        "authority_num": "0",
        "additional_num": "1",
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
            "ttl": "30",
            "data": "151.101.193.67"
          },
          {
            "name": "cnn.com.",
            "class": "IN",
            "type": "A",
            "ttl": "30",
            "data": "151.101.1.67"
          },
          {
            "name": "cnn.com.",
            "class": "IN",
            "type": "A",
            "ttl": "30",
            "data": "151.101.65.67"
          },
          {
            "name": "cnn.com.",
            "class": "IN",
            "type": "A",
            "ttl": "30",
            "data": "151.101.129.67"
          }
        ],
        "query_time": "24 msec",
        "server": "192.168.1.254#53(192.168.1.254)",
        "when": "Tue Nov 12 07:16:19 PST 2019",
        "rcvd": "100"
      },
      {
        "id": "8266",
        "opcode": "QUERY",
        "status": "NOERROR",
        "flags": [
          "qr",
          "aa",
          "rd"
        ],
        "query_num": "1",
        "answer_num": "1",
        "authority_num": "4",
        "additional_num": "1",
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
            "ttl": "300",
            "data": "turner-tls.map.fastly.net."
          }
        ],
        "authority": [
          {
            "name": "cnn.com.",
            "class": "IN",
            "type": "NS",
            "ttl": "3600",
            "data": "ns-1086.awsdns-07.org."
          },
          {
            "name": "cnn.com.",
            "class": "IN",
            "type": "NS",
            "ttl": "3600",
            "data": "ns-1630.awsdns-11.co.uk."
          },
          {
            "name": "cnn.com.",
            "class": "IN",
            "type": "NS",
            "ttl": "3600",
            "data": "ns-47.awsdns-05.com."
          },
          {
            "name": "cnn.com.",
            "class": "IN",
            "type": "NS",
            "ttl": "3600",
            "data": "ns-576.awsdns-08.net."
          }
        ],
        "query_time": "26 msec",
        "server": "205.251.194.64#53(205.251.194.64)",
        "when": "Tue Nov 12 07:16:19 PST 2019",
        "rcvd": "212"
      }
    ]

    $ dig -x 1.1.1.1 | jc --dig -p
    [
      {
        "id": 34898,
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
            "ttl": 952,
            "data": "one.one.one.one."
          }
        ],
        "query_time": 103,
        "server": "2600",
        "when": "Tue Nov 12 07:15:33 PST 2019",
        "rcvd": 78
      }
    ]

    $ dig -x 1.1.1.1 | jc --dig -p -r
    [
      {
        "id": "50986",
        "opcode": "QUERY",
        "status": "NOERROR",
        "flags": [
          "qr",
          "rd",
          "ra"
        ],
        "query_num": "1",
        "answer_num": "1",
        "authority_num": "0",
        "additional_num": "1",
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
            "ttl": "1800",
            "data": "one.one.one.one."
          }
        ],
        "query_time": "38 msec",
        "server": "2600",
        "when": "Tue Nov 12 07:17:19 PST 2019",
        "rcvd": "78"
      }
    ]
"""
import jc.utils


class info():
    version = '1.3'
    description = 'dig command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'aix', 'freebsd', 'darwin']
    magic_commands = ['dig']


__version__ = info.version


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (dictionary) raw structured data to process

    Returns:

        List of dictionaries. Structured data with the following schema:

        [
          {
            "id":             integer,
            "opcode":         string,
            "status":         string,
            "flags": [
                              string
            ],
            "query_num":      integer,
            "answer_num":     integer,
            "authority_num":  integer,
            "additional_num": integer,
            "axfr": [
              {
                "name":       string,
                "class":      string,
                "type":       string,
                "ttl":        integer,
                "data":       string
              }
            ],
            "question": {
              "name":         string,
              "class":        string,
              "type":         string
            },
            "answer": [
              {
                "name":       string,
                "class":      string,
                "type":       string,
                "ttl":        integer,
                "data":       string
              }
            ],
            "authority": [
              {
                "name":       string,
                "class":      string,
                "type":       string,
                "ttl":        integer,
                "data":       string
              }
            ],
            "query_time":     integer,   # in msec
            "server":         string,
            "when":           string,
            "rcvd":           integer
            "size":           string
          }
        ]
    """

    for entry in proc_data:
        int_list = ['id', 'query_num', 'answer_num', 'authority_num', 'additional_num', 'rcvd']
        for key in int_list:
            if key in entry:
                try:
                    key_int = int(entry[key])
                    entry[key] = key_int
                except (ValueError):
                    entry[key] = None

        if 'axfr' in entry:
            for ax in entry['axfr']:
                try:
                    ttl_int = int(ax['ttl'])
                    ax['ttl'] = ttl_int
                except (ValueError):
                    ax['ttl'] = None

        if 'answer' in entry:
            for ans in entry['answer']:
                try:
                    ttl_int = int(ans['ttl'])
                    ans['ttl'] = ttl_int
                except (ValueError):
                    ans['ttl'] = None

        if 'authority' in entry:
            for auth in entry['authority']:
                try:
                    ttl_int = int(auth['ttl'])
                    auth['ttl'] = ttl_int
                except (ValueError):
                    auth['ttl'] = None

        if 'query_time' in entry:
            try:
                qt_int = int(entry['query_time'].split()[0])
                entry['query_time'] = qt_int
            except (ValueError):
                entry['query_time'] = None

    return proc_data


def parse_header(header):
    # ;; ->>HEADER<<- opcode: QUERY, status: NXDOMAIN, id: 6140
    header = header.split()
    opcode = header[3].rstrip(',')
    status = header[5].rstrip(',')
    header_id = header[7]

    return {'id': header_id,
            'opcode': opcode,
            'status': status}


def parse_flags_line(flagsline):
    # ;; flags: qr rd ra; QUERY: 1, ANSWER: 0, AUTHORITY: 0, ADDITIONAL: 1
    flagsline = flagsline.split(';')
    flags = flagsline.pop(0)
    flags = flagsline.pop(0)
    flags = flagsline.pop(0).split(':')
    flags = flags[1].lstrip()
    flags = flags.split()

    restline = flagsline[0].replace(',', ' ').replace(':', ' ')
    restlist = restline.split()

    query_num = restlist[1]
    answer_num = restlist[3]
    authority_num = restlist[5]
    additional_num = restlist[7]

    return {'flags': flags,
            'query_num': query_num,
            'answer_num': answer_num,
            'authority_num': authority_num,
            'additional_num': additional_num}


def parse_question(question):
    # ;www.cnn.com.           IN  A
    question = question.split()
    dns_name = question[0].lstrip(';')
    dns_class = question[1]
    dns_type = question[2]

    return {'name': dns_name,
            'class': dns_class,
            'type': dns_type}


def parse_authority(authority):
    # cnn.com.      3600    IN  NS  ns-1086.awsdns-07.org.
    authority = authority.split()
    authority_name = authority[0]
    authority_class = authority[2]
    authority_type = authority[3]
    authority_ttl = authority[1]
    authority_data = authority[4]

    return {'name': authority_name,
            'class': authority_class,
            'type': authority_type,
            'ttl': authority_ttl,
            'data': authority_data}


def parse_answer(answer):
    # www.cnn.com.        5   IN  CNAME   turner-tls.map.fastly.net.
    answer = answer.split()
    answer_name = answer[0]
    answer_class = answer[2]
    answer_type = answer[3]
    answer_ttl = answer[1]
    answer_data = answer[4]

    return {'name': answer_name,
            'class': answer_class,
            'type': answer_type,
            'ttl': answer_ttl,
            'data': answer_data}


def parse_axfr(axfr):
    # ; <<>> DiG 9.11.14-3-Debian <<>> @81.4.108.41 axfr zonetransfer.me +nocookie
    # ; (1 server found)
    # ;; global options: +cmd
    # zonetransfer.me. 7200 IN A 5.196.105.14
    axfr = axfr.split(maxsplit=4)
    axfr_name = axfr[0]
    axfr_ttl = axfr[1]
    axfr_class = axfr[2]
    axfr_type = axfr[3]
    axfr_data = axfr[4]

    return {'name': axfr_name,
            'ttl': axfr_ttl,
            'class': axfr_class,
            'type': axfr_type,
            'data': axfr_data}


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of dictionaries. Raw or processed structured data.
    """

    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = []
    cleandata = data.splitlines()
    # remove blank lines
    cleandata = list(filter(None, cleandata))

    question = False
    authority = False
    answer = False
    axfr = False

    output_entry = {}

    if jc.utils.has_data(data):
        for line in cleandata:

            if line.startswith('; <<>> ') and ' axfr ' in line.lower():
                question = False
                authority = False
                answer = False
                axfr = True
                axfr_list = []
                continue

            if ';' not in line and axfr:
                axfr_list.append(parse_axfr(line))
                output_entry.update({'axfr': axfr_list})
                continue

            if line.startswith(';; ->>HEADER<<-'):
                output_entry = {}
                output_entry.update(parse_header(line))
                continue

            if line.startswith(';; flags:'):
                output_entry.update(parse_flags_line(line))
                continue

            if line.startswith(';; QUESTION SECTION:'):
                question = True
                authority = False
                answer = False
                axfr = False
                continue

            if question:
                output_entry['question'] = parse_question(line)
                question = False
                authority = False
                answer = False
                axfr = False
                continue

            if line.startswith(';; AUTHORITY SECTION:'):
                question = False
                authority = True
                answer = False
                axfr = False
                authority_list = []
                continue

            if ';' not in line and authority:
                authority_list.append(parse_authority(line))
                output_entry.update({'authority': authority_list})
                continue

            if line.startswith(';; ANSWER SECTION:'):
                question = False
                authority = False
                answer = True
                axfr = False
                answer_list = []
                continue

            if ';' not in line and answer:
                answer_list.append(parse_answer(line))
                output_entry.update({'answer': answer_list})
                continue

            # footer consists of 4 lines
            # footer line 1
            if line.startswith(';; Query time:'):
                output_entry.update({'query_time': line.split(':')[1].lstrip()})
                continue

            # footer line 2
            if line.startswith(';; SERVER:'):
                output_entry.update({'server': line.split(':')[1].lstrip()})
                continue

            # footer line 3
            if line.startswith(';; WHEN:'):
                output_entry.update({'when': line.split(':', maxsplit=1)[1].lstrip()})
                continue

            # footer line 4 (last line)
            if line.startswith(';; MSG SIZE  rcvd:'):
                output_entry.update({'rcvd': line.split(':')[1].lstrip()})

                if output_entry:
                    raw_output.append(output_entry)
            elif line.startswith(';; XFR size:'):
                output_entry.update({'size': line.split(':')[1].lstrip()})

                if output_entry:
                    raw_output.append(output_entry)

        raw_output = list(filter(None, raw_output))

    if raw:
        return raw_output
    else:
        return process(raw_output)
