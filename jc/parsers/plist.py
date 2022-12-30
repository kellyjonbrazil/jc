"""jc - JSON Convert PLIST file parser

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
from typing import Dict, Union
import plistlib
import binascii
from datetime import datetime
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.1'
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
      colon_seperated = ':'.join(hex_string[i:i+2] for i in range(0, len(hex_string), 2))
      return colon_seperated


def _fix_objects(obj):
    """
    Recursively traverse the nested dictionary or list and convert objects
    into JSON serializable types.
    """
    if isinstance(obj, dict):
        for k, v in obj.copy().items():

            if isinstance(v, datetime):
                iso = v.isoformat()
                v = int(round(v.timestamp()))
                obj.update({k: v, f'{k}_iso': iso})
                continue

            if isinstance(v, bytes):
                v = _b2a(v)
                obj.update({k: v})
                continue

            if isinstance(v, dict):
                obj.update({k: _fix_objects(v)})
                continue

            if isinstance(v, list):
                newlist = []
                for i in v:
                    newlist.append(_fix_objects(i))
                obj.update({k: newlist})
                continue

    if isinstance(obj, list):
        new_list = []
        for i in obj:
            new_list.append(_fix_objects(i))
        obj = new_list

    return obj


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

        try:
            raw_output = plistlib.loads(data)

        except Exception:
            # Try parsing as an old-style NeXTSTEP Plist format
            # pbPlist library only works on file paths, not strings :(
            from jc.parsers.pbPlist.pbPlist import PBPlist
            import tempfile
            import os

            # use delete=False for windows compatibility
            with tempfile.NamedTemporaryFile(mode='w+b', delete=False) as plist_file:
                plist_file_name = plist_file.name
                plist_file.write(data)
                plist_file.seek(0)
                parsed_plist = PBPlist(plist_file_name)
                raw_output = parsed_plist.root.nativeType()

            # try to delete the temp file
            if os.path.exists(plist_file_name):
                os.remove(plist_file_name)

        raw_output = _fix_objects(raw_output)

    return raw_output if raw else _process(raw_output)
