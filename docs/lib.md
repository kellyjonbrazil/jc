# Table of Contents

* [jc.lib](#jc.lib)
  * [data\_dir](#jc.lib.data_dir)
  * [get\_parser](#jc.lib.get_parser)
  * [parse](#jc.lib.parse)
  * [parser\_mod\_list](#jc.lib.parser_mod_list)
  * [plugin\_parser\_mod\_list](#jc.lib.plugin_parser_mod_list)
  * [standard\_parser\_mod\_list](#jc.lib.standard_parser_mod_list)
  * [streaming\_parser\_mod\_list](#jc.lib.streaming_parser_mod_list)
  * [slurpable\_parser\_mod\_list](#jc.lib.slurpable_parser_mod_list)
  * [parser\_info](#jc.lib.parser_info)
  * [all\_parser\_info](#jc.lib.all_parser_info)
  * [get\_help](#jc.lib.get_help)

<a id="jc.lib"></a>

# jc.lib

jc - JSON Convert lib module

<a id="jc.lib.get_parser"></a>

### get\_parser

```python
def get_parser(parser_mod_name) -> ModuleType
```

Return the parser module object

Parameters:

    parser_mod_name:    (string or   name of the parser module. This
                        Module)      function will accept module_name,
                                     cli-name, and --argument-name
                                     variants of the module name.
Returns:

    Parser: the parser module object

<a id="jc.lib.parse"></a>

### parse

```python
def parse(
    parser_mod_name: Union[str, ModuleType],
    data: Union[str, bytes, Iterable[str]],
    quiet: bool = False,
    raw: bool = False,
    ignore_exceptions: Optional[bool] = None,
    **kwargs
) -> Union[JSONDictType, List[JSONDictType], Iterator[JSONDictType]]
```

Parse the data (string or bytes) using the supplied parser (string or
module object).

This function provides a high-level API to simplify parser use. This
function will call built-in parsers and custom plugin parsers.

Example (standard parsers):

    >>> import jc
    >>> date_obj = jc.parse('date', 'Tue Jan 18 10:23:07 PST 2022')
    >>> print(f'The year is: {date_obj["year"]}')
    The year is: 2022

Example (streaming parsers):

    >>> import jc
    >>> ping_gen = jc.parse('ping_s', ping_output.splitlines())
    >>> for item in ping_gen:
    >>>     print(f'Response time: {item["time_ms"]} ms')
    Response time: 102 ms
    Response time: 109 ms
    ...

To get a list of available parser module names, use `parser_mod_list()`.

Alternatively, a parser module object can be supplied:

    >>> import jc
    >>> import jc.parsers.date as jc_date
    >>> date_obj = jc.parse(jc_date, 'Tue Jan 18 10:23:07 PST 2022')
    >>> print(f'The year is: {date_obj["year"]}')
    The year is: 2022

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

    parser_mod_name:    (string or   name of the parser module. This
                        Module)      function will accept module_name,
                                     cli-name, and --argument-name
                                     variants of the module name.

                                     A Module object can also be passed
                                     directly or via _get_parser()

    data:               (string or   data to parse (string or bytes for
                        bytes or     standard parsers, iterable of
                        iterable)    strings for streaming parsers)

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
def parser_mod_list(show_hidden: bool = False,
                    show_deprecated: bool = False) -> List[str]
```

Returns a list of all available parser module names.

<a id="jc.lib.plugin_parser_mod_list"></a>

### plugin\_parser\_mod\_list

```python
def plugin_parser_mod_list(show_hidden: bool = False,
                           show_deprecated: bool = False) -> List[str]
```

Returns a list of plugin parser module names. This function is a
subset of `parser_mod_list()`.

<a id="jc.lib.standard_parser_mod_list"></a>

### standard\_parser\_mod\_list

```python
def standard_parser_mod_list(show_hidden: bool = False,
                             show_deprecated: bool = False) -> List[str]
```

Returns a list of standard parser module names. This function is a
subset of `parser_mod_list()` and does not contain any streaming
parsers.

<a id="jc.lib.streaming_parser_mod_list"></a>

### streaming\_parser\_mod\_list

```python
def streaming_parser_mod_list(show_hidden: bool = False,
                              show_deprecated: bool = False) -> List[str]
```

Returns a list of streaming parser module names. This function is a
subset of `parser_mod_list()`.

<a id="jc.lib.slurpable_parser_mod_list"></a>

### slurpable\_parser\_mod\_list

```python
def slurpable_parser_mod_list(show_hidden: bool = False,
                              show_deprecated: bool = False) -> List[str]
```

Returns a list of slurpable parser module names. This function is a
subset of `parser_mod_list()`.

<a id="jc.lib.parser_info"></a>

### parser\_info

```python
def parser_info(parser_mod_name: Union[str, ModuleType],
                documentation: bool = False) -> ParserInfoType
```

Returns a dictionary that includes the parser module metadata.

Parameters:

    parser_mod_name:    (string or   name of the parser module. This
                        Module)      function will accept module_name,
                                     cli-name, and --argument-name
                                     variants of the module name as well
                                     as a parser module object.

    documentation:      (boolean)    include parser docstring if True

<a id="jc.lib.all_parser_info"></a>

### all\_parser\_info

```python
def all_parser_info(documentation: bool = False,
                    show_hidden: bool = False,
                    show_deprecated: bool = False) -> List[ParserInfoType]
```

Returns a list of dictionaries that includes metadata for all parser
modules. By default only non-hidden, non-deprecated parsers are
returned.

Parameters:

    documentation:      (boolean)    include parser docstrings if True
    show_hidden:        (boolean)    also show parsers marked as hidden
                                     in their info metadata.
    show_deprecated:    (boolean)    also show parsers marked as
                                     deprecated in their info metadata.

<a id="jc.lib.get_help"></a>

### get\_help

```python
def get_help(parser_mod_name: Union[str, ModuleType]) -> None
```

Show help screen for the selected parser.

This function will accept **module_name**, **cli-name**, and
**--argument-name** variants of the module name string as well as a
parser module object.

