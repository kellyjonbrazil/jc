[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.ip_address"></a>

# jc.parsers.ip\_address

jc - JSON Convert IP Address string parser

Accepts standard and integer IP address notation for both IPv4 and IPv6
addresses. CIDR subnet mask and Scope ID is also allowed for standard
notation. See examples below.

Usage (cli):

    $ echo '192.168.1.1' | jc --ip-address

Usage (module):

    import jc
    result = jc.parse('ip_address', ip_address_string)

Schema:

    {
      "version":                  integer,
      "max_prefix_length":        integer,
      "ip":                       string,
      "ip_compressed":            string,
      "ip_exploded":              string,
      "ip_split": [
                                  string
      ],
      "scope_id":                 string/null,
      "ipv4_mapped":              string/null,
      "six_to_four":              string/null,
      "teredo_client":            string/null,
      "teredo_server":            string/null,
      "dns_ptr":                  string,
      "network":                  string,
      "broadcast":                string,
      "hostmask":                 string,
      "netmask":                  string,
      "cidr_netmask":             integer,
      "hosts":                    integer,
      "first_host":               string,
      "last_host":                string,
      "is_multicast":             boolean,
      "is_private":               boolean,
      "is_global":                boolean,
      "is_link_local":            boolean,
      "is_loopback":              boolean,
      "is_reserved":              boolean,
      "is_unspecified":           boolean,
      "int": {
        "ip":                     integer,
        "network":                integer,
        "broadcast":              integer,
        "first_host":             integer,
        "last_host":              integer
      },
      "hex": {
        "ip":                     string,
        "network":                string,
        "broadcast":              string,
        "hostmask":               string,
        "netmask":                string,
        "first_host":             string,
        "last_host":              string
      },
      "bin": {
        "ip":                     string,
        "network":                string,
        "broadcast":              string,
        "hostmask":               string,
        "netmask":                string,
        "first_host":             string,
        "last_host":              string
      }
    }

Examples:

    $ echo 192.168.2.10/24 | jc --ip-address -p
    {
      "version": 4,
      "max_prefix_length": 32,
      "ip": "192.168.2.10",
      "ip_compressed": "192.168.2.10",
      "ip_exploded": "192.168.2.10",
      "ip_split": [
        "192",
        "168",
        "2",
        "10"
      ],
      "scope_id": null,
      "ipv4_mapped": null,
      "six_to_four": null,
      "teredo_client": null,
      "teredo_server": null,
      "dns_ptr": "10.2.168.192.in-addr.arpa",
      "network": "192.168.2.0",
      "broadcast": "192.168.2.255",
      "hostmask": "0.0.0.255",
      "netmask": "255.255.255.0",
      "cidr_netmask": 24,
      "hosts": 254,
      "first_host": "192.168.2.1",
      "last_host": "192.168.2.254",
      "is_multicast": false,
      "is_private": true,
      "is_global": false,
      "is_link_local": false,
      "is_loopback": false,
      "is_reserved": false,
      "is_unspecified": false,
      "int": {
        "ip": 3232236042,
        "network": 3232236032,
        "broadcast": 3232236287,
        "first_host": 3232236033,
        "last_host": 3232236286
      },
      "hex": {
        "ip": "c0:a8:02:0a",
        "network": "c0:a8:02:00",
        "broadcast": "c0:a8:02:ff",
        "hostmask": "00:00:00:ff",
        "netmask": "ff:ff:ff:00",
        "first_host": "c0:a8:02:01",
        "last_host": "c0:a8:02:fe"
      },
      "bin": {
        "ip": "11000000101010000000001000001010",
        "network": "11000000101010000000001000000000",
        "broadcast": "11000000101010000000001011111111",
        "hostmask": "00000000000000000000000011111111",
        "netmask": "11111111111111111111111100000000",
        "first_host": "11000000101010000000001000000001",
        "last_host": "11000000101010000000001011111110"
      }
    }

    $ echo 3232236042 | jc --ip-address -p
    {
      "version": 4,
      "max_prefix_length": 32,
      "ip": "192.168.2.10",
      "ip_compressed": "192.168.2.10",
      "ip_exploded": "192.168.2.10",
      "ip_split": [
        "192",
        "168",
        "2",
        "10"
      ],
      "scope_id": null,
      "ipv4_mapped": null,
      "six_to_four": null,
      "teredo_client": null,
      "teredo_server": null,
      "dns_ptr": "10.2.168.192.in-addr.arpa",
      "network": "192.168.2.10",
      "broadcast": "192.168.2.10",
      "hostmask": "0.0.0.0",
      "netmask": "255.255.255.255",
      "cidr_netmask": 32,
      "hosts": 1,
      "first_host": "192.168.2.10",
      "last_host": "192.168.2.10",
      "is_multicast": false,
      "is_private": true,
      "is_global": false,
      "is_link_local": false,
      "is_loopback": false,
      "is_reserved": false,
      "is_unspecified": false,
      "int": {
        "ip": 3232236042,
        "network": 3232236042,
        "broadcast": 3232236042,
        "first_host": 3232236042,
        "last_host": 3232236042
      },
      "hex": {
        "ip": "c0:a8:02:0a",
        "network": "c0:a8:02:0a",
        "broadcast": "c0:a8:02:0a",
        "hostmask": "00:00:00:00",
        "netmask": "ff:ff:ff:ff",
        "first_host": "c0:a8:02:0a",
        "last_host": "c0:a8:02:0a"
      },
      "bin": {
        "ip": "11000000101010000000001000001010",
        "network": "11000000101010000000001000001010",
        "broadcast": "11000000101010000000001000001010",
        "hostmask": "00000000000000000000000000000000",
        "netmask": "11111111111111111111111111111111",
        "first_host": "11000000101010000000001000001010",
        "last_host": "11000000101010000000001000001010"
      }
    }

    $ echo 127:0:de::1%128/96 | jc --ip-address -p
    {
      "version": 6,
      "max_prefix_length": 128,
      "ip": "127:0:de::1",
      "ip_compressed": "127:0:de::1",
      "ip_exploded": "0127:0000:00de:0000:0000:0000:0000:0001",
      "ip_split": [
        "0127",
        "0000",
        "00de",
        "0000",
        "0000",
        "0000",
        "0000",
        "0001"
      ],
      "scope_id": "128",
      "ipv4_mapped": null,
      "six_to_four": null,
      "teredo_client": null,
      "teredo_server": null,
      "dns_ptr": "1.0.0.0.0.0...0.0.0.e.d.0.0.0.0.0.0.7.2.1.0.ip6.arpa",
      "network": "127:0:de::",
      "broadcast": "127:0:de::ffff:ffff",
      "hostmask": "::ffff:ffff",
      "netmask": "ffff:ffff:ffff:ffff:ffff:ffff::",
      "cidr_netmask": 96,
      "hosts": 4294967294,
      "first_host": "127:0:de::1",
      "last_host": "127:0:de::ffff:fffe",
      "is_multicast": false,
      "is_private": false,
      "is_global": true,
      "is_link_local": false,
      "is_loopback": false,
      "is_reserved": true,
      "is_unspecified": false,
      "int": {
        "ip": 1531727573536155682370944093904699393,
        "network": 1531727573536155682370944093904699392,
        "broadcast": 1531727573536155682370944098199666687,
        "first_host": 1531727573536155682370944093904699393,
        "last_host": 1531727573536155682370944098199666686
      },
      "hex": {
        "ip": "01:27:00:00:00:de:00:00:00:00:00:00:00:00:00:01",
        "network": "01:27:00:00:00:de:00:00:00:00:00:00:00:00:00:00",
        "broadcast": "01:27:00:00:00:de:00:00:00:00:00:00:ff:ff:ff:ff",
        "hostmask": "00:00:00:00:00:00:00:00:00:00:00:00:ff:ff:ff:ff",
        "netmask": "ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:00:00:00:00",
        "first_host": "01:27:00:00:00:de:00:00:00:00:00:00:00:00:00:01",
        "last_host": "01:27:00:00:00:de:00:00:00:00:00:00:ff:ff:ff:fe"
      },
      "bin": {
        "ip": "0000000100100111000000000000000000000000110...000000000001",
        "network": "00000001001001110000000000000000000000...000000000000",
        "broadcast": "000000010010011100000000000000000000...111111111111",
        "hostmask": "0000000000000000000000000000000000000...111111111111",
        "netmask": "11111111111111111111111111111111111111...000000000000",
        "first_host": "00000001001001110000000000000000000...000000000001",
        "last_host": "000000010010011100000000000000000000...1111111111110"
      }
    }

    $ echo 1531727573536155682370944093904699393 | jc --ip-address -p
    {
      "version": 6,
      "max_prefix_length": 128,
      "ip": "127:0:de::1",
      "ip_compressed": "127:0:de::1",
      "ip_exploded": "0127:0000:00de:0000:0000:0000:0000:0001",
      "ip_split": [
        "0127",
        "0000",
        "00de",
        "0000",
        "0000",
        "0000",
        "0000",
        "0001"
      ],
      "scope_id": null,
      "ipv4_mapped": null,
      "six_to_four": null,
      "teredo_client": null,
      "teredo_server": null,
      "dns_ptr": "1.0.0.0.0.0....0.0.0.0.e.d.0.0.0.0.0.0.7.2.1.0.ip6.arpa",
      "network": "127:0:de::1",
      "broadcast": "127:0:de::1",
      "hostmask": "::",
      "netmask": "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff",
      "cidr_netmask": 128,
      "hosts": 1,
      "first_host": "127:0:de::1",
      "last_host": "127:0:de::1",
      "is_multicast": false,
      "is_private": false,
      "is_global": true,
      "is_link_local": false,
      "is_loopback": false,
      "is_reserved": true,
      "is_unspecified": false,
      "int": {
        "ip": 1531727573536155682370944093904699393,
        "network": 1531727573536155682370944093904699393,
        "broadcast": 1531727573536155682370944093904699393,
        "first_host": 1531727573536155682370944093904699393,
        "last_host": 1531727573536155682370944093904699393
      },
      "hex": {
        "ip": "01:27:00:00:00:de:00:00:00:00:00:00:00:00:00:01",
        "network": "01:27:00:00:00:de:00:00:00:00:00:00:00:00:00:01",
        "broadcast": "01:27:00:00:00:de:00:00:00:00:00:00:00:00:00:01",
        "hostmask": "00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00",
        "netmask": "ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff",
        "first_host": "01:27:00:00:00:de:00:00:00:00:00:00:00:00:00:01",
        "last_host": "01:27:00:00:00:de:00:00:00:00:00:00:00:00:00:01"
      },
      "bin": {
        "ip": "0000000100100111000000000000000000000000110111100...000001",
        "network": "00000001001001110000000000000000000000001101...000001",
        "broadcast": "000000010010011100000000000000000000000011...000001",
        "hostmask": "0000000000000000000000000000000000000000000...000000",
        "netmask": "11111111111111111111111111111111111111111111...111111",
        "first_host": "00000001001001110000000000000000000000001...000001",
        "last_host": "000000010010011100000000000000000000000011...0000001"
      }
    }

    # IPv4 Mapped Address
    $ echo ::FFFF:192.168.1.35 | jc --ip-address -p
    {
      "version": 6,
      "max_prefix_length": 128,
      "ip": "::ffff:c0a8:123",
      "ip_compressed": "::ffff:c0a8:123",
      "ip_exploded": "0000:0000:0000:0000:0000:ffff:c0a8:0123",
      "ip_split": [
        "0000",
        "0000",
        "0000",
        "0000",
        "0000",
        "ffff",
        "c0a8",
        "0123"
      ],
      "scope_id": null,
      "ipv4_mapped": "192.168.1.35",
      "six_to_four": null,
      "teredo_client": null,
      "teredo_server": null,
      "dns_ptr": "3.2.1.0.8.a.0.c.f.f.f.f.0.0....0.0.0.0.0.0.ip6.arpa",
      "network": "::ffff:c0a8:123",
      "broadcast": "::ffff:c0a8:123",
      "hostmask": "::",
      "netmask": "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff",
      "cidr_netmask": 128,
      "hosts": 1,
      "first_host": "::ffff:c0a8:123",
      "last_host": "::ffff:c0a8:123",
      "is_multicast": false,
      "is_private": true,
      "is_global": false,
      "is_link_local": false,
      "is_loopback": false,
      "is_reserved": true,
      "is_unspecified": false,
      "int": {
        "ip": 281473913979171,
        "network": 281473913979171,
        "broadcast": 281473913979171,
        "first_host": 281473913979171,
        "last_host": 281473913979171
      },
      "hex": {
        "ip": "00:00:00:00:00:00:00:00:00:00:ff:ff:c0:a8:01:23",
        "network": "00:00:00:00:00:00:00:00:00:00:ff:ff:c0:a8:01:23",
        "broadcast": "00:00:00:00:00:00:00:00:00:00:ff:ff:c0:a8:01:23",
        "hostmask": "00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00",
        "netmask": "ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff",
        "first_host": "00:00:00:00:00:00:00:00:00:00:ff:ff:c0:a8:01:23",
        "last_host": "00:00:00:00:00:00:00:00:00:00:ff:ff:c0:a8:01:23"
      },
      "bin": {
        "ip": "000000000000000000000000000000000000000000000...100100011",
        "network": "0000000000000000000000000000000000000000...000100011",
        "broadcast": "00000000000000000000000000000000000000...000100011",
        "hostmask": "000000000000000000000000000000000000000...000000000",
        "netmask": "1111111111111111111111111111111111111111...111111111",
        "first_host": "0000000000000000000000000000000000000...100100011",
        "last_host": "00000000000000000000000000000000000000...0100100011"
      }
    }

    # 6to4 Address
    $ echo 2002:c000:204::/48 | jc --ip-address -p
    {
      "version": 6,
      "max_prefix_length": 128,
      "ip": "2002:c000:204::",
      "ip_compressed": "2002:c000:204::",
      "ip_exploded": "2002:c000:0204:0000:0000:0000:0000:0000",
      "ip_split": [
        "2002",
        "c000",
        "0204",
        "0000",
        "0000",
        "0000",
        "0000",
        "0000"
      ],
      "scope_id": null,
      "ipv4_mapped": null,
      "six_to_four": "192.0.2.4",
      "teredo_client": null,
      "teredo_server": null,
      "dns_ptr": "0.0.0.0.0.0.0...0.0.0.4.0.2.0.0.0.0.c.2.0.0.2.ip6.arpa",
      "network": "2002:c000:204::",
      "broadcast": "2002:c000:204:ffff:ffff:ffff:ffff:ffff",
      "hostmask": "::ffff:ffff:ffff:ffff:ffff",
      "netmask": "ffff:ffff:ffff::",
      "cidr_netmask": 48,
      "hosts": 1208925819614629174706174,
      "first_host": "2002:c000:204::1",
      "last_host": "2002:c000:204:ffff:ffff:ffff:ffff:fffe",
      "is_multicast": false,
      "is_private": false,
      "is_global": true,
      "is_link_local": false,
      "is_loopback": false,
      "is_reserved": false,
      "is_unspecified": false,
      "int": {
        "ip": 42549574682102084431821433448024768512,
        "network": 42549574682102084431821433448024768512,
        "broadcast": 42549574682103293357641048077199474687,
        "first_host": 42549574682102084431821433448024768513,
        "last_host": 42549574682103293357641048077199474686
      },
      "hex": {
        "ip": "20:02:c0:00:02:04:00:00:00:00:00:00:00:00:00:00",
        "network": "20:02:c0:00:02:04:00:00:00:00:00:00:00:00:00:00",
        "broadcast": "20:02:c0:00:02:04:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff",
        "hostmask": "00:00:00:00:00:00:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff",
        "netmask": "ff:ff:ff:ff:ff:ff:00:00:00:00:00:00:00:00:00:00",
        "first_host": "20:02:c0:00:02:04:00:00:00:00:00:00:00:00:00:01",
        "last_host": "20:02:c0:00:02:04:ff:ff:ff:ff:ff:ff:ff:ff:ff:fe"
      },
      "bin": {
        "ip": "00100000000000101100000000000000000000100000010...00000000",
        "network": "001000000000001011000000000000000000001000...00000000",
        "broadcast": "0010000000000010110000000000000000000010...11111111",
        "hostmask": "00000000000000000000000000000000000000000...11111111",
        "netmask": "111111111111111111111111111111111111111111...00000000",
        "first_host": "001000000000001011000000000000000000001...00000001",
        "last_host": "0010000000000010110000000000000000000010...111111110"
      }
    }

    # Teredo Address
    $ echo 2001:0000:4136:e378:8000:63bf:3fff:fdd2 | jc --ip-address -p
    {
      "version": 6,
      "max_prefix_length": 128,
      "ip": "2001:0:4136:e378:8000:63bf:3fff:fdd2",
      "ip_compressed": "2001:0:4136:e378:8000:63bf:3fff:fdd2",
      "ip_exploded": "2001:0000:4136:e378:8000:63bf:3fff:fdd2",
      "ip_split": [
        "2001",
        "0000",
        "4136",
        "e378",
        "8000",
        "63bf",
        "3fff",
        "fdd2"
      ],
      "scope_id": null,
      "ipv4_mapped": null,
      "six_to_four": null,
      "teredo_client": "192.0.2.45",
      "teredo_server": "65.54.227.120",
      "dns_ptr": "2.d.d.f.f.f.f.3.f.b.3.6.0.0.0.8.8....0.1.0.0.2.ip6.arpa",
      "network": "2001:0:4136:e378:8000:63bf:3fff:fdd2",
      "broadcast": "2001:0:4136:e378:8000:63bf:3fff:fdd2",
      "hostmask": "::",
      "netmask": "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff",
      "cidr_netmask": 128,
      "hosts": 1,
      "first_host": "2001:0:4136:e378:8000:63bf:3fff:fdd2",
      "last_host": "2001:0:4136:e378:8000:63bf:3fff:fdd2",
      "is_multicast": false,
      "is_private": true,
      "is_global": false,
      "is_link_local": false,
      "is_loopback": false,
      "is_reserved": false,
      "is_unspecified": false,
      "int": {
        "ip": 42540488182158724593221357832373272018,
        "network": 42540488182158724593221357832373272018,
        "broadcast": 42540488182158724593221357832373272018,
        "first_host": 42540488182158724593221357832373272018,
        "last_host": 42540488182158724593221357832373272018
      },
      "hex": {
        "ip": "20:01:00:00:41:36:e3:78:80:00:63:bf:3f:ff:fd:d2",
        "network": "20:01:00:00:41:36:e3:78:80:00:63:bf:3f:ff:fd:d2",
        "broadcast": "20:01:00:00:41:36:e3:78:80:00:63:bf:3f:ff:fd:d2",
        "hostmask": "00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00",
        "netmask": "ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff",
        "first_host": "20:01:00:00:41:36:e3:78:80:00:63:bf:3f:ff:fd:d2",
        "last_host": "20:01:00:00:41:36:e3:78:80:00:63:bf:3f:ff:fd:d2"
      },
      "bin": {
        "ip": "0010000000000001000000000000000001000001001...110111010010",
        "network": "00100000000000010000000000000000010000...110111010010",
        "broadcast": "001000000000000100000000000000000100...110111010010",
        "hostmask": "0000000000000000000000000000000000000...000000000000",
        "netmask": "11111111111111111111111111111111111111...111111111111",
        "first_host": "00100000000000010000000000000000010...110111010010",
        "last_host": "001000000000000100000000000000000100...110111010010"
      }
    }

<a id="jc.parsers.ip_address.parse"></a>

### parse

```python
def parse(data: str, raw: bool = False, quiet: bool = False) -> Dict
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    Dictionary. Raw or processed structured data.

### Parser Information
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Source: [`jc/parsers/ip_address.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/ip_address.py)

Version 1.3 by Kelly Brazil (kellyjonbrazil@gmail.com)
