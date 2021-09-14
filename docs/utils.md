
# utils
jc - JSON CLI output utility utils

## warning_message
```python
warning_message(message)
```

Prints a warning message for non-fatal issues

Parameters:

    message:        (string) text of message

Returns:

    None - just prints output to STDERR


## error_message
```python
error_message(message)
```

Prints an error message for fatal issues

Parameters:

    message:        (string) text of message

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


## stream_error
```python
stream_error(e, quiet, line)
```
reraise the stream exception with annotation or print an error _meta field if quiet=True

## timestamp
```python
timestamp(datetime_string)
```

Input a date-time text string of several formats and convert to a naive or timezone-aware epoch timestamp in UTC

Parameters:

    datetime_string:    (str)   a string representation of a date-time in several supported formats

Attributes:

    string              (str)   the input datetime string
    format              (int)   the format rule that was used to decode the datetime string
    naive               (int)   timestamp based on locally configured timezone. None if conversion fails
    utc                 (int)   aware timestamp only if UTC timezone detected in datetime string. None if conversion fails

