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
        "when_epoch":     integer,   # naive timestamp if when field is parsable, else null
        "when_epoch_utc": integer,   # timezone aware timestamp availabe for UTC, else null
        "rcvd":           integer
        "size":           string
      }
    ]

Examples:

    $ dig cnn.com www.cnn.com @205.251.194.64 | jc --dig -p
    

    $ dig cnn.com www.cnn.com @205.251.194.64 | jc --dig -p -r
    

    $ dig -x 1.1.1.1 | jc --dig -p
    [
      {
        "id": 22191,
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
            "ttl": 1800,
            "data": "one.one.one.one."
          }
        ],
        "query_time": 44,
        "server": "2600",
        "when": "Tue Mar 30 20:10:34 PDT 2021",
        "rcvd": 78,
        "when_epoch": 1617160234,
        "when_epoch_utc": null
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
    """Provides parser metadata (version, author, etc.)"""
    version = '1.8'
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

        if 'opt_pseudosection' in entry:
            if 'edns' in entry['opt_pseudosection']:
                if 'version' in entry['opt_pseudosection']['edns']:
                    try:
                        entry['opt_pseudosection']['edns']['version'] = int(entry['opt_pseudosection']['edns']['version'])
                    except (ValueError):
                        entry['opt_pseudosection']['edns']['version'] = None

                if 'udp' in entry['opt_pseudosection']['edns']:
                    try:
                        entry['opt_pseudosection']['edns']['udp'] = int(entry['opt_pseudosection']['edns']['udp'])
                    except (ValueError):
                        entry['opt_pseudosection']['edns']['udp'] = None

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


def _parse_authority(authority):
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

    # section can be: header, flags, question, authority, answer, xfr, additional, opt_pseudosection, footer
    section = ''
    output_entry = {}

    if jc.utils.has_data(data):
        for line in cleandata:

            # identify sections

            if line.startswith('; <<>> ') and ' axfr ' in line.lower():
                section = 'axfr'
                axfr_list = []
                continue

            if line.startswith(';; ->>HEADER<<-'):
                section = 'header'
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

            # parse sections

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
                authority_list.append(_parse_authority(line))
                output_entry.update({'authority': authority_list})
                continue

            if not line.startswith(';') and section == 'answer':
                answer_list.append(_parse_answer(line))
                output_entry.update({'answer': answer_list})
                continue

            # footer consists of 4 lines
            # footer line 1
            if line.startswith(';; Query time:'):
                section = 'footer'
                output_entry.update({'query_time': line.split(':')[1].lstrip()})
                continue

            # footer line 2
            if line.startswith(';; SERVER:'):
                output_entry.update({'server': line.split(':', maxsplit=1)[1].lstrip()})
                continue

            # footer line 3
            if line.startswith(';; WHEN:'):
                output_entry.update({'when': line.split(':', maxsplit=1)[1].lstrip()})
                continue

            # footer line 4 (last line)
            if line.startswith(';; MSG SIZE  rcvd:'):
                section = ''
                output_entry.update({'rcvd': line.split(':')[1].lstrip()})

                if output_entry:
                    raw_output.append(output_entry)

            elif line.startswith(';; XFR size:'):
                section = ''
                output_entry.update({'size': line.split(':')[1].lstrip()})

                if output_entry:
                    raw_output.append(output_entry)

        raw_output = list(filter(None, raw_output))

    if raw:
        return raw_output
    else:
        return _process(raw_output)
