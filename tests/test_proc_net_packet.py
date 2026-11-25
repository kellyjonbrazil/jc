import os
import unittest
import json
from typing import Dict
import jc.parsers.proc_net_packet

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'proc_net_packet': (
                'fixtures/linux-proc/net_packet',
                'fixtures/linux-proc/net_packet.json'),
            'proc_net_packet2': (
                'fixtures/linux-proc/net_packet2',
                'fixtures/linux-proc/net_packet2.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_proc_net_packet_nodata(self):
        """
        Test 'proc_net_packet' with no data
        """
        self.assertEqual(jc.parsers.proc_net_packet.parse('', quiet=True), [])

    def test_proc_net_packet(self):
        """
        Test '/proc/net/packet'
        """
        self.assertEqual(jc.parsers.proc_net_packet.parse(self.f_in['proc_net_packet'], quiet=True),
                                                          self.f_json['proc_net_packet'])

    def test_proc_net_packet2(self):
        """
        Test '/proc/net/packet' from a 64-bit kernel with several sockets
        """
        self.assertEqual(jc.parsers.proc_net_packet.parse(self.f_in['proc_net_packet2'], quiet=True),
                                                          self.f_json['proc_net_packet2'])


    def test_proc_net_packet_multiple_rows(self):
        """
        Test '/proc/net/packet' with more than one row
        """
        data = (
            'sk       RefCnt Type Proto  Iface R Rmem   User   Inode\n'
            'ffff9b61b56c1800 3      3    88cc   2     1 0      101    34754 \n'
            'ffff9b61b56c2000 3      3    0003   0     1 0      0      40012 \n'
        )
        result = jc.parsers.proc_net_packet.parse(data, quiet=True)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[1]['sk'], 'ffff9b61b56c2000')
        self.assertEqual(result[1]['Inode'], 40012)

    def test_proc_net_packet_header_only(self):
        """
        Test '/proc/net/packet' with only the header row
        """
        data = 'sk       RefCnt Type Proto  Iface R Rmem   User   Inode\n'
        self.assertEqual(jc.parsers.proc_net_packet.parse(data, quiet=True), [])


if __name__ == '__main__':
    unittest.main()
