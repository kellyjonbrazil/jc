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

    no return, just prints output to STDERR

## error_message
```python
error_message(message)
```

Prints an error message for fatal issues

Parameters:

    message:        (string) text of message

Returns:

    no return, just prints output to STDERR

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

    no return, just prints output to STDERR

## has_data
```python
has_data(data)
```

Checks if the input contains data. If there are any non-whitespace characters then return True, else return False

Parameters:

    data:        (string) input to check whether it contains data

Returns:

    Boolean      True if input string (data) contains non-whitespace characters, otherwise False

