
# utils
jc - JSON CLI output utility utils

## warning_message
```python
warning_message(message_lines)
```

Prints warning message for non-fatal issues. The first line is prepended with
'jc:  Warning - ' and subsequent lines are indented. Wraps text as needed based
on the terminal width.

Parameters:

    message:   (list) list of string lines

Returns:

    None - just prints output to STDERR


## error_message
```python
error_message(message_lines)
```

Prints an error message for fatal issues. The first line is prepended with
'jc:  Error - ' and subsequent lines are indented. Wraps text as needed based
on the terminal width.

Parameters:

    message:   (list) list of string lines

Returns:

    None - just prints output to STDERR


## compatibility
```python
compatibility(mod_name, compatible)
```
Checks for the parser's compatibility with the running OS platform.

Parameters:

    mod_name:       (string) __name__ of the calling module

    compatible:     (list) sys.platform name(s) compatible with the parser
                    compatible options:
                    linux, darwin, cygwin, win32, aix, freebsd

Returns:

    None - just prints output to STDERR


## has_data
```python
has_data(data)
```

Checks if the input contains data. If there are any non-whitespace characters then return True, else return False

Parameters:

    data:        (string) input to check whether it contains data

Returns:

    Boolean      True if input string (data) contains non-whitespace characters, otherwise False


## convert_to_int
```python
convert_to_int(value)
```

Converts string and float input to int. Strips all non-numeric characters from strings.

Parameters:

    value:          (string/integer/float) Input value

Returns:

    integer/None    Integer if successful conversion, otherwise None


## convert_to_float
```python
convert_to_float(value)
```

Converts string and int input to float. Strips all non-numeric characters from strings.

Parameters:

    value:          (string) Input value

Returns:

    float/None      Float if successful conversion, otherwise None


## convert_to_bool
```python
convert_to_bool(value)
```

Converts string, integer, or float input to boolean by checking for 'truthy' values

Parameters:

    value:          (string/integer/float) Input value

Returns:

    True/False      False unless a 'truthy' number or string is found ('y', 'yes', 'true', '1', 1, -1, etc.)


## stream_success
```python
stream_success(output_line, ignore_exceptions)
```
Add `_jc_meta` object to output line if `ignore_exceptions=True`

## stream_error
```python
stream_error(e, ignore_exceptions, line)
```
Reraise the stream exception with annotation or print an error `_jc_meta`
field if `ignore_exceptions=True`


## timestamp
```python
timestamp(datetime_string)
```

Input a date-time text string of several formats and convert to a naive or timezone-aware epoch timestamp in UTC

Parameters:

    datetime_string:    (str)   a string representation of a date-time in several supported formats

Attributes:

    string              (str)   the input datetime string
    format              (int)   the format rule that was used to decode the datetime string. None if conversion fails
    naive               (int)   timestamp based on locally configured timezone. None if conversion fails
    utc                 (int)   aware timestamp only if UTC timezone detected in datetime string. None if conversion fails

