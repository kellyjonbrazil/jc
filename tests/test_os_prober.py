import os
import unittest
from jc.parsers.os_prober import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def test_os_prober_nodata(self):
        """
        Test 'os_prober' with no data
        """
        self.assertEqual(parse('', quiet=True), {})

    def test_os_prober_1(self):
        """
        Test 'os_prober' 1
        """
        self.assertEqual(
            parse('/dev/sda1:Windows 7 (loader):Windows:chain', quiet=True),
            {"partition":"/dev/sda1","name":"Windows 7 (loader)","short_name":"Windows","type":"chain"}
        )

    def test_os_prober_2(self):
        """
        Test 'os_prober' 2
        """
        self.assertEqual(
            parse('/dev/sda1:Windows 10:Windows:chain', quiet=True),
            {"partition":"/dev/sda1","name":"Windows 10","short_name":"Windows","type":"chain"}
        )

    def test_os_prober_3(self):
        """
        Test 'os_prober' 3
        """
        self.assertEqual(
            parse('/dev/sda1@/efi/Microsoft/Boot/bootmgfw.efi:Windows Boot Manager:Windows:efi', quiet=True),
            {"partition":"/dev/sda1","efi_bootmgr":"/efi/Microsoft/Boot/bootmgfw.efi","name":"Windows Boot Manager","short_name":"Windows","type":"efi"}
        )

    def test_os_prober_3_raw(self):
        """
        Test 'os_prober' 3 with raw output
        """
        self.assertEqual(
            parse('/dev/sda1@/efi/Microsoft/Boot/bootmgfw.efi:Windows Boot Manager:Windows:efi', quiet=True, raw=True),
            {"partition":"/dev/sda1@/efi/Microsoft/Boot/bootmgfw.efi","name":"Windows Boot Manager","short_name":"Windows","type":"efi"}
        )


if __name__ == '__main__':
    unittest.main()
