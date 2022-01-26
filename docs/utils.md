<a id="jc.utils"></a>

# jc.utils

jc - JSON CLI output utility utils

<a id="jc.utils.warning_message"></a>

### warning\_message

```python
def warning_message(message_lines)
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
def error_message(message_lines)
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
def compatibility(mod_name, compatible, quiet=False)
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
def has_data(data)
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
def convert_to_int(value)
```

Converts string and float input to int. Strips all non-numeric
characters from strings.

Parameters:

    value:         (string/integer/float) Input value

Returns:

    integer/None   Integer if successful conversion, otherwise None

<a id="jc.utils.convert_to_float"></a>

### convert\_to\_float

```python
def convert_to_float(value)
```

Converts string and int input to float. Strips all non-numeric
characters from strings.

Parameters:

    value:         (string) Input value

Returns:

    float/None     Float if successful conversion, otherwise None

<a id="jc.utils.convert_to_bool"></a>

### convert\_to\_bool

```python
def convert_to_bool(value)
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
def stream_success(output_line, ignore_exceptions)
```

Add `_jc_meta` object to output line if `ignore_exceptions=True`

<a id="jc.utils.stream_error"></a>

### stream\_error

```python
def stream_error(e, ignore_exceptions, line)
```

Reraise the stream exception with annotation or print an error
`_jc_meta` field if `ignore_exceptions=True`.

<a id="jc.utils.input_type_check"></a>

### input\_type\_check

```python
def input_type_check(data)
```

Ensure input data is a string

<a id="jc.utils.streaming_input_type_check"></a>

### streaming\_input\_type\_check

```python
def streaming_input_type_check(data)
```

Ensure input data is an iterable, but not a string or bytes

<a id="jc.utils.streaming_line_input_type_check"></a>

### streaming\_line\_input\_type\_check

```python
def streaming_line_input_type_check(line)
```

Ensure each line is a string

<a id="jc.utils.timestamp"></a>

## timestamp Objects

```python
class timestamp()
```

Input a date-time text string of several formats and convert to a
naive or timezone-aware epoch timestamp in UTC.

Parameters:

    datetime_string:  (str)  a string representation of a
                             date-time in several supported formats

Attributes:

    string            (str)   the input datetime string

    format            (int)   the format rule that was used to
                              decode the datetime string. None if
                              conversion fails

    naive             (int)   timestamp based on locally configured
                              timezone. None if conversion fails

    utc               (int)   aware timestamp only if UTC timezone
                              detected in datetime string. None if
                              conversion fails

