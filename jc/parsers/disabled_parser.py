"""jc - JSON Convert disabled parser"""

class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'Disabled parser'
    author = 'N/A'
    author_email = 'N/A'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    hidden = True


__version__ = info.version


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> dict:
    """Main text parsing function"""
    return {}
