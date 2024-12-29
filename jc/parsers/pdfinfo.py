r"""jc - JSON Convert `pdfinfo` command output parser


Usage (cli):

    $ pdfinfo ~/Desktop/sample-1.pdf | jc --pdfinfo

or

    $ jc pfdinfo

Usage (module):

    import jc
    result = jc.parse('pdfinfo', pdfinfo_command_output)

Schema:

    [
        {
            "title":        string,
            "producer":     string,
            "creationdate": string,
            "moddate":      string,
            "tagged":       string,
            "form":         string,
            "pages":        int,
            "encrypted":    string,
            "permissions":  string,
            "page_size":    string,
            "file_size":    string,
            "optimized":    string,
            "javascript":   string,
            "pdf_version":  string
        }
    ]

Examples:

    $ pdfinfo ~/Desktop/sample-1.pdf | jc --pdfinfo -p
    [
        {
            "title": "Brochure",
            "producer": "Skia/PDF m111 Google Docs Renderer",
            "creationdate": "Sun Dec 29 12:24:50 2024",
            "moddate": "Sun Dec 29 12:24:50 2024",
            "tagged": "no",
            "form": "none",
            "pages": 2,
            "encrypted": "AES 128-bit",
            "permissions": "print:no copy:no change:no addNotes:no",
            "page_size": "612 x 792 pts (letter) (rotated 0 degrees)",
            "file_size": "76259 bytes",
            "optimized": "yes",
            "javascript": "no",
            "pdf_version": "1.6"
        }
    ]

    $ pdfinfo ~/Desktop/sample-1.pdf | jc --pdfinfo -p -r
    [
        {
            "title": "Brochure"
        },
        {
            "producer": "Skia/PDF m111 Google Docs Renderer"
        },
        {
            "creationdate": "Sun Dec 29 12:24:50 2024"
        },
        {
            "moddate": "Sun Dec 29 12:24:50 2024"
        },
        {
            "tagged": "no"
        },
        {
            "form": "none"
        },
        {
            "pages": "2"
        },
        {
            "encrypted": "AES 128-bit"
        },
        {
            "permissions": "print:no copy:no change:no addNotes:no"
        },
        {
            "page_size": "612 x 792 pts (letter) (rotated 0 degrees)"
        },
        {
            "file_size": "76259 bytes"
        },
        {
            "optimized": "yes"
        },
        {
            "javascript": "no"
        },
        {
            "pdf_version": "1.6"
        }
    ]
"""

from typing import List
from jc.jc_types import JSONDictType
import jc.utils
from jc.parsers.universal import simple_key_value_parse


class info:
    """Provides parser metadata (version, author, etc.)"""

    version = "1.0"
    description = "`pdfinfo` command parser"
    author = "Hamza Saht"
    author_email = "hamzasaht01@gmail.com"
    compatible = ["linux", "darwin", "cygwin", "win32", "aix", "freebsd"]
    tags = ["command"]
    magic_commands = ["pdfinfo"]

    deprecated = False
    hidden = False


__version__ = info.version


def _process(proc_data: List[JSONDictType]) -> List[JSONDictType]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """

    data = [{key: value for d in proc_data for key, value in d.items()}]
    for record in data:
        for fieldName in record.keys():
            if fieldName == "pages":
                record[fieldName] = jc.utils.convert_to_int(record[fieldName])
    return data


def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
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

    cleandata = list(filter(None, data.splitlines()))
    raw_output: List[JSONDictType] = []

    if not jc.utils.has_data(data):
        return raw_output

    raw_output = simple_key_value_parse(cleandata)

    return raw_output if raw else _process(raw_output)
