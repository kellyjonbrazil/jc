"""jc - JSON Convert `certbot` command output parser

Supports the following `certbot` commands:

- `certbot show_account`
- `certbot certificates`

Verbose options are not supported.

Usage (cli):

    $ certbot show_account | jc --certbot
    $ certbot certificates | jc --certbot

or

    $ jc certbot show_account
    $ jc certbot certificates

Usage (module):

    import jc
    result = jc.parse('certbot', certbot_command_output)

Schema:

    {
      "certificates": [
        {
          "name":                             string,
          "serial_number":                    string,
          "key_type":                         string,
          "domains": [
                                              string
          ],
          "expiration_date":                  string,
          "expiration_date_epoch":            integer,
          "expiration_date_epoch_utc":        integer,
          "expiration_date_iso":              string,
          "validity":                         string,
          "certificate_path":                 string,
          "private_key_path":                 string
        }
      ],
      "account": {
        "server":                             string,
        "url":                                string,
        "email":                              string
      }
    }

Examples:

    $ certbot certificates | jc --certbot -p
    {
      "certificates": [
        {
          "name": "example.com",
          "serial_number": "3f7axxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
          "key_type": "RSA",
          "domains": [
            "example.com",
            "www.example.com"
          ],
          "expiration_date": "2023-05-11 01:33:10+00:00",
          "validity": "63 days",
          "certificate_path": "/etc/letsencrypt/live/example.com/chain.pem",
          "private_key_path": "/etc/letsencrypt/live/example.com/priv.pem",
          "expiration_date_epoch": 1683793990,
          "expiration_date_epoch_utc": 1683768790,
          "expiration_date_iso": "2023-05-11T01:33:10+00:00"
        },
        {
          "name": "example.org",
          "serial_number": "3bcyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy",
          "key_type": "RSA",
          "domains": [
            "example.org",
            "www.example.org"
          ],
          "expiration_date": "2023-06-12 01:35:30+00:00",
          "validity": "63 days",
          "certificate_path": "/etc/letsencrypt/live/example.org/chain.pem",
          "private_key_path": "/etc/letsencrypt/live/example.org/key.pem",
          "expiration_date_epoch": 1686558930,
          "expiration_date_epoch_utc": 1686533730,
          "expiration_date_iso": "2023-06-12T01:35:30+00:00"
        }
      ]
    }

    $ certbot certificates | jc --certbot -p -r
    {
      "certificates": [
        {
          "name": "example.com",
          "serial_number": "3f7axxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
          "key_type": "RSA",
          "domains": [
            "example.com",
            "www.example.com"
          ],
          "expiration_date": "2023-05-11 01:33:10+00:00",
          "validity": "63 days",
          "certificate_path": "/etc/letsencrypt/live/example.com/chain.pem",
          "private_key_path": "/etc/letsencrypt/live/example.com/priv.pem"
        },
        {
          "name": "example.org",
          "serial_number": "3bcyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy",
          "key_type": "RSA",
          "domains": [
            "example.org",
            "www.example.org"
          ],
          "expiration_date": "2023-06-12 01:35:30+00:00",
          "validity": "63 days",
          "certificate_path": "/etc/letsencrypt/live/example.org/chain.pem",
          "private_key_path": "/etc/letsencrypt/live/example.org/key.pem"
        }
      ]
    }

    $ certbot show_account | jc --certbot -p
    {
      "account": {
        "server": "https://acme-staging-v02.api.letsencrypt.org/directory",
        "url": "https://acme-staging-v02.api.letsencrypt.org/acme/acct/123",
        "email": "some@example.com"
      }
    }
"""
import re
from typing import List, Dict
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.2'
    description = '`certbot` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['command']
    magic_commands = ['certbot']


__version__ = info.version


def _process(proc_data: JSONDictType) -> JSONDictType:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        Dictionary. Structured to conform to the schema.
    """
    if 'certificates' in proc_data:
        for cert in proc_data['certificates']:
            if 'expiration_date' in cert:
                dt = jc.utils.timestamp(cert['expiration_date'], format_hint=(1760,))
                cert['expiration_date_epoch'] = dt.naive
                cert['expiration_date_epoch_utc'] = dt.utc
                cert['expiration_date_iso'] = dt.iso
    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> JSONDictType:
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: Dict = {}
    cert_list: List = []
    cert_dict: Dict = {}
    acct_dict: Dict = {}
    cmd_option = ''

    if jc.utils.has_data(data):

        cert_pattern = re.compile(r'^Found the following certs:\r?$', re.MULTILINE)

        if re.search(cert_pattern, data):
            cmd_option = 'certificates'
        else:
            cmd_option = 'account'

        for line in filter(None, data.splitlines()):

            if cmd_option == 'certificates':
                if line.startswith('  Certificate Name:'):
                    if cert_dict:
                        cert_list.append(cert_dict)
                        cert_dict = {}

                    cert_dict['name'] = line.split()[-1]

                if line.startswith('    Serial Number:'):
                    cert_dict['serial_number'] = line.split()[-1]

                if line.startswith('    Key Type:'):
                    cert_dict['key_type'] = line.split(': ', maxsplit=1)[1]

                if line.startswith('    Domains:'):
                    splitline = line.split(': ', maxsplit=1)[1]
                    cert_dict['domains'] = splitline.split()

                if line.startswith('    Expiry Date:'):
                    splitline = line.split(': ', maxsplit=1)[1]
                    cert_datetime = splitline.split('(')[0]
                    validity = splitline.split('(')[1]
                    cert_dict['expiration_date'] = cert_datetime.strip()
                    cert_dict['validity'] = validity[:-1].replace('VALID: ', '')

                if line.startswith('    Certificate Path:'):
                    cert_dict['certificate_path'] = line.split(': ', maxsplit=1)[1]

                if line.startswith('    Private Key Path:'):
                    cert_dict['private_key_path'] = line.split(': ', maxsplit=1)[1]

            if cmd_option == 'account':
                if line.startswith('Account details for server'):
                    acct_dict['server'] = line.split()[-1][:-1]

                if line.startswith('  Account URL:'):
                    acct_dict['url'] = line.split()[-1]

                if line.startswith('  Email contact:'):
                    acct_dict['email'] = line.split()[-1]

    if acct_dict:
        raw_output['account'] = acct_dict

    if cert_dict:
        cert_list.append(cert_dict)

    if cert_list:
        raw_output['certificates'] = cert_list

    return raw_output if raw else _process(raw_output)
