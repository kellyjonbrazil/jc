"""JC - JSON CLI output utility

* kellyjonbrazil@gmail.com

This package serializes the output of many standard unix command line tools
to dictionaries and lists of dictionaries.

For documentation on each parser, see the
[documentation site](https://kellyjonbrazil.github.io/jc/) or use
`jc.get_help('parser_module_name')`

Example:

    >>> import subprocess
    >>> import jc
    >>>
    >>> cmd_output = subprocess.check_output(['dig', 'example.com'],
                                             text=True)
    >>> data = jc.parse('dig', cmd_output)
    >>> data
    [{'id': 64612, 'opcode': 'QUERY', 'status': 'NOERROR', ...}]

Alternatively, you can bypass the high-level API and call the parser
modules directly:

    >>> import subprocess
    >>> import jc.parsers.dig
    >>>
    >>> cmd_output = subprocess.check_output(['dig', 'example.com'],
                                             text=True)
    >>> data = jc.parsers.dig.parse(cmd_output)
    >>> data
    [{'id': 64612, 'opcode': 'QUERY', 'status': 'NOERROR', ...}]

Available Functions (use `help(jc.lib)` for details):

    parse(parser_module_name: str, data: str | iterable)
        High-level API to easily access the parser. This API will find both
        built-in parsers and local plugin parsers.

    get_help(parser_module_name: str)
        Convenience function to display the help screen for a parser using
        its module name.

    parser_mod_list()
        Get a list of all available parser module names to be used in
        parse() and get_help().

    plugin_parser_mod_list()
        Get a list of plugin parser module names. This list is a subset of
        parser_mod_list().
"""
from .lib import (__version__, parse, parser_mod_list,
                  plugin_parser_mod_list, get_help)
