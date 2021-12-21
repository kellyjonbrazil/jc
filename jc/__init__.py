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
    >>> import subprocess
    >>> import jc.parsers.dig
    >>>
    >>> cmd_output = subprocess.check_output(['dig', 'example.com'], text=True)
    >>> data = jc.parsers.dig.parse(cmd_output)
    >>>
    >>> data
    [{'id': 64612, 'opcode': 'QUERY', 'status': 'NOERROR', 'flags': ['qr', 'rd', 'ra'], 'query_num': 1, 'answer_num':
    1, 'authority_num': 0, 'additional_num': 1, 'opt_pseudosection': {'edns': {'version': 0, 'flags': [], 'udp':
    4096}}, 'question': {'name': 'example.com.', 'class': 'IN', 'type': 'A'}, 'answer': [{'name': 'example.com.',
    'class': 'IN', 'type': 'A', 'ttl': 29658, 'data': '93.184.216.34'}], 'query_time': 52, 'server':
    '2600:1700:bab0:d40::1#53(2600:1700:bab0:d40::1)', 'when': 'Fri Apr 16 16:13:00 PDT 2021', 'rcvd': 56,
    'when_epoch': 1618614780, 'when_epoch_utc': None}]
"""

name = 'jc'
__version__ = '1.17.5'
