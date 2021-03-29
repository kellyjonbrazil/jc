
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


## parse_datetime_to_timestamp
```python
parse_datetime_to_timestamp(data)
```

Input a date-time text string of several formats and convert to a naive or timezone-aware epoch timestamp in UTC

Parameters:

    data:       (string) a string representation of a date-time in several supported formats

Returns:

    Dictionary  A Dictionary of the following format:

                {
                    "format":               integer,     # for debugging purposes. None if conversion fails
                    "timestamp_naive":      integer,     # timestamp based on locally configured timezone. None if conversion fails
                    "timestamp_utc":        integer      # aware timestamp only if UTC timezone detected. None if conversion fails
                }

                The format integer denotes which date_time format conversion succeeded.
                The timestamp_naive integer is the converted date-time string to a naive epoch timestamp.
                The timestamp_utc integer is the converted date-time string to an aware epoch timestamp
                    in the UTC timezone. If an aware conversion cannot be performed (e.g. the UTC timezone
                    is not found in the date-time string), then this field will be None.

                If the conversion completely fails, all fields will be None.

