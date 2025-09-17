"""jc - JSON Convert
JC cli module
"""

import io
import sys
import os
import re
from datetime import datetime, timezone
import textwrap
import shlex
import subprocess
from typing import List, Dict, Iterable, Union, Optional, TextIO
from types import ModuleType
from .lib import (
    __version__, parser_info, all_parser_info, parsers, get_parser, _parser_is_streaming,
    parser_mod_list, standard_parser_mod_list, plugin_parser_mod_list, streaming_parser_mod_list,
    slurpable_parser_mod_list, _parser_is_slurpable
)
from .jc_types import JSONDictType, CustomColorType, ParserInfoType
from . import utils
from .cli_data import (
    long_options_map, new_pygments_colors, old_pygments_colors, helptext_preamble_string,
    slicetext_string, helptext_end_string
)
from .shell_completions import bash_completion, zsh_completion
from . import tracebackplus
from .exceptions import LibraryNotInstalled, ParseError

PYGMENTS_INSTALLED: bool = False
try:
    import pygments
    from pygments import highlight
    from pygments.style import Style
    from pygments.token import (Name, Number, String, Keyword)
    from pygments.lexers.data import JsonLexer, YamlLexer
    from pygments.formatters import Terminal256Formatter
    PYGMENTS_INSTALLED = True
except Exception:
    pass

JC_CLEAN_EXIT: int = 0
JC_ERROR_EXIT: int = 100
MAX_EXIT: int = 255
SLICER_PATTERN: str = r'-?[0-9]*\:-?[0-9]*$'
SLICER_RE = re.compile(SLICER_PATTERN)


class info():
    version: str = __version__
    description: str = 'JSON Convert'
    author: str = 'Kelly Brazil'
    author_email: str = 'kellyjonbrazil@gmail.com'
    website: str = 'https://github.com/kellyjonbrazil/jc'
    copyright: str = '© 2019-2025 Kelly Brazil'
    license: str = 'MIT License'


# We only support 2.3.0+, pygments changed color names in 2.4.0.
# startswith is sufficient and avoids potential exceptions from split and int.
if PYGMENTS_INSTALLED:
    if pygments.__version__.startswith('2.3.'):
        PYGMENT_COLOR = old_pygments_colors
    else:
        PYGMENT_COLOR = new_pygments_colors


class JcCli():
    __slots__ = ('data_in', 'data_out', 'options', 'args', 'parser_module',
                 'parser_name', 'indent', 'pad', 'custom_colors',
                 'show_hidden', 'show_categories', 'ascii_only',
                 'json_separators', 'json_indent', 'run_timestamp',
                 'inputlist', 'about', 'debug', 'verbose_debug',
                 'force_color', 'mono', 'help_me', 'pretty', 'quiet',
                 'ignore_exceptions', 'raw', 'slurp', 'meta_out', 'unbuffer',
                 'version_info', 'yaml_output', 'bash_comp', 'zsh_comp',
                 'magic_found_parser', 'magic_options', 'magic_run_command',
                 'magic_run_command_str', 'magic_stdout', 'magic_stderr',
                 'magic_returncode', 'slice_str', 'slice_start', 'slice_end')

    def __init__(self) -> None:
        self.data_in: Optional[Union[str, bytes, TextIO, Iterable[str]]] = None
        self.data_out: Optional[Union[List[JSONDictType], JSONDictType]] = None
        self.options: List[str] = []
        self.args: List[str] = []
        self.parser_module: Optional[ModuleType] = None
        self.parser_name: Optional[str] = None
        self.indent: int = 0
        self.pad: int = 0
        self.custom_colors: CustomColorType = {}
        self.show_hidden: bool = False
        self.show_categories: bool = False
        self.ascii_only: bool = False
        self.json_separators: Optional[tuple[str, str]] = (',', ':')
        self.json_indent: Optional[int] = None
        self.run_timestamp: Optional[datetime] = None
        self.inputlist: Optional[List[str]] = None

        # slicer
        self.slice_str: str = ''
        self.slice_start: Optional[int] = None
        self.slice_end: Optional[int] = None

        # cli options
        self.about: bool = False
        self.debug: bool = False
        self.verbose_debug: bool = False
        self.force_color: bool = False
        self.mono: bool = False
        self.help_me: bool = False
        self.pretty: bool = False
        self.quiet: bool = False
        self.ignore_exceptions: bool = False
        self.raw: bool = False
        self.slurp: bool = False
        self.meta_out: bool = False
        self.unbuffer: bool = False
        self.version_info: bool = False
        self.yaml_output: bool = False
        self.bash_comp: bool = False
        self.zsh_comp: bool = False

        # magic attributes
        self.magic_found_parser: Optional[str] = None
        self.magic_options: List[str] = []
        self.magic_run_command: Optional[List[str]] = None
        self.magic_run_command_str: str = ''
        self.magic_stdout: Optional[Union[str, Iterable[str]]] = None
        self.magic_stderr: Optional[str] = None
        self.magic_returncode: int = 0

    def set_custom_colors(self) -> None:
        """
        Sets the custom_colors dictionary to be used in Pygments custom style class.

        Grab custom colors from JC_COLORS environment variable. JC_COLORS env
        variable takes 4 comma separated string values and should be in the
        format of:

        JC_COLORS=<keyname_color>,<keyword_color>,<number_color>,<string_color>

        Where colors are: black, red, green, yellow, blue, magenta, cyan, gray,
        brightblack, brightred, brightgreen, brightyellow, brightblue, brightmagenta,
        brightcyan, white, default

        Default colors:
        JC_COLORS=blue,brightblack,magenta,green
        JC_COLORS=default,default,default,default
        """
        if PYGMENTS_INSTALLED:
            input_error = False
            env_colors = os.getenv('JC_COLORS')

            if env_colors:
                color_list = env_colors.split(',')
            else:
                color_list = ['default', 'default', 'default', 'default']

            if len(color_list) != 4:
                input_error = True

            for color in color_list:
                if color != 'default' and color not in PYGMENT_COLOR:
                    input_error = True

            # if there is an issue with the env variable, just set all colors to default and move on
            if input_error:
                utils.warning_message(['Could not parse JC_COLORS environment variable'])
                color_list = ['default', 'default', 'default', 'default']

            # Try the color set in the JC_COLORS env variable first. If it is set to default, then fall back to default colors
            self.custom_colors = {
                Name.Tag: f'bold {PYGMENT_COLOR[color_list[0]]}' if color_list[0] != 'default' else f"bold {PYGMENT_COLOR['blue']}",   # key names
                Keyword: PYGMENT_COLOR[color_list[1]] if color_list[1] != 'default' else PYGMENT_COLOR['brightblack'],                 # true, false, null
                Number: PYGMENT_COLOR[color_list[2]] if color_list[2] != 'default' else PYGMENT_COLOR['magenta'],                      # numbers
                String: PYGMENT_COLOR[color_list[3]] if color_list[3] != 'default' else PYGMENT_COLOR['green']                         # strings
            }

    def set_mono(self) -> None:
        """
        Sets mono attribute based on CLI options.

        Then set to False if `STDOUT` is a TTY. True if output is being piped to
        another program and foce_color is True. This allows forcing of ANSI
        color codes even when using pipes.

        Also set mono to True if Pygments is not installed.
        """
        self.mono = ('m' in self.options or bool(os.getenv('NO_COLOR'))) and not self.force_color

        if not sys.stdout.isatty() and not self.force_color:
            self.mono = True

        if not PYGMENTS_INSTALLED:
            self.mono = True

    @staticmethod
    def parser_shortname(parser_arg: str) -> str:
        """Return short name of the parser with dashes and no -- prefix"""
        p = parser_arg.lstrip('-')
        return p.replace('_', '-')

    def parsers_text(self) -> str:
        """Return the argument and description information from each parser"""
        ptext: str = ''
        padding_char: str = ' '
        for p in all_parser_info(show_hidden=self.show_hidden, show_deprecated=False):
            parser_arg: str = p.get('argument', 'UNKNOWN')
            padding: int = self.pad - len(parser_arg)
            parser_desc: str = p.get('description', 'No description available.')
            indent_text: str = padding_char * self.indent
            padding_text: str = padding_char * padding
            ptext += indent_text + parser_arg + padding_text + parser_desc + '\n'

        return ptext

    def parser_categories_text(self) -> str:
        """Return lists of parsers by category"""
        category_text: str = ''
        padding_char: str = ' '
        all_parsers = all_parser_info(show_hidden=True, show_deprecated=False)
        generic = [{'arg': x['argument'], 'desc': x['description']} for x in all_parsers if 'generic' in x.get('tags', [])]
        standard = [{'arg': x['argument'], 'desc': x['description']} for x in all_parsers if 'standard' in x.get('tags', [])]
        command = [{'arg': x['argument'], 'desc': x['description']} for x in all_parsers if 'command' in x.get('tags', [])]
        slurpable = [{'arg': x['argument'], 'desc': x['description']} for x in all_parsers if 'slurpable' in x.get('tags', [])]
        file_str_bin = [
            {'arg': x['argument'], 'desc': x['description']} for x in all_parsers
                if 'file' in x.get('tags', []) or
                'string' in x.get('tags', []) or
                'binary' in x.get('tags', [])
        ]
        streaming = [{'arg': x['argument'], 'desc': x['description']} for x in all_parsers if x.get('streaming')]
        categories: Dict = {
            'Generic Parsers:': generic,
            'Standard Spec Parsers:': standard,
            'File/String/Binary Parsers:': file_str_bin,
            'Slurpable Parsers:': slurpable,
            'Streaming Parsers:': streaming,
            'Command Parsers:': command
        }

        for cat, cat_objs in categories.items():
            category_text += f'{cat}  ({len(cat_objs)})\n'
            for p in cat_objs:
                parser_arg: str = p.get('arg', 'UNKNOWN')
                parser_desc: str = p.get('desc', 'No description available.')
                padding: int = self.pad - len(parser_arg)
                padding_text: str = padding_char * padding
                category_text += f'{parser_arg}{padding_text}{parser_desc}\n'
            category_text += '\n'

        return category_text[:-1]

    def options_text(self) -> str:
        """Return the argument and description information from each option"""
        otext: str = ''
        padding_char: str = ' '
        for option in long_options_map:
            o_short: str = '-' + long_options_map[option][0]
            o_desc: str = long_options_map[option][1]
            o_combined: str = o_short + ',  ' + option
            padding: int = self.pad - len(o_combined)
            indent_text: str = padding_char * self.indent
            padding_text: str = padding_char * padding
            otext += indent_text + o_combined + padding_text + o_desc + '\n'

        return otext

    @staticmethod
    def about_jc() -> JSONDictType:
        """Return jc info and the contents of each parser.info as a dictionary"""
        return {
            'name': 'jc',
            'version': info.version,
            'description': info.description,
            'author': info.author,
            'author_email': info.author_email,
            'website': info.website,
            'copyright': info.copyright,
            'license': info.license,
            'python_version': '.'.join((str(sys.version_info.major), str(sys.version_info.minor), str(sys.version_info.micro))),
            'python_path': sys.executable,
            'parser_count': len(parser_mod_list(show_hidden=True, show_deprecated=True)),
            'standard_parser_count': len(standard_parser_mod_list(show_hidden=True, show_deprecated=True)),
            'streaming_parser_count': len(streaming_parser_mod_list(show_hidden=True, show_deprecated=True)),
            'plugin_parser_count': len(plugin_parser_mod_list(show_hidden=True, show_deprecated=True)),
            'slurpable_parser_count': len(slurpable_parser_mod_list(show_hidden=True, show_deprecated=True)),
            'parsers': all_parser_info(show_hidden=True, show_deprecated=True)
        }

    def helptext(self) -> str:
        """Return the help text with the list of parsers"""
        parsers_string: str = self.parsers_text()
        options_string: str = self.options_text()
        helptext_string: str = f'{helptext_preamble_string}{parsers_string}\nOptions:\n{options_string}\n{slicetext_string}\n{helptext_end_string}'
        return helptext_string

    def help_doc(self) -> None:
        """
        Pages the parser documentation if a parser is found in the arguments,
        otherwise the general help text is printed.
        """
        self.indent = 4
        self.pad = 22

        if self.show_categories:
            utils._safe_print(self.parser_categories_text())
            return

        for arg in self.args:
            parser_name: str = self.parser_shortname(arg)

            if parser_name in parsers:
                p_info: ParserInfoType = parser_info(parser_name, documentation=True)
                compatible: str = ', '.join(p_info.get('compatible', ['unknown']))
                docs: str = p_info.get('documentation', 'No documentation available.')
                version: str = p_info.get('version', 'unknown')
                author: str = p_info.get('author', 'unknown')
                author_email: str = p_info.get('author_email', 'unknown')

                slurpy = ''
                if 'slurpable' in p_info.get('tags', []):
                    slurpy = 'This parser can be used with the `--slurp` command-line option.\n\n'

                doc_text: str = \
                    f'{docs}\n' \
                    f'Compatibility:  {compatible}\n\n' \
                    f'{slurpy}' \
                    f'Version {version} by {author} ({author_email})\n'

                utils._safe_pager(doc_text)
                return

        utils._safe_print(self.helptext())
        return

    @staticmethod
    def versiontext() -> str:
        """Return the version text"""
        py_ver: str = '.'.join((str(sys.version_info.major), str(sys.version_info.minor), str(sys.version_info.micro)))
        versiontext_string: str = f'''\
        jc version:  {info.version}
        python interpreter version:  {py_ver}
        python path:  {sys.executable}

        {info.website}
        {info.copyright}
        '''
        return textwrap.dedent(versiontext_string)

    def yaml_out(self) -> str:
        """
        Return a YAML formatted string. String may include color codes. If the
        YAML library is not installed, output will fall back to JSON with a
        warning message to STDERR"""
        # make ruamel.yaml import optional
        try:
            from ruamel.yaml import YAML, representer
            YAML_INSTALLED = True
        except Exception:
            YAML_INSTALLED = False

        if YAML_INSTALLED:
            y_string_buf = io.BytesIO()

            # monkey patch to disable plugins since we don't use them and in
            # ruamel.yaml versions prior to 0.17.0 the use of __file__ in the
            # plugin code is incompatible with the pyoxidizer packager
            YAML.official_plug_ins = lambda a: []  # type: ignore

            # monkey patch to disable aliases
            representer.RoundTripRepresenter.ignore_aliases = lambda x, y: True  # type: ignore

            yaml = YAML()
            yaml.default_flow_style = False
            yaml.explicit_start = True  # type: ignore
            yaml.allow_unicode = not self.ascii_only
            yaml.encoding = 'utf-8'
            yaml.dump(self.data_out, y_string_buf)
            y_string = y_string_buf.getvalue().decode('utf-8')[:-1]

            if not self.mono:
                class JcStyle(Style):
                    styles: CustomColorType = self.custom_colors

                return str(highlight(y_string, YamlLexer(), Terminal256Formatter(style=JcStyle))[0:-1])

            return y_string

        utils.warning_message(['YAML Library not installed. Reverting to JSON output.'])
        return self.json_out()

    def json_out(self) -> str:
        """
        Return a JSON formatted string. String may include color codes or be
        pretty printed.
        """
        import json

        if self.pretty:
            self.json_indent = 2
            self.json_separators = None

        # Convert any non-serializable object to a string
        def string_serializer(data):
            return str(data)

        j_string = json.dumps(
            self.data_out,
            indent=self.json_indent,
            separators=self.json_separators,
            ensure_ascii=self.ascii_only,
            default=string_serializer
        )

        if not self.mono and PYGMENTS_INSTALLED:
            class JcStyle(Style):
                styles: CustomColorType = self.custom_colors

            return str(highlight(j_string, JsonLexer(), Terminal256Formatter(style=JcStyle))[0:-1])

        return j_string

    def safe_print_out(self) -> None:
        """Safely prints JSON or YAML output in both UTF-8 and ASCII systems"""
        if self.yaml_output:
            try:
                print(self.yaml_out(), flush=self.unbuffer)
            except UnicodeEncodeError:
                self.ascii_only = True
                print(self.yaml_out(), flush=self.unbuffer)

        else:
            try:
                print(self.json_out(), flush=self.unbuffer)
            except UnicodeEncodeError:
                self.ascii_only = True
                print(self.json_out(), flush=self.unbuffer)

    def magic_parser(self) -> None:
        """
        Parse command arguments for magic syntax: `jc -p ls -al` and set the
        magic attributes.
        """
        # bail immediately if there are no args or a parser is defined
        if len(self.args) <= 1 or (self.args[1].startswith('--') and self.args[1] not in long_options_map):
            return

        args_given: List[str] = self.args[1:]

        # find the options
        for arg in list(args_given):
            # long option found - populate option list
            if arg in long_options_map:
                self.magic_options.extend(long_options_map[arg][0])
                args_given.pop(0)
                continue

            # parser found - use standard syntax
            if arg.startswith('--'):
                self.magic_options = []
                return

            # slicer found
            if ':' in arg:
                if SLICER_RE.match(arg):
                    self.slice_str = arg
                    args_given.pop(0)
                    continue
                else:
                    utils.warning_message(['Invalid slice syntax.'])
                    args_given.pop(0)
                    continue

            # option found - populate option list
            if arg.startswith('-'):
                self.magic_options.extend(args_given.pop(0)[1:])
                continue

            # command found if iterator didn't already stop - stop iterating
            else:
                break

        # all options popped and no command found - for case like 'jc -x'
        if len(args_given) == 0:
            self.magic_options = []
            return

        # create a dictionary of magic_commands to their respective parsers.
        magic_dict = {}
        for entry in all_parser_info():
            magic_dict.update({mc: entry['argument'] for mc in entry.get('magic_commands', [])})

        # set the command list and string
        self.magic_run_command = args_given

        if self.magic_run_command:
            try:
                # python 3.8+
                self.magic_run_command_str = shlex.join(self.magic_run_command)
            except AttributeError:
                # older python versions
                self.magic_run_command_str = ' '.join(self.magic_run_command)

        # try to get a parser for two_word_command, otherwise get one for one_word_command
        one_word_command: str = self.magic_run_command[0]
        two_word_command: str = ' '.join(self.magic_run_command[0:2])
        self.magic_found_parser = magic_dict.get(two_word_command, magic_dict.get(one_word_command))

    @staticmethod
    def open_text_file(path_string: str) -> str:
        with open(path_string, 'r') as f:
            return f.read()

    def run_user_command(self) -> None:
        """
        Use subprocess to run the user's command.
        Updates magic_stdout, magic_stderr, and magic_returncode.
        """
        if self.magic_run_command:
            proc = subprocess.Popen(
                self.magic_run_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                close_fds=False,           # Allows inheriting file descriptors
                universal_newlines=True,   # which is useful for process substitution
                encoding='UTF-8'
            )

            self.magic_stdout, self.magic_stderr = proc.communicate()
            self.magic_stdout = self.magic_stdout or '\n'
            self.magic_returncode = proc.returncode

    def do_magic(self) -> None:
        """
        Try to run the command and error if it's not found, executable, etc.

        Supports running magic commands or opening /proc files to set the
        output to magic_stdout.

        If multiple /proc files are detected, then a list of string output
        is sent to self.magic_stdout and a corresponding list of proc filenames
        is sent to self.inputlist.
        """
        if self.magic_run_command_str.startswith('/proc'):
            try:
                self.magic_found_parser = 'proc'
                filelist = shlex.split(self.magic_run_command_str)

                # multiple proc files detected
                if len(filelist) > 1:
                    self.slurp = True
                    multi_out: List[str] = []
                    self.inputlist = filelist

                    for file in self.inputlist:
                        # multi_out.append(self.open_text_file('/Users/kelly/temp' + file))
                        multi_out.append(self.open_text_file(file))

                    self.magic_stdout = multi_out

                # single proc file
                else:
                    file = filelist[0]
                    # self.magic_stdout = self.open_text_file('/Users/kelly/temp' + file)
                    self.magic_stdout = self.open_text_file(file)

            except OSError as e:
                if self.debug:
                    raise

                error_msg = os.strerror(e.errno)
                utils.error_message([
                    f'"{file}" file could not be opened: {error_msg}.'
                ])
                self.exit_error()

            except Exception:
                if self.debug:
                    raise

                utils.error_message([
                    f'"{file}" file could not be opened. For details use the -d or -dd option.'
                ])
                self.exit_error()

        elif self.magic_found_parser:
            try:
                self.run_user_command()
                if self.magic_stderr:
                    utils._safe_print(self.magic_stderr[:-1], file=sys.stderr)

            except OSError as e:
                if self.debug:
                    raise

                error_msg = os.strerror(e.errno)
                utils.error_message([
                    f'"{self.magic_run_command_str}" command could not be run: {error_msg}.'
                ])
                self.exit_error()

            except Exception:
                if self.debug:
                    raise

                utils.error_message([
                    f'"{self.magic_run_command_str}" command could not be run. For details use the -d or -dd option.'
                ])
                self.exit_error()

        elif self.magic_run_command is not None:
            utils.error_message([f'"{self.magic_run_command_str}" cannot be used with Magic syntax. Use "jc -h" for help.'])
            self.exit_error()

    def set_parser_module_and_parser_name(self) -> None:
        if self.magic_found_parser:
            self.parser_module = get_parser(self.magic_found_parser)
            self.parser_name = self.parser_shortname(self.magic_found_parser)

        else:
            found = False
            for arg in self.args:
                self.parser_name = self.parser_shortname(arg)

                if self.parser_name in parsers:
                    self.parser_module = get_parser(arg)
                    found = True
                    break

            if not found:
                utils.error_message(['Missing or incorrect arguments. Use "jc -h" for help.'])
                self.exit_error()

        if sys.stdin.isatty() and self.magic_stdout is None:
            utils.error_message(['Missing piped data. Use "jc -h" for help.'])
            self.exit_error()

    def add_metadata_to_output(self) -> None:
        """
        This function mutates self.data_out in place. If the _jc_meta field
        does not already exist, it will be created with the metadata fields. If
        the _jc_meta field already exists, the metadata fields will be added to
        the existing object.

        In the case of an empty list (no data), a dictionary with a _jc_meta
        object will be added to the list. This way you always get metadata,
        even if there are no results.
        """
        if self.run_timestamp:
            meta_obj: JSONDictType = {
                'parser': self.parser_name,
                'timestamp': self.run_timestamp.timestamp(),
                'slice_start': self.slice_start,
                'slice_end': self.slice_end
            }

            if self.magic_run_command:
                meta_obj['magic_command'] = self.magic_run_command
                meta_obj['magic_command_exit'] = self.magic_returncode

            if self.inputlist:
                meta_obj['input_list'] = self.inputlist

            if isinstance(self.data_out, dict):
                if '_jc_meta' not in self.data_out:
                    self.data_out['_jc_meta'] = {}

                self.data_out['_jc_meta'].update(meta_obj)

            elif isinstance(self.data_out, list):
                if not self.data_out:
                    self.data_out.append({})

                for item in self.data_out:
                    if isinstance(item, dict):
                        if '_jc_meta' not in item:
                            item['_jc_meta'] = {}

                        item['_jc_meta'].update(meta_obj)

            else:
                utils.error_message(['Parser returned an unsupported object type.'])
                self.exit_error()

    def slicer(self) -> None:
        """Slice input data lazily, if possible. Updates self.data_in"""
        if self.slice_str:
            slice_start_str, slice_end_str = self.slice_str.split(':', maxsplit=1)
            if slice_start_str:
                self.slice_start = int(slice_start_str)
            if slice_end_str:
                self.slice_end = int(slice_end_str)

        self.data_in = utils.line_slice(self.data_in, self.slice_start, self.slice_end)

    def create_slurp_output(self) -> None:
        """
        Slurp input into a list. If input is coming from multiple /proc files
        using magic syntax, then also add a `_file` key to the output.

        If --meta-out is used then further wrap the data in a dict like so:
            {"result": data}

        self.input_list will already exist if the data is coming from the
        /proc magic sytnax. Otherwise this funcion will build it for normal
        slurp items.

        This will allow --meta-out to add its information in a clean way.

        This method updates self.data_out
        """
        if self.parser_module and isinstance(self.data_in, (str, Iterable)):
            self.data_out = []

            # single-line string parsers
            if isinstance(self.data_in, str):
                items = self.data_in.splitlines()
                self.inputlist = []

                for line in items:
                    line = line.strip()
                    self.inputlist.append(line)
                    parsed_line = self.parser_module.parse(
                        line,
                        raw=self.raw,
                        quiet=self.quiet
                    )

                    self.data_out.append(parsed_line)

            # multiple files from /proc magic syntax
            elif isinstance(self.data_in, List) and self.inputlist:
                items = self.data_in

                for mline in zip(self.inputlist, items):
                    parsed_line = self.parser_module.parse(
                        mline[1],
                        raw=self.raw,
                        quiet=self.quiet
                    )

                    if isinstance(parsed_line, dict):
                        parsed_line.update({'_file': mline[0]})

                    elif isinstance(parsed_line, List):
                        for obj in parsed_line:
                            obj.update({'_file': mline[0]})

                    self.data_out.append(parsed_line)

            if self.meta_out:
                self.data_out = {"result": self.data_out}
                self.run_timestamp = datetime.now(timezone.utc)
                self.add_metadata_to_output()

    def create_normal_output(self) -> None:
        """standard output - updates self.data_out"""
        if self.parser_module:
            self.data_out = self.parser_module.parse(
                self.data_in,
                raw=self.raw,
                quiet=self.quiet
            )

            if self.meta_out:
                self.run_timestamp = datetime.now(timezone.utc)
                self.add_metadata_to_output()

    def streaming_parse_and_print(self) -> None:
        """only supports UTF-8 string data for now"""
        self.data_in = sys.stdin
        self.slicer()

        if self.parser_module:
            result = self.parser_module.parse(
                self.data_in,
                raw=self.raw,
                quiet=self.quiet,
                ignore_exceptions=self.ignore_exceptions
            )

            for line in result:
                self.data_out = line
                if self.meta_out:
                    self.run_timestamp = datetime.now(timezone.utc)
                    self.add_metadata_to_output()

                self.safe_print_out()

    def standard_parse_and_print(self) -> None:
        """supports binary and UTF-8 string data"""
        self.data_in = self.magic_stdout or sys.stdin.buffer.read()

        # convert to UTF-8, if possible. Otherwise, leave as bytes
        try:
            if isinstance(self.data_in, bytes):
                self.data_in = self.data_in.decode('utf-8')
        except UnicodeDecodeError:
            pass

        self.slicer()

        if self.parser_module:
            if self.slurp:
                self.create_slurp_output()
            else:
                self.create_normal_output()

            self.safe_print_out()

    def exit_clean(self) -> None:
        exit_code: int = self.magic_returncode + JC_CLEAN_EXIT
        exit_code = min(exit_code, MAX_EXIT)
        sys.exit(exit_code)

    def exit_error(self) -> None:
        exit_code: int = self.magic_returncode + JC_ERROR_EXIT
        exit_code = min(exit_code, MAX_EXIT)
        sys.exit(exit_code)

    def _run(self) -> None:
        # enable colors for Windows cmd.exe terminal
        if sys.platform.startswith('win32'):
            os.system('')

        # parse magic syntax first: e.g. jc -p ls -al
        self.args = sys.argv
        self.magic_parser()

        # add magic options to regular options
        self.options.extend(self.magic_options)

        # find options if magic_parser did not find a command
        if not self.magic_found_parser:
            for opt in self.args:
                if SLICER_RE.match(opt):
                    self.slice_str = opt

                if opt in long_options_map:
                    self.options.extend(long_options_map[opt][0])

                if opt.startswith('-') and not opt.startswith('--'):
                    self.options.extend(opt[1:])

        self.about = 'a' in self.options
        self.debug = 'd' in self.options
        self.verbose_debug = self.options.count('d') > 1
        self.force_color = 'C' in self.options
        self.help_me = 'h' in self.options
        self.show_hidden = self.options.count('h') > 1   # verbose help
        self.show_categories = self.options.count('h') > 2
        self.pretty = 'p' in self.options
        self.quiet = 'q' in self.options
        self.ignore_exceptions = self.options.count('q') > 1
        self.raw = 'r' in self.options
        self.slurp = 's' in self.options
        self.meta_out = 'M' in self.options
        self.unbuffer = 'u' in self.options
        self.version_info = 'v' in self.options
        self.yaml_output = 'y' in self.options
        self.bash_comp = 'B' in self.options
        self.zsh_comp = 'Z' in self.options

        self.set_mono()
        self.set_custom_colors()

        if self.quiet:
            utils.CLI_QUIET = True

        if self.verbose_debug:
            tracebackplus.enable(context=11)  # type: ignore

        if self.about:
            self.data_out = self.about_jc()
            self.safe_print_out()
            self.exit_clean()

        if self.help_me:
            self.help_doc()
            self.exit_clean()

        if self.version_info:
            utils._safe_print(self.versiontext())
            self.exit_clean()

        if self.bash_comp:
            utils._safe_print(bash_completion())
            self.exit_clean()

        if self.zsh_comp:
            utils._safe_print(zsh_completion())
            self.exit_clean()

        # if magic syntax used, try to run the command and set the magic attributes
        self.do_magic()

        # set parser_module and parser_name based on magic parser or user-supplied
        self.set_parser_module_and_parser_name()

        # parse and print to stdout
        if self.parser_module:
            if self.slurp and not _parser_is_slurpable(self.parser_module):
                utils.error_message([
                    f'Slurp option not available with the {self.parser_name} parser.',
                    'Use "jc -hhh" to find compatible parsers.'
                ])
                self.exit_error()

            try:
                if _parser_is_streaming(self.parser_module):
                    self.streaming_parse_and_print()
                    self.exit_clean()

                else:
                    self.standard_parse_and_print()
                    self.exit_clean()

            except BrokenPipeError:
                sys.stdout = None  # type: ignore

            except (ParseError, LibraryNotInstalled) as e:
                if self.debug:
                    raise

                utils.error_message([
                    f'Parser issue with {self.parser_name}:',
                    f'{e.__class__.__name__}: {e}',
                    'If this is the correct parser, try setting the locale to C (LC_ALL=C).',
                    f'For details use the -d or -dd option. Use "jc -h --{self.parser_name}" for help.'
                ])
                self.exit_error()

            except Exception:
                if self.debug:
                    raise

                streaming_msg = ''
                if _parser_is_streaming(self.parser_module):
                    streaming_msg = 'Use the -qq option to ignore streaming parser errors.'

                utils.error_message([
                    f'{self.parser_name} parser could not parse the input data.',
                    f'{streaming_msg}',
                    'If this is the correct parser, try setting the locale to C (LC_ALL=C).',
                    f'For details use the -d or -dd option. Use "jc -h --{self.parser_name}" for help.'
                ])
                self.exit_error()

    def run(self) -> None:
        try:
            self._run()

        except KeyboardInterrupt:
            utils.error_message(['Exit due to SIGINT.'])
            self.exit_error()

        except Exception as e:
            if self.debug:
                raise

            utils.error_message([
                'Exit due to unexpected error:',
                f'{e.__class__.__name__}: {e}'
            ])
            self.exit_error()


def main():
    JcCli().run()


if __name__ == '__main__':
    main()
