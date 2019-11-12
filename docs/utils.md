# utils
jc - JSON CLI output utility utils
## warning_message
```python
warning_message(message)
```
Prints a warning message for non-fatal issues
## error_message
```python
error_message(message)
```
Prints an error message for fatal issues
## compatibility
```python
compatibility(mod_name, compatible)
```
Checks for the parser's compatibility with the running OS platform.

compatible options:

    linux, darwin, cygwin, win32, aix, freebsd

