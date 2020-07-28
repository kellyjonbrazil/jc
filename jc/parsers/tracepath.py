"""jc - JSON CLI output utility tracepath Parser

Usage:

    specify --tracepath as the first argument if the piped input is coming from tracepath

Compatibility:

    'linux'

Examples:

    $ tracepath6 3ffe:2400:0:109::2 | jc --tracepath -p
    {
      "pmtu": 1480,
      "forward_hops": 2,
      "return_hops": 2,
      "hops": [
        {
          "ttl": 1,
          "guess": true,
          "host": "[LOCALHOST]",
          "reply_ms": null,
          "pmtu": 1500,
          "asymmetric_difference": null,
          "reached": false
        },
        {
          "ttl": 1,
          "guess": false,
          "host": "dust.inr.ac.ru",
          "reply_ms": 0.411,
          "pmtu": null,
          "asymmetric_difference": null,
          "reached": false
        },
        {
          "ttl": 2,
          "guess": false,
          "host": "dust.inr.ac.ru",
          "reply_ms": 0.39,
          "pmtu": 1480,
          "asymmetric_difference": 1,
          "reached": false
        },
        {
          "ttl": 2,
          "guess": false,
          "host": "3ffe:2400:0:109::2",
          "reply_ms": 463.514,
          "pmtu": null,
          "asymmetric_difference": null,
          "reached": true
        }
      ]
    }

    $ tracepath6 3ffe:2400:0:109::2 | jc --tracepath -p -r
    {
      "pmtu": "1480",
      "forward_hops": "2",
      "return_hops": "2",
      "hops": [
        {
          "ttl": "1",
          "guess": true,
          "host": "[LOCALHOST]",
          "reply_ms": null,
          "pmtu": "1500",
          "asymmetric_difference": null,
          "reached": false
        },
        {
          "ttl": "1",
          "guess": false,
          "host": "dust.inr.ac.ru",
          "reply_ms": "0.411",
          "pmtu": null,
          "asymmetric_difference": null,
          "reached": false
        },
        {
          "ttl": "2",
          "guess": false,
          "host": "dust.inr.ac.ru",
          "reply_ms": "0.390",
          "pmtu": "1480",
          "asymmetric_difference": "1",
          "reached": false
        },
        {
          "ttl": "2",
          "guess": false,
          "host": "3ffe:2400:0:109::2",
          "reply_ms": "463.514",
          "pmtu": null,
          "asymmetric_difference": null,
          "reached": true
        }
      ]
    }

"""
import re
import jc.utils


class info():
    version = '1.0'
    description = 'tracepath command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux']
    magic_commands = ['tracepath', 'tracepath6']


__version__ = info.version


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data with the following schema:

        {
          "pmtu":                       integer,
          "forward_hops":               integer,
          "return_hops":                integer,
          "hops": [
            {
              "ttl":                    integer,
              "guess":                  boolean,
              "host":                   string,
              "reply_ms":               float,
              "pmtu":                   integer,
              "asymmetric_difference":  integer,
              "reached":                boolean
            }
          ]
        }
    """
    int_list = ['pmtu', 'forward_hops', 'return_hops', 'ttl', 'asymmetric_difference']
    float_list = ['reply_ms']

    for key, value in proc_data.items():
        for item in int_list:
            if key in int_list:
                try:
                    proc_data[key] = int(proc_data[key])
                except (ValueError, TypeError):
                    proc_data[key] = None

        for item in int_list:
            if key in float_list:
                try:
                    proc_data[key] = float(proc_data[key])
                except (ValueError, TypeError):
                    proc_data[key] = None

    if 'hops' in proc_data:
        for entry in proc_data['hops']:
            for key in int_list:
                if key in entry:
                    try:
                        entry[key] = int(entry[key])
                    except (ValueError, TypeError):
                        entry[key] = None

            for key in float_list:
                if key in entry:
                    try:
                        entry[key] = float(entry[key])
                    except (ValueError, TypeError):
                        entry[key] = None

    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    RE_TTL_HOST = re.compile(r'^\s?(?P<ttl>\d+)(?P<ttl_guess>\??):\s+(?P<host>(?:no reply|\S+))')  # groups: ttl, ttl_guess, host
    RE_PMTU = re.compile(r'\spmtu\s(?P<pmtu>[\d]+)')          # group: pmtu
    RE_REPLY_MS = re.compile(r'\s(?P<reply_ms>\d*\.\d*)ms')   # group: reply_ms
    RE_ASYMM = re.compile(r'\sasymm\s+(?P<asymm>[\d]+)')      # group: asymm
    RE_REACHED = re.compile(r'\sreached')
    RE_SUMMARY = re.compile(r'\s+Resume:\s+pmtu\s+(?P<pmtu>\d+)(?:\s+hops\s+(?P<hops>\d+))?(?:\s+back\s+(?P<back>\d+))?')  # groups: pmtu, hops, back

    raw_output = {}

    if jc.utils.has_data(data):
        hops = []

        for line in filter(None, data.splitlines()):
            # grab hop information
            ttl_host = re.search(RE_TTL_HOST, line)
            pmtu = re.search(RE_PMTU, line)
            reply_ms = re.search(RE_REPLY_MS, line)
            asymm = re.search(RE_ASYMM, line)
            reached = re.search(RE_REACHED, line)
            summary = re.search(RE_SUMMARY, line)

            if ttl_host:
                hop = {
                    'ttl': ttl_host.group('ttl'),
                    'guess': bool(ttl_host.group('ttl_guess')),
                    'host': ttl_host.group('host') if ttl_host.group('host') != 'no reply' else None,
                    'reply_ms': reply_ms.group('reply_ms') if reply_ms else None,
                    'pmtu': pmtu.group('pmtu') if pmtu else None,
                    'asymmetric_difference': asymm.group('asymm') if asymm else None,
                    'reached': bool(reached)
                }

                hops.append(hop)
                continue

            elif summary:
                raw_output = {
                    'pmtu': summary.group('pmtu') if summary.group('pmtu') else None,
                    'forward_hops': summary.group('hops') if summary.group('hops') else None,
                    'return_hops': summary.group('back') if summary.group('back') else None,
                    'hops': hops
                }

    if raw:
        return raw_output
    else:
        return process(raw_output)
