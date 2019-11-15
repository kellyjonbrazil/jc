"""jc - JSON CLI output utility fstab Parser

Usage:
    specify --fstab as the first argument if the piped input is coming from a fstab file

Examples:

    
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
            "ip":           string,
            "hostname": [
                            string
            ]
          }
        ]
    """

    # no additional processing needed
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

            line_list = line.split(maxsplit=5)
            fs_spec = line_list[0]
            fs_file = line_list[1]
            fs_vfstype = line_list[2]
            fs_mntops = line_list[3]
            fs_freq = line_list[4]
            fs_passno = line_list[5]

            # fstab_list = fstab.split()

            # comment_found = False
            # for i, item in enumerate(fstab_list):
            #     if item.find('#') != -1:
            #         comment_found = True
            #         comment_item = i
            #         break

            # if comment_found:
            #     fstab_list = fstab_list[:comment_item]

            output_line['fs_spec'] = fs_spec
            output_line['fs_file'] = fs_file
            output_line['fs_vfstype'] = fs_vfstype
            output_line['fs_mntops'] = fs_mntops
            output_line['fs_freq'] = fs_freq
            output_line['fs_passno'] = fs_passno

            raw_output.append(output_line)

    if raw:
        return raw_output
    else:
        return process(raw_output)
