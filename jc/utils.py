"""jc - JSON CLI output utility utils"""
import textwrap
import sys


def warning_message(message):
    error_string = f'''
    jc:  Warning - {message}
    '''
    print(textwrap.dedent(error_string), file=sys.stderr)


def error_message(message):
    error_string = f'''
    jc:  Error - {message}
    '''
    print(textwrap.dedent(error_string), file=sys.stderr)


def compatibility(mod_name, compatible):
    """
    compatible options: linux, darwin, cygwin, win32, aix, freebsd
    """
    if sys.platform not in compatible:
        mod = mod_name.split('.')[-1]
        compat_list = ', '.join(compatible)
        warning_message(f'{mod} parser not compatible with your OS ({sys.platform}).\n         Compatible platforms: {compat_list}')
