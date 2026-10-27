r"""jc - JSON Convert PLIST file parser

Converts binary, XML, and NeXTSTEP PLIST files.

Binary values are converted into an ASCII hex representation.

Datetime objects are converted into Unix epoch timestamps and ISO strings.
The timestamp and ISO string will maintain the same naive or timezone-aware
properties as the object in the original PLIST file.

Usage (cli):

    $ cat file.plist | jc --plist

Usage (module):

    import jc
    result = jc.parse('plist', plist_file_output)

Schema:

    {
      "<key>":            string/integer/float/boolean/object/array/null
    }

Examples:

    $ cat info.plist | jc --plist -p
    {
      "NSAppleScriptEnabled": true,
      "LSMultipleInstancesProhibited": true,
      "CFBundleInfoDictionaryVersion": "6.0",
      "DTPlatformVersion": "GM",
      "CFBundleIconFile": "GarageBand.icns",
      "CFBundleName": "GarageBand",
      "DTSDKName": "macosx10.13internal",
      "NSSupportsAutomaticGraphicsSwitching": true,
      "RevisionDate": "2018-12-03_14:10:56",
      "UTImportedTypeDeclarations": [
        {
          "UTTypeConformsTo": [
            "public.data",
            "public.content"
      ...
    }
"""
import sys

# ugly hack because I accidentally shadowed the xml module from the
# standard library with the xml parser. :(
sys.path = [x for x in sys.path if 'jc/jc/parsers' not in x]

from typing import Dict, Union
import plistlib
import binascii
from datetime import datetime
import jc.utils
from jc.exceptions import ParseError


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.3'
    description = 'PLIST file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Using the pbPlist library from https://github.com/samdmarshall/pbPlist/releases/tag/v1.0.4 for NeXTSTEP support'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['standard', 'file', 'string', 'binary']


__version__ = info.version


def _process(proc_data: Dict) -> Dict:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured to conform to the schema.
    """
    return proc_data


def _b2a(byte_string: bytes) -> str:
    """Convert a byte string to a colon-delimited hex ascii string"""
    # need try/except since separator was only introduced in python 3.8.
    # provides compatibility for python 3.6 and 3.7.
    try:
      return binascii.hexlify(byte_string, ':').decode('utf-8')
    except TypeError:
      hex_string = binascii.hexlify(byte_string).decode('utf-8')
      colon_separated = ':'.join(hex_string[i:i+2] for i in range(0, len(hex_string), 2))
      return colon_separated


def _fix_objects(obj, _memo=None):
    """
    Recursively traverse the nested dictionary or list and convert objects
    into JSON serializable types.

    Objects referenced more than once (binary plist object references) are
    only converted once and stay shared, so the work and memory used here
    follow the size of the input.
    """
    if not isinstance(obj, (dict, list)):
        return obj

    if _memo is None:
        _memo = {}

    # converted objects keyed by id(): [original, converted, finished]
    # The original is kept so its id cannot be reused during the walk.
    obj_id = id(obj)
    if obj_id in _memo:
        if not _memo[obj_id][2]:
            raise ParseError('Plist contains a circular reference.')
        return _memo[obj_id][1]

    if isinstance(obj, dict):
        entry = [obj, obj, False]
        _memo[obj_id] = entry

        for k, v in obj.copy().items():

            if isinstance(v, datetime):
                iso = v.isoformat()
                v = int(round(v.timestamp()))
                obj.update({k: v, f'{k}_iso': iso})
                continue

            if isinstance(v, bytes):
                if id(v) not in _memo:
                    _memo[id(v)] = [v, _b2a(v), True]
                obj.update({k: _memo[id(v)][1]})
                continue

            if isinstance(v, (dict, list)):
                obj.update({k: _fix_objects(v, _memo)})
                continue

        entry[2] = True
        return obj

    new_list = []
    entry = [obj, new_list, False]
    _memo[obj_id] = entry

    for i in obj:
        new_list.append(_fix_objects(i, _memo))

    entry[2] = True
    return new_list


def parse(
    data: Union[str, bytes],
    raw: bool = False,
    quiet: bool = False
) -> Dict:
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

    raw_output: Dict = {}

    if jc.utils.has_data(data):

        if isinstance(data, str):
            data = bytes(data, 'utf-8')

        # attribute default values declared in the DTD of an XML plist are
        # added to every matching element by the XML parser, so limit how
        # much they can add
        jc.utils.xml_defaults_check(data)

        try:
            raw_output = plistlib.loads(data)

        except Exception:
            # Try parsing as an old-style NeXTSTEP Plist format
            # pbPlist library only works on file paths, not strings :(
            from jc.parsers.pbPlist.pbPlist import PBPlist
            import tempfile
            import os

            # use delete=False for windows compatibility
            plist_file = tempfile.NamedTemporaryFile(mode='w+b', delete=False)
            plist_file_name = plist_file.name

            # always delete the temp file, even if parsing fails
            try:
                with plist_file:
                    plist_file.write(data)
                    plist_file.seek(0)
                    parsed_plist = PBPlist(plist_file_name)
                    raw_output = parsed_plist.root.nativeType()

            finally:
                if os.path.exists(plist_file_name):
                    os.remove(plist_file_name)

        raw_output = _fix_objects(raw_output)

        # objects referenced more than once are written out in full for
        # each reference, so limit how much the output can grow from them
        jc.utils.expansion_check(raw_output, len(data))

    return raw_output if raw else _process(raw_output)
