"""jc - JSON CLI output utility history Parser

Usage:
    specify --history as the first argument if the piped input is coming from history

Example:

$ history | jc --history -p
{
  "118": "sleep 100",
  "119": "ls /bin",
  "120": "echo \"hello\"",
  "121": "docker images",
  ...
}
"""


def parse(data):
    output = {}

    linedata = data.splitlines()

    # Clear any blank lines
    cleandata = list(filter(None, linedata))

    if cleandata:
        for entry in cleandata:
            parsed_line = entry.split(maxsplit=1)
            output[parsed_line[0]] = parsed_line[1]

    return output
