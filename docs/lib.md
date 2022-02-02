# Table of Contents

* [jc.lib](#jc.lib)
  * [parse](#jc.lib.parse)
  * [parser\_mod\_list](#jc.lib.parser_mod_list)
  * [plugin\_parser\_mod\_list](#jc.lib.plugin_parser_mod_list)
  * [parser\_info](#jc.lib.parser_info)
  * [all\_parser\_info](#jc.lib.all_parser_info)
  * [get\_help](#jc.lib.get_help)

<a id="jc.lib"></a>

# jc.lib

jc - JSON CLI output utility
JC lib module

<a id="jc.lib.parse"></a>

### parse

```python
def parse(parser_mod_name: str, data: Union[str, Iterable[str]], quiet: bool = False, raw: bool = False, ignore_exceptions: bool = None, **kwargs) -> Union[Dict, List[Dict], Iterator[Dict]]
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

Though, accessing plugin parsers directly is a bit more cumbersome, so
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

    parser_mod_name:    (string)     name of the parser module. This
                                     function will accept module_name,
                                     cli-name, and --argument-name
                                     variants of the module name.

    data:               (string or   data to parse (string for normal
                        iterator)    parsers, iterator of strings for
                                     streaming parsers)

    raw:                (boolean)    output preprocessed JSON if True

    quiet:              (boolean)    suppress warning messages if True

    ignore_exceptions:  (boolean)    ignore parsing exceptions if True
                                     (streaming parsers only)

Returns:

    Standard Parsers:   Dictionary or List of Dictionaries
    Streaming Parsers:  Generator Object containing Dictionaries

<a id="jc.lib.parser_mod_list"></a>

### parser\_mod\_list

```python
def parser_mod_list() -> List[str]
```

Returns a list of all available parser module names.

<a id="jc.lib.plugin_parser_mod_list"></a>

### plugin\_parser\_mod\_list

```python
def plugin_parser_mod_list() -> List[str]
```

Returns a list of plugin parser module names. This function is a
subset of `parser_mod_list()`.

<a id="jc.lib.parser_info"></a>

### parser\_info

```python
def parser_info(parser_mod_name: str) -> Dict
```

Returns a dictionary that includes the module metadata.

This function will accept **module_name**, **cli-name**, and
**--argument-name** variants of the module name string.

<a id="jc.lib.all_parser_info"></a>

### all\_parser\_info

```python
def all_parser_info() -> List[Dict]
```

Returns a list of dictionaries that includes metadata for all modules.

<a id="jc.lib.get_help"></a>

### get\_help

```python
def get_help(parser_mod_name: str) -> None
```

Show help screen for the selected parser.

This function will accept **module_name**, **cli-name**, and
**--argument-name** variants of the module name string.

