r"""jc - JSON Convert CEF string output streaming parser

> This streaming parser outputs JSON Lines (cli) or returns an Iterable of
> Dictionaries (module)

This parser conforms to the Microfocus Arcsight CEF specification.

This parser will accept a single CEF string or multiple CEF string lines.
Any text before "CEF" will be ignored. Syslog and CEF escaped characters
(`\\`, `\\"`, `\\]`, `\\|`, `\\=`, `\\%`, `\\#`, `\\n`, and `\\r`) are
unescaped.

Extended fields, as defined in the CEF specification, are relabeled
and the values are converted to their respective types. Extra naive and
UTC epoch timestamps are added where appropriate per the CEF specification.

A warning message to `STDERR` will be printed if an unparsable line is found
unless `--quiet` or `quiet=True` is used.

To preserve escaping and original keynames and to prevent type conversions
use the `--raw` CLI option or `raw=True` param in the `parse()` function.

Usage (cli):

    $ echo 'CEF:0|Vendor|Product|3.2.0|1|SYSTEM|1|... | jc --cef-s

Usage (module):

    import jc

    result = jc.parse('cef_s', cef_command_output.splitlines())
    for item in result:
        # do something

Schema:

See: https://www.microfocus.com/documentation/arcsight/arcsight-smartconnectors-8.3/cef-implementation-standard/Content/CEF/Chapter%201%20What%20is%20CEF.htm

> Note: Special characters in key names will be converted to underscores.

    {
      "deviceVendor":                   string,
      "deviceProduct":                  string,
      "deviceVersion":                  string,
      "deviceEventClassId":             string,
      "deviceEventClassIdNum":          integer/null,
      "name":                           string,
      "agentSeverity":                  string/integer,
      "agentSeverityString":            string,
      "agentSeverityNum":               integer/null,
      "CEFVersion":                     integer,
      <extended fields>                 string/integer/float,  # [0]
      <extended fields>"_epoch":        integer/null,  # [1]
      <extended fields>"_epoch_utc":    integer/null,  # [2]
      <custom fields>                   string,
      "unparsable":                     string  # [3]

      # below object only exists if using -qq or ignore_exceptions=True
      "_jc_meta": {
        "success":      boolean,     # false if error parsing
        "error":        string,      # exists if "success" is false
        "line":         string       # exists if "success" is false
      }
    }

    [0] Will attempt to convert extended fields to the type specified in the
        CEF specification. If conversion fails, then the field will remain
        a string.
    [1] Naive calculated epoch timestamp
    [2] Timezone-aware calculated epoch timestamp. (UTC only) This value
        will be null if a UTC timezone cannot be extracted from the original
        timestamp string value.
    [3] This field exists if the CEF line is not parsable. The value
        is the original syslog line.

Examples:

    $ cat cef.log | jc --cef-s
    {"deviceVendor":"Fortinet","deviceProduct":"FortiDeceptor","deviceV...}
    {"deviceVendor":"Trend Micro","deviceProduct":"Deep Security Agent"...}
    ...

    $ cat cef.log | jc --cef-s -r
    {"deviceVendor":"Fortinet","deviceProduct":"FortiDeceptor","deviceV...}
    {"deviceVendor":"Trend Micro","deviceProduct":"Deep Security Agent"...}
    ...
"""
from typing import Dict, Iterable, Union
import re
import jc.utils
from jc.streaming import (
    add_jc_meta, streaming_input_type_check, streaming_line_input_type_check, raise_or_yield
)
from jc.exceptions import ParseError
from jc.parsers.cef import _pycef_parse


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'CEF string streaming parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Using the pycef library at https://github.com/DavidJBianco/pycef/releases/tag/v1.11-2'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['standard', 'file', 'string']
    streaming = True


__version__ = info.version


def _process(proc_data: Dict) -> Dict:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data to conform to the schema.
    """
    # fix escape chars specified in syslog RFC 5424 and CEF spec
    # https://www.rfc-editor.org/rfc/rfc5424.html#section-6
    # https://www.microfocus.com/documentation/arcsight/arcsight-smartconnectors-8.3/cef-implementation-standard/Content/CEF/Chapter%201%20What%20is%20CEF.htm?tocpath=_____2#_Toc494359738
    escape_map = {
        r'\\': '\\',
        r'\"': '"',
        r'\]': ']',
        r'\|': '|',
        r'\=': '=',
        r'\%': '%',
        r'\#': '#',
        r'\n': '\n',
        r'\r': '\r'
    }

    int_list = {'CEFVersion'}

    severity_map = {
        None: 'Unknown',
        0: 'Low',
        1: 'Low',
        2: 'Low',
        3: 'Low',
        4: 'Medium',
        5: 'Medium',
        6: 'Medium',
        7: 'High',
        8: 'High',
        9: 'Very-High',
        10: 'Very-High'
    }

    severity_set = {'unknown', 'low', 'medium', 'high', 'very-high'}

    # set defined types for extended fields
    # see https://www.microfocus.com/documentation/arcsight/arcsight-smartconnectors-8.3/cef-implementation-standard/#CEF/Chapter%202%20ArcSight%20Extension.htm
    extended_ints = {
        'spid', 'customerKey', 'deviceTranslatedZoneKey', 'oldFileSize',
        'destinationTranslatedPort', 'cn3', 'sourceTranslatedPort', 'in', 'fsize', 'slat',
        'dpid', 'cnt', 'agentZoneKey', 'out', 'type', 'eventId', 'dlong', 'cn2',
        'deviceDirection', 'spt', 'agentTranslatedZoneKey', 'sTranslatedZoneKey', 'cn1',
        'slong', 'dZoneKey', 'deviceZoneKey', 'dvcpid', 'dpt', 'dTranslatedZoneKey', 'dlat',
        'sZoneKey'
    }

    extended_floats = {
        'cfp1', 'cfp2', 'cfp3', 'cfp4'
    }

    extended_dt = {
        'deviceCustomDate1', 'deviceCustomDate2', 'end', 'fileCreateTime',
        'fileModificationTime', 'flexDate1', 'oldFileCreateTime', 'oldFileModificationTime',
        'rt', 'start', 'art'
    }

    for key, value in proc_data.copy().items():
        if key in extended_ints:
            try:
                proc_data[key] = int(value)
            except Exception:
                pass

        if key in extended_floats:
            try:
                proc_data[key] = float(value)
            except Exception:
                pass

        if key in extended_dt:
            if re.match(r'\d{10,13}', proc_data[key]):
                proc_data[key + '_epoch'] = int(proc_data[key][:10])
                proc_data[key + '_epoch_utc'] = None
            else:
                formats = (1400, 1410, 1420, 1430)
                dt = jc.utils.timestamp(proc_data[key], formats)
                proc_data[key + '_epoch'] = dt.naive
                proc_data[key + '_epoch_utc'] = dt.utc

    # Process custom field labels (adapted from pycef library)
    cleanup_list = []
    custom_fields = list(proc_data.keys())
    for key in custom_fields:
        if key.endswith('Label'):
            customlabel = key[:-5]
            for customfield in custom_fields:
                new_name = proc_data[key]
                # check for normal custom fields
                if customfield == customlabel:
                    proc_data[new_name] = proc_data[customfield]
                    cleanup_list.append(customfield)
                    cleanup_list.append(key)

                # check for datetime objects
                if customfield == customlabel + '_epoch':
                    proc_data[new_name + '_epoch'] = proc_data[customfield]
                    cleanup_list.append(customfield)

                if customfield == customlabel + '_epoch_utc':
                    proc_data[new_name + '_epoch_utc'] = proc_data[customfield]
                    cleanup_list.append(customfield)

    # cleanup extra custom fields
    for key in cleanup_list:
        del proc_data[key]

    # more normalization
    for key, value in proc_data.copy().items():
        if isinstance(proc_data[key], str):
            # remove any spaces around values
            proc_data[key] = value.strip()

            # fixup escaped characters
            for esc, esc_sub in escape_map.items():
                proc_data[key] = proc_data[key].replace(esc, esc_sub)

        # normalize keynames
        new_key = key.strip()
        new_key = re.sub(r'[^a-zA-Z0-9]', '_', new_key)
        new_key = new_key.strip('_')
        proc_data[new_key] = proc_data.pop(key)

        # integer conversions
        if key in int_list:
            proc_data[key] = jc.utils.convert_to_int(proc_data[key])

    # set agentSeverityString and agentSeverityNum:
    if 'agentSeverity' in proc_data:
        if proc_data['agentSeverity'].lower() in severity_set:
            proc_data['agentSeverityString'] = proc_data['agentSeverity']
            proc_data['agentSeverityNum'] = None
        else:
            try:
                proc_data['agentSeverityString'] = severity_map[int(proc_data['agentSeverity'])]
                proc_data['agentSeverityNum'] = int(proc_data['agentSeverity'])
            except Exception:
                pass

    # set deviceEventClassIdNum:
    if 'deviceEventClassId' in proc_data:
        proc_data['deviceEventClassIdNum'] = jc.utils.convert_to_int(proc_data['deviceEventClassId'])

    return proc_data


@add_jc_meta
def parse(
    data: Iterable[str],
    raw: bool = False,
    quiet: bool = False,
    ignore_exceptions: bool = False
) -> Union[Iterable[Dict], tuple]:
    """
    Main text parsing generator function. Returns an iterable object.

    Parameters:

        data:              (iterable)  line-based text data to parse
                                       (e.g. sys.stdin or str.splitlines())

        raw:               (boolean)   unprocessed output if True
        quiet:             (boolean)   suppress warning messages if True
        ignore_exceptions: (boolean)   ignore parsing exceptions if True


    Returns:

        Iterable of Dictionaries
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    streaming_input_type_check(data)

    for line in data:
        try:
            streaming_line_input_type_check(line)
            output_line: Dict = {}

            #skip blank lines
            if not line.strip():
                continue

            try:
                output_line = _pycef_parse(line)

            except Exception:
                output_line = {
                    'unparsable': line.rstrip()
                }

                if not quiet:
                    jc.utils.warning_message(
                        [f'Unparsable line found: {line.rstrip()}']
                    )

            if output_line:
                yield output_line if raw else _process(output_line)

        except Exception as e:
            yield raise_or_yield(ignore_exceptions, e, line)
