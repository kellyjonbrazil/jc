"""jc - JSON CLI output utility `date` command output parser

The `epoch` calculated timestamp field is naive. (i.e. based on the local time of the system the parser is run on)

The `epoch_utc` calculated timestamp field is timezone-aware and is only available if the timezone field is UTC.

Usage (cli):

    $ date | jc --date

    or

    $ jc date

Usage (module):

    import jc.parsers.date
    result = jc.parsers.date.parse(date_command_output)

Schema:

    {
      "year":               integer,
      "month":              string,
      "month_num":          integer,
      "day":                integer,
      "weekday":            string,
      "weekday_num":        integer,
      "hour":               integer,
      "hour_24":            integer,
      "minute":             integer,
      "second":             integer,
      "period":             string,
      "timezone":           string,
      "utc_offset":         string,       # null if timezone field is not UTC
      "day_of_year":        integer,
      "week_of_year":       integer,
      "iso":                string,
      "epoch":              integer,      # naive timestamp
      "epoch_utc":          integer,      # timezone-aware timestamp. Only available if timezone field is UTC
      "timezone_aware":     boolean       # if true, all fields are correctly based on UTC
    }

Examples:

    $ date | jc --date -p
    {
      "year": 2021,
      "month": "Mar",
      "month_num": 3,
      "day": 25,
      "weekday": "Thu",
      "weekday_num": 4,
      "hour": 2,
      "hour_24": 2,
      "minute": 2,
      "second": 26,
      "period": "AM",
      "timezone": "UTC",
      "utc_offset": "+0000",
      "day_of_year": 84,
      "week_of_year": 12,
      "iso": "2021-03-25T02:02:26+00:00",
      "epoch": 1616662946,
      "epoch_utc": 1616637746,
      "timezone_aware": true
    }
"""
from datetime import datetime, timezone
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '2.1'
    description = '`date` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'freebsd']
    magic_commands = ['date']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data to conform to the schema.
    """
    # no further processing
    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = {}

    if jc.utils.has_data(data):

        # find the timezone no matter where it is in the string
        # from https://www.timeanddate.com/time/zones/
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
                   'UTC', 'UTC-1200', 'UTC-1100', 'UTC-1000', 'UTC-0930', 'UTC-0900', 'UTC-0800', 'UTC-0700', 'UTC-0600',
                   'UTC-0500', 'UTC-0400', 'UTC-0300', 'UTC-0230', 'UTC-0200', 'UTC-0100', 'UTC+0000', 'UTC-0000',
                   'UTC+0100', 'UTC+0200', 'UTC+0300', 'UTC+0400', 'UTC+0430', 'UTC+0500', 'UTC+0530', 'UTC+0545',
                   'UTC+0600', 'UTC+0630', 'UTC+0700', 'UTC+0800', 'UTC+0845', 'UTC+0900', 'UTC+1000', 'UTC+1030',
                   'UTC+1100', 'UTC+1200', 'UTC+1300', 'UTC+1345', 'UTC+1400']
        tz = None
        for term in data.replace('(', '').replace(')', '').split():
            if term in tz_abbr:
                tz = term

        dt = None
        dt_utc = None

        timestamp = jc.utils.timestamp(data)
        if timestamp.naive:
            dt = datetime.fromtimestamp(timestamp.naive)
        if timestamp.utc:
            dt_utc = datetime.fromtimestamp(timestamp.utc, timezone.utc)

        if dt_utc:
            dt = dt_utc

        raw_output = {
            'year': dt.year,
            'month': dt.strftime('%b'),
            'month_num': dt.month,
            'day': dt.day,
            'weekday': dt.strftime('%a'),
            'weekday_num': dt.isoweekday(),
            'hour': int(dt.strftime('%I')),
            'hour_24': dt.hour,
            'minute': dt.minute,
            'second': dt.second,
            'period': dt.strftime('%p'),
            'timezone': tz,
            'utc_offset': dt.strftime('%z') or None,
            'day_of_year': int(dt.strftime('%j')),
            'week_of_year': int(dt.strftime('%W')),
            'iso': dt.isoformat(),
            'epoch': timestamp.naive,
            'epoch_utc': timestamp.utc,
            'timezone_aware': True if timestamp.utc else False
        }

    if raw:
        return raw_output
    else:
        return _process(raw_output)
