"""jc - JSON CLI output utility lsof Parser

Usage:
    specify --lsof as the first argument if the piped input is coming from lsof

Example:

$ sudo lsof | jc --lsof -p | more
[
  {
    "command": "systemd",
    "pid": "1",
    "tid": null,
    "user": "root",
    "fd": "cwd",
    "type": "DIR",
    "device": "8,2",
    "size_off": "4096",
    "node": "2",
    "name": "/"
  },
  {
    "command": "systemd",
    "pid": "1",
    "tid": null,
    "user": "root",
    "fd": "rtd",
    "type": "DIR",
    "device": "8,2",
    "size_off": "4096",
    "node": "2",
    "name": "/"
  },
  {
    "command": "systemd",
    "pid": "1",
    "tid": null,
    "user": "root",
    "fd": "txt",
    "type": "REG",
    "device": "8,2",
    "size_off": "1595792",
    "node": "668802",
    "name": "/lib/systemd/systemd"
  },
  {
    "command": "systemd",
    "pid": "1",
    "tid": null,
    "user": "root",
    "fd": "mem",
    "type": "REG",
    "device": "8,2",
    "size_off": "1700792",
    "node": "656167",
    "name": "/lib/x86_64-linux-gnu/libm-2.27.so"
  },
  {
    "command": "systemd",
    "pid": "1",
    "tid": null,
    "user": "root",
    "fd": "mem",
    "type": "REG",
    "device": "8,2",
    "size_off": "121016",
    "node": "655394",
    "name": "/lib/x86_64-linux-gnu/libudev.so.1.6.9"
  },
  ...
]
"""
import string


def parse(data):
    output = []

    linedata = data.splitlines()

    # Clear any blank lines
    cleandata = list(filter(None, linedata))

    if cleandata:

        # find column value of last character of each header
        header_text = cleandata.pop(0).lower()

        # clean up 'size/off' header
        # even though forward slash in a key is valid json, it can make things difficult
        header_row = header_text.replace('size/off', 'size_off')

        headers = header_row.split()

        header_spec = []
        for i, h in enumerate(headers):
            # header tuple is (index, header_name, col)
            header_spec.append((i, h, header_row.find(h) + len(h)))

        # parse lines
        for entry in cleandata:
            output_line = {}

            # normalize data by inserting Null for missing data
            temp_line = entry.split(maxsplit=len(headers) - 1)

            for spec in header_spec:

                index = spec[0]
                header_name = spec[1]
                col = spec[2] - 1     # subtract one since column starts at 0 instead of 1

                if header_name == 'command' or header_name == 'name':
                    continue
                if entry[col] in string.whitespace:
                    temp_line.insert(index, None)

            name = ' '.join(temp_line[9:])
            fixed_line = temp_line[0:9]
            fixed_line.append(name)

            output_line = dict(zip(headers, fixed_line))
            output.append(output_line)

    return output
