"""jc - JSON CLI output utility hosts Parser

Usage:
    specify --hosts as the first argument if the piped input is coming from hosts

Examples:

    $ hosts | jc --hosts -p
    []

    $ hosts | jc --hosts -p -r
    []
"""
import jc.utils


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (dictionary) raw structured data to process

    Returns:

        dictionary   structured data with the following schema:

        [
          {
            "hosts":     string,
            "bar":     boolean,
            "baz":     integer
          }
        ]
    """

    # rebuild output for added semantic information
    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        dictionary   raw or processed structured data
    """

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']

    if not quiet:
        jc.utils.compatibility(__name__, compatible)

    raw_output = []
    cleandata = data.splitlines()

    # Clear any blank lines
    cleandata = list(filter(None, cleandata))

    if cleandata:
        for line in cleandata:
            output_line = {}
            # ignore commented lines
            if line.strip().find('#') == 0:
                continue

            line_list = line.split(maxsplit=1)
            ip = line_list[0]
            hosts = line_list[1]
            hosts_list = hosts.split()

            output_line['ip'] = ip
            output_line['hostname'] = hosts_list

            raw_output.append(output_line)

    if raw:
        return raw_output
    else:
        return process(raw_output)
