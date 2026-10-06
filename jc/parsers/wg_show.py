r"""jc - JSON Convert `wg show` command output parser

Parses the output of the `wg show all dump` command, providing structured JSON output for easy integration and analysis.

Usage (cli):

    $ wg show all dump | jc --wg-show

or

    $ jc wg show all dump

Usage (module):

    import jc
    result = jc.parse('wg-show', wg_command_output)

Schema:

    [
      {
        "device":                       string,
        "private_key":                  string,
        "public_key":                   string,
        "listen_port":                  integer,
        "fwmark":                       integer,
        "peers": [
          {
            "public_key":               string,
            "preshared_key":            string,
            "endpoint":                 string,
            "latest_handshake":         integer,
            "transfer_rx":              integer,
            "transfer_sx":              integer,
            "persistent_keepalive":     integer,
            "allowed_ips": [
                                        string
            ]
          }
        ]
      }
    ]

Examples:

    $ wg show all dump | jc --wg-show -p
    [
      {
        "device": "wg0",
        "private_key": "aEbVdvHSEp3oofHDNVCsUoaRSxk1Og8/pTLof5yF+1M=",
        "public_key": "OIxbQszw1chdO5uigAxpsl4fc/h04yMYafl72gUbakM=",
        "listen_port": 51820,
        "fwmark": null,
        "peers": [
          {
            "public_key": "sQFGAhSdx0aC7DmTFojzBOW8Ccjv1XV5+N9FnkZu5zc=",
            "preshared_key": null,
            "endpoint": "79.134.136.199:40036",
            "latest_handshake": 1728809756,
            "transfer_rx": 1378724,
            "transfer_sx": 406524,
            "persistent_keepalive": null,
            "allowed_ips": ["10.10.0.2/32"]
          },
          {
            "public_key": "B9csmpvrv4Q7gpjc6zAbNNO8hIOYfpBqxmik2aNpwwE=",
            "preshared_key": null,
            "endpoint": "79.134.136.199:35946",
            "latest_handshake": 1728809756,
            "transfer_rx": 4884248,
            "transfer_sx": 3544596,
            "persistent_keepalive": null,
            "allowed_ips": ["10.10.0.3/32"]
          },
          {
            "public_key": "miiSYR5UdevREhlWpmnci+vv/dEGLHbNtKu7u1CuOD4=",
            "preshared_key": null,
            "allowed_ips": ["10.10.0.4/32"]
          },
          {
            "public_key": "gx9+JHLHJvOfBNjTmZ8KQAnThFFiZMQrX1kRaYcIYzw=",
            "preshared_key": null,
            "endpoint": "173.244.225.194:45014",
            "latest_handshake": 1728809827,
            "transfer_rx": 1363652,
            "transfer_sx": 458252,
            "persistent_keepalive": null,
            "allowed_ips": ["10.10.0.5/32"]
          }
        ]
      }
    ]

    $ wg show all dump | jc --wg-show -p -r
    [
      {
        "device": "wg0",
        "private_key": "aEbVdvHSEp3oofHDNVCsUoaRSxk1Og8/pTLof5yF+1M=",
        "public_key": "OIxbQszw1chdO5uigAxpsl4fc/h04yMYafl72gUbakM=",
        "listen_port": 51820,
        "fwmark": null,
        "peers": {
          "sQFGAhSdx0aC7DmTFojzBOW8Ccjv1XV5+N9FnkZu5zc=": {
            "preshared_key": null,
            "endpoint": "79.134.136.199:40036",
            "latest_handshake": 1728809756,
            "transfer_rx": 1378724,
            "transfer_sx": 406524,
            "persistent_keepalive": -1,
            "allowed_ips": ["10.10.0.2/32"]
          },
          "B9csmpvrv4Q7gpjc6zAbNNO8hIOYfpBqxmik2aNpwwE=": {
            "preshared_key": null,
            "endpoint": "79.134.136.199:35946",
            "latest_handshake": 1728809756,
            "transfer_rx": 4884248,
            "transfer_sx": 3544596,
            "persistent_keepalive": -1,
            "allowed_ips": ["10.10.0.3/32"]
          },
          "miiSYR5UdevREhlWpmnci+vv/dEGLHbNtKu7u1CuOD4=": {
            "preshared_key": null,
            "allowed_ips": ["10.10.0.4/32"]
          },
          "gx9+JHLHJvOfBNjTmZ8KQAnThFFiZMQrX1kRaYcIYzw=": {
            "preshared_key": null,
            "endpoint": "173.244.225.194:45014",
            "latest_handshake": 1728809827,
            "transfer_rx": 1363652,
            "transfer_sx": 458252,
            "persistent_keepalive": -1,
            "allowed_ips": ["10.10.0.5/32"]
          }
        }
      }
    ]
"""

from typing import List, Dict, Optional, Union
from jc.jc_types import JSONDictType
import jc.utils
import re

PeerData = Dict[str, Union[Optional[str], Optional[int], List[str]]]
DeviceData = Dict[str, Union[Optional[str], Optional[int], Dict[str, PeerData]]]


class info:
    """Provides parser metadata (version, author, etc.)"""

    version = "1.0"
    description = "`wg show` command parser"
    author = "Hamza Saht"
    author_email = "hamzasaht01@gmail.com"
    compatible = ["linux", "darwin", "cygwin", "win32", "aix", "freebsd"]
    tags = ["command"]
    magic_commands = ["wg show"]


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
            "private_key": device.get("private_key"),
            "public_key": device.get("public_key"),
            "listen_port": device.get("listen_port"),
            "fwmark": device.get("fwmark"),
            "peers": [
                {
                    "public_key": peer_key,
                    "preshared_key": peer_data.get("preshared_key"),
                    "endpoint": peer_data.get("endpoint"),
                    "latest_handshake": peer_data.get("latest_handshake", 0),
                    "transfer_rx": peer_data.get("transfer_rx", 0),
                    "transfer_sx": peer_data.get("transfer_sx", 0),
                    "persistent_keepalive": peer_data.get("persistent_keepalive", -1),
                    "allowed_ips": peer_data.get("allowed_ips", []),
                }
                for peer_key, peer_data in device.get("peers", {}).items()
            ],
        }
        processed_data.append(processed_device)
    return processed_data


def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
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
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
