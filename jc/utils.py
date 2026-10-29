"""jc - JSON Convert utils"""
import sys
import re
import math
import locale
import shutil
from itertools import islice
from collections import namedtuple
from numbers import Number
from datetime import datetime, timezone
from textwrap import TextWrapper
from functools import lru_cache
from typing import Any, List, Dict, Iterable, Union, Optional, TextIO, Set, Tuple
from .jc_types import TimeStampFormatType

CLI_QUIET = False

def _asciify(string: str) -> str:
    """
    Return a string downgraded from Unicode to ASCII with some simple
    conversions.
    """
    string = string.replace('©', '(c)')
    # the ascii() function adds single quotes around the string
    string = ascii(string)[1:-1]
    string = string.replace(r'\n', '\n')
    return string


def _safe_print(
    string: str,
    sep: str = ' ',
    end: str = '\n',
    file: TextIO = sys.stdout,
    flush: bool = False
) -> None:
    """Output for both UTF-8 and ASCII encoding systems"""
    try:
        print(string, sep=sep, end=end, file=file, flush=flush)
    except UnicodeEncodeError:
        print(_asciify(string), sep=sep, end=end, file=file, flush=flush)


def _safe_pager(string: str) -> None:
    """Pager output for both UTF-8 and ASCII encoding systems"""
    from pydoc import pager
    try:
        pager(string)
    except UnicodeEncodeError:
        pager(_asciify(string))


# C0 controls (except tab and newline), DEL, and C1 controls are shown as
# escapes in warning and error messages
_CONTROL_CHAR_ESCAPES = {
    c: f'\\x{c:02x}'
    for c in list(range(0x00, 0x20)) + [0x7f] + list(range(0x80, 0xa0))
    if c not in (0x09, 0x0a)
}


def _escape_controls(string: str) -> str:
    """
    Return the string with control characters other than tab and newline
    replaced by visible `\\xNN` escapes.
    """
    return string.translate(_CONTROL_CHAR_ESCAPES)


# message lines longer than this are shortened before they are wrapped.
# TextWrapper takes time proportional to the square of the length of a
# long unbroken word.
_MAX_MESSAGE_LINE_LENGTH = 4096


def _message_line(string: str) -> str:
    """
    Return a message line ready for wrapping: shortened with an ellipsis
    and the original length if it is very long, and with control
    characters escaped.
    """
    if len(string) > _MAX_MESSAGE_LINE_LENGTH:
        string = f'{string[:_MAX_MESSAGE_LINE_LENGTH]}... ({len(string)} characters)'

    return _escape_controls(string)


def warning_message(message_lines: List[str]) -> None:
    """
    Prints warning message to `STDERR` for non-fatal issues. The first line
    is prepended with 'jc:  Warning - ' and subsequent lines are indented.
    Wraps text as needed based on the terminal width.

    Parameters:

        message:   (list) list of string lines

    Returns:

        None - just prints output to STDERR
    """
    if CLI_QUIET:
        return

    # this is for backwards compatibility with existing custom parsers
    if isinstance(message_lines, str):
        message_lines = [message_lines]

    columns = shutil.get_terminal_size().columns

    first_wrapper = TextWrapper(width=columns, subsequent_indent=' ' * 15)
    next_wrapper = TextWrapper(width=columns, initial_indent=' ' * 15,
                               subsequent_indent=' ' * 19)

    first_line = _message_line(message_lines.pop(0))
    first_str = f'jc:  Warning - {first_line}'
    first_str = first_wrapper.fill(first_str)
    _safe_print(first_str, file=sys.stderr)

    for line in message_lines:
        if line == '':
            continue
        message = next_wrapper.fill(_message_line(line))
        _safe_print(message, file=sys.stderr)


def error_message(message_lines: List[str]) -> None:
    """
    Prints an error message to `STDERR` for fatal issues. The first line is
    prepended with 'jc:  Error - ' and subsequent lines are indented.
    Wraps text as needed based on the terminal width.

    Parameters:

        message:   (list) list of string lines

    Returns:

        None - just prints output to `STDERR`
    """
    columns = shutil.get_terminal_size().columns

    first_wrapper = TextWrapper(width=columns, subsequent_indent=' ' * 13)
    next_wrapper = TextWrapper(width=columns, initial_indent=' ' * 13,
                               subsequent_indent=' ' * 17)

    first_line = _message_line(message_lines.pop(0))
    first_str = f'jc:  Error - {first_line}'
    first_str = first_wrapper.fill(first_str)
    _safe_print(first_str, file=sys.stderr)

    for line in message_lines:
        if line == '':
            continue
        message = next_wrapper.fill(_message_line(line))
        _safe_print(message, file=sys.stderr)


def is_compatible(compatible: List[str]) -> bool:
    """
    Returns True if the parser is compatible with the running OS platform.
    """
    platform_found = False

    for platform in compatible:
        if sys.platform.startswith(platform):
            platform_found = True
            break

    return platform_found


def compatibility(mod_name: str, compatible: List[str], quiet: bool = False) -> None:
    """
    Checks for the parser's compatibility with the running OS platform and
    prints a warning message to `STDERR` if not compatible and
    `quiet=False.`

    Parameters:

        mod_name:     (string) __name__ of the calling module

        compatible:   (list) sys.platform name(s) compatible with
                      the parser. compatible options:
                      linux, darwin, cygwin, win32, aix, freebsd

        quiet:        (bool) suppress compatibility message if `True`

    Returns:

        None - just prints output to STDERR
    """
    if not quiet and not is_compatible(compatible):
        mod = mod_name.split('.')[-1]
        compat_list = ', '.join(compatible)
        warning_message([
            f'`{mod}` command output from this OS ({sys.platform}) is not supported.',
            f'`{mod}` command output from the following platforms is supported: {compat_list}',
            'Disregard this warning if you are processing output that came from a supported platform. (Use the -q option to suppress this warning)'
        ])


def has_data(data: Union[str, bytes]) -> bool:
    """
    Checks if the string input contains data. If there are any
    non-whitespace characters then return `True`, else return `False`.

    For bytes, returns `True` if there is any data.

    Parameters:

        data:        (string, bytes) input to check whether it contains data

    Returns:

        Boolean      `True` if input string (data) contains non-whitespace
                     characters, otherwise `False`. For bytes data, returns
                     `True` if there is any data, otherwise `False`.
    """
    if isinstance(data, str):
        return bool(data and not data.isspace())

    return bool(data)


def remove_quotes(data: str) -> str:
    """
    Remove single or double quotes surrounding a string. If no quotes are
    found then the string is returned unmodified.

    Parameters:

        data:       (string) Input value

    Returns:

        string
    """
    if data.startswith('"') and data.endswith('"'):
        data = data[1:-1]

    elif data.startswith("'") and data.endswith("'"):
        data = data[1:-1]

    return data


_GIT_ESCAPES = {
    'a': '\a', 'b': '\b', 'f': '\f', 'n': '\n', 'r': '\r', 't': '\t',
    'v': '\v', '\\': '\\', '"': '"'
}
_git_escape_pattern = re.compile(r'\\([0-3][0-7]{2}|.)', re.DOTALL)


def _git_quoted_end(data: str, start: int = 0) -> int:
    """
    Return the index of the double quote that closes the C-quoted string
    that opens at data[start], or -1 if there is none.
    """
    i = start + 1
    size = len(data)
    while i < size:
        char = data[i]
        if char == '\\':
            i += 2
            continue
        if char == '"':
            return i
        i += 1
    return -1


def _git_unquote_one(data: str) -> str:
    """Decode the content of one C-quoted git path (quotes already removed)"""
    out = bytearray()
    pos = 0

    for match in _git_escape_pattern.finditer(data):
        out += data[pos:match.start()].encode('utf-8', 'backslashreplace')
        pos = match.end()
        esc = match.group(1)

        if len(esc) == 3 and esc[0] in '0123':
            out.append(int(esc, 8))
        elif esc in _GIT_ESCAPES:
            out += _GIT_ESCAPES[esc].encode('utf-8')
        else:
            out += match.group(0).encode('utf-8', 'backslashreplace')

    out += data[pos:].encode('utf-8', 'backslashreplace')
    return out.decode('utf-8', 'backslashreplace')


def unquote_git_path(data: str) -> str:
    """
    Decode a file path as printed by git. By default (`core.quotePath`) git
    wraps a path that has non-ASCII characters, double quotes, backslashes or
    control characters in double quotes and C-style escapes those characters
    (e.g. `"d\\303\\251ploy.yml"`). The escapes are decoded and the bytes are
    interpreted as UTF-8. Invalid UTF-8 is shown as backslash escapes.

    A path that is not quoted is returned unmodified. Each side of a rename
    in the `"old" => new` or `old => "new"` form is decoded separately.

    Parameters:

        data:       (string) Input value

    Returns:

        string
    """
    if data.startswith('"'):
        end = _git_quoted_end(data)
        if end == len(data) - 1:
            return _git_unquote_one(data[1:end])

        if end > 0 and data.startswith(' => ', end + 1):
            rest = data[end + 5:]
            if rest.startswith('"') and _git_quoted_end(rest) == len(rest) - 1:
                rest = _git_unquote_one(rest[1:-1])
            return _git_unquote_one(data[1:end]) + ' => ' + rest

        return data

    if data.endswith('"'):
        # a plain name can not contain a double quote, so the first one
        # opens the quoted second name of the rename
        idx = data.find(' => "')
        if idx >= 0 and '"' not in data[:idx]:
            start = idx + 4
            if _git_quoted_end(data, start) == len(data) - 1:
                return (data[:start] + _git_unquote_one(data[start + 1:-1]))

    return data


def normalize_key(data: str) -> str:
    r"""
    Normalize a key name by shifting to lower-case and converting special
    characters to underscores.

    Special characters are defined as `space` and the following:

        !"#$%&'()*+,-./:;<=>?@[\]^`{|}~

    This is a lossy algorithm. Repeating and trailing underscores are
    removed.

    Parameters:

        data:       (string) Input value

    Returns:

        string
    """
    special = r'''!"#$%&'()*+,-./:;<=>?@[\]^`{|}~ '''
    initial_underscore = False
    data = data.strip().lower()

    for special_char in special:
        data = data.replace(special_char, '_')

    if data.startswith('_'):
        initial_underscore = True

    # swap back to space so split() will compress multiple consecutive down to one
    data = data.strip('_').replace('_', ' ')
    data = '_'.join(data.split())

    if initial_underscore:
        data = '_' + data

    return data


def convert_to_int(value: object) -> Optional[int]:
    """
    Converts string and float input to int. Strips all non-numeric
    characters from strings.

    Parameters:

        value:         (string/float) Input value

    Returns:

        integer/None   Integer if successful conversion, otherwise None
    """
    if isinstance(value, str):
        str_val = re.sub(r'[^0-9\-\.]', '', value)
        try:
            return int(str_val)
        except (ValueError, TypeError):
            # also reached for digit strings longer than the int() digit
            # limit (Python 3.11+), where float() overflows to inf
            try:
                return int(float(str_val))
            except (ValueError, TypeError, OverflowError):
                return None

    elif isinstance(value, (int, float)):
        # int() raises on inf and nan
        try:
            return int(value)
        except (ValueError, OverflowError):
            return None

    else:
        return None


def _str_to_float(value: str) -> float:
    """float() of a string with all non-numeric characters removed"""
    return float(re.sub(r'[^0-9\-\.]', '', value))


def convert_to_float(value: object) -> Optional[float]:
    """
    Converts string and int input to float. Strips all non-numeric
    characters from strings.

    Parameters:

        value:         (string/integer) Input value

    Returns:

        float/None     Float if successful conversion, otherwise None.
                       Infinite and NaN results also return None.
    """
    if isinstance(value, str):
        try:
            result = _str_to_float(value)
        except (ValueError, TypeError):
            return None

    elif isinstance(value, (int, float)):
        try:
            result = float(value)
        except OverflowError:
            return None

    else:
        return None

    # JSON has no inf or nan, and a digit string that is too long for a
    # float overflows to inf
    return result if math.isfinite(result) else None


def convert_to_bool(value: object) -> bool:
    """
    Converts string, integer, or float input to boolean by checking
    for 'truthy' values.

    Parameters:

        value:          (string/integer/float) Input value

    Returns:

        True/False      False unless a 'truthy' number or string is found
                        ('y', 'yes', 'true', '1', 1, -1, etc.)
    """
    # if number, then bool it
    # if string, try to convert to float
    #   if float converts, then bool the result
    #   if float does not convert then look for truthy string and bool True
    #   else False
    truthy = ['y', 'yes', 'true', '*']

    if isinstance(value, (int, float)):
        return bool(value)

    if isinstance(value, str):
        try:
            # not convert_to_float(), which returns None for numbers too
            # large for a float
            return bool(_str_to_float(value))
        except Exception:
            pass

        if value:
            return value.lower() in truthy

    return False


# convert_size_to_int from https://github.com/xolox/python-humanfriendly

# Copyright (c) 2021 Peter Odding

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
def convert_size_to_int(
    size: str,
    binary: bool = False,
    posix_mode: bool = False,
    decimal_bias: bool = False) -> Optional[int]:
    """
    Parse a human readable data size and return the number of bytes.

    Parameters:

        size:           (string) The human readable file size to parse.
        binary:         (boolean) `True` to use binary multiples of bytes
                        (base-2) for ambiguous unit symbols and names,
                        `False` to use decimal multiples of bytes (base-10).
        posix_mode:     (boolean) Treat one-letter units (k, m, g, etc.) as
                        binary.
        decimal_bias:   (boolean) `True` to treat slightly ambiguous two-
                        letter unit symbols ending in "i" (e.g. Ki, Gi) to
                        use decimal multiples of bytes (base-10). `False`
                        (default) to use binary multiples of bytes.
    Returns:

        integer/None    Integer if successful conversion, otherwise None

    This function knows how to parse sizes in bytes, kilobytes, megabytes,
    gigabytes, terabytes and petabytes. Some examples:

        >>> convert_size_to_int('42')
        42
        >>> convert_size_to_int('13b')
        13
        >>> convert_size_to_int('5 bytes')
        5
        >>> convert_size_to_int('1 KB')
        1000
        >>> convert_size_to_int('1 kilobyte')
        1000
        >>> convert_size_to_int('1 KiB')
        1024
        >>> convert_size_to_int('1 Ki')
        1024
        >>> convert_size_to_int('1 Ki', decimal_bias=True)
        1000
        >>> convert_size_to_int('1 KB', binary=True)
        1024
        >>> convert_size_to_int('1.5 GB')
        1500000000
        >>> convert_size_to_int('1.5 GB', binary=True)
        1610612736
    """
    # normalize input by removing commas
    size = size.replace(',', '')

    def tokenize(text: str) -> List[str]:
        tokenized_input: List = []
        for token in re.split(r'(\d+(?:\.\d+)?)', text):
            token = token.strip()
            if re.match(r'\d+\.\d+', token):
                tokenized_input.append(float(token))
            elif token.isdigit():
                tokenized_input.append(int(token))
            elif token:
                tokenized_input.append(token)
        return tokenized_input

    SizeUnit = namedtuple('SizeUnit', 'divider, symbol, name')
    CombinedUnit = namedtuple('CombinedUnit', 'decimal, binary')
    disk_size_units = (
        CombinedUnit(SizeUnit(1000**1, 'KB', 'kilobyte'), SizeUnit(1024**1, 'KiB', 'kibibyte')),
        CombinedUnit(SizeUnit(1000**2, 'MB', 'megabyte'), SizeUnit(1024**2, 'MiB', 'mebibyte')),
        CombinedUnit(SizeUnit(1000**3, 'GB', 'gigabyte'), SizeUnit(1024**3, 'GiB', 'gibibyte')),
        CombinedUnit(SizeUnit(1000**4, 'TB', 'terabyte'), SizeUnit(1024**4, 'TiB', 'tebibyte')),
        CombinedUnit(SizeUnit(1000**5, 'PB', 'petabyte'), SizeUnit(1024**5, 'PiB', 'pebibyte')),
        CombinedUnit(SizeUnit(1000**6, 'EB', 'exabyte'), SizeUnit(1024**6, 'EiB', 'exbibyte')),
        CombinedUnit(SizeUnit(1000**7, 'ZB', 'zettabyte'), SizeUnit(1024**7, 'ZiB', 'zebibyte')),
        CombinedUnit(SizeUnit(1000**8, 'YB', 'yottabyte'), SizeUnit(1024**8, 'YiB', 'yobibyte')),
    )
    tokens = tokenize(size)
    if tokens and isinstance(tokens[0], Number):
        # Get the normalized unit (if any) from the tokenized input.
        normalized_unit = tokens[1].lower() if len(tokens) == 2 and isinstance(tokens[1], str) else ''
        # If the input contains only a number, it's assumed to be the number of
        # bytes. The second token can also explicitly reference the unit bytes.
        if len(tokens) == 1 or normalized_unit.startswith('b'):
            return int(tokens[0])
        # Otherwise we expect two tokens: A number and a unit.
        if normalized_unit:
            # Convert plural units to singular units, for details:
            # https://github.com/xolox/python-humanfriendly/issues/26
            normalized_unit = normalized_unit.rstrip('s')

            # Handle POSIX mode units where `k`, `m`, etc. are treated as binary
            # https://www.gnu.org/software/coreutils/manual/html_node/Block-size.html
            if len(normalized_unit) == 1 and posix_mode:
                normalized_unit = normalized_unit + 'ib'

            # Handle two-letter units (Ki, Gi, etc.) These are somewhat
            # ambiguous, but are treated as binary by default. This can be
            # changed with the `decimal_bias` parameter
            if len(normalized_unit) == 2 and normalized_unit[1].lower() == 'i':
                if decimal_bias:
                    normalized_unit = normalized_unit[0]
                else:
                    normalized_unit = normalized_unit + 'b'

            for unit in disk_size_units:
                # First we check for unambiguous symbols (KiB, MiB, GiB, etc)
                # and names (kibibyte, mebibyte, gibibyte, etc) because their
                # handling is always the same.
                if normalized_unit in (unit.binary.symbol.lower(), unit.binary.name.lower()):
                    return int(tokens[0] * unit.binary.divider)

                # Now we will deal with ambiguous prefixes (K, M, G, etc),
                # symbols (KB, MB, GB, etc) and names (kilobyte, megabyte,
                # gigabyte, etc) according to the caller's preference.
                if (normalized_unit in (unit.decimal.symbol.lower(), unit.decimal.name.lower())
                    or normalized_unit.startswith(unit.decimal.symbol[0].lower())):
                    return int(tokens[0] * (unit.binary.divider if binary else unit.decimal.divider))
    # We failed to parse the size specification.
    return None


def input_type_check(data: object) -> None:
    """Ensure input data is a string. Raises `TypeError` if not."""
    if not isinstance(data, str):
        raise TypeError("Input data must be a 'str' object.")


# The output may be up to this many times the input size, plus a fixed
# allowance, before `expansion_check()` raises `ParseError`.
_EXPANSION_RATIO = 1000
_EXPANSION_ALLOWANCE = 50 * 1000 * 1000


def expansion_limit(input_size: int) -> int:
    """
    Return the largest output size (in characters of JSON) accepted for
    an input of `input_size` characters or bytes. Used by parsers that
    limit how much the output can grow from shared references or
    declared default values.

    Parameters:

        input_size:  (int) length of the input data

    Returns:

        Integer      maximum accepted output size
    """
    return _EXPANSION_RATIO * input_size + _EXPANSION_ALLOWANCE


def _scalar_json_size(obj: object) -> int:
    """Estimate the JSON size of a value that is not a list or dict."""
    if obj is None or obj is True:
        return 4
    if obj is False:
        return 5
    if isinstance(obj, str):
        return len(obj) + 2
    if isinstance(obj, int):
        if obj.bit_length() <= 64:
            return len(int.__repr__(obj))
        return obj.bit_length() * 3 // 10 + 2
    if isinstance(obj, float):
        return len(float.__repr__(obj))
    if isinstance(obj, (bytes, bytearray)):
        return 4 * len(obj) + 3
    return len(str(obj)) + 2


def expansion_check(data: object, input_size: int) -> None:
    """
    Ensure the JSON output for `data` will not be far larger than the
    input. Objects referenced more than once (e.g. YAML aliases or binary
    plist object references) are counted once per reference, as they are
    when serialized, but each object is only walked once. Raises
    `ParseError` if the estimated output size is larger than
    `expansion_limit(input_size)`.

    Parameters:

        data:        (object) parsed data (dictionaries, lists, scalars)
        input_size:  (int) length of the input data

    Returns:

        None         raises `ParseError` if the output would be too large
    """
    from .exceptions import ParseError

    limit = expansion_limit(input_size)

    def too_large() -> ParseError:
        return ParseError(
            'Output would be too large: shared references or default values '
            f'expand to more than {limit} characters.'
        )

    # sizes of objects already walked, keyed by id(). The object is kept
    # in the value so its id cannot be reused during the walk.
    sizes: Dict[int, Tuple[object, int]] = {}
    in_progress: Set[int] = set()

    def known_size(obj: object) -> Optional[int]:
        """Return the size of a scalar or an already walked object, else None"""
        if isinstance(obj, (dict, list, tuple)):
            obj_id = id(obj)
            if obj_id in sizes:
                return sizes[obj_id][1]
            if obj_id in in_progress:
                # circular reference: cannot be serialized, so not counted
                return 0
            return None
        if obj is None or isinstance(obj, (str, int, float, bytes)):
            return _scalar_json_size(obj)
        obj_id = id(obj)
        if obj_id not in sizes:
            sizes[obj_id] = (obj, _scalar_json_size(obj))
        return sizes[obj_id][1]

    def new_frame(obj: Any) -> List[Any]:
        """[object, is_dict, iterator, running size]

        Each item adds one separator (the opening bracket counts as the
        first), so an empty container is fixed up when it is finished.
        """
        in_progress.add(id(obj))
        if isinstance(obj, dict):
            return [obj, True, iter(obj.items()), 1]
        return [obj, False, iter(obj), 1]

    size = known_size(data)
    if size is not None:
        if size > limit:
            raise too_large()
        return

    stack = [new_frame(data)]

    while stack:
        frame = stack[-1]
        descend = False

        for item in frame[2]:
            if frame[1]:
                key, value = item
                frame[3] += _scalar_json_size(key) + 2
            else:
                value = item
                frame[3] += 1

            size = known_size(value)
            if size is None:
                stack.append(new_frame(value))
                descend = True
                break

            frame[3] += size
            if frame[3] > limit:
                raise too_large()

        if descend:
            continue

        stack.pop()
        obj = frame[0]
        if not obj:
            frame[3] += 1
        in_progress.discard(id(obj))
        sizes[id(obj)] = (obj, frame[3])

        if stack:
            stack[-1][3] += frame[3]
            if stack[-1][3] > limit:
                raise too_large()
        elif frame[3] > limit:
            raise too_large()


class _StopDefaultsCheck(Exception):
    pass


def xml_defaults_check(data: Union[str, bytes]) -> None:
    """
    Ensure attribute default values declared in an XML document's DTD
    (`<!ATTLIST>`) do not make the output far larger than the input. The
    XML parser adds the defaults to every matching element, so they are
    counted with a separate pass that keeps no per-element data. Raises
    `ParseError` if they would add more than `expansion_limit(len(data))`
    characters. Malformed documents and documents with entity declarations
    are left for the XML library to report.

    Parameters:

        data:        (string, bytes) XML document. A string is parsed as
                     UTF-8, bytes use the document's declared encoding.

    Returns:

        None         raises `ParseError` if the output would be too large
    """
    marker = '<!ATTLIST' if isinstance(data, str) else b'<!ATTLIST'
    if marker not in data:  # type: ignore
        return

    from xml.parsers import expat
    from .exceptions import ParseError

    limit = expansion_limit(len(data))
    added = 0

    # element name -> {attribute name: output size of its default or 0}
    # the first declaration of an attribute is the one that applies
    declared: Dict[str, Dict[str, int]] = {}
    element_size: Dict[str, int] = {}

    def attlist_decl(elname, attname, attr_type, default, required):
        attrs = declared.setdefault(elname, {})
        if attname not in attrs:
            # "@name":"value", plus a separator
            attrs[attname] = 0 if default is None else len(attname) + len(default) + 7
            element_size.pop(elname, None)

    def start_element(name, attrs):
        nonlocal added
        defaults = declared.get(name)
        if not defaults:
            return

        size = element_size.get(name)
        if size is None:
            size = element_size[name] = sum(defaults.values())

        # attributes given in the document are not defaulted
        for attname in attrs[0::2]:
            size -= defaults.get(attname, 0)

        added += size
        if added > limit:
            raise ParseError(
                'Output would be too large: attribute default values expand '
                f'to more than {limit} characters.'
            )

    def entity_decl(*args):
        raise _StopDefaultsCheck()

    if isinstance(data, str):
        parser = expat.ParserCreate('utf-8')
        xml_bytes = data.encode('utf-8')
    else:
        parser = expat.ParserCreate()
        xml_bytes = data

    # only attributes given in the document are passed to start_element
    parser.ordered_attributes = True
    parser.specified_attributes = True
    parser.AttlistDeclHandler = attlist_decl
    parser.StartElementHandler = start_element
    parser.EntityDeclHandler = entity_decl

    try:
        parser.Parse(xml_bytes, True)
    except ParseError:
        raise
    except Exception:
        pass


_LF_LINE_END_RE = re.compile(r'\r?\n')
_CR_LF_LINE_END_RE = re.compile(r'\r\n|\r|\n')


def splitlines(
    text: str,
    keepends: bool = False,
    split_cr: bool = False
) -> List[str]:
    """
    Split text into lines on LF and CRLF only (optionally also on a lone CR).

    Unlike `str.splitlines()`, this does not treat VT, FF, FS, GS, RS,
    NEL (U+0085), LINE SEPARATOR (U+2028) or PARAGRAPH SEPARATOR (U+2029)
    as line terminators, so those characters stay inside the line. By
    default a lone CR also stays inside the line.

    Parameters:

        text:        (string)  text to split
        keepends:    (boolean) keep the line terminators if True
        split_cr:    (boolean) also treat a lone CR as a line terminator
                               if True (for files that may use CR-only
                               line endings)

    Returns:

        List of strings. Like `str.splitlines()`, a trailing line terminator
        does not produce an empty final line.
    """
    lines: List[str]

    # fast path: str.split() is much faster than iterating regex matches
    if not keepends:
        if split_cr:
            text = text.replace('\r\n', '\n').replace('\r', '\n')

        lines = text.split('\n')
        tail = lines.pop()

        if not split_cr:
            lines = [line[:-1] if line.endswith('\r') else line for line in lines]

        if tail:
            lines.append(tail)

        return lines

    line_end = _CR_LF_LINE_END_RE if split_cr else _LF_LINE_END_RE
    lines = []
    start = 0

    for match in line_end.finditer(text):
        lines.append(text[start:match.end()])
        start = match.end()

    if start < len(text):
        lines.append(text[start:])

    return lines


def _lazy_splitlines(text: str) -> Iterable[str]:
    NEWLINES_PATTERN: str = r'\r?\n'
    NEWLINES_RE = re.compile(NEWLINES_PATTERN)
    start = 0
    for m in NEWLINES_RE.finditer(text):
        begin, end = m.span()
        if begin != start:
            yield text[start:begin]
        else:
            yield ''
        start = end

    if text[start:]:
        yield text[start:]


def line_slice(
        data: Union[str, Iterable[str], TextIO, bytes, None],
        slice_start: Optional[int] = None,
        slice_end: Optional[int] = None
) -> Union[str, Iterable[str], TextIO, bytes, None]:
    """
    Slice input data by lines - lazily, if possible.

    Accepts a string (for normal parsers) or an iterable (for streaming
    parsers). Uses normal start/stop slicing values, but will always slice
    on lines instead of characters. Positive slices will use less memory as
    the function will attempt to lazily iterate over the input. A negative
    slice parameter will force the function to read in all of the data and
    then slice, which will use more memory.

    Parameters:

        data:              (string or iterable) - input to slice by lines
        slice_start:       (int) - starting line
        slice_end:         (int) - ending line

    Returns:
        string if input is a string.
        iterable of strings if input is an iterable (for streaming parsers)
    """
    if not slice_start is None or not slice_end is None:
        # standard parsers UTF-8 input
        if isinstance(data, str):
            data_iter = _lazy_splitlines(data)

            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0):

                return '\n'.join(islice(data_iter, slice_start, slice_end))

            # negative slices found (non-lazy, uses more memory)
            else:
                return '\n'.join(list(data_iter)[slice_start:slice_end])

        # standard parsers bytes input
        elif isinstance(data, bytes):
            raise ValueError('Cannot slice bytes data.')

        # streaming parsers UTF-8 input
        else:
            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0) \
                and data:

                return islice(data, slice_start, slice_end)

            # negative slices found (non-lazy, uses more memory)
            elif data:
                return list(data)[slice_start:slice_end]

    return data


class timestamp:
    __slots__ = ('string', 'format', 'naive', 'utc', 'iso')

    # no supported format matches a longer normalized string
    _MAX_LENGTH = 100
    _DIGIT = re.compile(r'\d')

    def __init__(self,
                 datetime_string: Optional[str],
                 format_hint: Optional[Iterable[int]] = None
    ) -> None:
        """
        Input a datetime text string of several formats and convert to a
        naive or timezone-aware epoch timestamp in UTC.

        Parameters:

            datetime_string  (str):  a string representation of a
                datetime in several supported formats

            format_hint  (iterable):  an optional iterable of format ID
                integers to instruct the timestamp object to try those
                formats first in the order given. Other formats will be
                tried after the format hint list is exhausted. This can
                speed up timestamp conversion so several different formats
                don't have to be tried in brute-force fashion.

        Returns a timestamp object with the following attributes:

            string  (str):  the input datetime string

            format  (int | None):  the format rule that was used to decode
                the datetime string. None if conversion fails.

            naive  (int | None):  timestamp based on locally configured
                timezone. None if conversion fails.

            utc  (int | None):  aware timestamp only if UTC timezone
                detected in datetime string. None if conversion fails.

            iso (str | None):  ISO string - timezone information is output
                only if UTC timezone is detected in the datetime string.
        """
        self.string = datetime_string

        if not format_hint:
            format_hint = tuple()
        else:
            format_hint = tuple(format_hint)

        if self._may_match(self.string):
            dt = self._parse_dt(self.string, format_hint=format_hint)
        else:
            dt = {
                'format': None,
                'timestamp_naive': None,
                'timestamp_utc': None,
                'iso': None
            }
        self.format = dt['format']
        self.naive = dt['timestamp_naive']
        self.utc = dt['timestamp_utc']
        self.iso = dt['iso']

    def __repr__(self) -> str:
        return f'timestamp(string={self.string!r}, format={self.format}, naive={self.naive}, utc={self.utc}, iso={self.iso!r})'

    @staticmethod
    def _may_match(dt_string: Optional[str]) -> bool:
        """
        Quick check for strings that no supported format can match: strings
        without a digit, or longer than 100 characters after normalization.
        These strings are not passed to the cached parser.
        """
        if not isinstance(dt_string, str) or not dt_string:
            return True

        if not timestamp._DIGIT.search(dt_string):
            return False

        if len(dt_string) <= timestamp._MAX_LENGTH:
            return True

        normalized_datetime, _ = timestamp._normalize_dt_string(dt_string)
        return len(normalized_datetime) <= timestamp._MAX_LENGTH

    @staticmethod
    def _normalize_dt_string(dt_string: Optional[str]) -> Tuple[str, bool]:
        """
        Normalize a datetime string before matching it against the supported
        formats. Returns the normalized string and whether a UTC timezone was
        detected.
        """
        # from https://www.timeanddate.com/time/zones/
        # only removed UTC & GMT timezones and added known non-UTC offsets
        tz_abbr: Set[str] = {
            'A', 'ACDT', 'ACST', 'ACT', 'ACWST', 'ADT', 'AEDT', 'AEST', 'AET', 'AFT', 'AKDT',
            'AKST', 'ALMT', 'AMST', 'AMT', 'ANAST', 'ANAT', 'AQTT', 'ART', 'AST', 'AT', 'AWDT',
            'AWST', 'AZOST', 'AZOT', 'AZST', 'AZT', 'AoE', 'B', 'BNT', 'BOT', 'BRST', 'BRT', 'BST',
            'BTT', 'C', 'CAST', 'CAT', 'CCT', 'CDT', 'CEST', 'CET', 'CHADT', 'CHAST', 'CHOST',
            'CHOT', 'CHUT', 'CIDST', 'CIST', 'CKT', 'CLST', 'CLT', 'COT', 'CST', 'CT', 'CVT', 'CXT',
            'ChST', 'D', 'DAVT', 'DDUT', 'E', 'EASST', 'EAST', 'EAT', 'ECT', 'EDT', 'EEST', 'EET',
            'EGST', 'EGT', 'EST', 'ET', 'F', 'FET', 'FJST', 'FJT', 'FKST', 'FKT', 'FNT', 'G',
            'GALT', 'GAMT', 'GET', 'GFT', 'GILT', 'GST', 'GYT', 'H', 'HDT', 'HKT', 'HOVST',
            'HOVT', 'HST', 'I', 'ICT', 'IDT', 'IOT', 'IRDT', 'IRKST', 'IRKT', 'IRST', 'IST', 'JST',
            'K', 'KGT', 'KOST', 'KRAST', 'KRAT', 'KST', 'KUYT', 'L', 'LHDT', 'LHST', 'LINT', 'M',
            'MAGST', 'MAGT', 'MART', 'MAWT', 'MDT', 'MHT', 'MMT', 'MSD', 'MSK', 'MST', 'MT', 'MUT',
            'MVT', 'MYT', 'N', 'NCT', 'NDT', 'NFDT', 'NFT', 'NOVST', 'NOVT', 'NPT', 'NRT', 'NST',
            'NUT', 'NZDT', 'NZST', 'O', 'OMSST', 'OMST', 'ORAT', 'P', 'PDT', 'PET', 'PETST', 'PETT',
            'PGT', 'PHOT', 'PHT', 'PKT', 'PMDT', 'PMST', 'PONT', 'PST', 'PT', 'PWT', 'PYST', 'PYT',
            'Q', 'QYZT', 'R', 'RET', 'ROTT', 'S', 'SAKT', 'SAMT', 'SAST', 'SBT', 'SCT', 'SGT',
            'SRET', 'SRT', 'SST', 'SYOT', 'T', 'TAHT', 'TFT', 'TJT', 'TKT', 'TLT', 'TMT', 'TOST',
            'TOT', 'TRT', 'TVT', 'U', 'ULAST', 'ULAT', 'UYST', 'UYT', 'UZT', 'V', 'VET', 'VLAST',
            'VLAT', 'VOST', 'VUT', 'W', 'WAKT', 'WARST', 'WAST', 'WAT', 'WEST', 'WET', 'WFT',
            'WGST', 'WGT', 'WIB', 'WIT', 'WITA', 'WST', 'WT', 'X', 'Y', 'YAKST', 'YAKT', 'YAPT',
            'YEKST', 'YEKT', 'UTC-1200', 'UTC-1100', 'UTC-1000', 'UTC-0930', 'UTC-0900',
            'UTC-0800', 'UTC-0700', 'UTC-0600', 'UTC-0500', 'UTC-0400', 'UTC-0300', 'UTC-0230',
            'UTC-0200', 'UTC-0100', 'UTC+0100', 'UTC+0200', 'UTC+0300', 'UTC+0400', 'UTC+0430',
            'UTC+0500', 'UTC+0530', 'UTC+0545', 'UTC+0600', 'UTC+0630', 'UTC+0700', 'UTC+0800',
            'UTC+0845', 'UTC+0900', 'UTC+1000', 'UTC+1030', 'UTC+1100', 'UTC+1200', 'UTC+1300',
            'UTC+1345', 'UTC+1400'
        }

        offset_suffixes: Tuple[str, ...] = (
            '-12:00', '-11:00', '-10:00', '-09:30', '-09:00',
            '-08:00', '-07:00', '-06:00', '-05:00', '-04:00', '-03:00', '-02:30',
            '-02:00', '-01:00', '+01:00', '+02:00', '+03:00', '+04:00', '+04:30',
            '+05:00', '+05:30', '+05:45', '+06:00', '+06:30', '+07:00', '+08:00',
            '+08:45', '+09:00', '+10:00', '+10:30', '+11:00', '+12:00', '+13:00',
            '+13:45', '+14:00'
        )

        data: str = dt_string or ''
        utc_tz: bool = False

        # sometimes UTC is referenced as 'Coordinated Universal Time'. Convert to 'UTC'
        data = data.replace('Coordinated Universal Time', 'UTC')

        # UTC can also be indicated with 'Z' for Zulu time (ISO-8601). Convert to 'UTC'
        data = data.replace('Z', 'UTC')

        # GMT and UTC are practically equivalent. Convert to 'UTC'
        data = data.replace('GMT', 'UTC')

        if 'UTC' in data:
            utc_tz = True
            if 'UTC+' in data or 'UTC-' in data:
                utc_tz = bool('UTC+0000' in data or 'UTC-0000' in data)

        elif '+0000' in data \
             or '-0000' in data \
             or '+00:00' in data \
             or '-00:00' in data:
            utc_tz = True
            data = data.replace('+00:00', '+0000')  # fix for python 3.6

        # normalize the timezone by taking out any timezone reference, except UTC
        cleandata = data.replace('(', '').replace(')', '')
        normalized_datetime_list: List[str] = []
        for term in cleandata.split():
            if term not in tz_abbr:
                normalized_datetime_list.append(term)

        normalized_datetime = ' '.join(normalized_datetime_list)

        # remove non UTC offset suffixes at the end of the string
        for suffix in offset_suffixes:
            if normalized_datetime.endswith(suffix):
                normalized_datetime = normalized_datetime[0:-len(suffix)]
                break

        # normalize further by converting any greater-than 6-digit subsecond to 6-digits
        p = re.compile(r'(\W\d\d:\d\d:\d\d\.\d{6})\d+\W')
        normalized_datetime = p.sub(r'\g<1> ', normalized_datetime)

        return normalized_datetime, utc_tz

    @staticmethod
    @lru_cache(maxsize=2048)
    def _parse_dt(
        dt_string: Optional[str],
        format_hint: Optional[Iterable[int]] = None
    ) -> Dict[str, Any]:
        """
        Input a datetime text string of several formats and convert to
        a naive or timezone-aware epoch timestamp in UTC.

        Parameters:

            dt_string:    (string) a string representation of a date-time
                          in several supported formats

            format_hint:  (list | tuple) a list of format ID int's that
                          should be tried first. This can increase
                          performance since the function will not need to
                          try many incorrect formats before finding the
                          correct one.

        Returns:

            Dictionary of the following format:

                {
                    # for debugging purposes. None if conversion fails
                    "format":               int,

                    # timestamp based on locally configured timezone.
                    # None if conversion fails.
                    "timestamp_naive":      int,

                    # aware timestamp only if UTC timezone detected.
                    # None if conversion fails.
                    "timestamp_utc":        int

                    # ISO string. None if conversion fails.
                    "iso":                  str
                }

                The `format` integer denotes which date_time format
                conversion succeeded.

                The `timestamp_naive` integer is the converted date-time
                string to a naive epoch timestamp.

                The `timestamp_utc` integer is the converted date-time
                string to an aware epoch timestamp in the UTC timezone. If
                an aware conversion cannot be performed (e.g. the UTC
                timezone is not found in the date-time string), then this
                field will be None.

                The `iso` string will only have timezone information if the
                UTC timezone is detected in `dt_string`.

                If the conversion completely fails, all fields will be None.
        """
        formats: Tuple[TimeStampFormatType, ...] = (
            {'id': 1000, 'format': '%a %b %d %H:%M:%S %Y', 'locale': None},  # manual C locale format conversion: Tue Mar 23 16:12:11 2021 or Tue Mar 23 16:12:11 IST 2021
            {'id': 1100, 'format': '%a %b %d %H:%M:%S %Y %z', 'locale': None}, # git date output: Thu Mar 5 09:17:40 2020 -0800
            {'id': 1200, 'format': '%a %b %d %I:%M:%S %p %Y', 'locale': None},  # 12-hour twin of 1000, for locales where `date` prints AM/PM: Thu Sep 10 11:10:44 AM 2026
            {'id': 1300, 'format': '%Y-%m-%dT%H:%M:%S.%f%Z', 'locale': None}, # ISO Format with UTC (found in syslog 5424): 2003-10-11T22:14:15.003Z
            {'id': 1310, 'format': '%Y-%m-%dT%H:%M:%S.%f', 'locale': None}, # ISO Format without TZ (found in syslog 5424): 2003-10-11T22:14:15.003
            {'id': 1400, 'format': '%b %d %Y %H:%M:%S.%f UTC', 'locale': None}, # CEF Format with UTC: Nov 08 2022 12:30:00.111 UTC
            {'id': 1410, 'format': '%b %d %Y %H:%M:%S.%f', 'locale': None}, # CEF Format without TZ: Nov 08 2022 12:30:00.111
            {'id': 1420, 'format': '%b %d %Y %H:%M:%S UTC', 'locale': None}, # CEF Format with UTC without microseconds: Nov 08 2022 12:30:00 UTC
            {'id': 1430, 'format': '%b %d %Y %H:%M:%S', 'locale': None}, # CEF Format without TZ or microseconds: Nov 08 2022 12:30:00
            {'id': 1500, 'format': '%Y-%m-%d %H:%M', 'locale': None},  # en_US.UTF-8 local format (found in who cli output): 2021-03-23 00:14
            {'id': 1600, 'format': '%m/%d/%Y %I:%M %p', 'locale': None},  # Windows english format (found in dir cli output): 12/07/2019 02:09 AM
            {'id': 1700, 'format': '%m/%d/%Y, %I:%M:%S %p', 'locale': None},  # Windows english format wint non-UTC tz (found in systeminfo cli output): 3/22/2021, 1:15:51 PM (UTC-0600)
            {'id': 1705, 'format': '%m/%d/%Y, %I:%M:%S %p %Z', 'locale': None},  # Windows english format with UTC tz (found in systeminfo cli output): 3/22/2021, 1:15:51 PM (UTC)
            {'id': 1710, 'format': '%m/%d/%Y, %I:%M:%S %p UTC%z', 'locale': None},  # Windows english format with UTC tz (found in systeminfo cli output): 3/22/2021, 1:15:51 PM (UTC+0000)
            {'id': 1720, 'format': '%A, %B %d, %Y %I:%M:%S %p', 'locale': None},  # ipconfig cli output format: Thursday, June 22, 2023 10:39:04 AM
            {'id': 1750, 'format': '%Y/%m/%d-%H:%M:%S.%f', 'locale': None},  # Google Big Table format with no timezone: 1970/01/01-01:00:00.000000
            {'id': 1755, 'format': '%Y/%m/%d-%H:%M:%S.%f%z', 'locale': None},  # Google Big Table format with timezone: 1970/01/01-01:00:00.000000+00:00
            {'id': 1760, 'format': '%Y-%m-%d %H:%M:%S%z', 'locale': None},  # certbot format with timezone: 2023-06-12 01:35:30+00:00
            {'id': 1800, 'format': '%d/%b/%Y:%H:%M:%S %z', 'locale': None},  # Common Log Format: 10/Oct/2000:13:55:36 -0700
            {'id': 2000, 'format': '%a %d %b %Y %I:%M:%S %p %Z', 'locale': None},  # en_US.UTF-8 local format (found in upower cli output): Tue 23 Mar 2021 04:12:11 PM UTC
            {'id': 3000, 'format': '%a %d %b %Y %I:%M:%S %p', 'locale': None},  # en_US.UTF-8 local format with non-UTC tz (found in upower cli output): Tue 23 Mar 2021 04:12:11 PM IST
            {'id': 3100, 'format': '%a %d %b %Y %I:%M:%S %p %z', 'locale': None},  # pacman format - append 00 to end to make it work: # Sat 11 May 2024 06:14:19 AM +0800
            {'id': 3500, 'format': '%a, %d %b %Y %H:%M:%S %Z', 'locale': None},  # HTTP header time format (always GMT so assume UTC): Wed, 31 Jan 2024 00:39:28 GMT
            {'id': 4000, 'format': '%A %d %B %Y %I:%M:%S %p %Z', 'locale': None},  # European-style local format (found in upower cli output): Tuesday 01 October 2019 12:50:41 PM UTC
            {'id': 5000, 'format': '%A %d %B %Y %I:%M:%S %p', 'locale': None},  # European-style local format with non-UTC tz (found in upower cli output): Tuesday 01 October 2019 12:50:41 PM IST
            {'id': 6000, 'format': '%a %b %d %I:%M:%S %p %Z %Y', 'locale': None},  # en_US.UTF-8 format (found in date cli): Wed Mar 24 06:16:19 PM UTC 2021
            {'id': 7000, 'format': '%a %b %d %H:%M:%S %Z %Y', 'locale': None},  # C locale format (found in date cli): Wed Mar 24 11:11:30 UTC 2021
            {'id': 7100, 'format': '%b %d %H:%M:%S %Y', 'locale': None},  # C locale format (found in stat cli output - osx): # Mar 29 11:49:05 2021
            {'id': 7200, 'format': '%Y-%m-%d %H:%M:%S.%f %z', 'locale': None},  # C locale format (found in stat cli output - linux): 2019-08-13 18:13:43.555604315 -0400
            {'id': 7250, 'format': '%Y-%m-%d %H:%M:%S', 'locale': None},  # C locale format with non-UTC tz (found in modified vmstat cli output): # 2021-09-16 20:32:28 PDT
            {'id': 7255, 'format': '%Y-%m-%d %H:%M:%S %Z', 'locale': None},  # C locale format (found in modified vmstat cli output): # 2021-09-16 20:32:28 UTC
            {'id': 7300, 'format': '%a %Y-%m-%d %H:%M:%S %Z', 'locale': None},  # C locale format (found in timedatectl cli output): # Wed 2020-03-11 00:53:21 UTC
            # attempt locale changes last
            {'id': 8000, 'format': '%a %d %b %Y %H:%M:%S %Z', 'locale': ''},  # current locale format (found in upower cli output): # mar. 23 mars 2021 23:12:11 UTC
            {'id': 8100, 'format': '%a %d %b %Y %H:%M:%S', 'locale': ''},  # current locale format with non-UTC tz (found in upower cli output): # mar. 23 mars 2021 19:12:11 EDT
            {'id': 8200, 'format': '%A %d %B %Y, %H:%M:%S UTC%z', 'locale': ''},  # fr_FR.utf8 locale format (found in date cli output): vendredi 26 mars 2021, 13:26:46 (UTC+0000)
            {'id': 8300, 'format': '%A %d %B %Y, %H:%M:%S', 'locale': ''},  # fr_FR.utf8 locale format with non-UTC tz (found in date cli output): vendredi 26 mars 2021, 13:26:46 (UTC-0400)
            {'id': 9000, 'format': '%c', 'locale': ''}  # locally configured locale format conversion: Could be anything :) this is a last-gasp attempt
        )

        # fixup for behavior changes in python 3.15
        # add any formats that need to be removed to `remove_ids`
        if sys.version_info >= (3, 15, 0):
            remove_ids = {7250}
            formats = tuple((x for x in formats if x['id'] not in remove_ids))

        dt: Optional[datetime] = None
        dt_utc: Optional[datetime] = None
        timestamp_naive: Optional[int] = None
        timestamp_utc: Optional[int] = None
        iso_string: Optional[str] = None
        timestamp_obj: Dict[str, Any] = {
            'format': None,
            'timestamp_naive': None,
            'timestamp_utc': None,
            'iso': None
        }

        # convert format_hint to a tuple so it is hashable (for lru_cache)
        if not format_hint:
            format_hint = tuple()
        else:
            format_hint = tuple(format_hint)

        normalized_datetime, utc_tz = timestamp._normalize_dt_string(dt_string)

        # try format hints first, then fall back to brute-force method
        hint_obj_list: List[TimeStampFormatType] = []
        for fmt_id in format_hint:
            for fmt in formats:
                if fmt_id == fmt['id']:
                    hint_obj_list.append(fmt)

        remaining_formats = [fmt for fmt in formats if not fmt['id'] in format_hint]
        optimized_formats = hint_obj_list + remaining_formats

        # save the original LC_TIME so it can be restored on every exit path.
        # (setlocale with None is a query and does not restore anything)
        original_lc_time = locale.setlocale(locale.LC_TIME)

        try:
            for fmt in optimized_formats:
                try:
                    locale.setlocale(locale.LC_TIME, fmt['locale'])
                    dt = datetime.strptime(normalized_datetime, fmt['format'])
                    timestamp_obj['format'] = fmt['id']
                    timestamp_naive = int(dt.replace(tzinfo=None).timestamp())
                    iso_string = dt.replace(tzinfo=None).isoformat()
                    break
                except Exception:
                    continue
        finally:
            locale.setlocale(locale.LC_TIME, original_lc_time)

        if dt and utc_tz:
            dt_utc = dt.replace(tzinfo=timezone.utc)
            timestamp_utc = int(dt_utc.timestamp())
            iso_string = dt_utc.isoformat()

        if timestamp_naive:
            timestamp_obj['timestamp_naive'] = timestamp_naive
            timestamp_obj['timestamp_utc'] = timestamp_utc
            timestamp_obj['iso'] = iso_string

        return timestamp_obj


def unescape_backslashes(
    data: str,
    octal_chars: Optional[str] = None,
    escapes: Optional[Dict[str, str]] = None
) -> str:
    r"""
    Decode the backslash escapes that tools such as `mount` (fstab, mtab),
    `getfacl` and `md5sum` use for special characters in names. The input is
    read from left to right in a single pass, so an escaped backslash is never
    used to start another escape.

    A backslash followed by three octal digits (`\040`) is decoded to the
    byte it stands for (the value is masked to 8 bits, as in libmount). A run
    of these bytes is interpreted as UTF-8 and invalid UTF-8 is shown as
    backslash escapes. A backslash that is not followed by three octal digits
    or by a key of `escapes` is kept as it is, along with the character after
    it.

    Parameters:

        data:         (string) Input value
        octal_chars:  (string) Decode an octal escape only when it stands for
                      one of these characters and keep any other octal escape
                      as it is. `None` (default) decodes every octal escape
                      and an empty string decodes none.
        escapes:      (dictionary) Maps the character that follows a
                      backslash to its replacement, e.g. `{'\\': '\\'}`
                      decodes `\\` to a single backslash. Octal escapes are
                      checked first.

    Returns:

        string
    """
    if '\\' not in data:
        return data

    escapes = escapes or {}
    result: List[str] = []
    octal_run = bytearray()
    start = 0
    idx = data.find('\\')

    while idx >= 0:
        seq = data[idx + 1:idx + 4]

        if (octal_chars != '' and len(seq) == 3
                and all(char in '01234567' for char in seq)):
            value = int(seq, 8) & 0xff

            if octal_chars is None or (value < 0x80 and chr(value) in octal_chars):
                if idx > start:
                    if octal_run:
                        result.append(octal_run.decode('utf-8', 'backslashreplace'))
                        octal_run = bytearray()
                    result.append(data[start:idx])

                octal_run.append(value)
                start = idx + 4
                idx = data.find('\\', start)
                continue

        if seq[:1] and seq[:1] in escapes:
            if octal_run:
                result.append(octal_run.decode('utf-8', 'backslashreplace'))
                octal_run = bytearray()

            result.append(data[start:idx])
            result.append(escapes[seq[:1]])
            start = idx + 2
            idx = data.find('\\', start)
            continue

        idx = data.find('\\', idx + 1)

    if octal_run:
        result.append(octal_run.decode('utf-8', 'backslashreplace'))

    result.append(data[start:])
    return ''.join(result)
