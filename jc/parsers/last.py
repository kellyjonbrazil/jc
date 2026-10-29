r"""jc - JSON Convert `last` and `lastb` command output parser

Supports `-w`, `-F`, and `-x` options.

Calculated epoch time fields are naive (i.e. based on the local time of the
system the parser is run on) since there is no timezone information in the
`last` command output.

Usage (cli):

    $ last | jc --last

or

    $ jc last

Usage (module):

    import jc
    result = jc.parse('last', last_command_output)

Schema:

    [
      {
        "user":             string,
        "tty":              string,
        "hostname":         string,
        "login":            string,
        "logout":           string,
        "duration":         string,
        "login_epoch":      integer,  # (naive) available w/last -F option
        "logout_epoch":     integer,  # (naive) available w/last -F option
        "duration_seconds": integer   # available w/last -F option
      }
    ]

Examples:

    $ last -F | jc --last -p
    [
      {
        "user": "kbrazil",
        "tty": "ttys002",
        "hostname": null,
        "login": "Mon Dec 28 17:24:10 2020",
        "logout": "still logged in"
      },
      {
        "user": "kbrazil",
        "tty": "ttys003",
        "hostname": null,
        "login": "Mon Dec 28 17:24:10 2020",
        "logout": "Mon Dec 28 17:25:01 2020",
        "duration": "00:00",
        "login_epoch": 1565891826,
        "logout_epoch": 1565895404,
        "duration_seconds": 3578
      },
      {
        "user": "kbrazil",
        "tty": "ttys003",
        "hostname": null,
        "login": "Mon Dec 28 17:24:10 2020",
        "logout": "Mon Dec 28 17:25:01 2020",
        "duration": "00:00",
        "login_epoch": 1565891826,
        "logout_epoch": 1565895404,
        "duration_seconds": 3578
      },
      ...
    ]

    $ last | jc --last -p -r
    [
      {
        "user": "kbrazil",
        "tty": "ttys002",
        "hostname": "-",
        "login": "Thu Feb 27 14:31",
        "logout": "still_logged_in"
      },
      {
        "user": "kbrazil",
        "tty": "ttys003",
        "hostname": "-",
        "login": "Thu Feb 27 10:38",
        "logout": "10:38",
        "duration": "00:00"
      },
      {
        "user": "kbrazil",
        "tty": "ttys003",
        "hostname": "-",
        "login": "Thu Feb 27 10:18",
        "logout": "10:18",
        "duration": "00:00"
      },
      ...
    ]
"""
import re
import jc.utils

DATE_RE = re.compile(r'[MTWFS][ouerha][nedritnu] [JFMASOND][aepuco][nbrynlgptvc]')
LAST_F_DATE_RE = re.compile(r'\d\d:\d\d:\d\d \d\d\d\d')
# a console or X display such as `:0`, `:0.0` or `:pts/0:S.0`, not an IPv6
# address such as `::1` or `::ffff:203.0.113.5`
CONSOLE_HOST_RE = re.compile(r':(?!:)')
LOGIN_LOGOUT_EPOCH_RE = re.compile(r'.*\d\d:\d\d:\d\d \d\d\d\d.*')
LOGOUT_IGNORED_EVENTS = ['down', 'crash']

# util-linux login row: "%-8s %-12.12s %-16s " followed by the login time,
# the logout time and the duration. The user and hostname columns are free
# text, so the row is read from the login time at the end of the line.
_DAYS = {'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'}
_MONTHS = {'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'}
_DAY_NUM_RE = re.compile(r'\d{1,2}\Z')
_HM_RE = re.compile(r'\d\d:\d\d\Z')
_HMS_RE = re.compile(r'\d\d:\d\d:\d\d\Z')
_YEAR_RE = re.compile(r'\d{4}\Z')
_DURATION_RE = re.compile(r'\([^()\s]+\)\Z')
_LOGOUT_WORDS = (['still', 'logged', 'in'], ['gone', '-', 'no', 'logout'], ['still', 'running'])
_MAX_TAIL_WORDS = 12  # full login time, '-', full logout time, duration


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.10'
    description = '`last` and `lastb` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Enhancements by https://github.com/zerolagtime'
    compatible = ['linux', 'darwin', 'aix', 'freebsd']
    magic_commands = ['last', 'lastb']
    tags = ['command']


__version__ = info.version


class _BootTimeRow(dict):
    """A row read from the FreeBSD/macOS `boot time` line."""


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema.
    """
    for entry in proc_data:
        if isinstance(entry, _BootTimeRow) and entry.get('user') == 'boot_time':
            entry['user'] = 'boot time'

        if 'tty' in entry and entry['tty'] == '~':
            entry['tty'] = None

        if 'hostname' in entry and entry['hostname'] == '-':
            entry['hostname'] = None

        if 'hostname' in entry and entry['hostname'] is not None and CONSOLE_HOST_RE.match(entry['hostname']):
            entry['hostname'] = f'CONSOLE{entry["hostname"]}'

        if 'logout' in entry and entry['logout'] == 'still_logged_in':
            entry['logout'] = 'still logged in'

        if 'logout' in entry and entry['logout'] == 'gone_-_no_logout':
            entry['logout'] = 'gone - no logout'

        if 'login' in entry and LOGIN_LOGOUT_EPOCH_RE.match(entry['login']):
            timestamp = jc.utils.timestamp(entry['login'])
            entry['login_epoch'] = timestamp.naive

        if 'logout' in entry and LOGIN_LOGOUT_EPOCH_RE.match(entry['logout']):
            timestamp = jc.utils.timestamp(entry['logout'])
            entry['logout_epoch'] = timestamp.naive

        if 'login_epoch' in entry and 'logout_epoch' in entry:
            entry['duration_seconds'] = entry['logout_epoch'] - entry['login_epoch']

        if 'duration' in entry and re.match(r'^\d+\+', entry['duration']):
            m = re.match(r'^(?P<days>\d+)\+(?P<hours>\d\d):(?P<minutes>\d\d)', entry['duration'])
            days, hours, minutes = m.groups()
            entry['duration'] = f'{int(days)*24 + int(hours)}:{minutes}'

    return proc_data


def _time_len(words, i, full=None):
    """Number of words of the login/logout time at words[i] (4, 5 or 0)"""
    if len(words) < i + 4 or words[i] not in _DAYS or words[i + 1] not in _MONTHS \
            or not _DAY_NUM_RE.match(words[i + 2]):
        return 0

    if full is not True and _HM_RE.match(words[i + 3]):
        return 4

    if full is not False and len(words) >= i + 5 and _HMS_RE.match(words[i + 3]) \
            and _YEAR_RE.match(words[i + 4]):
        return 5

    return 0


def _is_login_tail(words):
    """True if words are a login time, logout time and duration"""
    n = _time_len(words, 0)
    if not n:
        return False

    rest = words[n:]
    if rest in _LOGOUT_WORDS:
        return True

    if rest and _DURATION_RE.match(rest[-1]):
        rest = rest[:-1]

    if len(rest) < 2 or rest[0] != '-':
        return False

    if len(rest) == 2 and (rest[1] in LOGOUT_IGNORED_EVENTS or (n == 4 and _HM_RE.match(rest[1]))):
        return True

    return n == 5 and len(rest) == 6 and _time_len(rest, 1, full=True) == 5


def _linux_columns(entry):
    """
    Split a util-linux `last` row into user, tty, hostname and the text
    from the login time on. Returns None for other layouts.
    """
    # the last words of the line with their start positions
    words = []
    end = len(entry)
    while len(words) < _MAX_TAIL_WORDS:
        while end > 0 and entry[end - 1] in ' \t':
            end -= 1
        if end == 0:
            break
        start = end
        while start > 0 and entry[start - 1] not in ' \t':
            start -= 1
        words.append((start, entry[start:end]))
        end = start
    words.reverse()

    # the rightmost login time that is followed by a valid logout part
    tail_words = [w for _, w in words]
    login_start = None
    for i in range(len(words) - 1, -1, -1):
        if _is_login_tail(tail_words[i:]):
            login_start = words[i][0]
            break

    if login_start is None or login_start < 1 or entry[login_start - 1] != ' ':
        return None

    prefix = entry[:login_start - 1]
    tail = entry[login_start:]
    length = len(prefix)

    # The hostname column is 16 wide, or wider with -w for a longer name.
    # Try that first so that spaces in the user name do not move it.
    last_word = prefix[prefix.rfind(' ') + 1:]
    host_start = length - len(last_word) if len(last_word) > 16 else length - 16
    tty_start = host_start - 13

    # a tty name has no run of spaces inside of it
    tty = prefix[tty_start:host_start - 1].rstrip(' ') if tty_start >= 9 else ''

    if tty and prefix[tty_start - 1] == ' ' and prefix[tty_start] != ' ' and '  ' not in tty \
            and prefix[host_start - 1] == ' ' \
            and (prefix[host_start] != ' ' or not prefix[host_start:].strip(' ')):
        return (prefix[:tty_start - 1].rstrip(' '), tty, prefix[host_start:].rstrip(' '), tail)

    # otherwise a user name without spaces and a long hostname with spaces
    user_end = prefix.find(' ')
    if user_end == -1:
        return None
    user_end = max(user_end, 8)
    tty_start = user_end + 1
    host_start = tty_start + 13

    if length - host_start >= 16 and prefix[user_end] == ' ' and prefix[tty_start] != ' ' \
            and prefix[host_start - 1] == ' ' and prefix[host_start] != ' ':
        return (prefix[:user_end].rstrip(' '), prefix[tty_start:host_start - 1].rstrip(' '),
                prefix[host_start:].rstrip(' '), tail)

    return None


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = []

    # Clear any blank lines
    cleandata = list(filter(None, jc.utils.splitlines(data)))

    if not jc.utils.has_data(data):
        return []

    for entry in cleandata:
        output_line = {}
        bsd_boot_time = False

        # util-linux rows: the user and hostname columns can contain spaces
        # (e.g. the user name of a failed login in lastb output)
        linux_columns = _linux_columns(entry)

        if linux_columns:
            user, tty, hostname, entry = linux_columns
            entry = entry.replace('  still logged in', '- still_logged_in')
            entry = entry.replace('  gone - no logout', '- gone_-_no_logout')
            linedata = [user, tty, hostname or '-'] + entry.split()

        else:
            if any(
                entry.startswith(f'{prefix} begins ')
                for prefix in ['wtmp', 'btmp', 'utx.log']
            ):
                continue

            entry = entry.replace('boot time', 'boot_time')
            entry = entry.replace('  still logged in', '- still_logged_in')
            entry = entry.replace('  gone - no logout', '- gone_-_no_logout')

            linedata = entry.split()

            # Adding "-" before the date part.
            if DATE_RE.match(' '.join(linedata[2:4])):
                linedata.insert(2, '-')

            # freebsd fix
            if linedata[0] == 'boot_time':
                linedata.insert(1, '-')
                linedata.insert(1, '~')
                bsd_boot_time = True

        output_line['user'] = linedata[0]

        # Fix for last -x (runlevel). Not needed when the columns were cut
        # at their positions.
        if not linux_columns:
            if output_line['user'] == 'runlevel' and  linedata[1] == '(to':
                linedata[1] += f' {linedata.pop(2)} {linedata.pop(2)}'
            elif output_line['user'] in ['reboot', 'shutdown'] and linedata[1] == 'system':  # system down\system boot
                linedata[1] += f' {linedata.pop(2)}'

        output_line['tty'] = linedata[1]
        output_line['hostname'] = linedata[2]

        # last -F support
        if LAST_F_DATE_RE.match(' '.join(linedata[6:8])):
            output_line['login'] = ' '.join(linedata[3:8])

            if len(linedata) > 9:
                if linedata[9] not in LOGOUT_IGNORED_EVENTS:
                    output_line['logout'] = ' '.join(linedata[9:14])
                else:
                    output_line['logout'] = linedata[9]
                    # add more items to the list to line up duration
                    for _ in range(4):
                        linedata.insert(10, '-')

            if len(linedata) > 14:
                output_line['duration'] = linedata[14].replace('(', '').replace(')', '')
        else: # normal last support
            output_line['login'] = ' '.join(linedata[3:7])

            if len(linedata) > 8:
                output_line['logout'] = linedata[8]

            if len(linedata) > 9:
                output_line['duration'] = linedata[9].replace('(', '').replace(')', '')

        if bsd_boot_time:
            output_line = _BootTimeRow(output_line)

        raw_output.append(output_line)

    if raw:
        return raw_output

    return _process(raw_output)
