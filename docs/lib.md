
# lib
jc - JSON CLI output utility
JC lib module


## parse
```python
parse(parser_mod_name,
      data,
      quiet=False,
      raw=False,
      ignore_exceptions=None,
      **kwargs)
```

Parse the string data using the supplied parser module.

This function provides a high-level API to simplify parser use. This
function will call built-in parsers and custom plugin parsers.

Example:

    >>> import jc
    >>> jc.parse('date', 'Tue Jan 18 10:23:07 PST 2022')
    {'year': 2022, 'month': 'Jan', 'month_num': 1, 'day'...}

To get a list of available parser module names, use `parser_mod_list()`
or `plugin_parser_mod_list()`. `plugin_parser_mod_list()` is a subset
of `parser_mod_list()`.

You can also use the lower-level parser modules directly:

    >>> import jc.parsers.date
    >>> jc.parsers.date.parse('Tue Jan 18 10:23:07 PST 2022')

Though, accessing plugin parsers directly is a bit more involved, so
this higher-level API is recommended. Here is how you can access plugin
parsers without this API:

    >>> import os
    >>> import sys
    >>> import jc.appdirs
    >>> data_dir = jc.appdirs.user_data_dir('jc', 'jc')
    >>> local_parsers_dir = os.path.join(data_dir, 'jcparsers')
    >>> sys.path.append(local_parsers_dir)
    >>> import my_custom_parser
    >>> my_custom_parser.parse('command_data')

Parameters:

    parser_mod_name:    (string)     Name of the parser module

    data:               (string or   Data to parse (string for normal
                        iterator)    parsers, iterator of strings for
                                     streaming parsers)

    raw:                (boolean)    output preprocessed JSON if True
    quiet:              (boolean)    suppress warning messages if True

    ignore_exceptions:  (boolean)    ignore parsing exceptions if True
                                     (streaming parsers only)

Returns:

    Standard Parsers:   Dictionary or List of Dictionaries
    Streaming Parsers:  Generator Object


## parser_mod_list
```python
parser_mod_list()
```
Returns a list of all available parser module names.

## plugin_parser_mod_list
```python
plugin_parser_mod_list()
```
Returns a list of plugin parser module names.

## get_help
```python
get_help(parser_mod_name)
```
Show help screen for the selected parser
