"""jc - JSON Convert exceptions"""

SHORT_MESSAGE_MAX = 300


class ParseError(Exception):
    @property
    def short_message(self) -> str:
        """
        The first line of the message, cut to 300 characters, with '...'
        added when anything was left out. Used by the CLI; `str(e)` keeps
        the full message.
        """
        msg = str(self).strip()
        first = msg.split('\n', 1)[0].rstrip('\r')
        if len(first) > SHORT_MESSAGE_MAX:
            return first[:SHORT_MESSAGE_MAX].rstrip() + '...'
        if first != msg:
            return first.rstrip() + ' ...'
        return first


class LibraryNotInstalled(Exception):
    pass
