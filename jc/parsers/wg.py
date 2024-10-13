r"""jc - JSON Convert `wg` command output parser

Parses the output of the `wg show all dump` command, providing structured JSON output for easy integration and analysis.

Usage (cli):

    $ wg show all dump | jc --wg

or

    $ jc wg

Usage (module):

    import jc
    result = jc.parse('wg', wg_command_output)

Schema:

    [
      {
        "device": string,
        "privateKey": string,
        "publicKey": string,
        "listenPort": integer,
        "fwmark": integer,
        "peers": [
          {
            "publicKey": string,
            "presharedKey": string,
            "endpoint": string,
            "latestHandshake": integer,
            "transferRx": integer,
            "transferSx": integer,
            "persistentKeepalive": integer,
            "allowedIps": [string]
          }
        ]
      }
    ]

Examples:

    $ wg show all dump | jc --wg -p
    [
        {
            "device": "wg0",
            "privateKey": "aEbVdvHSEp3oofHDNVCsUoaRSxk1Og8/pTLof5yF+1M=",
            "publicKey": "OIxbQszw1chdO5uigAxpsl4fc/h04yMYafl72gUbakM=",
            "listenPort": 51820,
            "fwmark": null,
            "peers": {
                "sQFGAhSdx0aC7DmTFojzBOW8Ccjv1XV5+N9FnkZu5zc=": {
                    "presharedKey": null,
                    "endpoint": "79.134.136.199:40036",
                    "latestHandshake": 1728809756,
                    "transferRx": 1378724,
                    "transferSx": 406524,
                    "persistentKeepalive": null,
                    "allowedIps": ["10.10.0.2/32"]
                },
                "B9csmpvrv4Q7gpjc6zAbNNO8hIOYfpBqxmik2aNpwwE=": {
                    "presharedKey": null,
                    "endpoint": "79.134.136.199:35946",
                    "latestHandshake": 1728809756,
                    "transferRx": 4884248,
                    "transferSx": 3544596,
                    "persistentKeepalive": null,
                    "allowedIps": ["10.10.0.3/32"]
                },
                "miiSYR5UdevREhlWpmnci+vv/dEGLHbNtKu7u1CuOD4=": {
                    "presharedKey": null,
                    "allowedIps": ["10.10.0.4/32"]
                },
                "gx9+JHLHJvOfBNjTmZ8KQAnThFFiZMQrX1kRaYcIYzw=": {
                    "presharedKey": null,
                    "endpoint": "173.244.225.194:45014",
                    "latestHandshake": 1728809827,
                    "transferRx": 1363652,
                    "transferSx": 458252,
                    "persistentKeepalive": null,
                    "allowedIps": ["10.10.0.5/32"]
                }
            }
        }
    ]


    $ wg show all dump | jc --wg -p -r
    [
        {
            "device": "wg0",
            "privateKey": "aEbVdvHSEp3oofHDNVCsUoaRSxk1Og8/pTLof5yF+1M=",
            "publicKey": "OIxbQszw1chdO5uigAxpsl4fc/h04yMYafl72gUbakM=",
            "listenPort": 51820,
            "fwmark": null,
            "peers": {
                "sQFGAhSdx0aC7DmTFojzBOW8Ccjv1XV5+N9FnkZu5zc=": {
                    "presharedKey": null,
                    "endpoint": "79.134.136.199:40036",
                    "latestHandshake": 1728809756,
                    "transferRx": 1378724,
                    "transferSx": 406524,
                    "persistentKeepalive": -1,
                    "allowedIps": ["10.10.0.2/32"]
                },
                "B9csmpvrv4Q7gpjc6zAbNNO8hIOYfpBqxmik2aNpwwE=": {
                    "presharedKey": null,
                    "endpoint": "79.134.136.199:35946",
                    "latestHandshake": 1728809756,
                    "transferRx": 4884248,
                    "transferSx": 3544596,
                    "persistentKeepalive": -1,
                    "allowedIps": ["10.10.0.3/32"]
                },
                "miiSYR5UdevREhlWpmnci+vv/dEGLHbNtKu7u1CuOD4=": {
                    "presharedKey": null,
                    "allowedIps": ["10.10.0.4/32"]
                },
                "gx9+JHLHJvOfBNjTmZ8KQAnThFFiZMQrX1kRaYcIYzw=": {
                    "presharedKey": null,
                    "endpoint": "173.244.225.194:45014",
                    "latestHandshake": 1728809827,
                    "transferRx": 1363652,
                    "transferSx": 458252,
                    "persistentKeepalive": -1,
                    "allowedIps": ["10.10.0.5/32"]
                }
            }
        }
    ]
"""

from typing import List, Dict, Optional, Union
from jc.jc_types import JSONDictType
import jc.utils

PeerData = Dict[str, Union[Optional[str], Optional[int], List[str]]]
DeviceData = Dict[str, Union[Optional[str], Optional[int], Dict[str, PeerData]]]

class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'Parses the output of the `wg` command to provide structured JSON data'
    author = 'Hamza Saht'
    author_email = 'hamzasaht01@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['command']
    magic_commands = ['wg']


__version__ = info.version

def _process(proc_data: List[DeviceData]) -> List[JSONDictType]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List[Dict]) Raw structured data to process

    Returns:

        List[Dict]: Structured data that conforms to the schema
    """
    processed_data: List[JSONDictType] = []
    for device in proc_data:
        processed_device = {
            "device": device["device"],
            "privateKey": device.get("privateKey"),
            "publicKey": device.get("publicKey"),
            "listenPort": device.get("listenPort"),
            "fwmark": device.get("fwmark"),
            "peers": [
                {
                    "publicKey": peer_key,
                    "presharedKey": peer_data.get("presharedKey"),
                    "endpoint": peer_data.get("endpoint"),
                    "latestHandshake": peer_data.get("latestHandshake", 0),
                    "transferRx": peer_data.get("transferRx", 0),
                    "transferSx": peer_data.get("transferSx", 0),
                    "persistentKeepalive": peer_data.get("persistentKeepalive", -1),
                    "allowedIps": peer_data.get("allowedIps", [])
                }
                for peer_key, peer_data in device.get("peers", {}).items()
            ]
        }
        processed_data.append(processed_device)
    return processed_data

def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> List[DeviceData]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = line.split('\t')
            if len(fields) == 5:  
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "privateKey": private_key if private_key != "(none)" else None,
                    "publicKey": public_key if public_key != "(none)" else None,
                    "listenPort": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {}
                }
            elif len(fields) == 9:  
                interface, public_key, preshared_key, endpoint, allowed_ips, latest_handshake, transfer_rx, transfer_tx, persistent_keepalive = fields
                peer_data: PeerData = {
                    "presharedKey": preshared_key if preshared_key != "(none)" else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latestHandshake": int(latest_handshake),
                    "transferRx": int(transfer_rx),
                    "transferSx": int(transfer_tx),
                    "persistentKeepalive": int(persistent_keepalive) if persistent_keepalive != "off" else -1,
                    "allowedIps": allowed_ips.split(',') if allowed_ips != "(none)" else []
                }
                device_data["peers"][public_key] = {k: v for k, v in peer_data.items() if v is not None}

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)

