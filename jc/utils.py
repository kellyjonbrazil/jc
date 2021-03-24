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
                         "format":               integer,     # for debugging purposes
                         "timestamp_naive":      integer,     # timestamp based on locally configured timezone
                         "timestamp_utc":        integer      # aware timestamp only if UTC timezone detected
                     }

                     The format integer denotes which date_time format conversion succeeded.
                     The timestamp_naive integer is the converted date-time string to a naive epoch timestamp.
                     The timestamp_utc integer is the converted date-time string to an aware epoch timestamp
                         in the UTC timezone. If an aware conversion cannot be performed (e.g. the UTC timezone
                         is not found in the date-time string), then this field will be None.

                     If the conversion completely fails, None is returned instead of a Dictionary
    """
    utc_tz = False
    dt = None
    dt_utc = None
    timestamp_naive = None
    timestamp_utc = None
    timestamp_obj = {}
    utc_tz = True if 'UTC' in data else False

    formats = [
        {'id': 1, 'format': '%c', 'locale': None},  # C locale format conversion: Tue Mar 23 16:12:11 2021
        {'id': 2, 'format': '%a %d %b %Y %I:%M:%S %p %Z', 'locale': None},  # en_US.UTF-8 local format (found in upower cli output): Tue 23 Mar 2021 04:12:11 PM UTC
        {'id': 3, 'format': '%A %d %B %Y %I:%M:%S %p %Z', 'locale': None},  # European local format (found in upower cli output): Tuesday 01 October 2019 12:50:41 PM UTC
        {'id': 4, 'format': '%a %b %d %I:%M:%S %p %Z %Y', 'locale': None},  # date cli command in en_US.UTF-8 format: Wed Mar 24 06:16:19 PM UTC 2021
        {'id': 5, 'format': '%a %b %d %H:%M:%S %Z %Y', 'locale': None},  # date cli command in C locale format: Wed Mar 24 11:11:30 PDT 2021
        {'id': 6, 'format': '%c', 'locale': ''}  # locally configured locale format conversion: Could be anything :) this is a last-gasp attempt
    ]

    for fmt in formats:
        try:
            locale.setlocale(locale.LC_TIME, fmt['locale'])
            dt = datetime.strptime(data, fmt['format'])
            timestamp_naive = int(dt.replace(tzinfo=None).timestamp())
            timestamp_obj['format'] = fmt['id']
            locale.setlocale(locale.LC_TIME, None)
            break
        except Exception:
            continue

    if dt and utc_tz:
        dt_utc = dt.replace(tzinfo=timezone.utc)
        timestamp_utc = int(dt_utc.timestamp())

    if timestamp_naive:
        timestamp_obj['timestamp_naive'] = timestamp_naive
        timestamp_obj['timestamp_utc'] = timestamp_utc

    return timestamp_obj if timestamp_obj else None
