"""jc - JSON CLI output utility netstat Parser

Usage:
    specify --netstat as the first argument if the piped input is coming from netstat

Example:

$ netstat | jc --netstat -p
"""

import re

def parse(data):
    output = []
    
    cleandata = data.splitlines()

    # Delete last line if it is blank
    if cleandata[-1] == '':
        cleandata.pop(-1)

    # Delete first line if it starts with 'total'
    if cleandata[0].find('total') == 0:
        cleandata.pop(0)

    # Check if -l was used to parse extra data
    if re.match('^[-dclpsbDCMnP?]([-r][-w][-xsS]){2}([-r][-w][-xtT])[+]?', cleandata[0]):
        for entry in cleandata:
            output_line = {}

            parsed_line = entry.split()

            # split filenames and links
            filename_field = ' '.join(parsed_line[8:]).split(' -> ')

            # create list of dictionaries
            output_line['filename'] = filename_field[0]

            if len(filename_field) > 1:
                output_line['link_to'] = filename_field[1]

            output_line['flags'] = parsed_line[0]
            output_line['links'] = int(parsed_line[1])
            output_line['owner'] = parsed_line[2]
            output_line['group'] = parsed_line[3]
            output_line['bytes'] = int(parsed_line[4])
            output_line['date'] = ' '.join(parsed_line[5:8])
            output.append(output_line)
    else:
        for entry in cleandata:
            output_line = {}
            output_line['filename'] = entry
            output.append(output_line)

    return output