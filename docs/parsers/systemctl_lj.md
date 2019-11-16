# jc.parsers.systemctl_lj
jc - JSON CLI output utility systemctl-lj Parser

Usage:
    specify --systemctl-luf as the first argument if the piped input is coming from systemctl list-jobs

Examples:

    $ systemctl list-jobs| jc --systemctl-lj -p
    [
      {
        "job": 3543,
        "unit": "nginxAfterGlusterfs.service",
        "type": "start",
        "state": "waiting"
      },
      {
        "job": 3545,
        "unit": "glusterReadyForLocalhostMount.service",
        "type": "start",
        "state": "running"
      },
      {
        "job": 3506,
        "unit": "nginx.service",
        "type": "start",
        "state": "waiting"
      }
    ]

    $ systemctl list-jobs| jc --systemctl-lj -p -r
    [
      {
        "job": "3543",
        "unit": "nginxAfterGlusterfs.service",
        "type": "start",
        "state": "waiting"
      },
      {
        "job": "3545",
        "unit": "glusterReadyForLocalhostMount.service",
        "type": "start",
        "state": "running"
      },
      {
        "job": "3506",
        "unit": "nginx.service",
        "type": "start",
        "state": "waiting"
      }
    ]


## process
```python
process(proc_data)
```

Final processing to conform to the schema.

Parameters:

    proc_data:   (dictionary) raw structured data to process

Returns:

    dictionary   structured data with the following schema:

    [
      {
        "job":      integer,
        "unit":     string,
        "type":     string,
        "state":    string
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

    dictionary   raw or processed structured data

