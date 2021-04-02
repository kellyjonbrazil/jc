"""jc - JSON CLI output utility `dir` command output parser

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
      "C:\\Program Files\\Internet Explorer": [
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
      "C:\\Program Files\\Internet Explorer": [
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

"""
import re
import jc.utils


class info():
    version = '1.0'
    description = 'dir command parser'
    author = 'Rasheed Elsaleh'
    author_email = 'rasheed@rebelliondefense.com'

    # compatible options: win32
    compatible = ['win32']
    magic_commands = ['dir']


__version__ = info.version


def process(proc_data):
    """
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
    """

    for _, dir_list in proc_data.items():
        for entry in dir_list:
            int_list = ["size"]
            for key in int_list:
                if entry.get(key):
                    try:
                        key_int = int(entry[key].replace(",", ""))
                    except ValueError:
                        entry[key] = None
                    else:
                        entry[key] = key_int
    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.

    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = {}

    if jc.utils.has_data(data):

        for line in data.splitlines():
            if line.startswith(" Directory of"):
                parent_dir = line.lstrip(" Directory of ")
                continue
            # skip lines that don't start with a date
            if not re.match(r'^\d{2}/\d{2}/\d{4}', line):
                continue

            raw_output.setdefault(parent_dir, [])
            output_line = {}
            parsed_line = line.split()
            output_line["date"] = parsed_line[0]
            output_line["time"] = " ".join(parsed_line[1:3])
            output_line.setdefault("dir", False)
            output_line.setdefault("size", None)
            if parsed_line[3] == "<DIR>":
                output_line["dir"] = True
            else:
                output_line["size"] = parsed_line[3]

            output_line["filename"] = " ".join(parsed_line[4:])
            raw_output[parent_dir].append(output_line)

    if raw:
        return raw_output
    else:
        return process(raw_output)
