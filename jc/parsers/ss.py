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
    
          {
            "netid":            string,
            "state":            string,
            "recv_q":           integer,
            "send_q":           integer,
            "local_address":    string,
            "local_port":       string,
            "local_port_num":   integer,
            "peer_address":     string,
            "peer_port":        string,
            "peer_port_num":    integer,
            "interface":        string
          }
        ]
    """
    for entry in proc_data:
        int_list = ['recv_q', 'send_q']
        for key in int_list:
            if key in entry:
                try:
                    key_int = int(entry[key])
                    entry[key] = key_int
                except (ValueError):
                    entry[key] = None

    if 'local_port' in entry:
            try:
                entry['local_port_num'] = int(entry['local_port'])
            except (ValueError):
                pass

    if 'peer_port' in entry:
        try:
            entry['peer_port_num'] = int(entry['peer_port'])
        except (ValueError):
            pass

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
        header_text = cleandata[0].lower()
        header_text = header_text.replace('netidstate', 'netid state')
        header_text = header_text.replace('local address:port', 'local_address local_port')
        header_text = header_text.replace('peer address:port', 'peer_address peer_port')
        header_text = header_text.replace('-', '_')

        header_list = header_text.split()

        for entry in cleandata[1:]:
            output_line = {}
            if entry[0] not in string.whitespace:
                
                # fix weird ss bug where first two columns have no space between them sometimes
                entry = entry[:5] + ' ' + entry[5:]

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

            if '%' in output_line['local_address']:
                i_field = output_line['local_address'].rsplit('%', maxsplit=1)
                output_line['local_address'] = i_field[0]
                output_line['interface'] = i_field[1]

            raw_output.append(output_line)

    if raw:
        return raw_output
    else:
        return process(raw_output)
