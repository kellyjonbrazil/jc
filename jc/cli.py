"""jc - JSON Convert
JC cli module
"""

import io
import sys
import os
from datetime import datetime, timezone
import textwrap
import signal
import shlex
import subprocess
from typing import List, Dict
from .lib import (__version__, parser_info, all_parser_info, parsers,
                  _get_parser, _parser_is_streaming, parser_mod_list,
                  standard_parser_mod_list, plugin_parser_mod_list,
                  streaming_parser_mod_list)
from . import utils
from .cli_data import long_options_map, new_pygments_colors, old_pygments_colors
from .shell_completions import bash_completion, zsh_completion
from . import tracebackplus
from .exceptions import LibraryNotInstalled, ParseError

# make pygments import optional
try:
    import pygments
    from pygments import highlight
    from pygments.style import Style
    from pygments.token import (Name, Number, String, Keyword)
    from pygments.lexers.data import JsonLexer, YamlLexer
    from pygments.formatters import Terminal256Formatter
    PYGMENTS_INSTALLED = True
except Exception:
    PYGMENTS_INSTALLED = False


class info():
    version = __version__
    description = 'JSON Convert'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    website = 'https://github.com/kellyjonbrazil/jc'
    copyright = '© 2019-2022 Kelly Brazil'
    license = 'MIT License'


# We only support 2.3.0+, pygments changed color names in 2.4.0.
# startswith is sufficient and avoids potential exceptions from split and int.
if PYGMENTS_INSTALLED:
    if pygments.__version__.startswith('2.3.'):
        PYGMENT_COLOR = old_pygments_colors
    else:
        PYGMENT_COLOR = new_pygments_colors


class JcCli():

    def __init__(self) -> None:
        self.data_in = None
        self.data_out = None
        self.options: List[str] = []
        self.args: List[str] = []
        self.parser_module = None
        self.parser_name = None
        self.indent = 0
        self.pad = 0
        self.env_colors = None
        self.custom_colors: Dict = {}
        self.show_hidden = False
        self.ascii_only = False
        self.flush = False
        self.json_separators = (',', ':')
        self.json_indent = None
        self.path_string = None
        self.jc_exit = 0
        self.JC_ERROR_EXIT = 100
        self.exit_code = 0
        self.run_timestamp = None

        # cli options
        self.about = False
        self.debug = False
        self.verbose_debug = False
        self.force_color = False
        self.mono = False
        self.help_me = False
        self.pretty = False
        self.quiet = False
        self.ignore_exceptions = False
        self.raw = False
        self.meta_out = False
        self.unbuffer = False
        self.version_info = False
        self.yaml_output = False
        self.bash_comp = False
        self.zsh_comp = False

        # magic attributes
        self.magic_found_parser = None
        self.magic_options: List[str] = []
        self.magic_run_command = None
        self.magic_run_command_str = ''
        self.magic_stdout = None
        self.magic_stderr = None
        self.magic_returncode = 0


    def set_custom_colors(self):
        """
        Sets the custom_colors dictionary to be used in Pygments custom style class.

        Grab custom colors from JC_COLORS environment variable. JC_COLORS env
        variable takes 4 comma separated string values and should be in the
        format of:

        JC_COLORS=<keyname_color>,<keyword_color>,<number_color>,<string_color>

        Where colors are: black, red, green, yellow, blue, magenta, cyan, gray,
                        brightblack, brightred, brightgreen, brightyellow,
                        brightblue, brightmagenta, brightcyan, white, default

        Default colors:

            JC_COLORS=blue,brightblack,magenta,green
        or
            JC_COLORS=default,default,default,default
        """
        input_error = False

        if self.env_colors:
            color_list = self.env_colors.split(',')
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

    def set_mono(self):
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
    def parser_shortname(parser_arg):
        """Return short name of the parser with dashes and no -- prefix"""
        return parser_arg[2:]

    def parsers_text(self):
        """Return the argument and description information from each parser"""
        ptext = ''
        padding_char = ' '
        for p in all_parser_info(show_hidden=self.show_hidden):
            parser_arg = p.get('argument', 'UNKNOWN')
            padding = self.pad - len(parser_arg)
            parser_desc = p.get('description', 'No description available.')
            indent_text = padding_char * self.indent
            padding_text = padding_char * padding
            ptext += indent_text + parser_arg + padding_text + parser_desc + '\n'

        return ptext

    def options_text(self):
        """Return the argument and description information from each option"""
        otext = ''
        padding_char = ' '
        for option in long_options_map:
            o_short = '-' + long_options_map[option][0]
            o_desc = long_options_map[option][1]
            o_combined = o_short + ',  ' + option
            padding = self.pad - len(o_combined)
            indent_text = padding_char * self.indent
            padding_text = padding_char * padding
            otext += indent_text + o_combined + padding_text + o_desc + '\n'

        return otext

    @staticmethod
    def about_jc():
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
            'parser_count': len(parser_mod_list()),
            'standard_parser_count': len(standard_parser_mod_list()),
            'streaming_parser_count': len(streaming_parser_mod_list()),
            'plugin_parser_count': len(plugin_parser_mod_list()),
            'parsers': all_parser_info(show_hidden=True)
        }

    def helptext(self):
        """Return the help text with the list of parsers"""
        self.indent = 4
        self.pad = 20
        parsers_string = self.parsers_text()
        options_string = self.options_text()

        helptext_string = f'''\
jc converts the output of many commands, file-types, and strings to JSON or YAML

Usage:

    Standard syntax:

        COMMAND | jc [OPTIONS] PARSER

        cat FILE | jc [OPTIONS] PARSER

        echo STRING | jc [OPTIONS] PARSER

    Magic syntax:

        jc [OPTIONS] COMMAND

        jc [OPTIONS] /proc/<path-to-procfile>

Parsers:
{parsers_string}
Options:
{options_string}
Examples:
    Standard Syntax:
        $ dig www.google.com | jc --pretty --dig
        $ cat /proc/meminfo | jc --pretty --proc

    Magic Syntax:
        $ jc --pretty dig www.google.com
        $ jc --pretty /proc/meminfo

    Parser Documentation:
        $ jc --help --dig

    Show Hidden Parsers:
        $ jc -hh
'''

        return helptext_string

    def help_doc(self):
        """
        Returns the parser documentation if a parser is found in the arguments,
        otherwise the general help text is returned.
        """
        for arg in self.args:
            parser_name = self.parser_shortname(arg)

            if parser_name in parsers:
                p_info = parser_info(parser_name, documentation=True)
                compatible = ', '.join(p_info.get('compatible', ['unknown']))
                docs = p_info.get('documentation', 'No documentation available.')
                version = p_info.get('version', 'unknown')
                author = p_info.get('author', 'unknown')
                author_email = p_info.get('author_email', 'unknown')
                doc_text = \
                    f'{docs}\n'\
                    f'Compatibility:  {compatible}\n\n'\
                    f'Version {version} by {author} ({author_email})\n'

                utils._safe_pager(doc_text)
                return

        utils._safe_print(self.helptext())
        return

    @staticmethod
    def versiontext():
        """Return the version text"""
        py_ver = '.'.join((str(sys.version_info.major), str(sys.version_info.minor), str(sys.version_info.micro)))
        versiontext_string = f'''\
        jc version:  {info.version}
        python interpreter version:  {py_ver}
        python path:  {sys.executable}

        {info.website}
        {info.copyright}
        '''
        return textwrap.dedent(versiontext_string)


    def yaml_out(self):
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
            YAML.official_plug_ins = lambda a: []

            # monkey patch to disable aliases
            representer.RoundTripRepresenter.ignore_aliases = lambda x, y: True

            yaml = YAML()
            yaml.default_flow_style = False
            yaml.explicit_start = True
            yaml.allow_unicode = not self.ascii_only
            yaml.encoding = 'utf-8'
            yaml.dump(self.data_out, y_string_buf)
            y_string = y_string_buf.getvalue().decode('utf-8')[:-1]

            if not self.mono:
                # set colors
                class JcStyle(Style):
                    styles = self.custom_colors

                return str(highlight(y_string, YamlLexer(), Terminal256Formatter(style=JcStyle))[0:-1])

            return y_string

        utils.warning_message(['YAML Library not installed. Reverting to JSON output.'])
        return self.json_out()

    def json_out(self):
        """
        Return a JSON formatted string. String may include color codes or be
        pretty printed.
        """
        import json

        if self.pretty:
            self.json_indent = 2
            self.json_separators = None

        j_string = json.dumps(self.data_out,
                              indent=self.json_indent,
                              separators=self.json_separators,
                              ensure_ascii=self.ascii_only)

        if not self.mono:
            # set colors
            class JcStyle(Style):
                styles = self.custom_colors

            return str(highlight(j_string, JsonLexer(), Terminal256Formatter(style=JcStyle))[0:-1])

        return j_string

    def safe_print_out(self):
        """Safely prints JSON or YAML output in both UTF-8 and ASCII systems"""
        if self.yaml_output:
            try:
                print(self.yaml_out(), flush=self.flush)
            except UnicodeEncodeError:
                self.ascii_only = True
                print(self.yaml_out(), flush=self.flush)

        else:
            try:
                print(self.json_out(), flush=self.flush)
            except UnicodeEncodeError:
                self.ascii_only = True
                print(self.json_out(), flush=self.flush)

    def magic_parser(self):
        """
        Parse command arguments for magic syntax: `jc -p ls -al` and set the
        magic attributes.
        """
        # bail immediately if there are no args or a parser is defined
        if len(self.args) <= 1 or (self.args[1].startswith('--') and self.args[1] not in long_options_map):
            return

        args_given = self.args[1:]

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

            # option found - populate option list
            if arg.startswith('-'):
                self.magic_options.extend(args_given.pop(0)[1:])
                continue

            # command found if iterator didn't already stop - stop iterating
            else:
                break

        # if -h, -a, or -v found in options, then clear options and bail out
        if 'h' in self.magic_options or 'a' in self.magic_options or 'v' in self.magic_options:
            self.magic_options = []
            return

        # all options popped and no command found - for case like 'jc -x'
        if len(args_given) == 0:
            return

        # create a dictionary of magic_commands to their respective parsers.
        magic_dict = {}
        for entry in all_parser_info():
            magic_dict.update({mc: entry['argument'] for mc in entry.get('magic_commands', [])})

        # find the command and parser
        self.magic_run_command = args_given
        one_word_command = args_given[0]
        two_word_command = ' '.join(args_given[0:2])

        # try to get a parser for two_word_command, otherwise get one for one_word_command
        self.magic_found_parser = magic_dict.get(two_word_command, magic_dict.get(one_word_command))

    def open_text_file(self):
        with open(self.path_string, 'r') as f:
            return f.read()

    def run_user_command(self):
        """
        Use subprocess to run the user's command. Returns the STDOUT, STDERR,
        and the Exit Code as a tuple.
        """
        proc = subprocess.Popen(self.magic_run_command,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                close_fds=False,            # Allows inheriting file descriptors;
                                universal_newlines=True,    #     useful for process substitution
                                encoding='UTF-8')
        self.magic_stdout, self.magic_stderr = proc.communicate()

        self.magic_stdout = self.magic_stdout or '\n'
        self.magic_returncode = proc.returncode

    def combined_exit_code(self):
        self.exit_code = self.magic_returncode + self.jc_exit
        self.exit_code = min(self.exit_code, 255)

    def add_metadata_to_output(self):
        """
        This function mutates a list or dict in place. If the _jc_meta field
        does not already exist, it will be created with the metadata fields. If
        the _jc_meta field already exists, the metadata fields will be added to
        the existing object.

        In the case of an empty list (no data), a dictionary with a _jc_meta
        object will be added to the list. This way you always get metadata,
        even if there are no results.
        """
        meta_obj = {
            'parser': self.parser_name,
            'timestamp': self.run_timestamp.timestamp()
        }

        if self.magic_run_command:
            meta_obj['magic_command'] = self.magic_run_command
            meta_obj['magic_command_exit'] = self.magic_returncode

        if isinstance(self.data_out, dict):
            if '_jc_meta' not in self.data_out:
                self.data_out['_jc_meta'] = {}

            self.data_out['_jc_meta'].update(meta_obj)

        elif isinstance(self.data_out, list):
            if not self.data_out:
                self.data_out.append({})

            for item in self.data_out:
                if '_jc_meta' not in item:
                    item['_jc_meta'] = {}

                item['_jc_meta'].update(meta_obj)

        else:
            utils.error_message(['Parser returned an unsupported object type.'])
            self.jc_exit = self.JC_ERROR_EXIT
            sys.exit(self.combined_exit_code())

    def ctrlc(self, signum, frame):
            """Exit with error on SIGINT"""
            sys.exit(self.JC_ERROR_EXIT)

    def run(self):
        # break on ctrl-c keyboard interrupt
        signal.signal(signal.SIGINT, self.ctrlc)

        # break on pipe error. need try/except for windows compatibility
        try:
            signal.signal(signal.SIGPIPE, signal.SIG_DFL)
        except AttributeError:
            pass

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
                if opt in long_options_map:
                    self.options.extend(long_options_map[opt][0])

                if opt.startswith('-') and not opt.startswith('--'):
                    self.options.extend(opt[1:])

        self.env_colors = os.getenv('JC_COLORS')

        self.about = 'a' in self.options
        self.debug = 'd' in self.options
        self.verbose_debug = self.options.count('d') > 1
        self.force_color = 'C' in self.options
        self.help_me = 'h' in self.options
        self.show_hidden = self.options.count('h') > 1   # verbose help
        self.pretty = 'p' in self.options
        self.quiet = 'q' in self.options
        self.ignore_exceptions = self.options.count('q') > 1
        self.raw = 'r' in self.options
        self.meta_out = 'M' in self.options
        self.unbuffer = 'u' in self.options
        self.version_info = 'v' in self.options
        self.yaml_output = 'y' in self.options
        self.bash_comp = 'B' in self.options
        self.zsh_comp = 'Z' in self.options

        self.set_mono()
        self.set_custom_colors()

        if self.verbose_debug:
            tracebackplus.enable(context=11)

        if self.about:
            self.data_out = self.about_jc()
            self.safe_print_out()
            sys.exit(0)

        if self.help_me:
            self.help_doc()
            sys.exit(0)

        if self.version_info:
            utils._safe_print(self.versiontext())
            sys.exit(0)

        if self.bash_comp:
            utils._safe_print(bash_completion())
            sys.exit(0)

        if self.zsh_comp:
            utils._safe_print(zsh_completion())
            sys.exit(0)

        # if magic syntax used, try to run the command and error if it's not found, etc.
        if self.magic_run_command:
            try:
                self.magic_run_command_str = shlex.join(self.magic_run_command)      # python 3.8+
            except AttributeError:
                self.magic_run_command_str = ' '.join(self.magic_run_command)        # older python versions

        if self.magic_run_command_str.startswith('/proc'):
            try:
                self.magic_found_parser = 'proc'
                self.magic_stdout = self.open_text_file()

            except OSError as e:
                if self.debug:
                    raise

                error_msg = os.strerror(e.errno)
                utils.error_message([
                    f'"{self.magic_run_command_str}" file could not be opened: {error_msg}.'
                ])
                self.jc_exit = self.JC_ERROR_EXIT
                sys.exit(self.combined_exit_code())

            except Exception:
                if self.debug:
                    raise

                utils.error_message([
                    f'"{self.magic_run_command_str}" file could not be opened. For details use the -d or -dd option.'
                ])
                self.jc_exit = self.JC_ERROR_EXIT
                sys.exit(self.combined_exit_code())

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
                self.jc_exit = self.JC_ERROR_EXIT
                sys.exit(self.combined_exit_code())

            except Exception:
                if self.debug:
                    raise

                utils.error_message([
                    f'"{self.magic_run_command_str}" command could not be run. For details use the -d or -dd option.'
                ])
                self.jc_exit = self.JC_ERROR_EXIT
                sys.exit(self.combined_exit_code())

        elif self.magic_run_command is not None:
            utils.error_message([f'"{self.magic_run_command_str}" cannot be used with Magic syntax. Use "jc -h" for help.'])
            sys.exit(self.combined_exit_code())

        # find the correct parser
        if self.magic_found_parser:
            self.parser_module = _get_parser(self.magic_found_parser)
            self.parser_name = self.parser_shortname(self.magic_found_parser)

        else:
            found = False
            for arg in self.args:
                self.parser_name = self.parser_shortname(arg)

                if self.parser_name in parsers:
                    self.parser_module = _get_parser(arg)
                    found = True
                    break

            if not found:
                utils.error_message(['Missing or incorrect arguments. Use "jc -h" for help.'])
                self.jc_exit = self.JC_ERROR_EXIT
                sys.exit(self.combined_exit_code())

        if sys.stdin.isatty() and self.magic_stdout is None:
            utils.error_message(['Missing piped data. Use "jc -h" for help.'])
            self.jc_exit = self.JC_ERROR_EXIT
            sys.exit(self.combined_exit_code())

        # parse and print to stdout
        try:
            # differentiate between regular and streaming parsers

            # streaming (only supports UTF-8 string data for now)
            if _parser_is_streaming(self.parser_module):
                self.data_in = sys.stdin
                result = self.parser_module.parse(self.data_in,
                                                  raw=self.raw,
                                                  quiet=self.quiet,
                                                  ignore_exceptions=self.ignore_exceptions)

                for line in result:
                    self.data_out = line
                    if self.meta_out:
                        self.run_timestamp = datetime.now(timezone.utc)
                        self.add_metadata_to_output()

                    self.safe_print_out()

                sys.exit(self.combined_exit_code())

            # regular (supports binary and UTF-8 string data)
            else:
                self.data_in = self.magic_stdout or sys.stdin.buffer.read()

                # convert to UTF-8, if possible. Otherwise, leave as bytes
                try:
                    if isinstance(self.data_in, bytes):
                        self.data_in = self.data_in.decode('utf-8')
                except UnicodeDecodeError:
                    pass

                self.data_out = self.parser_module.parse(self.data_in,
                                                         raw=self.raw,
                                                         quiet=self.quiet)

                if self.meta_out:
                    self.run_timestamp = datetime.now(timezone.utc)
                    self.add_metadata_to_output()

                self.safe_print_out()

            sys.exit(self.combined_exit_code())

        except (ParseError, LibraryNotInstalled) as e:
            if self.debug:
                raise

            utils.error_message([
                f'Parser issue with {self.parser_name}:', f'{e.__class__.__name__}: {e}',
                'If this is the correct parser, try setting the locale to C (LC_ALL=C).',
                f'For details use the -d or -dd option. Use "jc -h --{self.parser_name}" for help.'
            ])
            self.jc_exit = self.JC_ERROR_EXIT
            sys.exit(self.combined_exit_code())

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
            self.jc_exit = self.JC_ERROR_EXIT
            sys.exit(self.combined_exit_code())


def main():
    JcCli().run()


if __name__ == '__main__':
    main()
