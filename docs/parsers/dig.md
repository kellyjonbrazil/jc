
# jc.parsers.dig
jc - JSON CLI output utility dig Parser

Usage (cli):

    Specify --dig as the first argument if the piped input is coming from dig

Usage (module):

    import jc.parsers.dig
    result = jc.parsers.dig.parse(dig_command_output)

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


## info
```python
info()
```


## process
```python
process(proc_data)
```

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

    List of dictionaries. Raw or processed structured data.

