"""jc - JSON CLI output utility ss Parser

Usage:
    specify --ss as the first argument if the piped input is coming from ss

Examples:

    $ ss | jc --ss -p
    []

    $ ss | jc --ss -p -r
    []
"""
import string
import jc.utils


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:
        
        proc_data    (dictionary) raw structured data to process

    Returns:

        dictionary   structured data with the following schema:
    
        [
          {
            "ss":     string,
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
    compatible = ['linux']

    if not quiet:
        jc.utils.compatibility(__name__, compatible)

    contains_colon = ['nl', 'p_raw', 'raw', 'udp', 'tcp', 'v_str', 'icmp6']
    raw_output = []
    cleandata = data.splitlines()

    # Clear any blank lines
    cleandata = list(filter(None, cleandata))

    if cleandata:
        # fix 'local address' to 'local_address', same with 'peer_address'
        # split headers by whitespace and :    = 8 columns

        # only parse lines if col 0 is not whitespace

        # These require additional rsplit(':') and replace/add cols 4,5,6,7
        #     check if ':' is in the field first...
        #     final columns may not have x:y and may just have *
        # nl
        # p_raw
        # raw
        # udp
        # tcp
        # v_str
        # icmp6

        # if % in col 4 or 6 then split that out to 'interface' field
        header_text = cleandata[0].lower()
        header_text = header_text.replace('local address:port', 'local_address local_port')
        header_text = header_text.replace('peer address:port', 'peer_address peer_port')

        header_list = header_text.split()

        for entry in cleandata[1:]:
            output_line = {}
            if entry[0] not in string.whitespace:
                entry_list = entry.split()

                if entry_list[0] in contains_colon and ':' in entry_list[4]:
                    l_field = entry_list[4].rsplit(':', maxsplit=1)
                    l_address = l_field[0]
                    l_port = l_field[1]
                    entry_list[4] = l_address
                    entry_list.insert(5, l_port)

                if entry_list[0] in contains_colon and ':' in entry_list[6]:
                    p_field = entry_list[6].rsplit(':', maxsplit=1)
                    p_address = p_field[0]
                    p_port = p_field[1]
                    entry_list[6] = p_address
                    entry_list.insert(7, p_port)

            output_line = dict(zip(header_list, entry_list))
            raw_output.append(output_line)

    if raw:
        return raw_output
    else:
        return process(raw_output)
