"""jc - JSON CLI output utility lsblk Parser

Usage:
    specify --lsblk as the first argument if the piped input is coming from lsblk



Examples:


"""
import jc.utils


def process(proc_data):
    '''schema:
    [
      {
        "name":         string,
        "maj_min":      string,
        "rm":           boolean,
        "size":         string,
        "ro":           boolean,
        "type":         string,
        "mountpoint":   string,
        "kname":        string,
        "fstype":       string,
        "label":        string,
        "uuid":         string,
        "partlabel":    string,
        "partuuid":     string,
        "ra":           boolean,
        "model":        string,
        "serial":       string,
        "state":        string,
        "owner":        string,
        "group":        string,
        "mode":         string,
        "alignment":    integer,
        "min_io":       integer,
        "opt_io":       integer,
        "phy_sec":      integer,
        "log_sec":      integer,
        "rota":         boolean,
        "sched":        string,
        "rq_size":      integer,
        "disc_aln":     integer,
        "disc_gran":    string,
        "disc_max":     string,
        "disc_zero":    boolean,
        "wsame":        string,
        "wwn":          string,
        "rand":         boolean,
        "pkname":       string,
        "hctl":         string,
        "tran":         string,
        "rev":          string,
        "vendor":       string
      }
    ]
    '''
    for entry in proc_data:
        # boolean changes
        bool_list = ['rm', 'ro', 'ra', 'rota', 'disc_zero', 'rand']
        for key in bool_list:
            if key in entry:
                try:
                    key_bool = bool(int(entry[key]))
                    entry[key] = key_bool
                except (ValueError):
                    entry[key] = None

        # integer changes
        int_list = ['alignment', 'min_io', 'opt_io', 'phy_sec', 'log_sec', 'rq_size', 'disc_aln']
        for key in int_list:
            if key in entry:
                try:
                    key_int = int(entry[key])
                    entry[key] = key_int
                except (ValueError):
                    entry[key] = None

    return proc_data


def parse_pairs(p_data):
    '''Used if -P option is detected'''
    pass


def parse(data, raw=False, quiet=False):
    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux']

    if not quiet:
        jc.utils.compatibility(__name__, compatible)

    raw_output = []
    linedata = data.splitlines()
    # Clear any blank lines
    cleandata = list(filter(None, linedata))
    cleandata = data.splitlines()

    header_text = cleandata.pop(0).lower()
    header_text = header_text.replace(':', '_')
    header_text = header_text.replace('-', '_')
    header_text = header_text + ' '

    header_list = header_text.split()

    # find each column index and end position
    header_search = [header_list[0]]
    for h in header_list[1:]:
        header_search.append(' ' + h + ' ')

    header_spec_list = []
    for i, column in enumerate(header_list[0:len(header_list) - 1]):
        header_spec = {
            'name': column,
            'end': header_text.find(header_search[i + 1]) + 1
        }

        # fix weird 'rev' column
        if header_search[i + 1] == ' rev ':
            end_fix = header_spec['end'] - 1
            header_spec['end'] = end_fix

        header_spec_list.append(header_spec)

    # parse lines
    if cleandata:
        for entry in cleandata:
            output_line = {}

            # insert new separator since data can contain spaces
            for col in reversed(header_list):
                # find the right header_spec
                for h_spec in header_spec_list:
                    if h_spec['name'] == col:
                        h_end = h_spec['end']
                        # insert \u2026 delimiter
                        entry = entry[:h_end] + '~' + entry[h_end:]

            # create the entry list from the new delimiter
            entry_list = entry.split('~', maxsplit=len(header_list) - 1)

            # clean up leading and trailing spaces in entry
            clean_entry_list = []
            for col in entry_list:
                clean_entry_list.append(col.strip().rstrip())

            output_line = dict(zip(header_list, clean_entry_list))
            raw_output.append(output_line)

        for entry in raw_output:
            entry['name'] = entry['name'].encode('ascii', errors='ignore').decode()

    if raw:
        return raw_output
    else:
        return process(raw_output)
