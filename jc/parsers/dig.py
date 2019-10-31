"""jc - JSON CLI output utility dig Parser

Usage:
    Specify --dig as the first argument if the piped input is coming from dig

Examples:
$ dig cnn.com www.cnn.com @205.251.194.64 | jc --dig -p
[
  {
    "id": "28182",
    "opcode": "QUERY",
    "status": "NOERROR",
    "flags": "qr rd ra",
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
        "ttl": "5",
        "data": "151.101.193.67"
      },
      {
        "name": "cnn.com.",
        "class": "IN",
        "type": "A",
        "ttl": "5",
        "data": "151.101.1.67"
      },
      {
        "name": "cnn.com.",
        "class": "IN",
        "type": "A",
        "ttl": "5",
        "data": "151.101.129.67"
      },
      {
        "name": "cnn.com.",
        "class": "IN",
        "type": "A",
        "ttl": "5",
        "data": "151.101.65.67"
      }
    ],
    "query_time": "45 msec",
    "server": "192.168.71.2#53(192.168.71.2)",
    "when": "Wed Oct 30 03:11:21 PDT 2019",
    "rcvd": "100"
  },
  {
    "id": "23264",
    "opcode": "QUERY",
    "status": "NOERROR",
    "flags": "qr aa rd",
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
    "query_time": "33 msec",
    "server": "205.251.194.64#53(205.251.194.64)",
    "when": "Wed Oct 30 03:11:21 PDT 2019",
    "rcvd": "212"
  }
]

$ dig -x 1.1.1.1 | jc --dig -p
[
  {
    "id": "27526",
    "opcode": "QUERY",
    "status": "NOERROR",
    "flags": "qr rd ra",
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
        "name": "1.1.1.1.IN-ADDR.ARPA.",
        "class": "IN",
        "type": "PTR",
        "ttl": "5",
        "data": "one.one.one.one."
      }
    ],
    "query_time": "34 msec",
    "server": "192.168.71.2#53(192.168.71.2)",
    "when": "Wed Oct 30 03:13:48 PDT 2019",
    "rcvd": "98"
  }
]
"""


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


def parse(data):
    output = []
    cleandata = data.splitlines()
    # remove blank lines
    cleandata = list(filter(None, cleandata))

    question = False
    authority = False
    answer = False

    output_entry = {}
    for line in cleandata:

        if line.find(';; ->>HEADER<<-') == 0:
            output_entry = {}
            output_entry.update(parse_header(line))
            continue

        if line.find(';; flags:') == 0:
            output_entry.update(parse_flags_line(line))
            continue

        if line.find(';; QUESTION SECTION:') == 0:
            question = True
            authority = False
            answer = False
            continue

        if question:
            output_entry['question'] = parse_question(line)
            question = False
            authority = False
            answer = False
            continue

        if line.find(';; AUTHORITY SECTION:') == 0:
            question = False
            authority = True
            answer = False
            authority_list = []
            continue

        if line.find(';') == -1 and authority:
            authority_list.append(parse_authority(line))
            output_entry.update({'authority': authority_list})
            continue

        if line.find(';; ANSWER SECTION:') == 0:
            question = False
            authority = False
            answer = True
            answer_list = []
            continue

        if line.find(';') == -1 and answer:
            answer_list.append(parse_answer(line))
            output_entry.update({'answer': answer_list})
            continue

        # footer consists of 4 lines
        # footer line 1
        if line.find(';; Query time:') == 0:
            output_entry.update({'query_time': line.split(':')[1].lstrip()})
            continue

        # footer line 2
        if line.find(';; SERVER:') == 0:
            output_entry.update({'server': line.split(':')[1].lstrip()})
            continue

        # footer line 3
        if line.find(';; WHEN:') == 0:
            output_entry.update({'when': line.split(':', maxsplit=1)[1].lstrip()})
            continue

        # footer line 4 (last line)
        if line.find(';; MSG SIZE  rcvd:') == 0:
            output_entry.update({'rcvd': line.split(':')[1].lstrip()})

            if output_entry:
                output.append(output_entry)

    clean_output = list(filter(None, output))
    return clean_output
