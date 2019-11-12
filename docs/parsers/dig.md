# jc.parsers.dig
jc - JSON CLI output utility dig Parser

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

## process
```python
process(proc_data)
```

schema:

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
      }
    ]

## parse
```python
parse(data, raw=False, quiet=False)
```

Main parsing function

Arguments:

    raw:    (boolean) output preprocessed JSON if True
    quiet:  (boolean) suppress warning messages if True

