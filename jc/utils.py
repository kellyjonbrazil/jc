"""jc - JSON CLI output utility utils"""
import textwrap
import sys


def warning_message(message):
    """
    Prints a warning message for non-fatal issues

    Parameters:

        message:        (string) text of message

    Returns:

        no return, just prints output to STDERR
    """

    error_string = f'''
    jc:  Warning - {message}
    '''
    print(textwrap.dedent(error_string), file=sys.stderr)


def error_message(message):
    """
    Prints an error message for fatal issues

    Parameters:

        message:        (string) text of message

    Returns:

        no return, just prints output to STDERR
    """

    error_string = f'''
    jc:  Error - {message}
    '''
    print(textwrap.dedent(error_string), file=sys.stderr)


def compatibility(mod_name, compatible):
    """Checks for the parser's compatibility with the running OS platform.

    Parameters:

        mod_name:       (string) __name__ of the calling module

        compatible:     (list) sys.platform name(s) compatible with the parser
                        compatible options:
                        linux, darwin, cygwin, win32, aix, freebsd

    Returns:

        no return, just prints output to STDERR
    """
    platform_found = False

    for platform in compatible:
        if sys.platform.startswith(platform):
            platform_found = True
            break

    if not platform_found:
        mod = mod_name.split('.')[-1]
        compat_list = ', '.join(compatible)
        warning_message(f'{mod} parser not compatible with your OS ({sys.platform}).\n'
                        f'                   Compatible platforms: {compat_list}')


def has_data(data):
    """
    Checks if the input contains data. If there are any non-whitespace characters then return True, else return False

    Parameters:

        data:        (string) input to check whether it contains data

    Returns:

        Boolean      True if input string (data) contains non-whitespace characters, otherwise False
    """
    return True if data and not data.isspace() else False
