"""jc - JSON CLI output utility stats Parser

Usage:
    specify --stats as the first argument if the piped input is coming from stats

Examples:

    $ stats | jc --stats -p
    []

    $ stats | jc --stats -p -r
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
            "stats":     string,
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
        output_line = {}
        # stats output contains 8 lines
        for line in cleandata:

            # line #1
            if line.find('File:') == 1:
                output_line = {}
                line_list = line.split(maxsplit=1)
                output_line['file'] = line_list[1]

            # line #2
            if line.find('Size:') == 1:
                line_list = line.split(maxsplit=5)
                output_line['size'] = line_list[1]
                output_line['Blocks'] = line_list[3]
                output_line['io_blocks'] = line_list[5]
                output_line['type'] = line_list[6]

    if raw:
        return raw_output
    else:
        return process(raw_output)
