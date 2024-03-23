r"""jc - JSON Convert `gpg --with-colons` command output parser

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
"""
from typing import List, Dict, Optional
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`gpg --with-colons` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    magic_commands = ['gpg --with-colons']
    tags = ['command']


__version__ = info.version


def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    return proc_data


def _list_get(my_list: List, index: int, default_val=None) -> Optional[str]:
    """get a list value or return None/default value if out of range."""
    if index <= len(my_list) - 1:
        return my_list[index] or None

    return default_val


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> List[Dict]:
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

    raw_output: List = []

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            values = line.split(':')
            temp_obj = {
                'type': _list_get(values, 0),
                'validity': _list_get(values, 1),
                'key_length': _list_get(values, 2),
                'pub_key_alg': _list_get(values, 3),
                'key_id': _list_get(values, 4),
                'creation_date': _list_get(values, 5),
                'expiration_date': _list_get(values, 6),
                'certsn_uidhash_trustinfo': _list_get(values, 7),
                'owner_trust': _list_get(values, 8),
                'user_id': _list_get(values, 9),
                'signature_class': _list_get(values, 10),
                'key_capabilities': _list_get(values, 11),
                'cert_fingerprint_other': _list_get(values, 12),
                'flag': _list_get(values, 13),
                'token_sn': _list_get(values, 14),
                'hash_alg': _list_get(values, 15),
                'curve_name': _list_get(values, 16),
                'compliance_flags': _list_get(values, 17),
                'last_update_date': _list_get(values, 18),
                'origin': _list_get(values, 19),
                'comment': _list_get(values, 20)
            }

            # field mappings change for special types: pkd, tfs, tru, skp, cfg

            if temp_obj['type'] == 'pkd':
                # pkd:0:1024:B665B1435F4C2 .... FF26ABB:
                #     !  !   !-- the value
                #     !  !------ for information number of bits in the value
                #     !--------- index (eg. DSA goes from 0 to 3: p,q,g,y)
                line_obj = {
                    'type': temp_obj['type'],
                    'index': temp_obj['validity'],
                    'bits': temp_obj['key_length'],
                    'value': temp_obj['pub_key_alg']
                }

            elif temp_obj['type'] == 'tfs':
                # - Field 2 :: tfs record version (must be 1)
                # - Field 3 :: validity -  A number with validity code.
                # - Field 4 :: signcount - The number of signatures seen.
                # - Field 5 :: encrcount - The number of encryptions done.
                # - Field 6 :: policy - A string with the policy
                # - Field 7 :: signture-first-seen - a timestamp or 0 if not known.
                # - Field 8 :: signature-most-recent-seen - a timestamp or 0 if not known.
                # - Field 9 :: encryption-first-done - a timestamp or 0 if not known.
                # - Field 10 :: encryption-most-recent-done - a timestamp or 0 if not known.
                line_obj = {
                    'type': temp_obj['type'],
                    'version': temp_obj['validity'],
                    'validity': temp_obj['key_length'],
                    'signature_count': temp_obj['pub_key_alg'],
                    'encryption_count': temp_obj['key_id'],
                    'policy': temp_obj['creation_date'],
                    'signature_first_seen': temp_obj['expiration_date'],
                    'signature_most_recent_seen': temp_obj['certsn_uidhash_trustinfo'],
                    'encryption_first_done': temp_obj['owner_trust'],
                    'encryption_most_recent_done': temp_obj['user_id']
                }

            elif temp_obj['type'] == 'tru':
                # tru:o:0:1166697654:1:3:1:5
                # - Field 2 :: Reason for staleness of trust.
                # - Field 3 :: Trust model
                # - Field 4 :: Date trustdb was created in seconds since Epoch.
                # - Field 5 :: Date trustdb will expire in seconds since Epoch.
                # - Field 6 :: Number of marginally trusted users to introduce a new key signer.
                # - Field 7 :: Number of completely trusted users to introduce a new key signer.
                # - Field 8 :: Maximum depth of a certification chain.
                line_obj = {
                    'type': temp_obj['type'],
                    'staleness_reason': temp_obj['validity'],
                    'trust_model': temp_obj['key_length'],
                    'trust_db_created': temp_obj['pub_key_alg'],
                    'trust_db_expires': temp_obj['key_id'],
                    'marginally_trusted_users': temp_obj['creation_date'],
                    'completely_trusted_users': temp_obj['expiration_date'],
                    'cert_chain_max_depth': temp_obj['certsn_uidhash_trustinfo']
                }

            elif temp_obj['type'] == 'skp':
                # - Field 2 :: Subpacket number as per RFC-4880 and later.
                # - Field 3 :: Flags in hex.
                # - Field 4 :: Length of the subpacket.
                # - Field 5 :: The subpacket data.
                line_obj = {
                    'type': temp_obj['type'],
                    'subpacket_number': temp_obj['validity'],
                    'hex_flags': temp_obj['key_length'],
                    'subpacket_length': temp_obj['pub_key_alg'],
                    'subpacket_data': temp_obj['key_id']
                }

            elif temp_obj['type'] == 'cfg':

                # there are several 'cfg' formats

                if temp_obj['validity'] == 'version':
                    # cfg:version:1.3.5
                    line_obj = {
                        'type': temp_obj['type'],
                        'version': temp_obj['key_length']
                    }

                elif temp_obj['validity'] == 'pubkey':
                    # cfg:pubkey:1;2;3;16;17
                    line_obj = {
                        'type': temp_obj['type'],
                        'pubkey': temp_obj['key_length']
                    }

                elif temp_obj['validity'] == 'cipher':
                    # cfg:cipher:2;3;4;7;8;9;10
                    line_obj = {
                        'type': temp_obj['type'],
                        'cipher': temp_obj['key_length']
                    }

                elif temp_obj['validity'] == 'digest':
                    # cfg:digest:1;2;3;8;9;10
                    line_obj = {
                        'type': temp_obj['type'],
                        'digest': temp_obj['key_length']
                    }

                elif temp_obj['validity'] == 'compress':
                    # cfg:compress:0;1;2;3
                    line_obj = {
                        'type': temp_obj['type'],
                        'compress': temp_obj['key_length']
                    }

                elif temp_obj['validity'] == 'group':
                    # cfg:group:mynames:patti;joe;0x12345678;paige
                    line_obj = {
                        'type': temp_obj['type'],
                        'group': temp_obj['key_length'],
                        'members': temp_obj['pub_key_alg']
                    }

                elif temp_obj['validity'] == 'curve':
                    # cfg:curve:ed25519;nistp256;nistp384;nistp521
                    line_obj = {
                        'type': temp_obj['type'],
                        'curve_names': temp_obj['key_length']
                    }

            else:
                line_obj = temp_obj

            raw_output.append(line_obj)

    return raw_output if raw else _process(raw_output)
