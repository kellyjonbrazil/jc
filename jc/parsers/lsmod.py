"""jc - JSON CLI output utility lsmod Parser

Usage:
    specify --lsmod as the first argument if the piped input is coming from lsmod

Example:


"""


def parse(data):

    # code adapted from Conor Heine at:
    # https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501

    cleandata = data.splitlines()
    headers = [h for h in ' '.join(cleandata[0].strip().split()).split() if h]

    raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), cleandata[1:])
    output = [dict(zip(headers, r)) for r in raw_data]

    for entry in output:
        entry['NAME'] = entry['NAME'].encode('ascii', errors='ignore').decode()

    return output
