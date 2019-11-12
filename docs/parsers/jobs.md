# jc.parsers.jobs
jc - JSON CLI output utility jobs Parser

Usage:
    specify --jobs as the first argument if the piped input is coming from jobs

    Also supports the -l option

Example:

    $ jobs -l | jc --jobs -p
    [
      {
        "job_number": 1,
        "pid": 5283,
        "status": "Running",
        "command": "sleep 10000 &"
      },
      {
        "job_number": 2,
        "pid": 5284,
        "status": "Running",
        "command": "sleep 10100 &"
      },
      {
        "job_number": 3,
        "pid": 5285,
        "history": "previous",
        "status": "Running",
        "command": "sleep 10001 &"
      },
      {
        "job_number": 4,
        "pid": 5286,
        "history": "current",
        "status": "Running",
        "command": "sleep 10112 &"
      }
    ]

    $ jobs -l | jc --jobs -p -r
    [
      {
        "job_number": "1",
        "pid": "19510",
        "status": "Running",
        "command": "sleep 1000 &"
      },
      {
        "job_number": "2",
        "pid": "19511",
        "status": "Running",
        "command": "sleep 1001 &"
      },
      {
        "job_number": "3",
        "pid": "19512",
        "history": "previous",
        "status": "Running",
        "command": "sleep 1002 &"
      },
      {
        "job_number": "4",
        "pid": "19513",
        "history": "current",
        "status": "Running",
        "command": "sleep 1003 &"
      }
    ]

## process
```python
process(proc_data)
```

schema:
    [
      {
        "job_number":   integer,
        "pid":          integer,
        "history":      string,
        "status":       string,
        "command":      string
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

