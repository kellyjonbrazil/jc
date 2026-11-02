import os
import unittest
from jc.parsers.proc_cmdline import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def test_proc_cmdline_nodata(self):
        """
        Test 'proc_cmdline' with no data
        """
        self.assertEqual(parse('', quiet=True), {})


    def test_proc_cmdline_samples(self):
        """
        Test 'proc_cmdline' with various samples
        """
        test_map = {
            'BOOT_IMAGE=/vmlinuz-5.4.0-166-generic root=/dev/mapper/ubuntu--vg-ubuntu--lv ro debian-installer/language=ru keyboard-configuration/layoutcode?=ru':
                {"BOOT_IMAGE":"/vmlinuz-5.4.0-166-generic","root":"/dev/mapper/ubuntu--vg-ubuntu--lv","debian-installer/language":"ru","keyboard-configuration/layoutcode?":"ru","_options":["ro"]},

            'BOOT_IMAGE=/boot/vmlinuz-4.4.0-210-generic root=UUID=e1d708ba-4448-4e96-baed-94b277eaa128 ro net.ifnames=0 biosdevname=0':
                {"BOOT_IMAGE":"/boot/vmlinuz-4.4.0-210-generic","root":"UUID=e1d708ba-4448-4e96-baed-94b277eaa128","net.ifnames":"0","biosdevname":"0","_options":["ro"]},

            'BOOT_IMAGE=/boot/vmlinuz-3.13.0-102-generic root=UUID=55707609-d20a-45f2-9130-60525bebf01f ro':
                {"BOOT_IMAGE":"/boot/vmlinuz-3.13.0-102-generic","root":"UUID=55707609-d20a-45f2-9130-60525bebf01f","_options":["ro"]},

            'BOOT_IMAGE=/vmlinuz-5.4.0-135-generic root=/dev/mapper/vg0-lv--root ro maybe-ubiquity':
                {"BOOT_IMAGE":"/vmlinuz-5.4.0-135-generic","root":"/dev/mapper/vg0-lv--root","_options":["ro","maybe-ubiquity"]},

            'BOOT_IMAGE=/vmlinuz-5.4.0-107-generic root=UUID=1b83a367-43a0-4e18-8ae3-3aaa37a89c7d ro quiet nomodeset splash net.ifnames=0 vt.handoff=7':
                {"BOOT_IMAGE":"/vmlinuz-5.4.0-107-generic","root":"UUID=1b83a367-43a0-4e18-8ae3-3aaa37a89c7d","net.ifnames":"0","vt.handoff":"7","_options":["ro","quiet","nomodeset","splash"]},

            'BOOT_IMAGE=clonezilla/live/vmlinuz consoleblank=0 keyboard-options=grp:ctrl_shift_toggle,lctrl_shift_toggle ethdevice-timeout=130 toram=filesystem.squashfs boot=live config noswap nolocales edd=on ocs_daemonon="ssh lighttpd" nomodeset noprompt ocs_live_run="sudo screen /usr/sbin/ocs-sr -g auto -e1 auto -e2 -batch -r -j2 -k -scr -p true restoreparts win7-64 sda1" ocs_live_extra_param="" keyboard-layouts=us,ru ocs_live_batch="no" locales=ru_RU.UTF-8 vga=788  nosplash net.ifnames=0 nodmraid components union=overlay fetch=http://172.16.11.8/tftpboot/clonezilla/live/filesystem.squashfs ocs_postrun99="sudo reboot" initrd=clonezilla/live/initrd.img':
                {"BOOT_IMAGE":"clonezilla/live/vmlinuz","consoleblank":"0","keyboard-options":"grp:ctrl_shift_toggle,lctrl_shift_toggle","ethdevice-timeout":"130","toram":"filesystem.squashfs","boot":"live","edd":"on","ocs_daemonon":"ssh lighttpd","ocs_live_run":"sudo screen /usr/sbin/ocs-sr -g auto -e1 auto -e2 -batch -r -j2 -k -scr -p true restoreparts win7-64 sda1","ocs_live_extra_param":"","keyboard-layouts":"us,ru","ocs_live_batch":"no","locales":"ru_RU.UTF-8","vga":"788","net.ifnames":"0","union":"overlay","fetch":"http://172.16.11.8/tftpboot/clonezilla/live/filesystem.squashfs","ocs_postrun99":"sudo reboot","initrd":"clonezilla/live/initrd.img","_options":["config","noswap","nolocales","nomodeset","noprompt","nosplash","nodmraid","components"]}
        }

        for data_in, expected in test_map.items():
            self.assertEqual(parse(data_in, quiet=True), expected)


    def test_proc_cmdline_kernel_quoting(self):
        """
        Test 'proc_cmdline' with kernel quoting rules
        """
        data = "tag='x selinux=0 y' note=it's initrd=\\EFI\\arch\\x.img \"a=b c\" d=\"e f\" g=\"h\x0bi\" j=\"unclosed k=l\n"
        expected = {
            "tag": "'x",
            "selinux": "0",
            "note": "it's",
            "initrd": "\\EFI\\arch\\x.img",
            "a": "b c",
            "d": "e f",
            "g": "h\x0bi",
            "j": "unclosed k=l",
            "_options": ["y'"]
        }
        self.assertEqual(parse(data, quiet=True), expected)

    def test_proc_cmdline_whitespace_separators(self):
        """
        Test 'proc_cmdline' with kernel whitespace separators
        """
        self.assertEqual(
            parse('a=1\x0bb=2\x0cc=3\td=4\r\ne', quiet=True),
            {"a": "1", "b": "2", "c": "3", "d": "4", "_options": ["e"]}
        )

    def test_proc_cmdline_init_args(self):
        """
        Test 'proc_cmdline' with init arguments after --
        """
        data = 'root=/dev/sda1 ro -- single x="a b" -- z\n'
        expected = {
            "root": "/dev/sda1",
            "_options": ["ro"],
            "_init_args": ["single", "x=a b"]
        }
        self.assertEqual(parse(data, quiet=True), expected)
        self.assertEqual(parse('ro --\n', quiet=True), {"_options": ["ro"], "_init_args": []})
        self.assertNotIn('_init_args', parse('ro a=--', quiet=True))

    def test_proc_cmdline_reserved_keys(self):
        """
        Test 'proc_cmdline' with parameters named like the reserved keys
        """
        data = '_options=x _repeated=1 _init_args=2 ro -- init'
        expected = {
            "_options": ["_options=x", "_repeated=1", "_init_args=2", "ro"],
            "_init_args": ["init"]
        }
        self.assertEqual(parse(data, quiet=True), expected)

    def test_proc_cmdline_repeated(self):
        """
        Test 'proc_cmdline' with repeated parameters
        """
        data = 'console=tty0 ro quiet console=ttyS0 ro a=1 b=2 a=3 console=hvc0'
        expected = {
            "console": "hvc0",
            "a": "3",
            "b": "2",
            "_options": ["ro", "quiet", "ro"],
            "_repeated": {
                "console": ["tty0", "ttyS0", "hvc0"],
                "a": ["1", "3"]
            }
        }
        self.assertEqual(parse(data, quiet=True), expected)


    def test_proc_cmdline_empty_parameters(self):
        """
        Test 'proc_cmdline' with empty parameters like the kernel
        """
        self.assertEqual(
            parse('a=1 "" ro -- "" b "', quiet=True),
            {"a": "1", "_options": ["", "ro"], "_init_args": ["", "b", ""]}
        )
        self.assertEqual(parse('" x', quiet=True), {"_options": [" x"]})

    def test_proc_cmdline_second_dashes(self):
        """
        Test 'proc_cmdline' with a second -- in the init arguments
        """
        self.assertEqual(
            parse('ro -- one -- two three', quiet=True),
            {"_options": ["ro"], "_init_args": ["one"]}
        )


if __name__ == '__main__':
    unittest.main()
