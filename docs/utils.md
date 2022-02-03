# Table of Contents

* [jc.utils](#jc.utils)
  * [warning\_message](#jc.utils.warning_message)
  * [error\_message](#jc.utils.error_message)
  * [compatibility](#jc.utils.compatibility)
  * [has\_data](#jc.utils.has_data)
  * [convert\_to\_int](#jc.utils.convert_to_int)
  * [convert\_to\_float](#jc.utils.convert_to_float)
  * [convert\_to\_bool](#jc.utils.convert_to_bool)
  * [stream\_success](#jc.utils.stream_success)
  * [stream\_error](#jc.utils.stream_error)
  * [add\_jc\_meta](#jc.utils.add_jc_meta)
  * [input\_type\_check](#jc.utils.input_type_check)
  * [streaming\_input\_type\_check](#jc.utils.streaming_input_type_check)
  * [streaming\_line\_input\_type\_check](#jc.utils.streaming_line_input_type_check)
  * [timestamp](#jc.utils.timestamp)
    * [\_\_init\_\_](#jc.utils.timestamp.__init__)

<a id="jc.utils"></a>

# jc.utils

jc - JSON CLI output utility utils

<a id="jc.utils.warning_message"></a>

### warning\_message

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

### error\_message

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

### compatibility

```python
def compatibility(mod_name: str, compatible: List, quiet: bool = False) -> None
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

### has\_data

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

### convert\_to\_int

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

### convert\_to\_float

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

### convert\_to\_bool

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

<a id="jc.utils.stream_success"></a>

### stream\_success

```python
def stream_success(output_line: Dict, ignore_exceptions: bool) -> Dict
```

Add `_jc_meta` object to output line if `ignore_exceptions=True`

<a id="jc.utils.stream_error"></a>

### stream\_error

```python
def stream_error(e: BaseException, ignore_exceptions: bool, line: str) -> Dict
```

Reraise the stream exception with annotation or print an error
`_jc_meta` field if `ignore_exceptions=True`.

<a id="jc.utils.add_jc_meta"></a>

### add\_jc\_meta

```python
def add_jc_meta(func)
```

Decorator for streaming parsers to add stream_success and stream_error
objects. This simplifies the yield lines in the streaming parsers.

With the decorator on parse():

    # successfully parsed line:
    yield output_line if raw else _process(output_line)

    # unsuccessfully parsed line:
    except Exception as e:
        yield e, line

Without the decorator on parse():

    # successfully parsed line:
    yield stream_success(output_line, ignore_exceptions) if raw else stream_success(_process(output_line), ignore_exceptions)

    # unsuccessfully parsed line:
    except Exception as e:
        yield stream_error(e, ignore_exceptions, line)

In all cases above:

    output_line:  (Dict):  successfully parsed line yielded as a dict

    e:            (BaseException):  exception object as the first value
                  of the tuple if the line was not successfully parsed.

    line:         (str):  string of the original line that did not
                  successfully parse.

<a id="jc.utils.input_type_check"></a>

### input\_type\_check

```python
def input_type_check(data: str) -> None
```

Ensure input data is a string. Raises `TypeError` if not.

<a id="jc.utils.streaming_input_type_check"></a>

### streaming\_input\_type\_check

```python
def streaming_input_type_check(data: Iterable) -> None
```

Ensure input data is an iterable, but not a string or bytes. Raises
`TypeError` if not.

<a id="jc.utils.streaming_line_input_type_check"></a>

### streaming\_line\_input\_type\_check

```python
def streaming_line_input_type_check(line: str) -> None
```

Ensure each line is a string. Raises `TypeError` if not.

<a id="jc.utils.timestamp"></a>

### timestamp Objects

```python
class timestamp()
```

<a id="jc.utils.timestamp.__init__"></a>

### \_\_init\_\_

```python
def __init__(datetime_string: str) -> None
```

Input a date-time text string of several formats and convert to a
naive or timezone-aware epoch timestamp in UTC.

Parameters:

    datetime_string  (str):  a string representation of a
        datetime in several supported formats

Returns a timestamp object with the following attributes:

    string  (str):  the input datetime string

    format  (int | None):  the format rule that was used to decode
        the datetime string. None if conversion fails.

    naive  (int | None):  timestamp based on locally configured
        timezone. None if conversion fails.

    utc  (int | None):  aware timestamp only if UTC timezone
        detected in datetime string. None if conversion fails.

