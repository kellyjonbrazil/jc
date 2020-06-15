"""jc - JSON CLI output utility hosts Parser

Usage:

    specify --hosts as the first argument if the piped input is coming from a hosts file

Compatibility:

    'linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd'

Examples:

    $ cat /etc/hosts | jc --hosts -p
    [
      {
        "ip": "127.0.0.1",
        "hostname": [
          "localhost"
        ]
      },
      {
        "ip": "127.0.1.1",
        "hostname": [
          "root-ubuntu"
        ]
      },
      {
        "ip": "::1",
        "hostname": [
          "ip6-localhost",
          "ip6-loopback"
        ]
      },
      {
        "ip": "fe00::0",
        "hostname": [
          "ip6-localnet"
        ]
      },
      {
        "ip": "ff00::0",
        "hostname": [
          "ip6-mcastprefix"
        ]
      },
      {
        "ip": "ff02::1",
        "hostname": [
          "ip6-allnodes"
        ]
      },
      {
        "ip": "ff02::2",
        "hostname": [
          "ip6-allrouters"
        ]
      }
    ]
"""
import jc.utils


class info():
    version = '1.2'
    description = '/etc/hosts file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']


__version__ = info.version


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (dictionary) raw structured data to process

    Returns:

        List of dictionaries. Structured data with the following schema:

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

        List of dictionaries. Raw or processed structured data.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = []

    # Clear any blank lines
    cleandata = list(filter(None, data.splitlines()))

    if jc.utils.has_data(data):

        for line in cleandata:
            output_line = {}
            # ignore commented lines
            if line.strip().startswith('#'):
                continue

            line_list = line.split(maxsplit=1)
            ip = line_list[0]
            hosts = line_list[1]
            hosts_list = hosts.split()

            comment_found = False
            for i, item in enumerate(hosts_list):
                if '#' in item:
                    comment_found = True
                    comment_item = i
                    break

            if comment_found:
                hosts_list = hosts_list[:comment_item]

            output_line['ip'] = ip
            output_line['hostname'] = hosts_list

            raw_output.append(output_line)

    if raw:
        return raw_output
    else:
        return process(raw_output)
