r"""jc - JSON Convert X.509 Certificate Request format file parser

This parser will convert DER and PEM encoded X.509 certificate request files.

Usage (cli):

    $ cat certificateRequest.pem | jc --x509-csr

Usage (module):

    import jc
    result = jc.parse('x509_csr', x509_csr_file_output)

Schema:

    [
      {
        "certification_request_info": {
          "version":                      string,
          "serial_number":                string,  # [0]
          "serial_number_str":            string,
          "signature": {
            "algorithm":                  string,
            "parameters":                 string/null,
          },
          "issuer": {
            "country_name":               string,
            "state_or_province_name"      string,
            "locality_name":              string,
            "organization_name":          array/string,
            "organizational_unit_name":   array/string,
            "common_name":                string,
            "email_address":              string,
            "serial_number":              string,   # [0]
            "serial_number_str":          string
          },
          "validity": {
            "not_before":                 integer,  # [1]
            "not_after":                  integer,  # [1]
            "not_before_iso":             string,
            "not_after_iso":              string
          },
          "subject": {
            "country_name":               string,
            "state_or_province_name":     string,
            "locality_name":              string,
            "organization_name":          array/string,
            "organizational_unit_name":   array/string,
            "common_name":                string,
            "email_address":              string,
            "serial_number":              string,   # [0]
            "serial_number_str":          string
          },
          "subject_public_key_info": {
            "algorithm": {
              "algorithm":                string,
              "parameters":               string/null,
            },
            "public_key": {
              "modulus":                  string,  # [0]
              "public_exponent":          integer
            }
          },
          "issuer_unique_id":             string/null,
          "subject_unique_id":            string/null,
          "extensions": [
            {
              "extn_id":                  string,
              "critical":                 boolean,
              "extn_value":               array/object/string/integer  # [2]
            }
          ]
        },
        "signature_algorithm": {
          "algorithm":                    string,
          "parameters":                   string/null
        },
        "signature_value":                string  # [0]
      }
    ]

    [0] in colon-delimited hex notation
    [1] time-zone-aware (UTC) epoch timestamp
    [2] See below for well-known Extension schemas:

        Basic Constraints:
        {
          "extn_id":                          "basic_constraints",
          "critical":                         boolean,
          "extn_value": {
            "ca":                             boolean,
            "path_len_constraint":            string/null
          }
        }

        Key Usage:
        {
          "extn_id":                          "key_usage",
          "critical":                         boolean,
          "extn_value": [
                                              string
          ]
        }

        Key Identifier:
        {
          "extn_id":                          "key_identifier",
          "critical":                         boolean,
          "extn_value":                       string  # [0]
        }

        Authority Key Identifier:
        {
          "extn_id":                          "authority_key_identifier",
          "critical":                         boolean,
          "extn_value": {
            "key_identifier":                 string,  # [0]
            "authority_cert_issuer":          string/null,
            "authority_cert_serial_number":   string/null
          }
        }

        Subject Alternative Name:
        {
          "extn_id":                          "subject_alt_name",
          "critical":                         boolean,
          "extn_value": [
                                              string
          ]
        }

        Certificate Policies:
        {
          "extn_id":                          "certificate_policies",
          "critical":                         boolean,
          "extn_value": [
            {
              "policy_identifier":            string,
              "policy_qualifiers": [          array or null
                {
                  "policy_qualifier_id":      string,
                  "qualifier":                string
                }
              ]
            }
          ]
        }

        Signed Certificate Timestamp List:
        {
          "extn_id":                    "signed_certificate_timestamp_list",
          "critical":                   boolean,
          "extn_value":                 string  # [0]
        }

Examples:

    $ cat server.csr| jc --x509-csr -p
      [
        {
          "certification_request_info": {
            "version": "v1",
            "subject": {
              "common_name": "myserver.for.example"
            },
            "subject_pk_info": {
              "algorithm": {
                "algorithm": "ec",
                "parameters": "secp256r1"
              },
              "public_key": "04:40:33:c0:91:8f:e9:46:ea:d0:dc:d0:f9:63:2..."
            },
            "attributes": [
              {
                "type": "extension_request",
                "values": [
                  [
                    {
                      "extn_id": "extended_key_usage",
                      "critical": false,
                      "extn_value": [
                        "server_auth"
                      ]
                    },
                    {
                      "extn_id": "subject_alt_name",
                      "critical": false,
                      "extn_value": [
                        "myserver.for.example"
                      ]
                    }
                  ]
                ]
              }
            ]
          },
          "signature_algorithm": {
            "algorithm": "sha384_ecdsa",
            "parameters": null
          },
          "signature": "30:45:02:20:77:ac:5b:51:bf:c5:f5:43:02:52:ae:66:..."
        }
      ]

    $ openssl req -in server.csr | jc --x509-csr -p
      [
        {
          "certification_request_info": {
            "version": "v1",
            "subject": {
              "common_name": "myserver.for.example"
            },
            "subject_pk_info": {
              "algorithm": {
                "algorithm": "ec",
                "parameters": "secp256r1"
              },
              "public_key": "04:40:33:c0:91:8f:e9:46:ea:d0:dc:d0:f9:63:2..."
            },
            "attributes": [
              {
                "type": "extension_request",
                "values": [
                  [
                    {
                      "extn_id": "extended_key_usage",
                      "critical": false,
                      "extn_value": [
                        "server_auth"
                      ]
                    },
                    {
                      "extn_id": "subject_alt_name",
                      "critical": false,
                      "extn_value": [
                        "myserver.for.example"
                      ]
                    }
                  ]
                ]
              }
            ]
          },
          "signature_algorithm": {
            "algorithm": "sha384_ecdsa",
            "parameters": null
          },
          "signature": "30:45:02:20:77:ac:5b:51:bf:c5:f5:43:02:52:ae:66:..."
        }
      ]
"""
# import binascii
# from collections import OrderedDict
# from datetime import datetime
from typing import List, Dict, Union
import jc.utils
from jc.parsers.asn1crypto import pem, csr, jc_global
from jc.parsers.x509_cert import _fix_objects, _process


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'X.509 PEM and DER certificate request file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Using the asn1crypto library at https://github.com/wbond/asn1crypto/releases/tag/1.5.1'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['standard', 'file', 'string', 'binary']


__version__ = info.version


def parse(
    data: Union[str, bytes],
    raw: bool = False,
    quiet: bool = False
) -> List[Dict]:
    """
    Main text parsing function

    Parameters:

        data:        (string or bytes) text or binary data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc_global.quiet = quiet  # to inject quiet setting into asn1crypto library

    raw_output: List = []

    if jc.utils.has_data(data):
        # convert to bytes, if not already, for PEM detection since that's
        # what pem.detect() needs. (cli.py will auto-convert to UTF-8 if it can)
        try:
            der_bytes = bytes(data, 'utf-8')  # type: ignore
        except TypeError:
            der_bytes = data  # type: ignore

        certs = []
        if pem.detect(der_bytes):
            for type_name, headers, der_bytes in pem.unarmor(der_bytes, multiple=True):
                if type_name == 'CERTIFICATE REQUEST' or type_name == 'NEW CERTIFICATE REQUEST':
                    certs.append(csr.CertificationRequest.load(der_bytes))

        else:
            certs.append(csr.CertificationRequest.load(der_bytes))

        raw_output = [_fix_objects(cert.native) for cert in certs]

    return raw_output if raw else _process(raw_output)
