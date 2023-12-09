# Table of Contents

* [jc.utils](#jc.utils)
  * [warning\_message](#jc.utils.warning_message)
  * [error\_message](#jc.utils.error_message)
  * [is\_compatible](#jc.utils.is_compatible)
  * [compatibility](#jc.utils.compatibility)
  * [has\_data](#jc.utils.has_data)
  * [convert\_to\_int](#jc.utils.convert_to_int)
  * [convert\_to\_float](#jc.utils.convert_to_float)
  * [convert\_to\_bool](#jc.utils.convert_to_bool)
  * [convert\_size\_to\_int](#jc.utils.convert_size_to_int)
  * [input\_type\_check](#jc.utils.input_type_check)
  * [timestamp](#jc.utils.timestamp)
    * [\_\_init\_\_](#jc.utils.timestamp.__init__)

<a id="jc.utils"></a>

# jc.utils

jc - JSON Convert utils

<a id="jc.utils.warning_message"></a>

### warning\_message

```python
def warning_message(message_lines: List[str]) -> None
```

Prints warning message to `STDERR` for non-fatal issues. The first line
is prepended with 'jc:  Warning - ' and subsequent lines are indented.
Wraps text as needed based on the terminal width.

Parameters:

    message:   (list) list of string lines

Returns:

    None - just prints output to STDERR

<a id="jc.utils.error_message"></a>

### error\_message

```python
def error_message(message_lines: List[str]) -> None
```

Prints an error message to `STDERR` for fatal issues. The first line is
prepended with 'jc:  Error - ' and subsequent lines are indented.
Wraps text as needed based on the terminal width.

Parameters:

    message:   (list) list of string lines

Returns:

    None - just prints output to STDERR

<a id="jc.utils.is_compatible"></a>

### is\_compatible

```python
def is_compatible(compatible: List[str]) -> bool
```

Returns True if the parser is compatible with the running OS platform.

<a id="jc.utils.compatibility"></a>

### compatibility

```python
def compatibility(mod_name: str,
                  compatible: List[str],
                  quiet: bool = False) -> None
```

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

<a id="jc.utils.has_data"></a>

### has\_data

```python
def has_data(data: Union[str, bytes]) -> bool
```

Checks if the string input contains data. If there are any
non-whitespace characters then return `True`, else return `False`.

For bytes, returns True if there is any data.

Parameters:

    data:        (string, bytes) input to check whether it contains data

Returns:

    Boolean      True if input string (data) contains non-whitespace
                 characters, otherwise False. For bytes data, returns
                 True if there is any data, otherwise False.

<a id="jc.utils.convert_to_int"></a>

### convert\_to\_int

```python
def convert_to_int(value: object) -> Optional[int]
```

Converts string and float input to int. Strips all non-numeric
characters from strings.

Parameters:

    value:         (string/float) Input value

Returns:

    integer/None   Integer if successful conversion, otherwise None

<a id="jc.utils.convert_to_float"></a>

### convert\_to\_float

```python
def convert_to_float(value: object) -> Optional[float]
```

Converts string and int input to float. Strips all non-numeric
characters from strings.

Parameters:

    value:         (string/integer) Input value

Returns:

    float/None     Float if successful conversion, otherwise None

<a id="jc.utils.convert_to_bool"></a>

### convert\_to\_bool

```python
def convert_to_bool(value: object) -> bool
```

Converts string, integer, or float input to boolean by checking
for 'truthy' values.

Parameters:

    value:          (string/integer/float) Input value

Returns:

    True/False      False unless a 'truthy' number or string is found
                    ('y', 'yes', 'true', '1', 1, -1, etc.)

<a id="jc.utils.convert_size_to_int"></a>

### convert\_size\_to\_int

```python
def convert_size_to_int(size: str, binary: bool = False) -> Optional[int]
```

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

<a id="jc.utils.input_type_check"></a>

### input\_type\_check

```python
def input_type_check(data: object) -> None
```

Ensure input data is a string. Raises `TypeError` if not.

<a id="jc.utils.timestamp"></a>

### timestamp Objects

```python
class timestamp()
```

<a id="jc.utils.timestamp.__init__"></a>

### \_\_init\_\_

```python
def __init__(datetime_string: Optional[str],
             format_hint: Optional[Iterable[int]] = None) -> None
```

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

