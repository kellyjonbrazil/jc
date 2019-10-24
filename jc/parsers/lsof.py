"""jc - JSON CLI output utility lsof Parser

Usage:
    specify --lsof as the first argument if the piped input is coming from lsof

    Limitations:
        No additional columns are supported

Example:


"""


def parse(data):
    output = []

    linedata = data.splitlines()

    # Clear any blank lines
    cleandata = list(filter(None, linedata))

    if cleandata:

        # find column value of last character of each header
        header_row = cleandata.pop(0)
        headers = header_row.split()
        header_spec = []

        for i, h in enumerate(headers):
            # header tuple is (index, header_name, col)
            header_spec.append((i, h, header_row.find(h) + len(h)))

        # parse lines
        for entry in cleandata:
            output_line = {}

            # normalize data by inserting Null for missing data
            temp_line = entry.split(maxsplit=len(headers) - 1)

            for spec in header_spec:
                if spec[1] == 'COMMAND' or spec[1] == 'NAME':
                    continue
                if entry[spec[2] - 1] == ' ':
                    temp_line.insert(spec[0], None)

            name = ' '.join(temp_line[9:])
            fixed_line = temp_line[0:9]
            fixed_line.append(name)

            output_line = dict(zip(headers, fixed_line))
            output.append(output_line)

    return output
