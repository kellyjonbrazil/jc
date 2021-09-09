import os
import json
import unittest
import jc.parsers.ascii

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/virsh-domifaddr.out'), 'r', encoding='utf-8') as f:
            self.generic_virsh_domifaddr = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/virsh-domifaddr.json'), 'r', encoding='utf-8') as f:
            self.generic_virsh_domifaddr_json = json.loads(f.read())

    def test_virsh_domifaddr(self):
        self.assertEqual(jc.parsers.ascii.parse(self.generic_virsh_domifaddr, quiet=True), self.generic_virsh_domifaddr_json)


if __name__ == '__main__':
    unittest.main()
