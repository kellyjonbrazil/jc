
# jc.parsers.dir
jc - JSON CLI output utility `dir` command output parser

Options supported:
- `/T timefield`
- `/O sortorder`
- `/C, /-C`
- `/S`

Usage (cli):

    $ dir | jc --dir -p -m

    or

    $ jc -p -m dir

Usage (module):

    import jc.parsers.dir
    result = jc.parsers.dir.parse(dir_command_output)

Compatibility:

    'win32'

Examples:

    $ dir | jc --dir -p -m
    {
      "C:\Program Files\Internet Explorer": [
        {
          "date": "03/24/2021",
          "time": "03:15 PM",
          "dir": true,
          "size": null,
          "filename": "."
        },
        {
          "date": "03/24/2021",
          "time": "03:15 PM",
          "dir": true,
          "size": null,
          "filename": ".."
        },
        {
          "date": "12/07/2019",
          "time": "02:49 AM",
          "dir": true,
          "size": null,
          "filename": "en-US"
        },
        {
          "date": "12/07/2019",
          "time": "02:09 AM",
          "dir": false,
          "size": 54784,
          "filename": "ExtExport.exe"
        },
        {
          "date": "03/24/2021",
          "time": "03:15 PM",
          "dir": false,
          "size": 0,
          "filename": "file name.txt"
        },
        {
          "date": "12/07/2019",
          "time": "02:09 AM",
          "dir": false,
          "size": 54784,
          "filename": "hmmapi.dll"
        },
        {
          "date": "12/07/2019",
          "time": "02:09 AM",
          "dir": false,
          "size": 515072,
          "filename": "iediagcmd.exe"
        },
        {
          "date": "12/07/2019",
          "time": "02:09 AM",
          "dir": false,
          "size": 504832,
          "filename": "ieinstal.exe"
        },
        {
          "date": "12/07/2019",
          "time": "02:09 AM",
          "dir": false,
          "size": 224768,
          "filename": "ielowutil.exe"
        },
        {
          "date": "12/07/2019",
          "time": "02:09 AM",
          "dir": false,
          "size": 421888,
          "filename": "IEShims.dll"
        },
        {
          "date": "12/06/2019",
          "time": "02:47 PM",
          "dir": false,
          "size": 819136,
          "filename": "iexplore.exe"
        },
        {
          "date": "12/07/2019",
          "time": "02:14 AM",
          "dir": true,
          "size": null,
          "filename": "images"
        },
        {
          "date": "12/07/2019",
          "time": "02:14 AM",
          "dir": true,
          "size": null,
          "filename": "SIGNUP"
        },
        {
          "date": "12/07/2019",
          "time": "02:09 AM",
          "dir": false,
          "size": 48536,
          "filename": "sqmapi.dll"
        }
      ]
    }


    $ dir | jc --dir -p -m -r
    {
      "C:\Program Files\Internet Explorer": [
        {
          "date": "03/24/2021",
          "time": "03:15 PM",
          "dir": true,
          "size": null,
          "filename": "."
        },
        {
          "date": "03/24/2021",
          "time": "03:15 PM",
          "dir": true,
          "size": null,
          "filename": ".."
        },
        {
          "date": "12/07/2019",
          "time": "02:49 AM",
          "dir": true,
          "size": null,
          "filename": "en-US"
        },
        {
          "date": "12/07/2019",
          "time": "02:09 AM",
          "dir": false,
          "size": "54,784",
          "filename": "ExtExport.exe"
        },
        {
          "date": "03/24/2021",
          "time": "03:15 PM",
          "dir": false,
          "size": "0",
          "filename": "file name.txt"
        },
        {
          "date": "12/07/2019",
          "time": "02:09 AM",
          "dir": false,
          "size": "54,784",
          "filename": "hmmapi.dll"
        },
        {
          "date": "12/07/2019",
          "time": "02:09 AM",
          "dir": false,
          "size": "515,072",
          "filename": "iediagcmd.exe"
        },
        {
          "date": "12/07/2019",
          "time": "02:09 AM",
          "dir": false,
          "size": "504,832",
          "filename": "ieinstal.exe"
        },
        {
          "date": "12/07/2019",
          "time": "02:09 AM",
          "dir": false,
          "size": "224,768",
          "filename": "ielowutil.exe"
        },
        {
          "date": "12/07/2019",
          "time": "02:09 AM",
          "dir": false,
          "size": "421,888",
          "filename": "IEShims.dll"
        },
        {
          "date": "12/06/2019",
          "time": "02:47 PM",
          "dir": false,
          "size": "819,136",
          "filename": "iexplore.exe"
        },
        {
          "date": "12/07/2019",
          "time": "02:14 AM",
          "dir": true,
          "size": null,
          "filename": "images"
        },
        {
          "date": "12/07/2019",
          "time": "02:14 AM",
          "dir": true,
          "size": null,
          "filename": "SIGNUP"
        },
        {
          "date": "12/07/2019",
          "time": "02:09 AM",
          "dir": false,
          "size": "48,536",
          "filename": "sqmapi.dll"
        }
      ]
    }



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

    proc_data:   (Dictionary of Lists) raw structured data to process

Returns:

    List of Dictionaries. Structured data with the following schema:
    {"parent_dir":
      [
        {
          "date": string,
          "time": string,
          "dir": string,
          "size": integer,
          "filename: string
        }
      ]
    }


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


