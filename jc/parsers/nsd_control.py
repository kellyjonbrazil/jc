"""jc - JSON Convert `nsd-control` command output parser

Usage (cli):

    $ nsd-control | jc --nsd-control

or

    $ jc nsd-control

Usage (module):

    import jc
    result = jc.parse('nsd_control', nsd_control_command_output)

Schema:

    [
      {
        "version":          string,
        "verbosity":        integer,
        "ratelimit":        integer
      }
    ]

    [
      {
        "zone":             string
        "status": {
          "state":          string,
          "served-serial":  string,
          "commit-serial":  string,
          "wait":           string
        }
      }
    ]

Examples:

    $ nsd-control | jc --nsd-control status
    [
      {
        "version": "4.6.2",
        "verbosity": "2",
        "ratelimit": "0"
      }
    ]

    $ nsd-control | jc --nsd-control zonestatus sunet.se
    [
      {
        "zone": "sunet.se",
        "status": {
          "state": "ok",
          "served-serial": "2023090704 since 2023-09-07T16:34:27",
          "commit-serial": "2023090704 since 2023-09-07T16:34:27",
          "wait": "28684 sec between attempts"
        }
      }
    ]

"""
from typing import List, Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.1'
    description = '`nsd-control` command parser'
    author = 'Pettai'
    author_email = 'pettai@sunet.se'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['command']
    magic_commands = ['nsd-control']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    int_list = {'verbosity', 'ratelimit', 'wait'}

    for entry in proc_data:
        for key in entry:
            if key in int_list:
                entry[key] = jc.utils.convert_to_int(entry[key])

    return proc_data


def parse(data: str, raw: bool = False, quiet: bool = False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[Dict] = []

    if jc.utils.has_data(data):

        itrparse = False
        itr: Dict = {}

        for line in filter(None, data.splitlines()):
            line = line.strip()

            # default 'ok'
            if line.startswith('ok'):
                raw_output.append({'command': 'ok'})
                continue

            # status
            if line.startswith('version:'):
                status = {}
                linedata = line.split(':', maxsplit=1)
                version = linedata[1].strip()
                status.update({'version': version})
                continue

            if line.startswith('verbosity:'):
                linedata = line.split(':', maxsplit=1)
                verbosity = linedata[1]
                status.update({'verbosity': verbosity})
                continue

            if line.startswith('ratelimit:'):
                linedata = line.split(':', maxsplit=1)
                ratelimit = linedata[1]
                status.update({'ratelimit': ratelimit})
                raw_output.append(status)
                continue

            # print_cookie_secrets
            if line.startswith('active'):
                itrparse = True
                itr = {}
                linedata = line.split(':', maxsplit=1)
                active = linedata[1].strip()
                itr.update({'active': active})
                continue

            if line.startswith('staging'):
                linedata = line.split(':', maxsplit=1)
                staging = linedata[1].strip()
                itr.update({'staging': staging})
                continue

            # print_tsig
            if line.startswith('key:'):
                tsigs = {}
                tsigdata = dict()
                linedata = line.split(' ', maxsplit=6)
                name = linedata[2].strip('"').rstrip('"')
                tsigdata.update({'name': name})
                secret = linedata[4].strip('"').rstrip('"')
                tsigdata.update({'secret': secret})
                algorithm = linedata[6].strip('"').rstrip('"')
                tsigdata.update({'algorithm': algorithm})
                tsigs.update({'key': tsigdata})
                raw_output.append(tsigs)
                continue

            # zonestatus
            if line.startswith('zone:'):
                zonename: Dict = dict()
                zstatus: Dict = dict()
                linedata = line.split(':\t', maxsplit=1)
                zone = linedata[1]
                zonename.update({'zone': zone})
                continue

            if line.startswith('pattern:'):
                linedata = line.split(': ', maxsplit=1)
                catz_pattern = linedata[1]
                zstatus.update({'pattern': catz_pattern})
                continue

            if line.startswith('catalog-member-id:'):
                linedata = line.split(': ', maxsplit=1)
                catz_member_id = linedata[1]
                zstatus.update({'catalog-member-id': catz_member_id})
                continue

            if line.startswith('state:'):
                linedata = line.split(': ', maxsplit=1)
                state = linedata[1]
                zstatus.update({'state': state})
                continue

            if line.startswith('served-serial:'):
                linedata = line.split(': ', maxsplit=1)
                served = linedata[1].strip('"').rstrip('"')
                zstatus.update({'served-serial': served})
                continue

            if line.startswith('commit-serial:'):
                linedata = line.split(': ', maxsplit=1)
                commit = linedata[1].strip('"').rstrip('"')
                zstatus.update({'commit-serial': commit})
                continue

            if line.startswith('wait:'):
                linedata = line.split(': ', maxsplit=1)
                wait = linedata[1].strip('"').rstrip('"')
                zstatus.update({'wait': wait})
                zonename.update({'status': zstatus})
                raw_output.append(zonename)
                continue

            # stats
            if line.startswith('server') or line.startswith('num.') or line.startswith('size.') or line.startswith('time.') or line.startswith('zone.'):
                itrparse = True
                linedata = line.split('=', maxsplit=1)
                key = linedata[0]
                if key.startswith('time.'):
                    value = float(linedata[1])
                else:
                    value = int(linedata[1])
                itr.update({key: value})
                continue

        if itrparse:
            raw_output.append(itr)

    return raw_output if raw else _process(raw_output)
