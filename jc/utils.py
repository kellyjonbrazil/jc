"""jc - JSON Convert utils"""
import sys
import re
import locale
import shutil
from itertools import islice
from collections import namedtuple
from numbers import Number
from datetime import datetime, timezone
from textwrap import TextWrapper
from functools import lru_cache
from typing import Any, List, Dict, Iterable, Union, Optional, TextIO
from .jc_types import TimeStampFormatType


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
    # this is for backwards compatibility with existing custom parsers
    if isinstance(message_lines, str):
        message_lines = [message_lines]

    columns = shutil.get_terminal_size().columns

    first_wrapper = TextWrapper(width=columns, subsequent_indent=' ' * 15)
    next_wrapper = TextWrapper(width=columns, initial_indent=' ' * 15,
                               subsequent_indent=' ' * 19)

    first_line = message_lines.pop(0)
    first_str = f'jc:  Warning - {first_line}'
    first_str = first_wrapper.fill(first_str)
    _safe_print(first_str, file=sys.stderr)

    for line in message_lines:
        if line == '':
            continue
        message = next_wrapper.fill(line)
        _safe_print(message, file=sys.stderr)


def error_message(message_lines: List[str]) -> None:
    """
    Prints an error message to `STDERR` for fatal issues. The first line is
    prepended with 'jc:  Error - ' and subsequent lines are indented.
    Wraps text as needed based on the terminal width.

    Parameters:

        message:   (list) list of string lines

    Returns:

        None - just prints output to STDERR
    """
    columns = shutil.get_terminal_size().columns

    first_wrapper = TextWrapper(width=columns, subsequent_indent=' ' * 13)
    next_wrapper = TextWrapper(width=columns, initial_indent=' ' * 13,
                               subsequent_indent=' ' * 17)

    first_line = message_lines.pop(0)
    first_str = f'jc:  Error - {first_line}'
    first_str = first_wrapper.fill(first_str)
    _safe_print(first_str, file=sys.stderr)

    for line in message_lines:
        if line == '':
            continue
        message = next_wrapper.fill(line)
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

        quiet:        (bool) suppress compatibility message if True

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

    For bytes, returns True if there is any data.

    Parameters:

        data:        (string, bytes) input to check whether it contains data

    Returns:

        Boolean      True if input string (data) contains non-whitespace
                     characters, otherwise False. For bytes data, returns
                     True if there is any data, otherwise False.
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


def normalize_key(data: str) -> str:
    """
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
    special = '''!"#$%&'()*+,-./:;<=>?@[\]^`{|}~ '''
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
            try:
                return int(float(str_val))
            except (ValueError, TypeError):
                return None

    elif isinstance(value, (int, float)):
        return int(value)

    else:
        return None


def convert_to_float(value: object) -> Optional[float]:
    """
    Converts string and int input to float. Strips all non-numeric
    characters from strings.

    Parameters:

        value:         (string/integer) Input value

    Returns:

        float/None     Float if successful conversion, otherwise None
    """
    if isinstance(value, str):
        try:
            return float(re.sub(r'[^0-9\-\.]', '', value))
        except (ValueError, TypeError):
            return None

    elif isinstance(value, (int, float)):
        return float(value)

    else:
        return None


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
            test_value = convert_to_float(value)
            if test_value is not None:
                return bool(test_value)
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
def convert_size_to_int(size: str, binary: bool = False) -> Optional[int]:
    """
    Parse a human readable data size and return the number of bytes.

    Parameters:

        size:           (string) The human readable file size to parse.
        binary:         (boolean) `True` to use binary multiples of bytes
                        (base-2) for ambiguous unit symbols and names,
                        `False` to use decimal multiples of bytes (base-10).
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
        >>> convert_size_to_int('1 KB', binary=True)
        1024
        >>> convert_size_to_int('1.5 GB')
        1500000000
        >>> convert_size_to_int('1.5 GB', binary=True)
        1610612736
    """
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
            for unit in disk_size_units:
                # First we check for unambiguous symbols (KiB, MiB, GiB, etc)
                # and names (kibibyte, mebibyte, gibibyte, etc) because their
                # handling is always the same.
                if normalized_unit in (unit.binary.symbol.lower(), unit.binary.name.lower()):
                    return int(tokens[0] * unit.binary.divider)
                # Now we will deal with ambiguous prefixes (K, M, G, etc),
                # symbols (KB, MB, GB, etc) and names (kilobyte, megabyte,
                # gigabyte, etc) according to the caller's preference.
                if (normalized_unit in (unit.decimal.symbol.lower(), unit.decimal.name.lower()) or
                        normalized_unit.startswith(unit.decimal.symbol[0].lower())):
                    return int(tokens[0] * (unit.binary.divider if binary else unit.decimal.divider))
    # We failed to parse the size specification.
    return None


def input_type_check(data: object) -> None:
    """Ensure input data is a string. Raises `TypeError` if not."""
    if not isinstance(data, str):
        raise TypeError("Input data must be a 'str' object.")


def _lazy_splitlines(text: str) -> Iterable[str]:
    NEWLINES_PATTERN: str = r'(\r\n|\r|\n)'
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

        dt = self._parse_dt(self.string, format_hint=format_hint)
        self.format = dt['format']
        self.naive = dt['timestamp_naive']
        self.utc = dt['timestamp_utc']
        self.iso = dt['iso']

    def __repr__(self) -> str:
        return f'timestamp(string={self.string!r}, format={self.format}, naive={self.naive}, utc={self.utc}, iso={self.iso!r})'

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
        formats: tuple[TimeStampFormatType, ...] = (
            {'id': 1000, 'format': '%a %b %d %H:%M:%S %Y', 'locale': None},  # manual C locale format conversion: Tue Mar 23 16:12:11 2021 or Tue Mar 23 16:12:11 IST 2021
            {'id': 1100, 'format': '%a %b %d %H:%M:%S %Y %z', 'locale': None}, # git date output: Thu Mar 5 09:17:40 2020 -0800
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
            {'id': 1750, 'format': '%Y/%m/%d-%H:%M:%S.%f', 'locale': None},  # Google Big Table format with no timezone: 1970/01/01-01:00:00.000000
            {'id': 1755, 'format': '%Y/%m/%d-%H:%M:%S.%f%z', 'locale': None},  # Google Big Table format with timezone: 1970/01/01-01:00:00.000000+00:00
            {'id': 1760, 'format': '%Y-%m-%d %H:%M:%S%z', 'locale': None},  # certbot format with timezone: 2023-06-12 01:35:30+00:00
            {'id': 1800, 'format': '%d/%b/%Y:%H:%M:%S %z', 'locale': None},  # Common Log Format: 10/Oct/2000:13:55:36 -0700
            {'id': 2000, 'format': '%a %d %b %Y %I:%M:%S %p %Z', 'locale': None},  # en_US.UTF-8 local format (found in upower cli output): Tue 23 Mar 2021 04:12:11 PM UTC
            {'id': 3000, 'format': '%a %d %b %Y %I:%M:%S %p', 'locale': None},  # en_US.UTF-8 local format with non-UTC tz (found in upower cli output): Tue 23 Mar 2021 04:12:11 PM IST
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

        # from https://www.timeanddate.com/time/zones/
        # only removed UTC & GMT timezones and added known non-UTC offsets
        tz_abbr: set[str] = {
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

        offset_suffixes: tuple[str, ...] = (
            '-12:00', '-11:00', '-10:00', '-09:30', '-09:00',
            '-08:00', '-07:00', '-06:00', '-05:00', '-04:00', '-03:00', '-02:30',
            '-02:00', '-01:00', '+01:00', '+02:00', '+03:00', '+04:00', '+04:30',
            '+05:00', '+05:30', '+05:45', '+06:00', '+06:30', '+07:00', '+08:00',
            '+08:45', '+09:00', '+10:00', '+10:30', '+11:00', '+12:00', '+13:00',
            '+13:45', '+14:00'
        )

        data: str = dt_string or ''
        normalized_datetime: str = ''
        utc_tz: bool = False
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

        # try format hints first, then fall back to brute-force method
        hint_obj_list: List[TimeStampFormatType] = []
        for fmt_id in format_hint:
            for fmt in formats:
                if fmt_id == fmt['id']:
                    hint_obj_list.append(fmt)

        remaining_formats = [fmt for fmt in formats if not fmt['id'] in format_hint]
        optimized_formats = hint_obj_list + remaining_formats

        for fmt in optimized_formats:
            try:
                locale.setlocale(locale.LC_TIME, fmt['locale'])
                dt = datetime.strptime(normalized_datetime, fmt['format'])
                timestamp_obj['format'] = fmt['id']
                timestamp_naive = int(dt.replace(tzinfo=None).timestamp())
                iso_string = dt.replace(tzinfo=None).isoformat()
                locale.setlocale(locale.LC_TIME, None)
                break
            except Exception:
                locale.setlocale(locale.LC_TIME, None)
                continue

        if dt and utc_tz:
            dt_utc = dt.replace(tzinfo=timezone.utc)
            timestamp_utc = int(dt_utc.timestamp())
            iso_string = dt_utc.isoformat()

        if timestamp_naive:
            timestamp_obj['timestamp_naive'] = timestamp_naive
            timestamp_obj['timestamp_utc'] = timestamp_utc
            timestamp_obj['iso'] = iso_string

        return timestamp_obj
