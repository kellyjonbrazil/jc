r"""jc - JSON Convert `/etc/resolve.conf` file parser

This parser may be more forgiving than the system parser. For example, if
multiple `search` lists are defined, this parser will append all entries to
the `search` field, while the system parser may only use the list from the
last defined instance.

Usage (cli):

    $ cat /etc/resolve.conf | jc --resolve-conf

Usage (module):

    import jc
    result = jc.parse('resolve_conf', resolve_conf_output)

Schema:

    {
      "domain":             string,
      "search": [
                            string
      ],
      "nameservers": [
                            string
      ],
      "options": [
                            string
      ],
      "sortlist": [
                            string
      ]
    }


Examples:

    $ cat /etc/resolve.conf | jc --resolve-conf -p
    {
      "search": [
        "eng.myprime.com",
        "dev.eng.myprime.com",
        "labs.myprime.com",
        "qa.myprime.com"
      ],
      "nameservers": [
        "10.136.17.15"
      ],
      "options": [
        "rotate",
        "ndots:1"
      ]
    }
"""
import re
from typing import List, Dict
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`/etc/resolve.conf` file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['file']


__version__ = info.version


def _process(proc_data: JSONDictType) -> JSONDictType:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   Dictionary raw structured data to process

    Returns:

        Dictionary. Structured to conform to the schema.
    """
    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> JSONDictType:
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: Dict = {}
    search: List[str] = []
    nameservers: List[str] = []
    options: List[str] = []
    sortlist: List[str] = []

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):

            # comments start with # or ; and can be inline
            if '#' in line or ';' in line:
                userdata = list(filter(None, re.split("[#;]+", line, maxsplit=1)))
                userdata = [x for x in userdata if x.strip()]
                if len(userdata) <= 1:    # whole line is a comment
                    continue

                userdata_str = userdata[0].strip()

            else:
                userdata_str = line.strip()

            if userdata_str.startswith('domain'):
                raw_output['domain'] = userdata_str.split()[1].strip()
                continue

            if userdata_str.startswith('search'):
                search_items = userdata_str.split(maxsplit=1)[1]
                search_list = search_items.split()
                search.extend(search_list)
                continue

            if userdata_str.startswith('nameserver'):
                ns_str = userdata_str.split()[1]
                nameservers.append(ns_str)
                continue

            if userdata_str.startswith('options'):
                option_items = userdata_str.split(maxsplit=1)[1]
                option_list = option_items.split()
                options.extend(option_list)
                continue

            if userdata_str.startswith('sortlist'):
                sortlist_items = userdata_str.split(maxsplit=1)[1]
                sortlist_list = sortlist_items.split()
                sortlist.extend(sortlist_list)
                continue

    if search:
        raw_output['search'] = search

    if nameservers:
        raw_output['nameservers'] = nameservers

    if options:
        raw_output['options'] = options

    if sortlist:
        raw_output['sortlist'] = sortlist

    return raw_output if raw else _process(raw_output)
