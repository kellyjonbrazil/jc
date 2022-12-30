"""jc - JSON Convert lib module"""

import sys
from typing import Any, Dict, List, Tuple, Iterator, Optional, Union

JSONDictType = Dict[str, Any]
StreamingOutputType = Iterator[Union[JSONDictType, Tuple[BaseException, str]]]

if sys.version_info >= (3, 8):
    from typing import TypedDict

    ParserInfoType = TypedDict(
        'ParserInfoType',
        {
            "name": str,
            "argument": str,
            "version": str,
            "description": str,
            "author": str,
            "author_email": str,
            "compatible": List[str],
            "magic_commands": List[str],
            "tags": List[str],
            "documentation": str,
            "streaming": bool,
            "plugin": bool,
            "hidden": bool,
            "deprecated": bool
        },
        total=False
    )

    TimeStampFormatType = TypedDict(
        'TimeStampFormatType',
        {
            'id': int,
            'format': str,
            'locale': Optional[str]
        }
    )

else:
    ParserInfoType = Dict
    TimeStampFormatType = Dict


try:
    from pygments.token import (Name, Number, String, Keyword)
    CustomColorType = Dict[Union[Name.Tag, Number, String, Keyword], str]

except Exception:
    CustomColorType = Dict  # type: ignore
