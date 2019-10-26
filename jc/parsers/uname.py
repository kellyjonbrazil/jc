"""jc - JSON CLI output utility uname Parser

Usage:
    specify --uname as the first argument if the piped input is coming from uname

Limitations:
    must use 'uname -a'

Example:

$ uname -a | jc --uname -p
{
  "kernel_name": "Linux",
  "node_name": "user-ubuntu",
  "kernel_release": "4.15.0-65-generic",
  "operating_system": "GNU/Linux",
  "hardware_platform": "x86_64",
  "processor": "x86_64",
  "machine": "x86_64",
  "kernel_version": "#74-Ubuntu SMP Tue Sep 17 17:06:04 UTC 2019"
}
"""


def parse(data):
    output = {}
    parsed_line = data.split(maxsplit=3)

    if len(parsed_line) > 1:

        output['kernel_name'] = parsed_line.pop(0)
        output['node_name'] = parsed_line.pop(0)
        output['kernel_release'] = parsed_line.pop(0)

        parsed_line = parsed_line[-1].rsplit(maxsplit=4)

        output['operating_system'] = parsed_line.pop(-1)
        output['hardware_platform'] = parsed_line.pop(-1)
        output['processor'] = parsed_line.pop(-1)
        output['machine'] = parsed_line.pop(-1)

        output['kernel_version'] = parsed_line.pop(0)

    return output
