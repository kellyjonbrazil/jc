[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.utils"></a>

# jc.utils

## Table of Contents

* [jc.utils](#jc.utils)
  * [compatibility](#jc.utils.compatibility)
  * [convert_size_to_int](#jc.utils.convert_size_to_int)
  * [convert_to_bool](#jc.utils.convert_to_bool)
  * [convert_to_float](#jc.utils.convert_to_float)
  * [convert_to_int](#jc.utils.convert_to_int)
  * [error_message](#jc.utils.error_message)
  * [has_data](#jc.utils.has_data)
  * [input_type_check](#jc.utils.input_type_check)
  * [is_compatible](#jc.utils.is_compatible)
  * [line_slice](#jc.utils.line_slice)
  * [normalize_key](#jc.utils.normalize_key)
  * [remove_quotes](#jc.utils.remove_quotes)
  * [warning_message](#jc.utils.warning_message)

jc - JSON Convert utils

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

    quiet:        (bool) suppress compatibility message if `True`

Returns:

    None - just prints output to STDERR

<a id="jc.utils.convert_size_to_int"></a>

### convert_size_to_int

```python
def convert_size_to_int(size: str,
                        binary: bool = False,
                        posix_mode: bool = False,
                        decimal_bias: bool = False) -> Optional[int]
```

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

<a id="jc.utils.convert_to_bool"></a>

### convert_to_bool

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

<a id="jc.utils.convert_to_float"></a>

### convert_to_float

```python
def convert_to_float(value: object) -> Optional[float]
```

Converts string and int input to float. Strips all non-numeric
characters from strings.

Parameters:

    value:         (string/integer) Input value

Returns:

    float/None     Float if successful conversion, otherwise None

<a id="jc.utils.convert_to_int"></a>

### convert_to_int

```python
def convert_to_int(value: object) -> Optional[int]
```

Converts string and float input to int. Strips all non-numeric
characters from strings.

Parameters:

    value:         (string/float) Input value

Returns:

    integer/None   Integer if successful conversion, otherwise None

<a id="jc.utils.error_message"></a>

### error_message

```python
def error_message(message_lines: List[str]) -> None
```

Prints an error message to `STDERR` for fatal issues. The first line is
prepended with 'jc:  Error - ' and subsequent lines are indented.
Wraps text as needed based on the terminal width.

Parameters:

    message:   (list) list of string lines

Returns:

    None - just prints output to `STDERR`

<a id="jc.utils.has_data"></a>

### has_data

```python
def has_data(data: Union[str, bytes]) -> bool
```

Checks if the string input contains data. If there are any
non-whitespace characters then return `True`, else return `False`.

For bytes, returns `True` if there is any data.

Parameters:

    data:        (string, bytes) input to check whether it contains data

Returns:

    Boolean      `True` if input string (data) contains non-whitespace
                 characters, otherwise `False`. For bytes data, returns
                 `True` if there is any data, otherwise `False`.

<a id="jc.utils.input_type_check"></a>

### input_type_check

```python
def input_type_check(data: object) -> None
```

Ensure input data is a string. Raises `TypeError` if not.

<a id="jc.utils.is_compatible"></a>

### is_compatible

```python
def is_compatible(compatible: List[str]) -> bool
```

Returns True if the parser is compatible with the running OS platform.

<a id="jc.utils.line_slice"></a>

### line_slice

```python
def line_slice(
    data: Union[str, Iterable[str], TextIO, bytes, NoneType],
    slice_start: Optional[int] = None,
    slice_end: Optional[int] = None
) -> Union[str, Iterable[str], TextIO, bytes, NoneType]
```

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

<a id="jc.utils.normalize_key"></a>

### normalize_key

```python
def normalize_key(data: str) -> str
```

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

<a id="jc.utils.remove_quotes"></a>

### remove_quotes

```python
def remove_quotes(data: str) -> str
```

Remove single or double quotes surrounding a string. If no quotes are
found then the string is returned unmodified.

Parameters:

    data:       (string) Input value

Returns:

    string

<a id="jc.utils.warning_message"></a>

### warning_message

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


