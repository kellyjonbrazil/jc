"""jc - JSON CLI output utility utils"""
import textwrap
import sys


def ctrlc(signum, frame):
    exit()


def helptext(message):
    helptext_string = f'''
    jc:     {message}

    Usage:  jc PARSER [OPTIONS]

    Parsers:
            --arp        arp parser
            --df         df parser
            --dig        dig parser
            --env        env parser
            --free       free parser
            --history    history parser
            --ifconfig   iconfig parser
            --iptables   iptables parser
            --jobs       jobs parser
            --ls         ls parser
            --lsblk      lsblk parser
            --lsmod      lsmod parser
            --lsof       lsof parser
            --mount      mount parser
            --netstat    netstat parser
            --ps         ps parser
            --route      route parser
            --uname      uname parser
            --uptime     uptime parser
            --w          w parser

    Options:
            -p           pretty print output
            -q           quiet - suppress warnings
            -r           raw JSON output

    Example:
            ls -al | jc --ls -p
    '''

    print(textwrap.dedent(helptext_string), file=sys.stderr)


def error_message(message):
    error_string = f'''
    jc:  {message}
    '''

    print(textwrap.dedent(error_string), file=sys.stderr)


def compatibility(mod_name, compatible):
    '''
    compatible options: linux, darwin, cygwin, win32, aix, freebsd
    '''
    if sys.platform not in compatible:
        mod = mod_name.split('.')[-1]
        compat_list = ', '.join(compatible)
        error_message(f'Warning - {mod} parser not compatible with your OS ({sys.platform}).\n         Compatible platforms: {compat_list}')
