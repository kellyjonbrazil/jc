import os
import unittest
import json
from typing import Dict
import jc.parsers.proc_net_unix

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'proc_net_unix': (
                'fixtures/linux-proc/net_unix',
                'fixtures/linux-proc/net_unix.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_proc_net_unix_nodata(self):
        """
        Test 'proc_net_unix' with no data
        """
        self.assertEqual(jc.parsers.proc_net_unix.parse('', quiet=True), [])

    def test_proc_net_unix(self):
        """
        Test '/proc/net/unix'
        """
        self.assertEqual(jc.parsers.proc_net_unix.parse(self.f_in['proc_net_unix'], quiet=True),
                                                         self.f_json['proc_net_unix'])


    def test_proc_net_unix_newline_in_path(self):
        """
        Test '/proc/net/unix' with a newline in a socket path
        """
        data = (
            'Num       RefCount Protocol Flags    Type St Inode Path\n'
            '00000000c7cde439: 00000002 00000000 00000000 0001 01 18096 @demo\n'
            '0: 2 0 10000 1 1 4242 /run/other.sock\n'
            '00000000c7cde43a: 00000002 00000000 00000000 0001 01 18097 /run/next.sock \n'
            '00000000c7cde43b: 00000003 00000000 00000000 0001 03 18098\n'
        )
        result = jc.parsers.proc_net_unix.parse(data, quiet=True)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]['Num'], '00000000c7cde439:')
        self.assertEqual(result[0]['Inode'], 18096)
        self.assertEqual(result[0]['Path'], '@demo\n0: 2 0 10000 1 1 4242 /run/other.sock')
        self.assertEqual(result[1]['Inode'], 18097)
        self.assertEqual(result[1]['Path'], '/run/next.sock ')
        self.assertEqual(result[2]['Inode'], 18098)
        self.assertNotIn('Path', result[2])

    def test_proc_net_unix_non_numeric_inode_line(self):
        """
        Test '/proc/net/unix' with a continuation line that has a non-numeric seventh word
        """
        data = (
            'Num       RefCount Protocol Flags    Type St Inode Path\n'
            '00000000c7cde439: 00000002 00000000 00000000 0001 01 18096 @demo\n'
            'a b c d e f xyz /not/a/row\n'
            '00000000c7cde43a: 00000002 00000000 00000000 0001 01 18097 /run/next.sock\n'
        )
        result = jc.parsers.proc_net_unix.parse(data, quiet=True)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['Path'], '@demo\na b c d e f xyz /not/a/row')
        self.assertEqual(result[1]['Path'], '/run/next.sock')
        self.assertEqual(result[1]['Inode'], 18097)


if __name__ == '__main__':
    unittest.main()
