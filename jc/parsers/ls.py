"""jc - JSON CLI output utility ls Parser

Usage:
    specify --ls as the first argument if the piped input is coming from ls

    ls options supported:
    - None
    - lah

Examples:

$ ls /usr/bin | jc --ls -p
[
  {
    "filename": "apropos"
  },
  {
    "filename": "arch"
  },
  {
    "filename": "awk"
  },
  {
    "filename": "base64"
  },
  ...
]

$ ls -l /usr/bin | jc --ls -p
[
  {
    "filename": "apropos",
    "link_to": "whatis",
    "flags": "lrwxrwxrwx.",
    "links": "1",
    "owner": "root",
    "group": "root",
    "size": "6",
    "date": "Aug 15 10:53"
  },
  {
    "filename": "arch",
    "flags": "-rwxr-xr-x.",
    "links": "1",
    "owner": "root",
    "group": "root",
    "size": "33080",
    "date": "Aug 19 23:25"
  },
  {
    "filename": "awk",
    "link_to": "gawk",
    "flags": "lrwxrwxrwx.",
    "links": "1",
    "owner": "root",
    "group": "root",
    "size": "4",
    "date": "Aug 15 10:53"
  },
  {
    "filename": "base64",
    "flags": "-rwxr-xr-x.",
    "links": "1",
    "owner": "root",
    "group": "root",
    "size": "37360",
    "date": "Aug 19 23:25"
  },
  {
    "filename": "basename",
    "flags": "-rwxr-xr-x.",
    "links": "1",
    "owner": "root",
    "group": "root",
    "size": "29032",
    "date": "Aug 19 23:25"
  },
  {
    "filename": "bash",
    "flags": "-rwxr-xr-x.",
    "links": "1",
    "owner": "root",
    "group": "root",
    "size": "964600",
    "date": "Aug 8 05:06"
  },
  ...
]

$ ls -l /usr/bin | jc --ls | jq '.[] | select(.size|tonumber > 50000000)'
{
  "filename": "emacs",
  "flags": "-r-xr-xr-x",
  "links": 1,
  "owner": "root",
  "group": "wheel",
  "size": "117164432",
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
                output_line['links'] = parsed_line[1]
                output_line['owner'] = parsed_line[2]
                output_line['group'] = parsed_line[3]
                output_line['size'] = parsed_line[4]
                output_line['date'] = ' '.join(parsed_line[5:8])
                output.append(output_line)
        else:
            for entry in cleandata:
                output_line = {}
                output_line['filename'] = entry
                output.append(output_line)

    return output
