r"""jc - JSON Convert Proc file output parser

This parser automatically identifies the Proc file and calls the
corresponding parser to perform the parsing.

Magic syntax for converting `/proc` files is also supported by running
`jc /proc/<path to file>`. Any `jc` options must be specified before the
`/proc` path. The magic syntax supports "slurping" multiple files as input.
When multiple files are selected (e.g. `jc /proc/*/stat`) all of the output
will be wrapped inside an array. Also, a `_file` field will be included in
the output which helps correlate the input and output. The `--meta-out`
option can also be used to list the `/proc` input files for correlation with
the output list.

Specific Proc file parsers can also be called directly, if desired, and have
a naming convention of `proc-<name>` (cli) or `proc_<name>` (module). To see
a list of Proc file parsers, use `jc -hh` or `jc -a`.

Usage (cli):

    $ cat /proc/meminfo | jc --proc

or

    $ jc /proc/meminfo

or

    $ cat /proc/meminfo | jc --proc-meminfo

Usage (module):

    import jc
    result = jc.parse('proc', proc_file)

Schema:

See the specific Proc parser for the schema:

    $ jc --help --proc-<name>

For example:

    $ jc --help --proc-meminfo

Specific Proc file parser names can be found with `jc -hh` or `jc -a`.

Schemas can also be found online at:

    https://kellyjonbrazil.github.io/jc/docs/parsers/proc_<name>

For example:

https://kellyjonbrazil.github.io/jc/docs/parsers/proc_meminfo

Examples:

    $ cat /proc/modules | jc --proc -p
    [
      {
        "module": "binfmt_misc",
        "size": 24576,
        "used": 1,
        "used_by": [],
        "status": "Live",
        "location": "0xffffffffc0ab4000"
      },
      {
        "module": "vsock_loopback",
        "size": 16384,
        "used": 0,
        "used_by": [],
        "status": "Live",
        "location": "0xffffffffc0a14000"
      },
      {
        "module": "vmw_vsock_virtio_transport_common",
        "size": 36864,
        "used": 1,
        "used_by": [
          "vsock_loopback"
        ],
        "status": "Live",
        "location": "0xffffffffc0a03000"
      },
      ...
    ]

    $ cat /proc/modules | jc --proc-modules -p -r
    [
      {
        "module": "binfmt_misc",
        "size": "24576",
        "used": "1",
        "used_by": [],
        "status": "Live",
        "location": "0xffffffffc0ab4000"
      },
      {
        "module": "vsock_loopback",
        "size": "16384",
        "used": "0",
        "used_by": [],
        "status": "Live",
        "location": "0xffffffffc0a14000"
      },
      {
        "module": "vmw_vsock_virtio_transport_common",
        "size": "36864",
        "used": "1",
        "used_by": [
          "vsock_loopback"
        ],
        "status": "Live",
        "location": "0xffffffffc0a03000"
      },
      ...
    ]
"""
import re
from typing import List, Dict, Union
import jc.utils
from jc.lib import get_parser
from jc.exceptions import ParseError


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.4'
    description = '`/proc/` file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    tags = ['file', 'slurpable']


__version__ = info.version


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> Union[List[Dict], Dict]:
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary or List of Dictionaries. Raw or processed structured data.
    """
    jc.utils.input_type_check(data)

    if jc.utils.has_data(data):
        # signatures
        buddyinfo_p = re.compile(r'^Node \d+, zone\s+\w+\s+(?:\d+\s+){11}\n')
        cmdline_p = re.compile(r'^BOOT_IMAGE=')
        consoles_p = re.compile(r'^\w+\s+[\-WUR]{3} \([ECBpba ]+\)\s+\d+:\d+\n')
        cpuinfo_p = re.compile(r'^processor\t+: \d+.*bogomips\t+: \d+.\d\d\n', re.DOTALL)
        crypto_p = re.compile(r'^name\s+:.*\ndriver\s+:.*\nmodule\s+:.*\n')
        devices_p = re.compile(r'^Character devices:\n\s+\d+ .*\n')
        diskstats_p = re.compile(r'^\s*\d+\s+\d\s\w+\s(?:\d+\s){10,16}\d+\n')
        filesystems_p = re.compile(r'^(?:(?:nodev\t|\t)\w+\n){3}')
        interrupts_p = re.compile(r'^\s+(?:CPU\d+ +)+\n\s*\d+:\s+\d+')
        iomem_p = re.compile(r'^00000000-[0-9a-f]{8} : .*\n[0-9a-f]{8}-[0-9a-f]{8} : ')
        ioports_p = re.compile(r'^0000-[0-9a-f]{4} : .*\n\s*0000-[0-9a-f]{4} : ')
        loadavg_p = re.compile(r'^\d+.\d\d \d+.\d\d \d+.\d\d \d+/\d+ \d+$')
        locks_p = re.compile(r'^\d+: (?:POSIX|FLOCK|OFDLCK)\s+(?:ADVISORY|MANDATORY)\s+(?:READ|WRITE) ')
        meminfo_p = re.compile(r'^MemTotal:.*\nMemFree:.*\nMemAvailable:.*\n')
        modules_p = re.compile(r'^\w+ \d+ \d+ (?:-|\w+,).*0x[0-9a-f]{16}\n')
        mtrr_p = re.compile(r'^reg\d+: base=0x[0-9a-f]+ \(')
        pagetypeinfo_p = re.compile(r'^Page block order:\s+\d+\nPages per block:\s+\d+\n\n')
        partitions_p = re.compile(r'^major minor  #blocks  name\n\n\s*\d+\s+\d+\s+\d+ \w+\n')
        slabinfo_p = re.compile(r'^slabinfo - version: \d+.\d+\n')
        softirqs_p = re.compile(r'^\s+(CPU\d+\s+)+\n\s+HI:\s+\d')
        stat_p = re.compile(r'^cpu\s+(?: \d+){7,10}.*intr ', re.DOTALL)
        swaps_p = re.compile(r'^Filename\t\t\t\tType\t\tSize\t\tUsed\t\tPriority\n')
        uptime_p = re.compile(r'^\d+.\d\d \d+.\d\d$')
        version_p = re.compile(r'^.+\sversion\s[^\n]+$')
        vmallocinfo_p = re.compile(r'^0x[0-9a-f]{16}-0x[0-9a-f]{16}\s+\d+ \w+\+\w+/\w+ ')
        vmstat_p = re.compile(r'nr_free_pages \d+\n.* \d$', re.DOTALL)
        zoneinfo_p = re.compile(r'^Node \d+, zone\s+\w+\n')

        driver_rtc_p = re.compile(r'^rtc_time\t: .*\nrtc_date\t: .*\nalrm_time\t: .*\n')

        net_arp_p = re.compile(r'^IP address\s+HW type\s+Flags\s+HW address\s+Mask\s+Device\n')
        net_dev_p = re.compile(r'^Inter-\|\s+Receive\s+\|\s+Transmit\n')
        net_dev_mcast_p = re.compile(r'^\d+\s+\w+\s+\d+\s+\d+\s+[0-9a-f]{12}')
        net_if_inet6_p = re.compile(r'^[0-9a-f]{32} \d\d \d\d \d\d \d\d\s+\w+')
        net_igmp_p = re.compile(r'^Idx\tDevice\s+:\s+Count\s+Querier\tGroup\s+Users\s+Timer\tReporter\n')
        net_igmp6_p = re.compile(r'^\d+\s+\w+\s+[0-9a-f]{32}\s+\d+\s+[0-9A-F]{8}\s+\d+')
        net_ipv6_route_p = re.compile(r'^[0-9a-f]{32} \d\d [0-9a-f]{32} \d\d [0-9a-f]{32} (?:[0-9a-f]{8} ){4}\s+\w+')
        net_netlink_p = re.compile(r'^sk\s+Eth Pid\s+Groups\s+Rmem\s+Wmem')
        net_netstat_p = re.compile(r'^TcpExt: SyncookiesSent SyncookiesRecv SyncookiesFailed')
        net_packet_p = re.compile(r'^sk       RefCnt Type Proto  Iface R Rmem   User   Inode\n')
        net_protocols_p = re.compile(r'^protocol  size sockets  memory press maxhdr  slab module     cl co di ac io in de sh ss gs se re sp bi br ha uh gp em\n')
        net_route_p = re.compile(r'^Iface\tDestination\tGateway \tFlags\tRefCnt\tUse\tMetric\tMask\t\tMTU\tWindow\tIRTT\s+\n')
        net_tcp_p = re.compile(r'^\s+sl\s+local_address\s+(?:rem_address|remote_address)\s+st\s+tx_queue\s+rx_queue\s+tr\s+tm->when\s+retrnsmt\s+uid\s+timeout\s+inode')
        net_unix_p = re.compile(r'^Num       RefCount Protocol Flags    Type St Inode Path\n')

        pid_fdinfo_p = re.compile(r'^pos:\t\d+\nflags:\t\d+\nmnt_id:\t\d+\n')
        pid_io_p = re.compile(r'^rchar: \d+\nwchar: \d+\nsyscr: \d+\n')
        pid_maps_p = re.compile(r'^[0-9a-f]{12}-[0-9a-f]{12} [rwxsp\-]{4} [0-9a-f]{8} [0-9a-f]{2}:[0-9a-f]{2} \d+ ')
        pid_mountinfo_p = re.compile(r'^\d+ \d+ \d+:\d+ /.+\n')
        pid_numa_maps_p = re.compile(r'^[a-f0-9]{12} default [^\n]+\n')
        pid_smaps_p = re.compile(r'^[0-9a-f]{12}-[0-9a-f]{12} [rwxsp\-]{4} [0-9a-f]{8} [0-9a-f]{2}:[0-9a-f]{2} \d+ [^\n]+\nSize:\s+\d+ \S\S\n')
        pid_stat_p = re.compile(r'^\d+ \(.+\) \S \d+ \d+ \d+ \d+ -?\d+ (?:\d+ ){43}\d+$', re.DOTALL)
        pid_statm_p = re.compile(r'^\d+ \d+ \d+\s\d+\s\d+\s\d+\s\d+$')
        pid_status_p = re.compile(r'^Name:\t.+\n(?:Umask:\t\d+\n)?State:\t.+\nTgid:\t\d+\n')

        # scsi_device_info = re.compile(r"^'\w+' '.+' 0x\d+")
        # scsi_scsi_p = re.compile(r'^Attached devices:\nHost: \w+ ')

        procmap = {
            buddyinfo_p: 'proc_buddyinfo',
            cmdline_p: 'proc_cmdline',
            consoles_p: 'proc_consoles',
            cpuinfo_p: 'proc_cpuinfo',
            crypto_p: 'proc_crypto',
            devices_p: 'proc_devices',
            diskstats_p: 'proc_diskstats',
            filesystems_p: 'proc_filesystems',
            interrupts_p: 'proc_interrupts',
            iomem_p: 'proc_iomem',
            ioports_p: 'proc_ioports',
            loadavg_p: 'proc_loadavg',
            locks_p: 'proc_locks',
            meminfo_p: 'proc_meminfo',
            modules_p: 'proc_modules',
            mtrr_p: 'proc_mtrr',
            pagetypeinfo_p: 'proc_pagetypeinfo',
            partitions_p: 'proc_partitions',
            slabinfo_p: 'proc_slabinfo',
            softirqs_p: 'proc_softirqs',
            stat_p: 'proc_stat',
            swaps_p: 'proc_swaps',
            uptime_p: 'proc_uptime',
            version_p: 'proc_version',
            vmallocinfo_p: 'proc_vmallocinfo',
            zoneinfo_p: 'proc_zoneinfo',  # before vmstat
            vmstat_p: 'proc_vmstat',      # after zoneinfo

            driver_rtc_p: 'proc_driver_rtc',

            net_arp_p: 'proc_net_arp',
            net_dev_p: 'proc_net_dev',
            net_if_inet6_p: 'proc_net_if_inet6',
            net_igmp_p: 'proc_net_igmp',
            net_igmp6_p: 'proc_net_igmp6',
            net_netlink_p: 'proc_net_netlink',
            net_netstat_p: 'proc_net_netstat',
            net_packet_p: 'proc_net_packet',
            net_protocols_p: 'proc_net_protocols',
            net_route_p: 'proc_net_route',
            net_tcp_p: 'proc_net_tcp',
            net_unix_p: 'proc_net_unix',
            net_ipv6_route_p: 'proc_net_ipv6_route',  # before net_dev_mcast
            net_dev_mcast_p: 'proc_net_dev_mcast',    # after net_ipv6_route

            pid_fdinfo_p: 'proc_pid_fdinfo',
            pid_io_p: 'proc_pid_io',
            pid_mountinfo_p: 'proc_pid_mountinfo',
            pid_numa_maps_p: 'proc_pid_numa_maps',
            pid_stat_p: 'proc_pid_stat',
            pid_statm_p: 'proc_pid_statm',
            pid_status_p: 'proc_pid_status',
            pid_smaps_p: 'proc_pid_smaps',  # before pid_maps
            pid_maps_p: 'proc_pid_maps',    # after pid_smaps

            # scsi_device_info: 'proc_scsi_device_info',
            # scsi_scsi_p: 'proc_scsi_scsi'
        }

        for reg_pattern, parse_mod in procmap.items():
            if reg_pattern.search(data):
                try:
                    procparser = get_parser(parse_mod)
                    return procparser.parse(data, quiet=quiet, raw=raw)
                except ModuleNotFoundError:
                    raise ParseError('Proc file type not yet implemented.')

    raise ParseError('Proc file could not be identified.')
