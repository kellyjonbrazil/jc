"""jc - JSON CLI output utility dig Parser

Usage:
    Specify --dig as the first argument if the piped input is coming from dig

Examples:
$ dig www.cnn.com

; <<>> DiG 9.11.4-P2-RedHat-9.11.4-9.P2.el7 <<>> www.cnn.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 11061
;; flags: qr rd ra; QUERY: 1, ANSWER: 5, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; MBZ: 0x0005, udp: 4096
;; QUESTION SECTION:
;www.cnn.com.           IN  A

;; ANSWER SECTION:
www.cnn.com.        5   IN  CNAME   turner-tls.map.fastly.net.
turner-tls.map.fastly.net. 5    IN  A   151.101.129.67
turner-tls.map.fastly.net. 5    IN  A   151.101.1.67
turner-tls.map.fastly.net. 5    IN  A   151.101.193.67
turner-tls.map.fastly.net. 5    IN  A   151.101.65.67

;; Query time: 43 msec
;; SERVER: 192.168.71.2#53(192.168.71.2)
;; WHEN: Wed Oct 30 00:43:32 PDT 2019
;; MSG SIZE  rcvd: 143


"""
import pprint


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
    return {}


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

        if line.find('; <<>> DiG') == 0:
            continue

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
            continue

        if line.find(';; AUTHORITY SECTION:') == 0:
            question = False
            authority = True
            answer = False
            continue

        if authority:
            output_entry['authority'] = parse_authority(line)
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
    pprint.pprint(clean_output)
    exit()
    # return clean_output
