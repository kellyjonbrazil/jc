"""jc - JSON Convert Syslog RFC 5424 string parser

<<Short syslog-5424 description and caveats>>

Usage (cli):

    $ syslogstring | jc --syslog

    or

    $ jc syslog-5424

Usage (module):

    import jc
    result = jc.parse('syslog', syslog_command_output)

Schema:

    [
      {
        "priority":                   integer,
        "version":                    integer,
        "timestamp":                  string,          # add epoch fields
        "hostname":                   string,
        "appname":                    string,
        "proc_id":                    integer,
        "msg_id":                     string,
        "structured_data": [
          {
            "identity":               string,
            "values": {
              "<key>":                string
            }
          }
        ],
        "message":                    string
      }
    ]

Examples:

    $ syslog-5424 | jc --syslog-5424 -p
    []

    $ syslog-5424 | jc --syslog-5424 -p -r
    []
"""
import re
from typing import List, Dict, Optional
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'Syslog RFC 5424 string parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']

__version__ = info.version


# fix escape chars specified in syslog RFC 5424
# https://www.rfc-editor.org/rfc/rfc5424.html#section-6
escape_map = {
    r'\\': '\\',
    r'\"': r'"',
    r'\]': r']'
}


def _extract_structs(structs_string: str) -> List[str]:
    struct_match = re.compile(r'(?P<eachstruct>\[.+?(?<!\\)\])')
    each_struct = struct_match.findall(structs_string)
    my_structs = []

    if each_struct:
        for structured in each_struct:
            my_structs.append(structured)

    return my_structs


def _extract_ident(struct_string) -> Optional[str]:
    ident = re.compile(r'\[(?P<ident>[^\[\=\x22\]\x20]{1,32})\s')
    ident_match = ident.search(struct_string)
    if ident_match:
        return ident_match.group('ident')
    return None


def _extract_kv(struct_string) -> List[Dict]:
    key_vals = re.compile(r'(?P<key>\w+)=(?P<val>\"[^\"]*\")')
    key_vals_match = key_vals.findall(struct_string)
    kv_list = []

    if key_vals_match:
        for kv in key_vals_match:
            key, val = kv

            # fixup escaped characters
            for esc, esc_sub in escape_map.items():
                val = val.replace(esc, esc_sub)

            kv_list.append({key: val[1:-1]})

    return kv_list


def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    for item in proc_data:
        for key, value in item.items():
            # remove any spaces around values
            if item[key]:
                item[key] = value.strip()

        # fixup escaped characters
        if item['message']:
            for esc, esc_sub in escape_map.items():
                item['message'] = item['message'].replace(esc, esc_sub)

        # parse identity and key value pairs in the structured data section
        structs = None
        if item['structured_data']:
            structs_list = []
            structs = _extract_structs(item['structured_data'])

            for a_struct in structs:
                struct_obj = {
                    'identity': _extract_ident(a_struct)
                }

                my_values = {}

                for val_obj in _extract_kv(a_struct):
                    my_values.update(val_obj)

                struct_obj.update({'values': my_values})  # type: ignore
                structs_list.append(struct_obj)

            item['structured_data'] = structs_list

    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> List[Dict]:
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

    raw_output: List = []
    syslog_out = {}

    # inspired by https://regex101.com/library/Wgbxn2
    syslog = re.compile(r'''
        (?P<priority><(\d|\d{2}|1[1-8]\d|19[01])>)?
        (?P<version>\d{1,2})?\s*
        (?P<timestamp>-|(?P<fullyear>[12]\d{3})-
            (?P<month>0\d|[1][012])-
            (?P<mday>[012]\d|3[01])T
            (?P<hour>[01]\d|2[0-4]):
            (?P<minute>[0-5]\d):
            (?P<second>[0-5]\d|60)(?#60seconds can be used for leap year!)(?:\.
            (?P<secfrac>\d{1,6}))?
            (?P<numoffset>Z|[+-]\d{2}:\d{2})(?#=timezone))\s
        (?P<hostname>[\S]{1,255})\s
        (?P<appname>[\S]{1,48})\s
        (?P<procid>[\S]{1,128})\s
        (?P<msgid>[\S]{1,32})\s
        (?P<structureddata>-|(?:\[.+?(?<!\\)\])+)
        (?:\s(?P<msg>.+))?
        ''', re.VERBOSE
    )

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            syslog_match = syslog.match(line)
            if syslog_match:
                syslog_dict = syslog_match.groupdict()
                for item in syslog_dict:
                    if syslog_dict[item] == '-':
                        syslog_dict[item] = None

                priority = None

                if syslog_dict['priority']:
                    priority = syslog_dict['priority'][1:-1]

                syslog_out = {
                    'priority': priority,
                    'version': syslog_dict['version'],
                    'timestamp': syslog_dict['timestamp'],
                    'hostname': syslog_dict['hostname'],
                    'appname': syslog_dict['appname'],
                    'proc_id': syslog_dict['procid'],
                    'msg_id': syslog_dict['msgid'],
                    'structured_data': syslog_dict['structureddata'],
                    'message': syslog_dict['msg']
                }

            if syslog_out:
                raw_output.append(syslog_out)

    return raw_output if raw else _process(raw_output)
