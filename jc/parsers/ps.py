"""jc - JSON CLI output utility ps Parser

Usage:
    specify --ps as the first argument if the piped input is coming from ps

    ps options supported:
    - ef
    - axu

Examples:

"""


def parse(data):

    cleandata = data.splitlines()

    headers = [h for h in ' '.join(cleandata[0].strip().split()).split() if h]
    raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), cleandata[1:])
    return [dict(zip(headers, r)) for r in raw_data]
