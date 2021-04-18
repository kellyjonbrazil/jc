"""jc - JSON CLI output utility `dig` command output parser

The `when_epoch` calculated timestamp field is naive (i.e. based on the local time of the system the parser is run on)

The `when_epoch_utc` calculated timestamp field is timezone-aware and is only available if the timezone field is UTC.

Usage (cli):

    $ dig example.com | jc --dig

    or

    $ jc dig example.com

Usage (module):

    import jc.parsers.dig
    result = jc.parsers.dig.parse(dig_command_output)

Schema:

    [
      {
        "id":                   integer,
        "opcode":               string,
        "status":               string,
        "flags": [
                                string
        ],
        "query_num":            integer,
        "answer_num":           integer,
        "authority_num":        integer,
        "additional_num":       integer,
        "axfr": [
          {
            "name":             string,
            "class":            string,
            "type":             string,
            "ttl":              integer,
            "data":             string
          }
        ],
        "opt_pseudosection": {
          "edns": {
            "version":          integer,
            "flags": [
                                string
            ],
            "udp":              integer
          },
          "cookie":             string
        },
        "question": {
          "name":               string,
          "class":              string,
          "type":               string
        },
        "answer": [
          {
            "name":             string,
            "class":            string,
            "type":             string,
            "ttl":              integer,
            "data":             string
          }
        ],
        "additional": [
          {
            "name":             string,
            "class":            string,
            "type":             string,
            "ttl":              integer,
            "data":             string
          }
        ],
        "authority": [
          {
            "name":             string,
            "class":            string,
            "type":             string,
            "ttl":              integer,
            "data":             string
          }
        ],
        "query_size":           integer,
        "query_time":           integer,   # in msec
        "server":               string,
        "when":                 string,
        "when_epoch":           integer,   # naive timestamp if when field is parsable, else null
        "when_epoch_utc":       integer,   # timezone aware timestamp availabe for UTC, else null
        "rcvd":                 integer
        "size":                 string
      }
    ]

Examples:

    $ dig example.com | jc --dig -p
    [
      {
        "id": 2951,
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
          "name": "example.com.",
          "class": "IN",
          "type": "A"
        },
        "answer": [
          {
            "name": "example.com.",
            "class": "IN",
            "type": "A",
            "ttl": 39302,
            "data": "93.184.216.34"
          }
        ],
        "query_time": 49,
        "server": "2600:1700:bab0:d40::1#53(2600:1700:bab0:d40::1)",
        "when": "Fri Apr 16 16:05:10 PDT 2021",
        "rcvd": 56,
        "when_epoch": 1618614310,
        "when_epoch_utc": null
      }
    ]

    $ dig cnn.com www.cnn.com @205.251.194.64 | jc --dig -p -r
    [
      {
        "id": "46052",
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
        "opt_pseudosection": {
          "edns": {
            "version": "0",
            "flags": [],
            "udp": "4096"
          }
        },
        "question": {
          "name": "example.com.",
          "class": "IN",
          "type": "A"
        },
        "answer": [
          {
            "name": "example.com.",
            "class": "IN",
            "type": "A",
            "ttl": "40426",
            "data": "93.184.216.34"
          }
        ],
        "query_time": "48 msec",
        "server": "2600:1700:bab0:d40::1#53(2600:1700:bab0:d40::1)",
        "when": "Fri Apr 16 16:06:12 PDT 2021",
        "rcvd": "56"
      }
    ]

    $ dig -x 1.1.1.1 | jc --dig -p
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

    $ dig -x 1.1.1.1 | jc --dig -p -r
    [
      {
        "id": "32644",
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
        "opt_pseudosection": {
          "edns": {
            "version": "0",
            "flags": [],
            "udp": "4096"
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
            "ttl": "1800",
            "data": "one.one.one.one."
          }
        ],
        "query_time": "52 msec",
        "server": "2600:1700:bab0:d40::1#53(2600:1700:bab0:d40::1)",
        "when": "Sat Apr 17 14:51:46 PDT 2021",
        "rcvd": "78"
      }
    ]
"""
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '2.0'
    description = '`dig` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'aix', 'freebsd', 'darwin']
    magic_commands = ['dig']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema.
    """
    for entry in proc_data:
        int_list = ['id', 'query_num', 'answer_num', 'authority_num', 'additional_num', 'rcvd',
                    'query_size', 'query_time']
        for key in entry:
            if key in int_list:
                entry[key] = jc.utils.convert_to_int(entry[key])

        if 'axfr' in entry:
            for ax in entry['axfr']:
                ax['ttl'] = jc.utils.convert_to_int(ax['ttl'])

        if 'opt_pseudosection' in entry:
            if 'edns' in entry['opt_pseudosection']:
                if 'version' in entry['opt_pseudosection']['edns']:
                    entry['opt_pseudosection']['edns']['version'] = jc.utils.convert_to_int(entry['opt_pseudosection']['edns']['version'])

                if 'udp' in entry['opt_pseudosection']['edns']:
                    entry['opt_pseudosection']['edns']['udp'] = jc.utils.convert_to_int(entry['opt_pseudosection']['edns']['udp'])

        if 'answer' in entry:
            for ans in entry['answer']:
                ans['ttl'] = jc.utils.convert_to_int(ans['ttl'])

        if 'additional' in entry:
            for add in entry['additional']:
                add['ttl'] = jc.utils.convert_to_int(add['ttl'])

        if 'authority' in entry:
            for auth in entry['authority']:
                auth['ttl'] = jc.utils.convert_to_int(auth['ttl'])

        if 'when' in entry:
            ts = jc.utils.timestamp(entry['when'])
            entry['when_epoch'] = ts.naive
            entry['when_epoch_utc'] = ts.utc

    return proc_data


def _parse_header(header):
    # ;; ->>HEADER<<- opcode: QUERY, status: NXDOMAIN, id: 6140
    header = header.split()
    opcode = header[3].rstrip(',')
    status = header[5].rstrip(',')
    header_id = header[7]

    return {'id': header_id,
            'opcode': opcode,
            'status': status}


def _parse_flags_line(flagsline):
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


def _parse_opt_pseudosection(optline):
    # ;; OPT PSEUDOSECTION:
    # ; EDNS: version: 0, flags:; udp: 4096
    # ; COOKIE: 1cbc06703eaef210
    if optline.startswith('; EDNS:'):
        optline_list = optline.replace(',', ' ').split(';')
        optline_first = optline_list[1]
        optline_rest = optline_list[2]
        _, _, ver, _, *flags = optline_first.split()
        udp = optline_rest.split()[-1]

        return {
            'edns': {
                'version': ver,
                'flags': flags,
                'udp': udp
            }
        }

    elif optline.startswith('; COOKIE:'):
        return {
            'cookie': optline.split()[2]
        }


def _parse_question(question):
    # ;www.cnn.com.           IN  A
    question = question.split()
    dns_name = question[0].lstrip(';')
    dns_class = question[1]
    dns_type = question[2]

    return {'name': dns_name,
            'class': dns_class,
            'type': dns_type}


def _parse_answer(answer):
    # www.cnn.com.        5   IN  CNAME   turner-tls.map.fastly.net.
    answer = answer.split(maxsplit=4)
    answer_name = answer[0]
    answer_class = answer[2]
    answer_type = answer[3]
    answer_ttl = answer[1]
    answer_data = answer[4]

    # remove surrounding quotation marks from answer_data if they exist
    if answer_data.startswith('"') and answer_data.endswith('"'):
        answer_data = answer_data[1:-1]

    return {'name': answer_name,
            'class': answer_class,
            'type': answer_type,
            'ttl': answer_ttl,
            'data': answer_data}


def _parse_axfr(axfr):
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


def _parse_footer(footer):
    # footer consists of 4 lines
    # footer line 1
    if footer.startswith(';; Query time:'):
        return {'query_time': footer.split(':')[1].lstrip()}

    # footer line 2
    if footer.startswith(';; SERVER:'):
        return {'server': footer.split(':', maxsplit=1)[1].lstrip()}

    # footer line 3
    if footer.startswith(';; WHEN:'):
        return {'when': footer.split(':', maxsplit=1)[1].lstrip()}

    # footer line 4 (last line)
    if footer.startswith(';; MSG SIZE  rcvd:'):
        return {'rcvd': footer.split(':')[1].lstrip()}

    elif footer.startswith(';; XFR size:'):
        return {'size': footer.split(':')[1].lstrip()}


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """

    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = []
    cleandata = data.splitlines()
    # remove blank lines
    cleandata = list(filter(None, cleandata))

    # section can be: header, flags, question, authority, answer, axfr, additional, opt_pseudosection, footer
    section = ''
    output_entry = {}

    if jc.utils.has_data(data):
        for line in cleandata:

            # identify sections
            if line.startswith(';; Got answer:'):
                section = ''
                continue

            if line.startswith('; <<>> ') and ' axfr ' in line.lower():
                section = 'axfr'
                axfr_list = []
                continue

            if line.startswith(';; ->>HEADER<<-'):
                section = 'header'
                if output_entry:
                    raw_output.append(output_entry)
                output_entry = {}
                output_entry.update(_parse_header(line))
                continue

            if line.startswith(';; flags:'):
                section = 'flags'
                output_entry.update(_parse_flags_line(line))
                continue

            if line.startswith(';; OPT PSEUDOSECTION:'):
                section = 'opt_pseudosection'
                continue

            if line.startswith(';; QUESTION SECTION:'):
                section = 'question'
                continue

            if line.startswith(';; AUTHORITY SECTION:'):
                section = 'authority'
                authority_list = []
                continue

            if line.startswith(';; ANSWER SECTION:'):
                section = 'answer'
                answer_list = []
                continue

            if line.startswith(';; ADDITIONAL SECTION:'):
                section = 'additional'
                additional_list = []
                continue

            if line.startswith(';; Query time:'):
                section = 'footer'
                output_entry.update(_parse_footer(line))
                continue

            # parse sections

            if line.startswith(';; QUERY SIZE:'):
                output_entry.update({'query_size': line.split(': ', maxsplit=1)[1]})
                continue

            if not line.startswith(';') and section == 'axfr':
                axfr_list.append(_parse_axfr(line))
                output_entry.update({'axfr': axfr_list})
                continue

            if section == 'opt_pseudosection':
                if 'opt_pseudosection' not in output_entry:
                    output_entry['opt_pseudosection'] = {}
                output_entry['opt_pseudosection'].update(_parse_opt_pseudosection(line))
                continue

            if section == 'question':
                output_entry['question'] = _parse_question(line)
                continue

            if not line.startswith(';') and section == 'authority':
                authority_list.append(_parse_answer(line))
                output_entry.update({'authority': authority_list})
                continue

            if not line.startswith(';') and section == 'answer':
                answer_list.append(_parse_answer(line))
                output_entry.update({'answer': answer_list})
                continue

            if not line.startswith(';') and section == 'additional':
                additional_list.append(_parse_answer(line))
                output_entry.update({'additional': additional_list})
                continue

            if section == 'footer':
                output_entry.update(_parse_footer(line))
                continue

        if output_entry:
            raw_output.append(output_entry)

        raw_output = list(filter(None, raw_output))

    if raw:
        return raw_output
    else:
        return _process(raw_output)
