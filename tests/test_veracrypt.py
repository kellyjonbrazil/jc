import json
import re
import unittest

from jc.parsers.veracrypt import (
    _volume_line_pattern,
    _volume_verbose_pattern,
    _parse_volume,
    Volume,
    parse,
)


class VeracryptTests(unittest.TestCase):
    def test_veracrypt_nodata(self):
        """
        Test 'veracrypt' with no data
        """

        output=''
        self.assertEqual(parse(output, quiet=True), [])

    def test_veracrypt_invalid_call(self):
        """
        Test 'veracrypt' with output from invalid call
        """

        output='Invalid command: foo'
        self.assertEqual(parse(output, quiet=True), [])

    def test_veracrypt_no_mounted_volumes(self):
        """
        Test 'veracrypt' with no mounted volumes
        """

        output='Error: No volumes mounted.'
        self.assertEqual(parse(output, quiet=True), [])

    def test_veracrypt_list_volumes(self):
        """
        Test 'veracrypt' list volumes
        """

        output = "1: /dev/sdb1 /dev/mapper/veracrypt1 /home/bob/mount/encrypt/sdb1\n"
        output += "2: /dev/sdb2 /dev/mapper/veracrypt2 /home/bob/mount/encrypt/sdb2"

        actual = parse(output, quiet=True)

        self.assertIsNotNone(actual)
        self.assertIsNotNone(actual[0])
        self.assertIsNotNone(actual[1])

        expected = [
            {
                "slot": 1,
                "path": "/dev/sdb1",
                "device": "/dev/mapper/veracrypt1",
                "mountpoint": "/home/bob/mount/encrypt/sdb1"
            },
            {
                "slot": 2,
                "path": "/dev/sdb2",
                "device": "/dev/mapper/veracrypt2",
                "mountpoint": "/home/bob/mount/encrypt/sdb2"
            }
        ]

        if actual:
            for k, v in expected[0].items():
                self.assertEqual(v, actual[0][k], f"Volume regex failed on {k}")

            for k, v in expected[1].items():
                self.assertEqual(v, actual[1][k], f"Volume regex failed on {k}")

    def test_veracrypt_verbose_list_volumes(self):
        """
        Test 'veracrypt' list volumes in verbose mode
        """

        with open("tests/fixtures/generic/veracrypt_verbose_list_volumes.out", "r") as f:
            output = f.read()

        actual = parse(output, quiet=True)

        self.assertIsNotNone(actual)
        self.assertIsNotNone(actual[0])
        self.assertIsNotNone(actual[1])

        expected = [
            {
                "slot": 1,
                "path": "/dev/sdb1",
                "device": "/dev/mapper/veracrypt1",
                "mountpoint": "/home/bob/mount/encrypt/sdb1",
                "size": "498 MiB",
                "type": "Normal",
                "readonly": "No",
                "hidden_protected": "No",
                "encryption_algo": "AES",
                "pk_size": "256 bits",
                "sk_size": "256 bits",
                "block_size": "128 bits",
                "mode": "XTS",
                "prf": "HMAC-SHA-512",
                "format_version": 2,
                "backup_header": "Yes"
            },
            {
                "slot": 2,
                "path": "/dev/sdb2",
                "device": "/dev/mapper/veracrypt2",
                "mountpoint": "/home/bob/mount/encrypt/sdb2",
                "size": "522 MiB",
                "type": "Normal",
                "readonly": "No",
                "hidden_protected": "No",
                "encryption_algo": "AES",
                "pk_size": "256 bits",
                "sk_size": "256 bits",
                "block_size": "128 bits",
                "mode": "XTS",
                "prf": "HMAC-SHA-512",
                "format_version": 2,
                "backup_header": "Yes"
            }
        ]

        if actual:
            for k, v in expected[0].items():
                self.assertEqual(v, actual[0][k], f"Volume regex failed on {k}")

            for k, v in expected[1].items():
                self.assertEqual(v, actual[1][k], f"Volume regex failed on {k}")

    def test_veracrypt_verbose_list_volumes_unknown_fields(self):
        """
        Test 'veracrypt' list volumes with unknown fields in verbose mode
        """

        with open("tests/fixtures/generic/veracrypt_verbose_list_volumes_unknown_fields.out", "r") as f:
            output = f.read()

        actual = parse(output, quiet=True)

        self.assertIsNotNone(actual)
        self.assertIsNotNone(actual[0])
        self.assertIsNotNone(actual[1])

        expected = [
            {
                "slot": 1,
                "path": "/dev/sdb1",
                "device": "/dev/mapper/veracrypt1",
                "mountpoint": "/home/bob/mount/encrypt/sdb1",
                "size": "498 MiB",
                "type": "Normal",
                "readonly": "No",
                "hidden_protected": "No",
                "encryption_algo": "AES",
                "pk_size": "256 bits",
                "sk_size": "256 bits",
                "block_size": "128 bits",
                "mode": "XTS",
                "prf": "HMAC-SHA-512",
                "format_version": 2,
                "backup_header": "Yes"
            },
            {
                "slot": 2,
                "path": "/dev/sdb2",
                "device": "/dev/mapper/veracrypt2",
                "mountpoint": "/home/bob/mount/encrypt/sdb2",
                "size": "522 MiB",
                "type": "Normal",
                "readonly": "No",
                "hidden_protected": "No",
                "encryption_algo": "AES",
                "pk_size": "256 bits",
                "sk_size": "256 bits",
                "block_size": "128 bits",
                "mode": "XTS",
                "prf": "HMAC-SHA-512",
                "format_version": 2,
                "backup_header": "Yes"
            }
        ]

        if actual:
            for k, v in expected[0].items():
                self.assertEqual(v, actual[0][k], f"Volume regex failed on {k}")

            for k, v in expected[1].items():
                self.assertEqual(v, actual[1][k], f"Volume regex failed on {k}")

if __name__ == '__main__':
    unittest.main()
