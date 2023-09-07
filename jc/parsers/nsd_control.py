"""jc - JSON Convert `nsd-control` command output parser

<<Short nsd-control description and caveats>>

Usage (cli):

    $ nsd-control | jc --nsd-control

or

    $ jc nsd-control

Usage (module):

    import jc
    result = jc.parse('nsd-control', nsd-control_command_output)

Schema:

    [
      {
        "version":    string,
        "verbosity":  integer,
        "ratelimit":  integer 
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
    version = '1.0'
    description = '`nsd-control` command parser'
    author = 'Pettai'
    author_email = 'pettai@sunet.se'
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']

    # tags options: generic, standard, file, string, binary, command
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

    # process the data here

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
 
    warned = False

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):

            # parse the content here
            # check out helper functions in jc.utils
            # and jc.parsers.universal

            # default 'ok'
            if line.startswith('ok'):
                raw_output.append({'command': 'ok'})

            # status
            elif line.startswith('version:'):
                status = {}
                linedata = line.rsplit(':', maxsplit=1)
                version = linedata[1].strip().rstrip()
                status.update({'version': version})

            elif line.startswith('verbosity:'):
                linedata = line.rsplit(':', maxsplit=1)
                verbosity = linedata[1].strip().rstrip()
                status.update({'verbosity': verbosity})

            elif line.startswith('ratelimit:'):
                linedata = line.rsplit(':', maxsplit=1)
                ratelimit = linedata[1].strip().rstrip()
                status.update({'ratelimit': ratelimit})
                raw_output.append(status)

            # print_cookie_secrets
            elif line.startswith('active'):
                linedata = line.rsplit(':', maxsplit=1)
                secret = linedata[1].strip().rstrip()
                raw_output.append({'active': secret})

            # print_tsig
            elif line.startswith('key:'):
                tsigs = {}
                tsigdata = dict()
                linedata = line.rsplit(' ', maxsplit=6)
                name = linedata[2].strip('"').rstrip('"')
                tsigdata.update({'name': name})
                secret = linedata[4].strip('"').rstrip('"')
                tsigdata.update({'secret': secret})
                algorithm = linedata[6].strip('"').rstrip('"')
                tsigdata.update({'algorithm': algorithm})
                tsigs.update({'key': tsigdata})
                raw_output.append(tsigs)

            # zonestatus
            elif line.startswith('zone:'):
                zonename = dict()
                zstatus = dict()
                linedata = line.rsplit(':\t', maxsplit=1)
                zone = linedata[1].strip().rstrip()
                zonename.update({'zone': zone})

            elif line.startswith('\tstate:'):
                linedata = line.rsplit(': ', maxsplit=1)
                state = linedata[1].strip().rstrip()
                zstatus.update({'state': state})

            elif line.startswith('\tserved-serial:'):
                linedata = line.rsplit(': ', maxsplit=1)
                served = linedata[1].strip('"').rstrip('"')
                zstatus.update({'served-serial': served})

            elif line.startswith('\tcommit-serial:'):
                linedata = line.rsplit(': ', maxsplit=1)
                commit = linedata[1].strip('"').rstrip('"')
                zstatus.update({'commit-serial': commit})

            elif line.startswith('\twait:'):
                linedata = line.rsplit(': ', maxsplit=1)
                wait = linedata[1].strip('"').rstrip('"')
                zstatus.update({'wait': wait})
                zonename.update({'status': zstatus})
                raw_output.append(zonename)


    return raw_output if raw else _process(raw_output)
