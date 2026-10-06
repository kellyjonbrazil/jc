[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.x509_cert"></a>

# jc.parsers.x509_cert

jc - JSON Convert X.509 Certificate format file parser

This parser will convert DER and PEM encoded X.509 certificate files.

You can convert other certificate formats (e.g. PKCS #7, PKCS #12, etc.) by
processing them through a program like `openssl` and sending the output to
`jc`. (See examples below)

> Note: `jc` does not verify the integrity of the certificate, which
> requires calculating the hash of the certificate body and comparing it to
> the the hash in the certificate's signature after it is decrypted with the
> issuer certificate's public key.

Usage (cli):

    $ cat certificate.pem | jc --x509-cert

Usage (module):

    import jc
    result = jc.parse('x509_cert', x509_cert_file_output)

Schema:

    [
      {
        "tbs_certificate": {
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

    $ cat entrust-ec1.pem | jc --x509-cert -p
    [
      {
        "tbs_certificate": {
          "version": "v3",
          "serial_number": "a6:8b:79:29:00:00:00:00:50:d0:91:f9",
          "signature": {
            "algorithm": "sha384_ecdsa",
            "parameters": null
          },
          "issuer": {
            "country_name": "US",
            "organization_name": "Entrust, Inc.",
            "organizational_unit_name": [
              "See www.entrust.net/legal-terms",
              "(c) 2012 Entrust, Inc. - for authorized use only"
            ],
            "common_name": "Entrust Root Certification Authority - EC1"
          },
          "validity": {
            "not_before": 1355844336,
            "not_after": 2144764536,
            "not_before_iso": "2012-12-18T15:25:36+00:00",
            "not_after_iso": "2037-12-18T15:55:36+00:00"
          },
          "subject": {
            "country_name": "US",
            "organization_name": "Entrust, Inc.",
            "organizational_unit_name": [
              "See www.entrust.net/legal-terms",
              "(c) 2012 Entrust, Inc. - for authorized use only"
            ],
            "common_name": "Entrust Root Certification Authority - EC1"
          },
          "subject_public_key_info": {
            "algorithm": {
              "algorithm": "ec",
              "parameters": "secp384r1"
            },
            "public_key": "04:84:13:c9:d0:ba:6d:41:7b:e2:6c:d0:eb:55:..."
          },
          "issuer_unique_id": null,
          "subject_unique_id": null,
          "extensions": [
            {
              "extn_id": "key_usage",
              "critical": true,
              "extn_value": [
                "crl_sign",
                "key_cert_sign"
              ]
            },
            {
              "extn_id": "basic_constraints",
              "critical": true,
              "extn_value": {
                "ca": true,
                "path_len_constraint": null
              }
            },
            {
              "extn_id": "key_identifier",
              "critical": false,
              "extn_value": "b7:63:e7:1a:dd:8d:e9:08:a6:55:83:a4:e0:6a:..."
            }
          ]
        },
        "signature_algorithm": {
          "algorithm": "sha384_ecdsa",
          "parameters": null
        },
        "signature_value": "30:64:02:30:61:79:d8:e5:42:47:df:1c:ae:53:..."
      }
    ]

    $ openssl pkcs7 -in thawte.p7b -inform der -print_certs | \\
              jc --x509-cert -p
    [
      {
        "tbs_certificate": {
          "version": "v3",
          "serial_number": "34:4e:d5:57:20:d5:ed:ec:49:f4:2f:ce:37:db...",
          "signature": {
            "algorithm": "sha1_rsa",
            "parameters": null
          },
          "issuer": {
            "country_name": "US",
            "organization_name": "thawte, Inc.",
            "organizational_unit_name": [
              "Certification Services Division",
              "(c) 2006 thawte, Inc. - For authorized use only"
            ],
            "common_name": "thawte Primary Root CA"
          },
          "validity": {
            "not_before": 1163721600,
            "not_after": 2099865599,
            "not_before_iso": "2006-11-17T00:00:00+00:00",
            "not_after_iso": "2036-07-16T23:59:59+00:00"
          },
          "subject": {
            "country_name": "US",
            "organization_name": "thawte, Inc.",
            "organizational_unit_name": [
              "Certification Services Division",
              "(c) 2006 thawte, Inc. - For authorized use only"
            ],
            "common_name": "thawte Primary Root CA"
          },
          "subject_public_key_info": {
            "algorithm": {
              "algorithm": "rsa",
              "parameters": null
            },
            "public_key": {
              "modulus": "ac:a0:f0:fb:80:59:d4:9c:c7:a4:cf:9d:a1:59:73...",
              "public_exponent": 65537
            }
          },
          "issuer_unique_id": null,
          "subject_unique_id": null,
          "extensions": [
            {
              "extn_id": "basic_constraints",
              "critical": true,
              "extn_value": {
                "ca": true,
                "path_len_constraint": null
              }
            },
            {
              "extn_id": "key_usage",
              "critical": true,
              "extn_value": [
                "crl_sign",
                "key_cert_sign"
              ]
            },
            {
              "extn_id": "key_identifier",
              "critical": false,
              "extn_value": "7b:5b:45:cf:af:ce:cb:7a:fd:31:92:1a:6a:b6:..."
            }
          ]
        },
        "signature_algorithm": {
          "algorithm": "sha1_rsa",
          "parameters": null
        },
        "signature_value": "79:11:c0:4b:b3:91:b6:fc:f0:e9:67:d4:0d:6e..."
      }
    ]

    $ openssl pkcs12 -info -in certificate.pfx \\
              -passin pass: -passout pass: | \\
              jc --x509-cert -p
    [
      {
        "tbs_certificate": {
          "version": "v3",
          "serial_number": "01",
          "signature": {
            "algorithm": "sha1_rsa",
            "parameters": null
          },
          "issuer": {
            "country_name": "FR",
            "state_or_province_name": "Alsace",
            "locality_name": "Strasbourg",
            "organization_name": "www.freelan.org",
            "organizational_unit_name": "freelan",
            "common_name": "Freelan Sample Certificate Authority",
            "email_address": "contact@freelan.org"
          },
          "validity": {
            "not_before": 1335522678,
            "not_after": 1650882678,
            "not_before_iso": "2012-04-27T10:31:18+00:00",
            "not_after_iso": "2022-04-25T10:31:18+00:00"
          },
          "subject": {
            "country_name": "FR",
            "state_or_province_name": "Alsace",
            "organization_name": "www.freelan.org",
            "organizational_unit_name": "freelan",
            "common_name": "alice",
            "email_address": "contact@freelan.org"
          },
          "subject_public_key_info": {
            "algorithm": {
              "algorithm": "rsa",
              "parameters": null
            },
            "public_key": {
              "modulus": "dd:6d:bd:f8:80:fa:d7:de:1b:1f:a7:a3:2e:b2:02...",
              "public_exponent": 65537
            }
          },
          "issuer_unique_id": null,
          "subject_unique_id": null,
          "extensions": [
            {
              "extn_id": "basic_constraints",
              "critical": false,
              "extn_value": {
                "ca": false,
                "path_len_constraint": null
              }
            },
            {
              "extn_id": "2.16.840.1.113730.1.13",
              "critical": false,
              "extn_value": "16:1d:4f:70:65:6e:53:53:4c:20:47:65:6e:65..."
            },
            {
              "extn_id": "key_identifier",
              "critical": false,
              "extn_value": "59:5f:c9:13:ba:1b:cc:b9:a8:41:4a:8a:49:79..."
            },
            {
              "extn_id": "authority_key_identifier",
              "critical": false,
              "extn_value": {
                "key_identifier": "23:6c:2d:3d:3e:29:5d:78:b8:6c:3e:aa...",
                "authority_cert_issuer": null,
                "authority_cert_serial_number": null
              }
            }
          ]
        },
        "signature_algorithm": {
          "algorithm": "sha1_rsa",
          "parameters": null
        },
        "signature_value": "13:e7:02:45:3e:a7:ab:bd:b8:da:e7:ef:74:88..."
      }
    ]

<a id="jc.parsers.x509_cert.parse"></a>

### parse

```python
def parse(data: Union[str, bytes],
          raw: bool = False,
          quiet: bool = False) -> List[Dict]
```

Main text parsing function

Parameters:

    data:        (string or bytes) text or binary data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

### Parser Information
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Source: [`jc/parsers/x509_cert.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/x509_cert.py)

Version 1.4 by Kelly Brazil (kellyjonbrazil@gmail.com)
