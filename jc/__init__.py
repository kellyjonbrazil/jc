"""JC - JSON CLI output utility

* kellyjonbrazil@gmail.com

This package serializes the output of many standard unix command line tools to JSON format.

For documentation on each parser, see the [documentation site](https://kellyjonbrazil.github.io/jc/).

CLI Example:

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

Module Example:

    >>> import jc.parsers.dig
    >>>
    >>> data = '''; <<>> DiG 9.10.6 <<>> example.com
    ... ;; global options: +cmd
    ... ;; Got answer:
    ... ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 64612
    ... ;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1
    ... 
    ... ;; OPT PSEUDOSECTION:
    ... ; EDNS: version: 0, flags:; udp: 4096
    ... ;; QUESTION SECTION:
    ... ;example.com.           IN  A
    ... 
    ... ;; ANSWER SECTION:
    ... example.com.        29658   IN  A   93.184.216.34
    ... 
    ... ;; Query time: 52 msec
    ... ;; SERVER: 2600:1700:bab0:d40::1#53(2600:1700:bab0:d40::1)
    ... ;; WHEN: Fri Apr 16 16:13:00 PDT 2021
    ... ;; MSG SIZE  rcvd: 56'''
    >>>
    >>> jc.parsers.dig.parse(data)
    [{'id': 64612, 'opcode': 'QUERY', 'status': 'NOERROR', 'flags': ['qr', 'rd', 'ra'], 'query_num': 1, 'answer_num':
    1, 'authority_num': 0, 'additional_num': 1, 'opt_pseudosection': {'edns': {'version': 0, 'flags': [], 'udp':
    4096}}, 'question': {'name': 'example.com.', 'class': 'IN', 'type': 'A'}, 'answer': [{'name': 'example.com.',
    'class': 'IN', 'type': 'A', 'ttl': 29658, 'data': '93.184.216.34'}], 'query_time': 52, 'server':
    '2600:1700:bab0:d40::1#53(2600:1700:bab0:d40::1)', 'when': 'Fri Apr 16 16:13:00 PDT 2021', 'rcvd': 56,
    'when_epoch': 1618614780, 'when_epoch_utc': None}]
"""

name = 'jc'
__version__ = '1.15.2'
