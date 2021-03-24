"""jc - JSON CLI output utility utils"""
import textwrap
import sys
import locale
from datetime import datetime, timezone


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


def parse_datetime_to_timestamp(data):
    """
    Input a date-time text string of several formats and convert to a naive or timezone-aware epoch timestamp in UTC

    Parameters:

        data:        (string) a string representation of a date-time in several supported formats

    Returns:

        Dict/None    A Dictionary of the following format:

                     {
                         "format":               integer,
                         "timestamp_naive":      integer,
                         "timestamp_utc":        integer      # aware timestamp only if UTC timezone detected
                     }

                     The format integer denotes which date_time format conversion succeeded.
                     The timestamp_naive integer is the converted date-time string to a naive epoch timestamp.
                     The timestamp_utc integer is the converted date-time string to an aware epoch timestamp
                         in the UTC timezone. If an aware conversion cannot be performed (e.g. the UTC timezone
                         is not found in the date-time string), then this field will be None.

                     If the conversion completely fails, None is returned instead of a Dictionary
    """
    found = False
    utc_tz = False
    epoch_dt = None
    epoch_dt_utc = None
    timestamp_naive = None
    timestamp_utc = None
    timestamp_obj = {}
    utc_tz = True if 'UTC' in data else False

    # Format: 1 try C locale format conversion
    # Tue Mar 23 16:12:11 2021
    if not found:
        try:
            locale.setlocale(locale.LC_TIME, None)
            epoch_dt = datetime.strptime(data, '%c')
            timestamp_naive = int(epoch_dt.replace(tzinfo=None).timestamp())
            timestamp_obj['format'] = 1
            found = True
        except Exception:
            pass

    # Format: 2 try en_US.UTF-8 local format (found in upower cli output)
    # Tue 23 Mar 2021 04:12:11 PM UTC
    if not found:
        try:
            epoch_dt = datetime.strptime(data, '%a %d %b %Y %I:%M:%S %p %Z')
            timestamp_naive = int(epoch_dt.replace(tzinfo=None).timestamp())
            timestamp_obj['format'] = 2
            found = True
        except Exception:
            pass

    # Format: 3 try date cli command in en_US.UTF-8 format
    # Wed Mar 24 06:16:19 PM UTC 2021
    if not found:
        try:
            epoch_dt = datetime.strptime(data, '%a %b %d %I:%M:%S %p %Z %Y')
            timestamp_naive = int(epoch_dt.replace(tzinfo=None).timestamp())
            timestamp_obj['format'] = 3
            found = True
        except Exception:
            pass

    # Format: 4 try date cli command in C locale format
    # Wed Mar 24 11:11:30 PDT 2021
    if not found:
        try:
            epoch_dt = datetime.strptime(data, '%a %b %d %H:%M:%S %Z %Y')
            timestamp_naive = int(epoch_dt.replace(tzinfo=None).timestamp())
            timestamp_obj['format'] = 4
            found = True
        except Exception:
            pass

    # Format: 5 try locally configured locale format conversion
    # Could be anything :) this is a last-gasp attempt
    if not found:
        try:
            locale.setlocale(locale.LC_TIME, '')
            epoch_dt = datetime.strptime(data, '%c')
            timestamp_naive = int(epoch_dt.replace(tzinfo=None).timestamp())
            locale.setlocale(locale.LC_TIME, None)
            timestamp_obj['format'] = 5
            found = True
        except Exception:
            pass

    if epoch_dt and utc_tz:
        epoch_dt_utc = epoch_dt.replace(tzinfo=timezone.utc)
        timestamp_utc = int(epoch_dt_utc.timestamp())

    if timestamp_naive:
        timestamp_obj['timestamp_naive'] = timestamp_naive
        timestamp_obj['timestamp_utc'] = timestamp_utc if timestamp_utc else None

    return timestamp_obj if timestamp_obj else None
