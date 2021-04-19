"""jc - JSON CLI output utility utils"""
import sys
import re
import locale
from datetime import datetime, timezone


def warning_message(message):
    """
    Prints a warning message for non-fatal issues

    Parameters:

        message:        (string) text of message

    Returns:

        None - just prints output to STDERR
    """

    error_string = f'jc:  Warning - {message}'
    print(error_string, file=sys.stderr)


def error_message(message):
    """
    Prints an error message for fatal issues

    Parameters:

        message:        (string) text of message

    Returns:

        None - just prints output to STDERR
    """

    error_string = f'jc:  Error - {message}'
    print(error_string, file=sys.stderr)


def compatibility(mod_name, compatible):
    """Checks for the parser's compatibility with the running OS platform.

    Parameters:

        mod_name:       (string) __name__ of the calling module

        compatible:     (list) sys.platform name(s) compatible with the parser
                        compatible options:
                        linux, darwin, cygwin, win32, aix, freebsd

    Returns:

        None - just prints output to STDERR
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
                        f'               Compatible platforms: {compat_list}')


def has_data(data):
    """
    Checks if the input contains data. If there are any non-whitespace characters then return True, else return False

    Parameters:

        data:        (string) input to check whether it contains data

    Returns:

        Boolean      True if input string (data) contains non-whitespace characters, otherwise False
    """
    return True if data and not data.isspace() else False


def convert_to_int(value):
    """
    Converts string input to integer by stripping all non-numeric characters

    Parameters:

        value:          (string/integer/float) Input value

    Returns:

        integer/None    Integer if successful conversion, otherwise None
    """
    if isinstance(value, str):
        try:
            return int(re.sub(r'[^0-9\-\.]', '', value))
        except ValueError:
            try:
                return int(convert_to_float(value))
            except (ValueError, TypeError):
                return None

    elif isinstance(value, (int, float)):
        return int(value)

    else:
        return None


def convert_to_float(value):
    """
    Converts string input to float by stripping all non-numeric characters

    Parameters:

        value:          (string) Input value

    Returns:

        float/None      Float if successful conversion, otherwise None
    """
    if isinstance(value, str):
        try:
            return float(re.sub(r'[^0-9\-\.]', '', value))
        except (ValueError, TypeError):
            return None

    elif isinstance(value, (int, float)):
        return float(value)

    else:
        return None


def convert_to_bool(value):
    """
    Converts string, integer, or float input to boolean by checking for 'truthy' values

    Parameters:

        value:          (string/integer/float) Input value

    Returns:

        True/False      False unless a 'truthy' number or string is found ('y', 'yes', 'true', '1', 1, -1, etc.)
    """
    # if number, then bool it
    # if string, try to convert to float
    #   if float converts, then bool the result
    #   if float does not convert then look for truthy string and bool True
    #   else False
    truthy = ['y', 'yes', 'true']

    if isinstance(value, (int, float)):
        return bool(value)

    if isinstance(value, str):
        try:
            test_value = convert_to_float(value)
            if test_value is not None:
                return bool(test_value)
        except Exception:
            pass

        if value:
            return True if value.lower() in truthy else False

    return False


class timestamp:
    """
    Input a date-time text string of several formats and convert to a naive or timezone-aware epoch timestamp in UTC

    Parameters:

        datetime_string:    (str)   a string representation of a date-time in several supported formats

    Attributes:

        string              (str)   the input datetime string
        format              (int)   the format rule that was used to decode the datetime string
        naive               (int)   timestamp based on locally configured timezone. None if conversion fails
        utc                 (int)   aware timestamp only if UTC timezone detected in datetime string. None if conversion fails
    """

    def __init__(self, datetime_string):
        self.string = datetime_string
        dt = self._parse()
        self.format = dt['format']
        self.naive = dt['timestamp_naive']
        self.utc = dt['timestamp_utc']

    def __repr__(self):
        return f'timestamp(string="{self.string}", format={self.format}, naive={self.naive}, utc={self.utc})'

    def _parse(self):
        """
        Input a date-time text string of several formats and convert to a naive or timezone-aware epoch timestamp in UTC

        Parameters:

            data:       (string) a string representation of a date-time in several supported formats

        Returns:

            Dictionary  A Dictionary of the following format:

                {
                    "format":               integer,     # for debugging purposes. None if conversion fails
                    "timestamp_naive":      integer,     # timestamp based on locally configured timezone. None if conversion fails
                    "timestamp_utc":        integer      # aware timestamp only if UTC timezone detected. None if conversion fails
                }

                The format integer denotes which date_time format conversion succeeded.
                The timestamp_naive integer is the converted date-time string to a naive epoch timestamp.
                The timestamp_utc integer is the converted date-time string to an aware epoch timestamp
                    in the UTC timezone. If an aware conversion cannot be performed (e.g. the UTC timezone
                    is not found in the date-time string), then this field will be None.

                If the conversion completely fails, all fields will be None.
        """
        data = self.string or ''
        normalized_datetime = ''
        utc_tz = False
        dt = None
        dt_utc = None
        timestamp_naive = None
        timestamp_utc = None
        timestamp_obj = {
            'format': None,
            'timestamp_naive': None,
            'timestamp_utc': None
        }
        utc_tz = False

        if 'UTC' in data:
            utc_tz = True
            if 'UTC+' in data or 'UTC-' in data:
                if 'UTC+0000' in data or 'UTC-0000' in data:
                    utc_tz = True
                else:
                    utc_tz = False
        elif '+0000' in data or '-0000' in data:
            utc_tz = True

        formats = [
            {'id': 1000, 'format': '%a %b %d %H:%M:%S %Y', 'locale': None},  # manual C locale format conversion: Tue Mar 23 16:12:11 2021 or Tue Mar 23 16:12:11 IST 2021
            {'id': 1500, 'format': '%Y-%m-%d %H:%M', 'locale': None},  # en_US.UTF-8 local format (found in who cli output): 2021-03-23 00:14
            {'id': 1600, 'format': '%m/%d/%Y %I:%M %p', 'locale': None},  # Windows english format (found in dir cli output): 12/07/2019 02:09 AM
            {'id': 1700, 'format': '%m/%d/%Y, %I:%M:%S %p', 'locale': None},  # Windows english format wint non-UTC tz (found in systeminfo cli output): 3/22/2021, 1:15:51 PM (UTC-0600)
            {'id': 1710, 'format': '%m/%d/%Y, %I:%M:%S %p UTC%z', 'locale': None},  # Windows english format with UTC tz (found in systeminfo cli output): 3/22/2021, 1:15:51 PM (UTC+0000)
            {'id': 2000, 'format': '%a %d %b %Y %I:%M:%S %p %Z', 'locale': None},  # en_US.UTF-8 local format (found in upower cli output): Tue 23 Mar 2021 04:12:11 PM UTC
            {'id': 3000, 'format': '%a %d %b %Y %I:%M:%S %p', 'locale': None},  # en_US.UTF-8 local format with non-UTC tz (found in upower cli output): Tue 23 Mar 2021 04:12:11 PM IST
            {'id': 4000, 'format': '%A %d %B %Y %I:%M:%S %p %Z', 'locale': None},  # European-style local format (found in upower cli output): Tuesday 01 October 2019 12:50:41 PM UTC
            {'id': 5000, 'format': '%A %d %B %Y %I:%M:%S %p', 'locale': None},  # European-style local format with non-UTC tz (found in upower cli output): Tuesday 01 October 2019 12:50:41 PM IST
            {'id': 6000, 'format': '%a %b %d %I:%M:%S %p %Z %Y', 'locale': None},  # en_US.UTF-8 format (found in date cli): Wed Mar 24 06:16:19 PM UTC 2021
            {'id': 7000, 'format': '%a %b %d %H:%M:%S %Z %Y', 'locale': None},  # C locale format (found in date cli): Wed Mar 24 11:11:30 UTC 2021
            {'id': 7100, 'format': '%b %d %H:%M:%S %Y', 'locale': None},  # C locale format (found in stat cli output - osx): # Mar 29 11:49:05 2021
            {'id': 7200, 'format': '%Y-%m-%d %H:%M:%S.%f %z', 'locale': None},  # C locale format (found in stat cli output - linux): 2019-08-13 18:13:43.555604315 -0400
            {'id': 7300, 'format': '%a %Y-%m-%d %H:%M:%S %Z', 'locale': None},  # C locale format (found in timedatectl cli output): # Wed 2020-03-11 00:53:21 UTC
            # attempt locale changes last
            {'id': 8000, 'format': '%a %d %b %Y %H:%M:%S %Z', 'locale': ''},  # current locale format (found in upower cli output): # mar. 23 mars 2021 23:12:11 UTC
            {'id': 8100, 'format': '%a %d %b %Y %H:%M:%S', 'locale': ''},  # current locale format with non-UTC tz (found in upower cli output): # mar. 23 mars 2021 19:12:11 EDT
            {'id': 8200, 'format': '%A %d %B %Y, %H:%M:%S UTC%z', 'locale': ''},  # fr_FR.utf8 locale format (found in date cli output): vendredi 26 mars 2021, 13:26:46 (UTC+0000)
            {'id': 8300, 'format': '%A %d %B %Y, %H:%M:%S', 'locale': ''},  # fr_FR.utf8 locale format with non-UTC tz (found in date cli output): vendredi 26 mars 2021, 13:26:46 (UTC-0400)
            {'id': 9000, 'format': '%c', 'locale': ''}  # locally configured locale format conversion: Could be anything :) this is a last-gasp attempt
        ]

        # from https://www.timeanddate.com/time/zones/
        # only removed UTC timezone and added known non-UTC offsets
        tz_abbr = ['A', 'ACDT', 'ACST', 'ACT', 'ACWST', 'ADT', 'AEDT', 'AEST', 'AET', 'AFT', 'AKDT', 'AKST', 'ALMT',
                   'AMST', 'AMT', 'ANAST', 'ANAT', 'AQTT', 'ART', 'AST', 'AT', 'AWDT', 'AWST', 'AZOST', 'AZOT',
                   'AZST', 'AZT', 'AoE', 'B', 'BNT', 'BOT', 'BRST', 'BRT', 'BST', 'BTT', 'C', 'CAST', 'CAT', 'CCT',
                   'CDT', 'CEST', 'CET', 'CHADT', 'CHAST', 'CHOST', 'CHOT', 'CHUT', 'CIDST', 'CIST', 'CKT', 'CLST',
                   'CLT', 'COT', 'CST', 'CT', 'CVT', 'CXT', 'ChST', 'D', 'DAVT', 'DDUT', 'E', 'EASST', 'EAST',
                   'EAT', 'ECT', 'EDT', 'EEST', 'EET', 'EGST', 'EGT', 'EST', 'ET', 'F', 'FET', 'FJST', 'FJT', 'FKST',
                   'FKT', 'FNT', 'G', 'GALT', 'GAMT', 'GET', 'GFT', 'GILT', 'GMT', 'GST', 'GYT', 'H', 'HDT', 'HKT',
                   'HOVST', 'HOVT', 'HST', 'I', 'ICT', 'IDT', 'IOT', 'IRDT', 'IRKST', 'IRKT', 'IRST', 'IST', 'JST',
                   'K', 'KGT', 'KOST', 'KRAST', 'KRAT', 'KST', 'KUYT', 'L', 'LHDT', 'LHST', 'LINT', 'M', 'MAGST',
                   'MAGT', 'MART', 'MAWT', 'MDT', 'MHT', 'MMT', 'MSD', 'MSK', 'MST', 'MT', 'MUT', 'MVT', 'MYT', 'N',
                   'NCT', 'NDT', 'NFDT', 'NFT', 'NOVST', 'NOVT', 'NPT', 'NRT', 'NST', 'NUT', 'NZDT', 'NZST', 'O',
                   'OMSST', 'OMST', 'ORAT', 'P', 'PDT', 'PET', 'PETST', 'PETT', 'PGT', 'PHOT', 'PHT', 'PKT', 'PMDT',
                   'PMST', 'PONT', 'PST', 'PT', 'PWT', 'PYST', 'PYT', 'Q', 'QYZT', 'R', 'RET', 'ROTT', 'S', 'SAKT',
                   'SAMT', 'SAST', 'SBT', 'SCT', 'SGT', 'SRET', 'SRT', 'SST', 'SYOT', 'T', 'TAHT', 'TFT', 'TJT', 'TKT',
                   'TLT', 'TMT', 'TOST', 'TOT', 'TRT', 'TVT', 'U', 'ULAST', 'ULAT', 'UYST', 'UYT', 'UZT', 'V', 'VET',
                   'VLAST', 'VLAT', 'VOST', 'VUT', 'W', 'WAKT', 'WARST', 'WAST', 'WAT', 'WEST', 'WET', 'WFT', 'WGST',
                   'WGT', 'WIB', 'WIT', 'WITA', 'WST', 'WT', 'X', 'Y', 'YAKST', 'YAKT', 'YAPT', 'YEKST', 'YEKT', 'Z',
                   'UTC-1200', 'UTC-1100', 'UTC-1000', 'UTC-0930', 'UTC-0900', 'UTC-0800', 'UTC-0700', 'UTC-0600',
                   'UTC-0500', 'UTC-0400', 'UTC-0300', 'UTC-0230', 'UTC-0200', 'UTC-0100', 'UTC+0100', 'UTC+0200',
                   'UTC+0300', 'UTC+0400', 'UTC+0430', 'UTC+0500', 'UTC+0530', 'UTC+0545', 'UTC+0600', 'UTC+0630',
                   'UTC+0700', 'UTC+0800', 'UTC+0845', 'UTC+0900', 'UTC+1000', 'UTC+1030', 'UTC+1100', 'UTC+1200',
                   'UTC+1300', 'UTC+1345', 'UTC+1400']

        # normalize the timezone by taking out any timezone reference, except UTC
        cleandata = data.replace('(', '').replace(')', '')
        normalized_datetime_list = []
        for term in cleandata.split():
            if term not in tz_abbr:
                normalized_datetime_list.append(term)

        normalized_datetime = ' '.join(normalized_datetime_list)

        # normalize further by converting any greater-than 6-digit subsecond to 6-digits
        p = re.compile(r'(\W\d\d:\d\d:\d\d\.\d{6})\d+\W')
        normalized_datetime = p.sub(r'\g<1> ', normalized_datetime)

        for fmt in formats:
            try:
                locale.setlocale(locale.LC_TIME, fmt['locale'])
                dt = datetime.strptime(normalized_datetime, fmt['format'])
                timestamp_naive = int(dt.replace(tzinfo=None).timestamp())
                timestamp_obj['format'] = fmt['id']
                locale.setlocale(locale.LC_TIME, None)
                break
            except Exception:
                locale.setlocale(locale.LC_TIME, None)
                continue

        if dt and utc_tz:
            dt_utc = dt.replace(tzinfo=timezone.utc)
            timestamp_utc = int(dt_utc.timestamp())

        if timestamp_naive:
            timestamp_obj['timestamp_naive'] = timestamp_naive
            timestamp_obj['timestamp_utc'] = timestamp_utc

        return timestamp_obj
