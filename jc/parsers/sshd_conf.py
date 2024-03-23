r"""jc - JSON Convert `sshd` configuration file and `sshd -T` command output parser

This parser will work with `sshd` configuration files or the output of
`sshd -T`. Any `Match` blocks in the `sshd` configuration file will be
ignored.

Usage (cli):

    $ sshd -T | jc --sshd-conf

or

    $ jc sshd -T

or

    $ cat sshd_conf | jc --sshd-conf

Usage (module):

    import jc
    result = jc.parse('sshd_conf', sshd_conf_output)

Schema:

    {
      "acceptenv": [
                                                  string
      ],
      "addressfamily":                            string,
      "allowagentforwarding":                     string,
      "allowstreamlocalforwarding":               string,
      "allowtcpforwarding":                       string,
      "authenticationmethods":                    string,
      "authorizedkeyscommand":                    string,
      "authorizedkeyscommanduser":                string,
      "authorizedkeysfile": [
                                                  string
      ],
      "authorizedprincipalscommand":              string,
      "authorizedprincipalscommanduser":          string,
      "authorizedprincipalsfile":                 string,
      "banner":                                   string,
      "casignaturealgorithms": [
                                                  string
      ],
      "chrootdirectory":                          string,
      "ciphers": [
                                                  string
      ],
      "ciphers_strategy":                         string,
      "clientalivecountmax":                      integer,
      "clientaliveinterval":                      integer,
      "compression":                              string,
      "disableforwarding":                        string,
      "exposeauthinfo":                           string,
      "fingerprinthash":                          string,
      "forcecommand":                             string,
      "gatewayports":                             string,
      "gssapiauthentication":                     string,
      "gssapicleanupcredentials":                 string,
      "gssapikexalgorithms": [
                                                  string
      ],
      "gssapikeyexchange":                        string,
      "gssapistorecredentialsonrekey":            string,
      "gssapistrictacceptorcheck":                string,
      "hostbasedacceptedalgorithms": [
                                                  string
      ],
      "hostbasedauthentication":                  string,
      "hostbasedusesnamefrompacketonly":          string,
      "hostkeyagent":                             string,
      "hostkeyalgorithms": [
                                                  string
      ],
      "hostkey": [
                                                  string
      ],
      "ignorerhosts":                             string,
      "ignoreuserknownhosts":                     string,
      "include": [
                                                  string
      ],
      "ipqos": [
                                                  string
      ],
      "kbdinteractiveauthentication":             string,
      "kerberosauthentication":                   string,
      "kerberosorlocalpasswd":                    string,
      "kerberosticketcleanup":                    sttring,
      "kexalgorithms": [
                                                  string
      ],
      "listenaddress": [
                                                  string
      ],
      "logingracetime":                           integer,
      "loglevel":                                 string,
      "macs": [
                                                  string
      ],
      "macs_strategy":                            string,
      "maxauthtries":                             integer,
      "maxsessions":                              integer,
      "maxstartups":                              integer,
      "maxstartups_rate":                         integer,
      "maxstartups_full":                         integer,
      "modulifile":                               string,
      "passwordauthentication":                   string,
      "permitemptypasswords":                     string,
      "permitlisten": [
                                                  string
      ],
      "permitopen": [
                                                  string
      ],
      "permitrootlogin":                          string,
      "permittty":                                string,
      "permittunnel":                             string,
      "permituserenvironment":                    string,
      "permituserrc":                             string,
      "persourcemaxstartups":                     string,
      "persourcenetblocksize":                    string,
      "pidfile":                                  string,
      "port": [
                                                  integer
      ],
      "printlastlog":                             string,
      "printmotd":                                string,
      "pubkeyacceptedalgorithms": [
                                                  string
      ],
      "pubkeyauthentication":                     string,
      "pubkeyauthoptions":                        string,
      "rekeylimit":                               integer,
      "rekeylimit_time":                          integer,
      "revokedkeys":                              string,
      "securitykeyprovider":                      string,
      "streamlocalbindmask":                      string,
      "streamlocalbindunlink":                    string,
      "strictmodes":                              string,
      "subsystem":                                string,
      "subsystem_command":                        string
      "syslogfacility":                           string,
      "tcpkeepalive":                             string,
      "trustedusercakeys":                        string,
      "usedns":                                   string,
      "usepam":                                   string,
      "versionaddendum":                          string,
      "x11displayoffset":                         integer,
      "x11forwarding":                            string,
      "x11uselocalhost":                          string,
      "xauthlocation":                            string
    }

Examples:

    $ sshd -T | jc --sshd-conf -p
    {
      "acceptenv": [
        "LANG",
        "LC_*"
      ],
      "addressfamily": "any",
      "allowagentforwarding": "yes",
      "allowstreamlocalforwarding": "yes",
      "allowtcpforwarding": "yes",
      "authenticationmethods": "any",
      "authorizedkeyscommand": "none",
      "authorizedkeyscommanduser": "none",
      "authorizedkeysfile": [
        ".ssh/authorized_keys",
        ".ssh/authorized_keys2"
      ],
      "authorizedprincipalscommand": "none",
      "authorizedprincipalscommanduser": "none",
      "authorizedprincipalsfile": "none",
      "banner": "none",
      "casignaturealgorithms": [
        "ssh-ed25519",
        "ecdsa-sha2-nistp256",
        "ecdsa-sha2-nistp384",
        "ecdsa-sha2-nistp521",
        "sk-ssh-ed25519@openssh.com",
        "sk-ecdsa-sha2-nistp256@openssh.com",
        "rsa-sha2-512",
        "rsa-sha2-256"
      ],
      "chrootdirectory": "none",
      "ciphers": [
        "chacha20-poly1305@openssh.com",
        "aes128-ctr",
        "aes192-ctr",
        "aes256-ctr",
        "aes128-gcm@openssh.com",
        "aes256-gcm@openssh.com"
      ],
      "ciphers_strategy": "+",
      "clientalivecountmax": 3,
      "clientaliveinterval": 0,
      "compression": "yes",
      "disableforwarding": "no",
      "exposeauthinfo": "no",
      "fingerprinthash": "SHA256",
      "forcecommand": "none",
      "gatewayports": "no",
      "gssapiauthentication": "no",
      "gssapicleanupcredentials": "yes",
      "gssapikexalgorithms": [
        "gss-group14-sha256-",
        "gss-group16-sha512-",
        "gss-nistp256-sha256-",
        "gss-curve25519-sha256-",
        "gss-group14-sha1-",
        "gss-gex-sha1-"
      ],
      "gssapikeyexchange": "no",
      "gssapistorecredentialsonrekey": "no",
      "gssapistrictacceptorcheck": "yes",
      "hostbasedacceptedalgorithms": [
        "ssh-ed25519-cert-v01@openssh.com",
        "ecdsa-sha2-nistp256-cert-v01@openssh.com",
        "ecdsa-sha2-nistp384-cert-v01@openssh.com",
        "ecdsa-sha2-nistp521-cert-v01@openssh.com",
        "sk-ssh-ed25519-cert-v01@openssh.com",
        "sk-ecdsa-sha2-nistp256-cert-v01@openssh.com",
        "rsa-sha2-512-cert-v01@openssh.com",
        "rsa-sha2-256-cert-v01@openssh.com",
        "ssh-ed25519",
        "ecdsa-sha2-nistp256",
        "ecdsa-sha2-nistp384",
        "ecdsa-sha2-nistp521",
        "sk-ssh-ed25519@openssh.com",
        "sk-ecdsa-sha2-nistp256@openssh.com",
        "rsa-sha2-512",
        "rsa-sha2-256"
      ],
      "hostbasedauthentication": "no",
      "hostbasedusesnamefrompacketonly": "no",
      "hostkeyagent": "none",
      "hostkeyalgorithms": [
        "ssh-ed25519-cert-v01@openssh.com",
        "ecdsa-sha2-nistp256-cert-v01@openssh.com",
        "ecdsa-sha2-nistp384-cert-v01@openssh.com",
        "ecdsa-sha2-nistp521-cert-v01@openssh.com",
        "sk-ssh-ed25519-cert-v01@openssh.com",
        "sk-ecdsa-sha2-nistp256-cert-v01@openssh.com",
        "rsa-sha2-512-cert-v01@openssh.com",
        "rsa-sha2-256-cert-v01@openssh.com",
        "ssh-ed25519",
        "ecdsa-sha2-nistp256",
        "ecdsa-sha2-nistp384",
        "ecdsa-sha2-nistp521",
        "sk-ssh-ed25519@openssh.com",
        "sk-ecdsa-sha2-nistp256@openssh.com",
        "rsa-sha2-512",
        "rsa-sha2-256"
      ],
      "hostkey": [
        "/etc/ssh/ssh_host_ecdsa_key",
        "/etc/ssh/ssh_host_ed25519_key",
        "/etc/ssh/ssh_host_rsa_key"
      ],
      "ignorerhosts": "yes",
      "ignoreuserknownhosts": "no",
      "ipqos": [
        "lowdelay",
        "throughput"
      ],
      "kbdinteractiveauthentication": "no",
      "kerberosauthentication": "no",
      "kerberosorlocalpasswd": "yes",
      "kerberosticketcleanup": "yes",
      "kexalgorithms": [
        "sntrup761x25519-sha512@openssh.com",
        "curve25519-sha256",
        "curve25519-sha256@libssh.org",
        "ecdh-sha2-nistp256",
        "ecdh-sha2-nistp384",
        "ecdh-sha2-nistp521",
        "diffie-hellman-group-exchange-sha256",
        "diffie-hellman-group16-sha512",
        "diffie-hellman-group18-sha512",
        "diffie-hellman-group14-sha256"
      ],
      "listenaddress": [
        "0.0.0.0:22",
        "[::]:22"
      ],
      "logingracetime": 120,
      "loglevel": "INFO",
      "macs": [
        "umac-64-etm@openssh.com",
        "umac-128-etm@openssh.com",
        "hmac-sha2-256-etm@openssh.com",
        "hmac-sha2-512-etm@openssh.com",
        "hmac-sha1-etm@openssh.com",
        "umac-64@openssh.com",
        "umac-128@openssh.com",
        "hmac-sha2-256",
        "hmac-sha2-512",
        "hmac-sha1"
      ],
      "macs_strategy": "^",
      "maxauthtries": 6,
      "maxsessions": 10,
      "maxstartups": 10,
      "modulifile": "/etc/ssh/moduli",
      "passwordauthentication": "yes",
      "permitemptypasswords": "no",
      "permitlisten": [
        "any"
      ],
      "permitopen": [
        "any"
      ],
      "permitrootlogin": "without-password",
      "permittty": "yes",
      "permittunnel": "no",
      "permituserenvironment": "no",
      "permituserrc": "yes",
      "persourcemaxstartups": "none",
      "persourcenetblocksize": "32:128",
      "pidfile": "/run/sshd.pid",
      "port": [
        22
      ],
      "printlastlog": "yes",
      "printmotd": "no",
      "pubkeyacceptedalgorithms": [
        "ssh-ed25519-cert-v01@openssh.com",
        "ecdsa-sha2-nistp256-cert-v01@openssh.com",
        "ecdsa-sha2-nistp384-cert-v01@openssh.com",
        "ecdsa-sha2-nistp521-cert-v01@openssh.com",
        "sk-ssh-ed25519-cert-v01@openssh.com",
        "sk-ecdsa-sha2-nistp256-cert-v01@openssh.com",
        "rsa-sha2-512-cert-v01@openssh.com",
        "rsa-sha2-256-cert-v01@openssh.com",
        "ssh-ed25519",
        "ecdsa-sha2-nistp256",
        "ecdsa-sha2-nistp384",
        "ecdsa-sha2-nistp521",
        "sk-ssh-ed25519@openssh.com",
        "sk-ecdsa-sha2-nistp256@openssh.com",
        "rsa-sha2-512",
        "rsa-sha2-256"
      ],
      "pubkeyauthentication": "yes",
      "pubkeyauthoptions": "none",
      "rekeylimit": 0,
      "revokedkeys": "none",
      "securitykeyprovider": "internal",
      "streamlocalbindmask": "0177",
      "streamlocalbindunlink": "no",
      "strictmodes": "yes",
      "subsystem": "sftp",
      "syslogfacility": "AUTH",
      "tcpkeepalive": "yes",
      "trustedusercakeys": "none",
      "usedns": "no",
      "usepam": "yes",
      "versionaddendum": "none",
      "x11displayoffset": 10,
      "x11forwarding": "yes",
      "x11uselocalhost": "yes",
      "xauthlocation": "/usr/bin/xauth",
      "maxstartups_rate": 30,
      "maxstartups_full": 100,
      "rekeylimit_time": 0,
      "subsystem_command": "/usr/lib/openssh/sftp-server"
    }

    $ sshd -T | jc --sshd-conf -p -r
    {
      "acceptenv": [
        "LANG",
        "LC_*"
      ],
      "addressfamily": "any",
      "allowagentforwarding": "yes",
      "allowstreamlocalforwarding": "yes",
      "allowtcpforwarding": "yes",
      "authenticationmethods": "any",
      "authorizedkeyscommand": "none",
      "authorizedkeyscommanduser": "none",
      "authorizedkeysfile": ".ssh/authorized_keys .ssh/authorized_keys2",
      "authorizedprincipalscommand": "none",
      "authorizedprincipalscommanduser": "none",
      "authorizedprincipalsfile": "none",
      "banner": "none",
      "casignaturealgorithms": "ssh-ed25519,ecdsa-sha2-nistp256,ecdsa-s...",
      "chrootdirectory": "none",
      "ciphers": "chacha20-poly1305@openssh.com,aes128-ctr,aes192-ctr,...",
      "ciphers_strategy": "+",
      "clientalivecountmax": "3",
      "clientaliveinterval": "0",
      "compression": "yes",
      "disableforwarding": "no",
      "exposeauthinfo": "no",
      "fingerprinthash": "SHA256",
      "forcecommand": "none",
      "gatewayports": "no",
      "gssapiauthentication": "no",
      "gssapicleanupcredentials": "yes",
      "gssapikexalgorithms": "gss-group14-sha256-,gss-group16-sha512-,...",
      "gssapikeyexchange": "no",
      "gssapistorecredentialsonrekey": "no",
      "gssapistrictacceptorcheck": "yes",
      "hostbasedacceptedalgorithms": "ssh-ed25519-cert-v01@openssh.co...",
      "hostbasedauthentication": "no",
      "hostbasedusesnamefrompacketonly": "no",
      "hostkeyagent": "none",
      "hostkeyalgorithms": "ssh-ed25519-cert-v01@openssh.com,ecdsa-sha2...",
      "hostkey": [
        "/etc/ssh/ssh_host_ecdsa_key",
        "/etc/ssh/ssh_host_ed25519_key",
        "/etc/ssh/ssh_host_rsa_key"
      ],
      "ignorerhosts": "yes",
      "ignoreuserknownhosts": "no",
      "ipqos": "lowdelay throughput",
      "kbdinteractiveauthentication": "no",
      "kerberosauthentication": "no",
      "kerberosorlocalpasswd": "yes",
      "kerberosticketcleanup": "yes",
      "kexalgorithms": "sntrup761x25519-sha512@openssh.com,curve25519...",
      "listenaddress": [
        "0.0.0.0:22",
        "[::]:22"
      ],
      "logingracetime": "120",
      "loglevel": "INFO",
      "macs": "umac-64-etm@openssh.com,umac-128-etm@openssh.com,hmac...",
      "macs_strategy": "^",
      "maxauthtries": "6",
      "maxsessions": "10",
      "maxstartups": "10:30:100",
      "modulifile": "/etc/ssh/moduli",
      "passwordauthentication": "yes",
      "permitemptypasswords": "no",
      "permitlisten": "any",
      "permitopen": "any",
      "permitrootlogin": "without-password",
      "permittty": "yes",
      "permittunnel": "no",
      "permituserenvironment": "no",
      "permituserrc": "yes",
      "persourcemaxstartups": "none",
      "persourcenetblocksize": "32:128",
      "pidfile": "/run/sshd.pid",
      "port": [
        "22"
      ],
      "printlastlog": "yes",
      "printmotd": "no",
      "pubkeyacceptedalgorithms": "ssh-ed25519-cert-v01@openssh.com,...",
      "pubkeyauthentication": "yes",
      "pubkeyauthoptions": "none",
      "rekeylimit": "0 0",
      "revokedkeys": "none",
      "securitykeyprovider": "internal",
      "streamlocalbindmask": "0177",
      "streamlocalbindunlink": "no",
      "strictmodes": "yes",
      "subsystem": "sftp /usr/lib/openssh/sftp-server",
      "syslogfacility": "AUTH",
      "tcpkeepalive": "yes",
      "trustedusercakeys": "none",
      "usedns": "no",
      "usepam": "yes",
      "versionaddendum": "none",
      "x11displayoffset": "10",
      "x11forwarding": "yes",
      "x11uselocalhost": "yes",
      "xauthlocation": "/usr/bin/xauth"
    }
"""
from typing import Set, List, Dict
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.1'
    description = '`sshd` config file and `sshd -T` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'freebsd']
    magic_commands = ['sshd -T']
    tags = ['command', 'file']


__version__ = info.version


def _process(proc_data: JSONDictType) -> JSONDictType:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured to conform to the schema.
    """
    split_fields_space: Set[str] = {
        'authorizedkeysfile', 'include', 'ipqos', 'permitlisten', 'permitopen'
    }

    split_fields_comma: Set[str] = {
        'casignaturealgorithms', 'ciphers', 'gssapikexalgorithms', 'hostbasedacceptedalgorithms',
        'hostbasedacceptedkeytypes', 'hostkeyalgorithms', 'kexalgorithms', 'macs',
        'pubkeyacceptedalgorithms', 'pubkeyacceptedkeytypes'
    }

    int_list: Set[str] = {'clientalivecountmax', 'clientaliveinterval', 'logingracetime',
        'maxauthtries', 'maxsessions', 'maxstartups', 'maxstartups_rate', 'maxstartups_full',
        'rekeylimit', 'rekeylimit_time', 'x11displayoffset', 'x11maxdisplays'
    }

    dict_copy = proc_data.copy()
    for key, val in dict_copy.items():
        # this is a list value
        if key == 'acceptenv':
            new_list: List[str] = []
            for item in val:
                new_list.extend(item.split())
            proc_data[key] = new_list
            continue

        # this is a list value
        if key == 'include':
            new_list = []
            for item in val:
                new_list.extend(item.split())
            proc_data[key] = new_list
            continue

        if key == 'maxstartups':
            maxstart_split = val.split(':', maxsplit=2)
            proc_data[key] = maxstart_split[0]
            if len(maxstart_split) > 1:
                proc_data[key + '_rate'] = maxstart_split[1]
            if len(maxstart_split) > 2:
                proc_data[key + '_full'] = maxstart_split[2]
            continue

        if key == 'port':
            port_list: List[int] = []
            for item in val:
                port_list.append(int(item))
            proc_data[key] = port_list
            continue

        if key == 'rekeylimit':
            rekey_split = val.split(maxsplit=1)
            proc_data[key] = rekey_split[0]
            if len(rekey_split) > 1:
                proc_data[key + '_time'] = rekey_split[1]
            continue

        if key == 'subsystem':
            sub_split = val.split(maxsplit=1)
            proc_data[key] = sub_split[0]
            if len(sub_split) > 1:
                proc_data[key + '_command'] = sub_split[1]
            continue

        if key in split_fields_space:
            proc_data[key] = val.split()
            continue

        if key in split_fields_comma:
            proc_data[key] = val.split(',')
            continue

    for key, val in proc_data.items():
        if key in int_list:
            proc_data[key] = jc.utils.convert_to_int(val)

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

    multi_fields: Set[str] = {'acceptenv', 'hostkey', 'include', 'listenaddress', 'port'}

    modified_fields: Set[str] = {
        'casignaturealgorithms', 'ciphers', 'hostbasedacceptedalgorithms',
        'kexalgorithms', 'macs', 'pubkeyacceptedalgorithms'
    }

    modifiers: Set[str] = {'+', '-', '^'}

    match_block_found = False

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            # skip any lines with only whitespace
            if not line.strip():
                continue

            # support configuration file by skipping commented lines
            if line.strip().startswith('#'):
                continue

            # support configuration file by ignoring all lines between
            # Match xxx and Match any
            if line.strip().startswith('Match all'):
                match_block_found = False
                continue

            if line.strip().startswith('Match'):
                match_block_found = True
                continue

            if match_block_found:
                continue

            key, val = line.split(maxsplit=1)

            # support configuration file by converting to lower case
            key = key.lower()

            if key in multi_fields:
                if key not in raw_output:
                    raw_output[key] = []
                raw_output[key].append(val)
                continue

            if key in modified_fields and val[0] in modifiers:
                raw_output[key] = val[1:]
                raw_output[key + '_strategy'] = val[0]
                continue

            raw_output[key] = val
            continue

    return raw_output if raw else _process(raw_output)
