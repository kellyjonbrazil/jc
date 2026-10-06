r"""jc - JSON Convert X.509 Certificate Revocation List format file parser

This parser will convert DER and PEM encoded X.509 certificate revocation
list files.

Usage (cli):

    $ cat certificateRevocationList.pem | jc --x509-crl
    $ cat certificateRevocationList.der | jc --x509-crl

Usage (module):

    import jc
    result = jc.parse('x509_crl', x509_crl_file_output)

Schema:

    {
      "tbs_cert_list": {
        "version":                      string,
        "signature": {
          "algorithm":                  string,
          "parameters":                 string/null
        },
        "issuer": {
          "organization_name":          string,
          "organizational_unit_name":   string,
          "common_name":                string
        },
        "this_update":                  integer,  # [1]
        "next_update":                  integer,  # [1]
        "revoked_certificates": [
          {
            "user_certificate":         integer,
            "revocation_date":          integer,  # [1]
            "crl_entry_extensions": [
              {
                "extn_id":              string,
                "critical":             boolean,
                "extn_value":           string,
                "extn_value_iso":       string
              },
            "revocation_date_iso":      string
          }
        ],
        "crl_extensions": [
          {
            "extn_id":                  string,
            "critical":                 boolean,
            "extn_value":               array/object/string/integer  # [2]
          }
        ],
        "this_update_iso":              string,
        "next_update_iso":              string
      },
      "signature_algorithm": {
        "algorithm":                    string,
        "parameters":                   string/null
      },
      "signature":                      string  # [0]
    }

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

    $ cat sample-crl.pem | jc --x509-crl -p
    {
      "tbs_cert_list": {
        "version": "v2",
        "signature": {
          "algorithm": "sha1_rsa",
          "parameters": null
        },
        "issuer": {
          "organization_name": "Sample Signer Organization",
          "organizational_unit_name": "Sample Signer Unit",
          "common_name": "Sample Signer Cert"
        },
        "this_update": 1361183520,
        "next_update": 1361184120,
        "revoked_certificates": [
          {
            "user_certificate": 1341767,
            "revocation_date": 1361182932,
            "crl_entry_extensions": [
              {
                "extn_id": "crl_reason",
                "critical": false,
                "extn_value": "affiliation_changed"
              },
              {
                "extn_id": "invalidity_date",
                "critical": false,
                "extn_value": 1361182920,
                "extn_value_iso": "2013-02-18T10:22:00+00:00"
              }
            ],
            "revocation_date_iso": "2013-02-18T10:22:12+00:00"
          },
          {
            "user_certificate": 1341768,
            "revocation_date": 1361182942,
            "crl_entry_extensions": [
              {
                "extn_id": "crl_reason",
                "critical": false,
                "extn_value": "certificate_hold"
              },
              {
                "extn_id": "invalidity_date",
                "critical": false,
                "extn_value": 1361182920,
                "extn_value_iso": "2013-02-18T10:22:00+00:00"
              }
            ],
            "revocation_date_iso": "2013-02-18T10:22:22+00:00"
          },
          {
            "user_certificate": 1341769,
            "revocation_date": 1361182952,
            "crl_entry_extensions": [
              {
                "extn_id": "crl_reason",
                "critical": false,
                "extn_value": "superseded"
              },
              {
                "extn_id": "invalidity_date",
                "critical": false,
                "extn_value": 1361182920,
                "extn_value_iso": "2013-02-18T10:22:00+00:00"
              }
            ],
            "revocation_date_iso": "2013-02-18T10:22:32+00:00"
          },
          {
            "user_certificate": 1341770,
            "revocation_date": 1361182962,
            "crl_entry_extensions": [
              {
                "extn_id": "crl_reason",
                "critical": false,
                "extn_value": "key_compromise"
              },
              {
                "extn_id": "invalidity_date",
                "critical": false,
                "extn_value": 1361182920,
                "extn_value_iso": "2013-02-18T10:22:00+00:00"
              }
            ],
            "revocation_date_iso": "2013-02-18T10:22:42+00:00"
          },
          {
            "user_certificate": 1341771,
            "revocation_date": 1361182971,
            "crl_entry_extensions": [
              {
                "extn_id": "crl_reason",
                "critical": false,
                "extn_value": "cessation_of_operation"
              },
              {
                "extn_id": "invalidity_date",
                "critical": false,
                "extn_value": 1361182920,
                "extn_value_iso": "2013-02-18T10:22:00+00:00"
              }
            ],
            "revocation_date_iso": "2013-02-18T10:22:51+00:00"
          }
        ],
        "crl_extensions": [
          {
            "extn_id": "authority_key_identifier",
            "critical": false,
            "extn_value": {
              "key_identifier": "be:12:01:cc:aa:ea:11:80:da:2e:ad:b2...",
              "authority_cert_issuer": null,
              "authority_cert_serial_number": null
            }
          },
          {
            "extn_id": "crl_number",
            "critical": false,
            "extn_value": 3
          }
        ],
        "this_update_iso": "2013-02-18T10:32:00+00:00",
        "next_update_iso": "2013-02-18T10:42:00+00:00"
      },
      "signature_algorithm": {
        "algorithm": "sha1_rsa",
        "parameters": null
      },
      "signature": "42:21:be:81:f1:c3:79:76:66:5b:ce:21:13:8a:68:a..."
    }
"""
from typing import List, Dict, Union
import jc.utils
from jc.parsers.asn1crypto import pem, crl, jc_global
from jc.parsers.x509_cert import _fix_objects


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'X.509 PEM and DER certificate revocation list file parser'
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
) -> Dict:
    """
    Main text parsing function

    Parameters:

        data:        (string or bytes) text or binary data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc_global.quiet = quiet  # to inject quiet setting into asn1crypto library

    raw_output: Dict = {}

    if jc.utils.has_data(data):
        # convert to bytes, if not already, for PEM detection since that's
        # what pem.detect() needs. (cli.py will auto-convert to UTF-8 if it can)
        try:
            der_bytes = bytes(data, 'utf-8')  # type: ignore
        except TypeError:
            der_bytes = data  # type: ignore

        if pem.detect(der_bytes):
            for type_name, headers, der_bytes in pem.unarmor(der_bytes, multiple=True):
                if type_name == 'X509 CRL':
                    crl_obj = crl.CertificateList.load(der_bytes)
                    break
        else:
            crl_obj = crl.CertificateList.load(der_bytes)

        raw_output = _fix_objects(crl_obj.native)

    return raw_output
