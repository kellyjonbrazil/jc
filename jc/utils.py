"""jc - JSON CLI output utility utils"""
import textwrap
import sys


def warning_message(message):
    """Prints a warning message for non-fatal issues"""

    error_string = f'''
    jc:  Warning - {message}
    '''
    print(textwrap.dedent(error_string), file=sys.stderr)


def error_message(message):
    """Prints an error message for fatal issues"""
    
    error_string = f'''
    jc:  Error - {message}
    '''
    print(textwrap.dedent(error_string), file=sys.stderr)


def compatibility(mod_name, compatible):
    """Checks for the parser's compatibility with the running OS platform.
    
    Arguments:

        mod_name        (string) __name__ of the calling module
        compatible      (list) sys.platform name(s) compatible with the parser
                        compatible options: 
                        linux, darwin, cygwin, win32, aix, freebsd
    """
    if sys.platform not in compatible:
        mod = mod_name.split('.')[-1]
        compat_list = ', '.join(compatible)
        warning_message(f'{mod} parser not compatible with your OS ({sys.platform}).\n         Compatible platforms: {compat_list}')
