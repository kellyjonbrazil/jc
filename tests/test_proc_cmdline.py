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


if __name__ == '__main__':
    unittest.main()
