"""jc - JSON CLI output utility arp Parser

Usage:
    specify --arp as the first argument if the piped input is coming from arp

Example:

$ arp | jc --arp -p
[
  {
    "address": "gateway",
    "hwtype": "ether",
    "hwaddress": "00:50:56:f7:4a:fc",
    "flags_mask": "C",
    "iface": "ens33"
  },
  {
    "address": "192.168.71.254",
    "hwtype": "ether",
    "hwaddress": "00:50:56:fe:7a:b4",
    "flags_mask": "C",
    "iface": "ens33"
  }
]
"""


def parse(data):

    # code adapted from Conor Heine at:
    # https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501

    cleandata = data.splitlines()

    # remove final Entries row if -v was used
    if cleandata[-1].find("Entries:") == 0:
        cleandata.pop(-1)

    # fix header row to change Flags Mask to flags_mask
    cleandata[0] = cleandata[0].replace('Flags Mask', 'flags_mask')

    headers = [h for h in ' '.join(cleandata[0].lower().strip().split()).split() if h]
    raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), cleandata[1:])

    return [dict(zip(headers, r)) for r in raw_data]
