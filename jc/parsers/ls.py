"""jc - JSON CLI output utility ls Parser

Usage:
    specify --ls as the first argument if the piped input is coming from ls

    ls options supported:
    - None
    - l
    - a

Examples:

$ ls -a /usr/bin | jc --ls -p
[
  {
    "filename": "."
  },
  {
    "filename": ".."
  },
  {
    "filename": "2to3-"
  },
  {
    "filename": "2to3-2.7"
  },
  {
    "filename": "AssetCacheLocatorUtil"
  },
  ...
]

$ ls -al /usr/bin | jc --ls -p
[
  {
    "filename": ".",
    "flags": "drwxr-xr-x",
    "links": 970,
    "owner": "root",
    "group": "wheel",
    "bytes": 31040,
    "date": "Aug 27 21:20"
  },
  {
    "filename": "..",
    "flags": "drwxr-xr-x@",
    "links": 9,
    "owner": "root",
    "group": "wheel",
    "bytes": 288,
    "date": "May 3 22:14"
  },
  {
    "filename": "2to3-",
    "flags": "-rwxr-xr-x",
    "links": 4,
    "owner": "root",
    "group": "wheel",
    "bytes": 925,
    "date": "Feb 22 2019"
  },
  {
    "filename": "2to3-2.7",
    "link_to": "../../System/Library/Frameworks/Python.framework/Versions/2.7/bin/2to3-2.7",
    "flags": "lrwxr-xr-x",
    "links": 1,
    "owner": "root",
    "group": "wheel",
    "bytes": 74,
    "date": "May 4 02:12"
  },
  ...
]

$ $ ls -l /usr/bin | jc --ls | jq .[] | jq 'select(.bytes > 50000000)'
{
  "filename": "emacs",
  "flags": "-r-xr-xr-x",
  "links": 1,
  "owner": "root",
  "group": "wheel",
  "bytes": 117164432,
  "date": "May 3 22:26"
}
"""
import re


def parse(data):
    output = []

    linedata = data.splitlines()

    # Delete first line if it starts with 'total'
    if linedata:
        if linedata[0].find('total') == 0:
            linedata.pop(0)

    # Clear any blank lines
    cleandata = list(filter(None, linedata))

    if cleandata:
        # Check if -l was used to parse extra data
        if re.match('^[-dclpsbDCMnP?]([-r][-w][-xsS]){2}([-r][-w][-xtT])[+]?', cleandata[0]):
            for entry in cleandata:
                output_line = {}

                parsed_line = entry.split(maxsplit=8)

                # split filenames and links
                filename_field = parsed_line[8].split(' -> ')

                # create list of dictionaries
                output_line['filename'] = filename_field[0]

                if len(filename_field) > 1:
                    output_line['link_to'] = filename_field[1]

                output_line['flags'] = parsed_line[0]
                output_line['links'] = int(parsed_line[1])
                output_line['owner'] = parsed_line[2]
                output_line['group'] = parsed_line[3]
                output_line['bytes'] = int(parsed_line[4])
                output_line['date'] = ' '.join(parsed_line[5:8])
                output.append(output_line)
        else:
            for entry in cleandata:
                output_line = {}
                output_line['filename'] = entry
                output.append(output_line)

    return output
