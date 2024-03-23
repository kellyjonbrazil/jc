[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.ssh_conf"></a>

# jc.parsers.ssh_conf

jc - JSON Convert `ssh` configuration file and `ssh -G` command output parser

This parser will work with `ssh` configuration files or the output of
`ssh -G`. Any `Match` blocks in the `ssh` configuration file will be
ignored.

Usage (cli):

    $ ssh -G hostname | jc --ssh-conf

or

    $ jc ssh -G hostname

or

    $ cat ~/.ssh/config | jc --ssh-conf

Usage (module):

    import jc
    result = jc.parse('ssh_conf', ssh_conf_output)

Schema:

    [
      {
        "host":                                       string,
        "host_list": [
                                                      string
        ],
        "addkeystoagent":                             string,
        "addressfamily":                              string,
        "batchmode":                                  string,
        "bindaddress":                                string,
        "bindinterface":                              string,
        "canonicaldomains": [
                                                      string
        ],
        "canonicalizefallbacklocal":                  string,
        "canonicalizehostname":                       string,
        "canonicalizemaxdots":                        integer,
        "canonicalizepermittedcnames": [
                                                      string
        ],
        "casignaturealgorithms": [
                                                      string
        ],
        "certificatefile": [
                                                      string
        ],
        "checkhostip":                                string,
        "ciphers": [
                                                      string
        ],
        "clearallforwardings":                        string,
        "compression":                                string,
        "connectionattempts":                         integer,
        "connecttimeout":                             integer,
        "controlmaster":                              string,
        "controlpath":                                string,
        "controlpersist":                             string,
        "dynamicforward":                             string,
        "enableescapecommandline":                    string,
        "enablesshkeysign":                           string,
        "escapechar":                                 string,
        "exitonforwardfailure":                       string,
        "fingerprinthash":                            string,
        "forkafterauthentication":                    string,
        "forwardagent":                               string,
        "forwardx11":                                 string,
        "forwardx11timeout":                          integer,
        "forwardx11trusted":                          string,
        "gatewayports":                               string,
        "globalknownhostsfile": [
                                                      string
        ],
        "gssapiauthentication":                       string,
        "gssapidelegatecredentials":                  string,
        "hashknownhosts":                             string,
        "hostbasedacceptedalgorithms": [
                                                      string
        ],
        "hostbasedauthentication":                    string,
        "hostkeyalgorithms": [
                                                      string
        ],
        "hostkeyalias":                               string,
        "hostname":                                   string,
        "identitiesonly":                             string,
        "identityagent":                              string,
        "identityfile": [
                                                      string
        ],
        "ignoreunknown":                              string,
        "include": [
                                                      string
        ],
        "ipqos": [
                                                      string
        ],
        "kbdinteractiveauthentication":               string,
        "kbdinteractivedevices": [
                                                      string
        ],
        "kexalgorithms": [
                                                      string
        ],
        "kexalgorithms_strategy":                     string,
        "knownhostscommand":                          string,
        "localcommand":                               string,
        "localforward": [
                                                      string
        ],
        "loglevel":                                   string,
        "logverbose": [
                                                      string
        ],
        "macs": [
                                                      string
        ],
        "macs_strategy":                              string,
        "nohostauthenticationforlocalhost":           string,
        "numberofpasswordprompts":                    integer,
        "passwordauthentication":                     string,
        "permitlocalcommand":                         string,
        "permitremoteopen": [
                                                      string
        ],
        "pkcs11provider":                             string,
        "port":                                       integer,
        "preferredauthentications": [
                                                      string
        ],
        "protocol":                                   integer,
        "proxycommand":                               string,
        "proxyjump": [
                                                      string
        ],
        "proxyusefdpass":                             string,
        "pubkeyacceptedalgorithms": [
                                                      string
        ],
        "pubkeyacceptedalgorithms_strategy":          string,
        "pubkeyauthentication":                       string,
        "rekeylimit":                                 string,
        "remotecommand":                              string,
        "remoteforward":                              string,
        "requesttty":                                 string,
        "requiredrsasize":                            integer,
        "revokedhostkeys":                            string,
        "securitykeyprovider":                        string,
        "sendenv": [
                                                      string
        ],
        "serveralivecountmax":                        integer,
        "serveraliveinterval":                        integer,
        "sessiontype":                                string,
        "setenv": [
                                                      string
        ],
        "stdinnull":                                  string,
        "streamlocalbindmask":                        string,
        "streamlocalbindunlink":                      string,
        "stricthostkeychecking":                      string,
        "syslogfacility":                             string,
        "tcpkeepalive":                               string,
        "tunnel":                                     string,
        "tunneldevice":                               string,
        "updatehostkeys":                             string,
        "user":                                       string,
        "userknownhostsfile": [
                                                      string
        ],
        "verifyhostkeydns":                           string,
        "visualhostkey":                              string,
        "xauthlocation":                              string
      }
    ]

Examples:

    $ ssh -G - | jc --ssh-conf -p
    [
      {
        "user": "foo",
        "hostname": "-",
        "port": 22,
        "addressfamily": "any",
        "batchmode": "no",
        "canonicalizefallbacklocal": "yes",
        "canonicalizehostname": "false",
        "checkhostip": "no",
        "compression": "no",
        "controlmaster": "false",
        "enablesshkeysign": "no",
        "clearallforwardings": "no",
        "exitonforwardfailure": "no",
        "fingerprinthash": "SHA256",
        "forwardx11": "no",
        "forwardx11trusted": "no",
        "gatewayports": "no",
        "gssapiauthentication": "no",
        "gssapidelegatecredentials": "no",
        "hashknownhosts": "no",
        "hostbasedauthentication": "no",
        "identitiesonly": "no",
        "kbdinteractiveauthentication": "yes",
        "nohostauthenticationforlocalhost": "no",
        "passwordauthentication": "yes",
        "permitlocalcommand": "no",
        "proxyusefdpass": "no",
        "pubkeyauthentication": "true",
        "requesttty": "auto",
        "sessiontype": "default",
        "stdinnull": "no",
        "forkafterauthentication": "no",
        "streamlocalbindunlink": "no",
        "stricthostkeychecking": "ask",
        "tcpkeepalive": "yes",
        "tunnel": "false",
        "verifyhostkeydns": "false",
        "visualhostkey": "no",
        "updatehostkeys": "true",
        "applemultipath": "no",
        "canonicalizemaxdots": 1,
        "connectionattempts": 1,
        "forwardx11timeout": 1200,
        "numberofpasswordprompts": 3,
        "serveralivecountmax": 3,
        "serveraliveinterval": 0,
        "ciphers": [
          "chacha20-poly1305@openssh.com",
          "aes128-ctr",
          "aes192-ctr",
          "aes256-ctr",
          "aes128-gcm@openssh.com",
          "aes256-gcm@openssh.com"
        ],
        "hostkeyalgorithms": [
          "ssh-ed25519-cert-v01@openssh.com",
          "ecdsa-sha2-nistp256-cert-v01@openssh.com",
          "ecdsa-sha2-nistp384-cert-v01@openssh.com",
          "ecdsa-sha2-nistp521-cert-v01@openssh.com",
          "rsa-sha2-512-cert-v01@openssh.com",
          "rsa-sha2-256-cert-v01@openssh.com",
          "ssh-ed25519",
          "ecdsa-sha2-nistp256",
          "ecdsa-sha2-nistp384",
          "ecdsa-sha2-nistp521",
          "rsa-sha2-512",
          "rsa-sha2-256"
        ],
        "hostbasedacceptedalgorithms": [
          "ssh-ed25519-cert-v01@openssh.com",
          "ecdsa-sha2-nistp256-cert-v01@openssh.com",
          "ecdsa-sha2-nistp384-cert-v01@openssh.com",
          "ecdsa-sha2-nistp521-cert-v01@openssh.com",
          "rsa-sha2-512-cert-v01@openssh.com",
          "rsa-sha2-256-cert-v01@openssh.com",
          "ssh-ed25519",
          "ecdsa-sha2-nistp256",
          "ecdsa-sha2-nistp384",
          "ecdsa-sha2-nistp521",
          "rsa-sha2-512",
          "rsa-sha2-256"
        ],
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
        "casignaturealgorithms": [
          "ssh-ed25519",
          "ecdsa-sha2-nistp256",
          "ecdsa-sha2-nistp384",
          "ecdsa-sha2-nistp521",
          "rsa-sha2-512",
          "rsa-sha2-256"
        ],
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
        "securitykeyprovider": "$SSH_SK_PROVIDER",
        "pubkeyacceptedalgorithms": [
          "ssh-ed25519-cert-v01@openssh.com",
          "ecdsa-sha2-nistp256-cert-v01@openssh.com",
          "ecdsa-sha2-nistp384-cert-v01@openssh.com",
          "ecdsa-sha2-nistp521-cert-v01@openssh.com",
          "rsa-sha2-512-cert-v01@openssh.com",
          "rsa-sha2-256-cert-v01@openssh.com",
          "ssh-ed25519",
          "ecdsa-sha2-nistp256",
          "ecdsa-sha2-nistp384",
          "ecdsa-sha2-nistp521",
          "rsa-sha2-512",
          "rsa-sha2-256"
        ],
        "xauthlocation": "/usr/X11R6/bin/xauth",
        "identityfile": [
          "~/.ssh/id_rsa",
          "~/.ssh/id_ecdsa",
          "~/.ssh/id_ecdsa_sk",
          "~/.ssh/id_ed25519",
          "~/.ssh/id_ed25519_sk",
          "~/.ssh/id_xmss",
          "~/.ssh/id_dsa"
        ],
        "canonicaldomains": [
          "none"
        ],
        "globalknownhostsfile": [
          "/etc/ssh/ssh_known_hosts",
          "/etc/ssh/ssh_known_hosts2"
        ],
        "userknownhostsfile": [
          "/Users/foo/.ssh/known_hosts",
          "/Users/foo/.ssh/known_hosts2"
        ],
        "sendenv": [
          "LANG",
          "LC_*"
        ],
        "logverbose": [
          "none"
        ],
        "permitremoteopen": [
          "any"
        ],
        "addkeystoagent": "false",
        "forwardagent": "no",
        "connecttimeout": null,
        "tunneldevice": "any:any",
        "canonicalizepermittedcnames": [
          "none"
        ],
        "controlpersist": "no",
        "escapechar": "~",
        "ipqos": [
          "af21",
          "cs1"
        ],
        "rekeylimit": "0 0",
        "streamlocalbindmask": "0177",
        "syslogfacility": "USER"
      }
    ]

    $ cat ~/.ssh/config | jc --ssh-conf -p
    [
      {
        "host": "server1",
        "host_list": [
          "server1"
        ],
        "hostname": "server1.cyberciti.biz",
        "user": "nixcraft",
        "port": 4242,
        "identityfile": [
          "/nfs/shared/users/nixcraft/keys/server1/id_rsa"
        ]
      },
      {
        "host": "nas01",
        "host_list": [
          "nas01"
        ],
        "hostname": "192.168.1.100",
        "user": "root",
        "identityfile": [
          "~/.ssh/nas01.key"
        ]
      },
      {
        "host": "aws.apache",
        "host_list": [
          "aws.apache"
        ],
        "hostname": "1.2.3.4",
        "user": "wwwdata",
        "identityfile": [
          "~/.ssh/aws.apache.key"
        ]
      },
      {
        "host": "uk.gw.lan uk.lan",
        "host_list": [
          "uk.gw.lan",
          "uk.lan"
        ],
        "hostname": "192.168.0.251",
        "user": "nixcraft",
        "proxycommand": "ssh nixcraft@gateway.uk.cyberciti.biz nc %h %p 2> /dev/null"
      },
      {
        "host": "proxyus",
        "host_list": [
          "proxyus"
        ],
        "hostname": "vps1.cyberciti.biz",
        "user": "breakfree",
        "identityfile": [
          "~/.ssh/vps1.cyberciti.biz.key"
        ],
        "localforward": [
          "3128 127.0.0.1:3128"
        ]
      },
      {
        "host": "*",
        "host_list": [
          "*"
        ],
        "forwardagent": "no",
        "forwardx11": "no",
        "forwardx11trusted": "yes",
        "user": "nixcraft",
        "port": 22,
        "protocol": 2,
        "serveraliveinterval": 60,
        "serveralivecountmax": 30
      }
    ]

    $ cat ~/.ssh/config | jc --ssh-conf -p -r
    [
      {
        "host": "server1",
        "host_list": [
          "server1"
        ],
        "hostname": "server1.cyberciti.biz",
        "user": "nixcraft",
        "port": "4242",
        "identityfile": [
          "/nfs/shared/users/nixcraft/keys/server1/id_rsa"
        ]
      },
      {
        "host": "nas01",
        "host_list": [
          "nas01"
        ],
        "hostname": "192.168.1.100",
        "user": "root",
        "identityfile": [
          "~/.ssh/nas01.key"
        ]
      },
      {
        "host": "aws.apache",
        "host_list": [
          "aws.apache"
        ],
        "hostname": "1.2.3.4",
        "user": "wwwdata",
        "identityfile": [
          "~/.ssh/aws.apache.key"
        ]
      },
      {
        "host": "uk.gw.lan uk.lan",
        "host_list": [
          "uk.gw.lan",
          "uk.lan"
        ],
        "hostname": "192.168.0.251",
        "user": "nixcraft",
        "proxycommand": "ssh nixcraft@gateway.uk.cyberciti.biz nc %h %p 2> /dev/null"
      },
      {
        "host": "proxyus",
        "host_list": [
          "proxyus"
        ],
        "hostname": "vps1.cyberciti.biz",
        "user": "breakfree",
        "identityfile": [
          "~/.ssh/vps1.cyberciti.biz.key"
        ],
        "localforward": [
          "3128 127.0.0.1:3128"
        ]
      },
      {
        "host": "*",
        "host_list": [
          "*"
        ],
        "forwardagent": "no",
        "forwardx11": "no",
        "forwardx11trusted": "yes",
        "user": "nixcraft",
        "port": "22",
        "protocol": "2",
        "serveraliveinterval": "60",
        "serveralivecountmax": "30"
      }
    ]

<a id="jc.parsers.ssh_conf.parse"></a>

### parse

```python
def parse(data: str,
          raw: bool = False,
          quiet: bool = False) -> List[Dict[str, Any]]
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

### Parser Information
Compatibility:  linux, darwin, freebsd

Source: [`jc/parsers/ssh_conf.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/ssh_conf.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
