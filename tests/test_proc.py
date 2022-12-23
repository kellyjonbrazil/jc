import os
import unittest
import json
from typing import Dict
import jc.parsers.proc
from jc.exceptions import ParseError

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    """
    These tests replicate the individual /proc file module tests, but the purpose
    is different. These tests ensure the file signature matching engine in the
    /proc parser module sends the user input to the correct parser.

    Signature match regex can be order dependent, so these tests make sure we
    don't break anything when adding/removing/re-ordering the signature regexes.
    """
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'proc_buddyinfo': (
                'fixtures/linux-proc/buddyinfo',
                'fixtures/linux-proc/buddyinfo.json'),
            'proc_consoles': (
                'fixtures/linux-proc/consoles',
                'fixtures/linux-proc/consoles.json'),
            'proc_consoles2': (
                'fixtures/linux-proc/consoles2',
                'fixtures/linux-proc/consoles2.json'),
            'proc_cpuinfo': (
                'fixtures/linux-proc/cpuinfo',
                'fixtures/linux-proc/cpuinfo.json'),
            'proc_cpuinfo2': (
                'fixtures/linux-proc/cpuinfo2',
                'fixtures/linux-proc/cpuinfo2.json'),
            'proc_crypto': (
                'fixtures/linux-proc/crypto',
                'fixtures/linux-proc/crypto.json'),
            'proc_devices': (
                'fixtures/linux-proc/devices',
                'fixtures/linux-proc/devices.json'),
            'proc_diskstats': (
                'fixtures/linux-proc/diskstats',
                'fixtures/linux-proc/diskstats.json'),
            'proc_filesystems': (
                'fixtures/linux-proc/filesystems',
                'fixtures/linux-proc/filesystems.json'),
            'proc_interrupts': (
                'fixtures/linux-proc/interrupts',
                'fixtures/linux-proc/interrupts.json'),
            'proc_iomem': (
                'fixtures/linux-proc/iomem',
                'fixtures/linux-proc/iomem.json'),
            'proc_ioports': (
                'fixtures/linux-proc/ioports',
                'fixtures/linux-proc/ioports.json'),
            'proc_loadavg': (
                'fixtures/linux-proc/loadavg',
                'fixtures/linux-proc/loadavg.json'),
            'proc_locks': (
                'fixtures/linux-proc/locks',
                'fixtures/linux-proc/locks.json'),
            'proc_meminfo': (
                'fixtures/linux-proc/meminfo',
                'fixtures/linux-proc/meminfo.json'),
            'proc_modules': (
                'fixtures/linux-proc/modules',
                'fixtures/linux-proc/modules.json'),
            'proc_mtrr': (
                'fixtures/linux-proc/mtrr',
                'fixtures/linux-proc/mtrr.json'),
            'proc_pagetypeinfo': (
                'fixtures/linux-proc/pagetypeinfo',
                'fixtures/linux-proc/pagetypeinfo.json'),
            'proc_partitions': (
                'fixtures/linux-proc/partitions',
                'fixtures/linux-proc/partitions.json'),
            'proc_slabinfo': (
                'fixtures/linux-proc/slabinfo',
                'fixtures/linux-proc/slabinfo.json'),
            'proc_softirqs': (
                'fixtures/linux-proc/softirqs',
                'fixtures/linux-proc/softirqs.json'),
            'proc_stat': (
                'fixtures/linux-proc/stat',
                'fixtures/linux-proc/stat.json'),
            'proc_stat2': (
                'fixtures/linux-proc/stat2',
                'fixtures/linux-proc/stat2.json'),
            'proc_swaps': (
                'fixtures/linux-proc/swaps',
                'fixtures/linux-proc/swaps.json'),
            'proc_uptime': (
                'fixtures/linux-proc/uptime',
                'fixtures/linux-proc/uptime.json'),
            'proc_version': (
                'fixtures/linux-proc/version',
                'fixtures/linux-proc/version.json'),
            'proc_version2': (
                'fixtures/linux-proc/version2',
                'fixtures/linux-proc/version2.json'),
            'proc_version3': (
                'fixtures/linux-proc/version3',
                'fixtures/linux-proc/version3.json'),
            'proc_vmallocinfo': (
                'fixtures/linux-proc/vmallocinfo',
                'fixtures/linux-proc/vmallocinfo.json'),
            'proc_vmstat': (
                'fixtures/linux-proc/vmstat',
                'fixtures/linux-proc/vmstat.json'),
            'proc_zoneinfo': (
                'fixtures/linux-proc/zoneinfo',
                'fixtures/linux-proc/zoneinfo.json'),
            'proc_zoneinfo2': (
                'fixtures/linux-proc/zoneinfo2',
                'fixtures/linux-proc/zoneinfo2.json'),

            'proc_driver_rtc': (
                'fixtures/linux-proc/driver_rtc',
                'fixtures/linux-proc/driver_rtc.json'),

            'proc_net_arp': (
                'fixtures/linux-proc/net_arp',
                'fixtures/linux-proc/net_arp.json'),
            'proc_net_dev_mcast': (
                'fixtures/linux-proc/net_dev_mcast',
                'fixtures/linux-proc/net_dev_mcast.json'),
            'proc_net_dev': (
                'fixtures/linux-proc/net_dev',
                'fixtures/linux-proc/net_dev.json'),
            'proc_net_if_inet6': (
                'fixtures/linux-proc/net_if_inet6',
                'fixtures/linux-proc/net_if_inet6.json'),
            'proc_net_igmp': (
                'fixtures/linux-proc/net_igmp',
                'fixtures/linux-proc/net_igmp.json'),
            'proc_net_igmp_more': (
                'fixtures/linux-proc/net_igmp_more',
                'fixtures/linux-proc/net_igmp_more.json'),
            'proc_net_igmp6': (
                'fixtures/linux-proc/net_igmp6',
                'fixtures/linux-proc/net_igmp6.json'),
            'proc_net_ipv6_route': (
                'fixtures/linux-proc/net_ipv6_route',
                'fixtures/linux-proc/net_ipv6_route.json'),
            'proc_net_netlink': (
                'fixtures/linux-proc/net_netlink',
                'fixtures/linux-proc/net_netlink.json'),
            'proc_net_netstat': (
                'fixtures/linux-proc/net_netstat',
                'fixtures/linux-proc/net_netstat.json'),
            'proc_net_packet': (
                'fixtures/linux-proc/net_packet',
                'fixtures/linux-proc/net_packet.json'),
            'proc_net_protocols': (
                'fixtures/linux-proc/net_protocols',
                'fixtures/linux-proc/net_protocols.json'),
            'proc_net_route': (
                'fixtures/linux-proc/net_route',
                'fixtures/linux-proc/net_route.json'),
            'proc_net_unix': (
                'fixtures/linux-proc/net_unix',
                'fixtures/linux-proc/net_unix.json'),

            'proc_pid_fdinfo': (
                'fixtures/linux-proc/pid_fdinfo',
                'fixtures/linux-proc/pid_fdinfo.json'),
            'proc_pid_fdinfo_dma': (
                'fixtures/linux-proc/pid_fdinfo_dma',
                'fixtures/linux-proc/pid_fdinfo_dma.json'),
            'proc_pid_fdinfo_epoll': (
                'fixtures/linux-proc/pid_fdinfo_epoll',
                'fixtures/linux-proc/pid_fdinfo_epoll.json'),
            'proc_pid_fdinfo_fanotify': (
                'fixtures/linux-proc/pid_fdinfo_fanotify',
                'fixtures/linux-proc/pid_fdinfo_fanotify.json'),
            'proc_pid_fdinfo_inotify': (
                'fixtures/linux-proc/pid_fdinfo_inotify',
                'fixtures/linux-proc/pid_fdinfo_inotify.json'),
            'proc_pid_fdinfo_timerfd': (
                'fixtures/linux-proc/pid_fdinfo_timerfd',
                'fixtures/linux-proc/pid_fdinfo_timerfd.json'),
            'proc_pid_io': (
                'fixtures/linux-proc/pid_io',
                'fixtures/linux-proc/pid_io.json'),
            'proc_pid_maps': (
                'fixtures/linux-proc/pid_maps',
                'fixtures/linux-proc/pid_maps.json'),
            'proc_pid_mountinfo': (
                'fixtures/linux-proc/pid_mountinfo',
                'fixtures/linux-proc/pid_mountinfo.json'),
            'proc_pid_numa_maps': (
                'fixtures/linux-proc/pid_numa_maps',
                'fixtures/linux-proc/pid_numa_maps.json'),
            'proc_pid_smaps': (
                'fixtures/linux-proc/pid_smaps',
                'fixtures/linux-proc/pid_smaps.json'),
            'proc_pid_stat': (
                'fixtures/linux-proc/pid_stat',
                'fixtures/linux-proc/pid_stat.json'),
            'pid_stat_w_space_and_nl_in_comm': (
                'fixtures/linux-proc/pid_stat_w_space_and_nl_in_comm',
                'fixtures/linux-proc/pid_stat_w_space_and_nl_in_comm.json'),
            'proc_pid_stat_hack': (
                'fixtures/linux-proc/pid_stat_hack',
                'fixtures/linux-proc/pid_stat_hack.json'),
            'proc_pid_statm': (
                'fixtures/linux-proc/pid_statm',
                'fixtures/linux-proc/pid_statm.json'),
            'proc_pid_status': (
                'fixtures/linux-proc/pid_status',
                'fixtures/linux-proc/pid_status.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_proc_nodata(self):
        """
        Test proc parser with no data
        """
        self.assertRaises(ParseError, jc.parsers.proc.parse, '', quiet=True)

    def test_proc_file_signature_detection(self):
        """
        Test proc parser file signature detection
        """
        for in_, expected in zip(self.f_in.keys(), self.f_json.keys()):
            self.assertEqual(jc.parsers.proc.parse(self.f_in[in_], quiet=True),
                                                   self.f_json[expected])


if __name__ == '__main__':
    unittest.main()
