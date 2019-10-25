"""jc - JSON CLI output utility jobs Parser

Usage:
    specify --jobs as the first argument if the piped input is coming from jobs

    Also supports the -l option

Example:

$ jobs -l | jc --jobs -p
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
"""
import string


def parse(data):
    output = []

    linedata = data.splitlines()

    # Clear any blank lines
    cleandata = list(filter(None, linedata))

    if cleandata:

        for entry in cleandata:
            output_line = {}
            remainder = []
            job_number = ''
            pid = ''
            job_history = ''

            parsed_line = entry.split(maxsplit=2)

            # check if -l was used
            if parsed_line[1][0] in string.digits:
                pid = parsed_line.pop(1)
                remainder = parsed_line.pop(1)
                job_number = parsed_line.pop(0)
                remainder = remainder.split(maxsplit=1)

                # rebuild parsed_line
                parsed_line = []

                for r in remainder:
                    parsed_line.append(r)

                parsed_line.insert(0, job_number)

            # check for + or - in first field
            if parsed_line[0].find('+') != -1:
                job_history = 'current'
                parsed_line[0] = parsed_line[0].rstrip('+')

            if parsed_line[0].find('-') != -1:
                job_history = 'previous'
                parsed_line[0] = parsed_line[0].rstrip('-')

            # clean up first field
            parsed_line[0] = parsed_line[0].lstrip('[').rstrip(']')

            # create list of dictionaries
            output_line['job_number'] = parsed_line[0]
            if pid:
                output_line['pid'] = pid
            if job_history:
                output_line['history'] = job_history
            output_line['status'] = parsed_line[1]
            output_line['command'] = parsed_line[2]

            output.append(output_line)

    return output
