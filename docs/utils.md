# Table of Contents

* [jc.utils](#jc.utils)
  * [warning\_message](#jc.utils.warning_message)
  * [error\_message](#jc.utils.error_message)
  * [compatibility](#jc.utils.compatibility)
  * [has\_data](#jc.utils.has_data)
  * [convert\_to\_int](#jc.utils.convert_to_int)
  * [convert\_to\_float](#jc.utils.convert_to_float)
  * [convert\_to\_bool](#jc.utils.convert_to_bool)
  * [input\_type\_check](#jc.utils.input_type_check)
  * [timestamp](#jc.utils.timestamp)
    * [\_\_init\_\_](#jc.utils.timestamp.__init__)

<a id="jc.utils"></a>

# jc.utils

jc - JSON Convert utils

<a id="jc.utils.warning_message"></a>

#### warning\_message

```python
def warning_message(message_lines: List[str]) -> None
```

Prints warning message for non-fatal issues. The first line is
prepended with 'jc:  Warning - ' and subsequent lines are indented.
Wraps text as needed based on the terminal width.

Parameters:

    message:   (list) list of string lines

Returns:

    None - just prints output to STDERR

<a id="jc.utils.error_message"></a>

#### error\_message

```python
def error_message(message_lines: List[str]) -> None
```

Prints an error message for fatal issues. The first line is
prepended with 'jc:  Error - ' and subsequent lines are indented.
Wraps text as needed based on the terminal width.

Parameters:

    message:   (list) list of string lines

Returns:

    None - just prints output to STDERR

<a id="jc.utils.compatibility"></a>

#### compatibility

```python
def compatibility(mod_name: str,
                  compatible: List,
                  quiet: bool = False) -> None
```

Checks for the parser's compatibility with the running OS
platform.

Parameters:

    mod_name:     (string) __name__ of the calling module

    compatible:   (list) sys.platform name(s) compatible with
                  the parser. compatible options:
                  linux, darwin, cygwin, win32, aix, freebsd

    quiet:        (bool) supress compatibility message if True

Returns:

    None - just prints output to STDERR

<a id="jc.utils.has_data"></a>

#### has\_data

```python
def has_data(data: str) -> bool
```

Checks if the input contains data. If there are any non-whitespace
characters then return True, else return False.

Parameters:

    data:        (string) input to check whether it contains data

Returns:

    Boolean      True if input string (data) contains non-whitespace
                 characters, otherwise False

<a id="jc.utils.convert_to_int"></a>

#### convert\_to\_int

```python
def convert_to_int(value: Union[str, float]) -> Optional[int]
```

Converts string and float input to int. Strips all non-numeric
characters from strings.

Parameters:

    value:         (string/float) Input value

Returns:

    integer/None   Integer if successful conversion, otherwise None

<a id="jc.utils.convert_to_float"></a>

#### convert\_to\_float

```python
def convert_to_float(value: Union[str, int]) -> Optional[float]
```

Converts string and int input to float. Strips all non-numeric
characters from strings.

Parameters:

    value:         (string/integer) Input value

Returns:

    float/None     Float if successful conversion, otherwise None

<a id="jc.utils.convert_to_bool"></a>

#### convert\_to\_bool

```python
def convert_to_bool(value: Union[str, int, float]) -> bool
```

Converts string, integer, or float input to boolean by checking
for 'truthy' values.

Parameters:

    value:          (string/integer/float) Input value

Returns:

    True/False      False unless a 'truthy' number or string is found
                    ('y', 'yes', 'true', '1', 1, -1, etc.)

<a id="jc.utils.input_type_check"></a>

#### input\_type\_check

```python
def input_type_check(data: str) -> None
```

Ensure input data is a string. Raises `TypeError` if not.

<a id="jc.utils.timestamp"></a>

## timestamp Objects

```python
class timestamp()
```

<a id="jc.utils.timestamp.__init__"></a>

#### \_\_init\_\_

```python
def __init__(datetime_string: str,
             format_hint: Union[List, Tuple, None] = None) -> None
```

Input a datetime text string of several formats and convert to a
naive or timezone-aware epoch timestamp in UTC.

Parameters:

    datetime_string  (str):  a string representation of a
        datetime in several supported formats

    format_hint  (list | tuple):  an optional list of format ID
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

