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
    [
      {
        "id": 52172,
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
            "ttl": 27,
            "data": "151.101.65.67"
          },
          {
            "name": "cnn.com.",
            "class": "IN",
            "type": "A",
            "ttl": 27,
            "data": "151.101.129.67"
          },
          {
            "name": "cnn.com.",
            "class": "IN",
            "type": "A",
            "ttl": 27,
            "data": "151.101.1.67"
          },
          {
            "name": "cnn.com.",
            "class": "IN",
            "type": "A",
            "ttl": 27,
            "data": "151.101.193.67"
          }
        ],
        "query_time": 38,
        "server": "2600",
        "when": "Tue Mar 30 20:07:59 PDT 2021",
        "rcvd": 100,
        "when_epoch": 1617160079,
        "when_epoch_utc": null
      },
      {
        "id": 36292,
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
        "query_time": 27,
        "server": "205.251.194.64#53(205.251.194.64)",
        "when": "Tue Mar 30 20:07:59 PDT 2021",
        "rcvd": 212,
        "when_epoch": 1617160079,
        "when_epoch_utc": null
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

Version 1.7 by Kelly Brazil (kellyjonbrazil@gmail.com)
