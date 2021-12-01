"""jc - JSON CLI output utility `iostat` command output parser

<<Short iostat description and caveats>>

Usage (cli):

    $ iostat | jc --iostat

    or

    $ jc iostat

Usage (module):

    import jc.parsers.iostat
    result = jc.parsers.iostat.parse(iostat_command_output)

Schema:

    [
      {
        "iostat":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ iostat | jc --iostat -p
    []

    $ iostat | jc --iostat -p -r
    []
"""
import jc.utils
import jc.parsers.universal


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`iostat` command parser'
    author = 'John Doe'
    author_email = 'johndoe@gmail.com'
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    magic_commands = ['iostat']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """

    # process the data here
    # rebuild output for added semantic information
    # use helper functions in jc.utils for int, float, bool conversions and timestamps

    return proc_data

def _normalize_headers(line):
    return line.replace('%', ' ').replace('/', '_').lower()

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
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = []

    if jc.utils.has_data(data):
        section = ''  # either 'cpu' or 'device'
        headers = ''
        cpu_list = []
        device_list = []

        for line in filter(None, data.splitlines()):
            if line.startswith('avg-cpu:'):
                if cpu_list:
                    output_list = jc.parsers.universal.simple_table_parse(cpu_list)
                    for item in output_list:
                        item['type'] = 'cpu'
                    raw_output.extend(output_list)
                    cpu_list = []

                if device_list:
                    output_list = jc.parsers.universal.simple_table_parse(device_list)
                    for item in output_list:
                        item['type'] = 'device'
                    raw_output.extend(output_list)
                    device_list = []

                section = 'cpu'
                headers = _normalize_headers(line)
                headers = headers.strip().split(':', maxsplit=1)[1:]
                headers = ' '.join(headers)
                cpu_list.append(headers)
                continue

            if line.startswith('Device:'):
                if cpu_list:
                    output_list = jc.parsers.universal.simple_table_parse(cpu_list)
                    for item in output_list:
                        item['type'] = 'cpu'
                    raw_output.extend(output_list)
                    cpu_list = []

                if device_list:
                    output_list = jc.parsers.universal.simple_table_parse(device_list)
                    for item in output_list:
                        item['type'] = 'device'
                    raw_output.extend(output_list)
                    device_list = []

                section = 'device'
                headers = _normalize_headers(line)
                headers = headers.replace(':', ' ')
                device_list.append(headers)
                continue

            if section == 'cpu':
                cpu_list.append(line)

            if section == 'device':
                device_list.append(line)

    if cpu_list:
        output_list = jc.parsers.universal.simple_table_parse(cpu_list)
        for item in output_list:
            item['type'] = 'cpu'
        raw_output.extend(output_list)
        cpu_list = []

    if device_list:
        output_list = jc.parsers.universal.simple_table_parse(device_list)
        for item in output_list:
            item['type'] = 'device'
        raw_output.extend(output_list)
        device_list = []

    return raw_output if raw else _process(raw_output)

if __name__ == '__main__':
    pass
