[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.gpg"></a>

# jc.parsers.gpg

jc - JSON Convert `gpg --with-colons` command output parser

Usage (cli):

    $ gpg --with-colons --show-keys file.gpg | jc --gpg

or

    $ jc gpg --with-colons --show-keys file.gpg

Usage (module):

    import jc
    result = jc.parse('gpg', gpg_command_output)

Schema:

Field definitions from https://git.gnupg.org/cgi-bin/gitweb.cgi?p=gnupg.git;a=blob_plain;f=doc/DETAILS

> Note: Number values are not converted to integers because many field
> specifications are overloaded and future augmentations are implied in the
> documentation.

    [
      {
        "type":                             string,
        "validity":                         string,
        "key_length":                       string,
        "pub_key_alg":                      string,
        "key_id":                           string,
        "creation_date":                    string,
        "expiration_date":                  string,
        "certsn_uidhash_trustinfo":         string,
        "owner_trust":                      string,
        "user_id":                          string,
        "signature_class":                  string,
        "key_capabilities":                 string,
        "cert_fingerprint_other":           string,
        "flag":                             string,
        "token_sn":                         string,
        "hash_alg":                         string,
        "curve_name":                       string,
        "compliance_flags":                 string,
        "last_update_date":                 string,
        "origin":                           string,
        "comment":                          string,
        "index":                            string,  # [0]
        "bits":                             string,  # [0]
        "value":                            string,  # [0]
        "version":                          string,  # [1], [4]
        "signature_count":                  string,  # [1]
        "encryption_count":                 string,  # [1]
        "policy":                           string,  # [1]
        "signature_first_seen":             string,  # [1]
        "signature_most_recent_seen":       string,  # [1]
        "encryption_first_done":            string,  # [1]
        "encryption_most_recent_done":      string,  # [1]
        "staleness_reason":                 string,  # [2]
        "trust_model":                      string,  # [2]
        "trust_db_created":                 string,  # [2]
        "trust_db_expires":                 string,  # [2]
        "marginally_trusted_users":         string,  # [2]
        "completely_trusted_users":         string,  # [2]
        "cert_chain_max_depth":             string,  # [2]
        "subpacket_number":                 string,  # [3]
        "hex_flags":                        string,  # [3]
        "subpacket_length":                 string,  # [3]
        "subpacket_data":                   string,  # [3]
        "pubkey":                           string,  # [4]
        "cipher":                           string,  # [4]
        "digest":                           string,  # [4]
        "compress":                         string,  # [4]
        "group":                            string,  # [4]
        "members":                          string,  # [4]
        "curve_names":                      string,  # [4]
      }
    ]

    All blank values are converted to null/None.

    [0] for 'pkd' type
    [1] for 'tfs' type
    [2] for 'tru' type
    [3] for 'skp' type
    [4] for 'cfg' type

Examples:

    $ gpg --with-colons --show-keys file.gpg | jc --gpg -p
    [
      {
        "type": "pub",
        "validity": "f",
        "key_length": "1024",
        "pub_key_alg": "17",
        "key_id": "6C7EE1B8621CC013",
        "creation_date": "899817715",
        "expiration_date": "1055898235",
        "certsn_uidhash_trustinfo": null,
        "owner_trust": "m",
        "user_id": null,
        "signature_class": null,
        "key_capabilities": "scESC",
        "cert_fingerprint_other": null,
        "flag": null,
        "token_sn": null,
        "hash_alg": null,
        "curve_name": null,
        "compliance_flags": null,
        "last_update_date": null,
        "origin": null,
        "comment": null
      },
      ...
    ]

<a id="jc.parsers.gpg.parse"></a>

### parse

```python
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[Dict]
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

### Parser Information
Compatibility:  linux

Source: [`jc/parsers/gpg.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/gpg.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
