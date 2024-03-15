r"""jc - JSON Convert broken parser - for testing purposes only"""
import non_existent_library

class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'broken parser'
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
