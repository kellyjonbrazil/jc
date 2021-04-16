[Home](https://kellyjonbrazil.github.io/jc/)

# jc.parsers.dig
jc - JSON CLI output utility `dig` command output parser

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
                "version":      integer,
                "flags": [
                                string
                ],
                "udp":          integer
            },
            "cookie":           string
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


## info
```python
info()
```
Provides parser metadata (version, author, etc.)

## parse
```python
parse(data, raw=False, quiet=False)
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) output preprocessed JSON if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

## Parser Information
Compatibility:  linux, aix, freebsd, darwin

Version 2.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
