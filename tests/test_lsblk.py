import os
import json
import unittest
import jc.parsers.lsblk

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/lsblk.out'), 'r', encoding='utf-8') as f:
        centos_7_7_lsblk = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/lsblk.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_lsblk = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/lsblk-allcols.out'), 'r', encoding='utf-8') as f:
        centos_7_7_lsblk_allcols = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/lsblk-allcols.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_lsblk_allcols = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/lsblk.json'), 'r', encoding='utf-8') as f:
        centos_7_7_lsblk_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/lsblk.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_lsblk_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/lsblk-allcols.json'), 'r', encoding='utf-8') as f:
        centos_7_7_lsblk_allcols_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/lsblk-allcols.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_lsblk_allcols_json = json.loads(f.read())


    def test_lsblk_nodata(self):
        """
        Test 'lsblk' with no data
        """
        self.assertEqual(jc.parsers.lsblk.parse('', quiet=True), [])

    def test_lsblk_centos_7_7(self):
        """
        Test 'lsblk' on Centos 7.7
        """
        self.assertEqual(jc.parsers.lsblk.parse(self.centos_7_7_lsblk, quiet=True), self.centos_7_7_lsblk_json)

    def test_lsblk_ubuntu_18_4(self):
        """
        Test 'lsblk' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.lsblk.parse(self.ubuntu_18_4_lsblk, quiet=True), self.ubuntu_18_4_lsblk_json)

    def test_lsblk_allcols_centos_7_7(self):
        """
        Test 'lsblk -o +KNAME,FSTYPE,LABEL,UUID,PARTLABEL,PARTUUID,RA,MODEL,SERIAL,STATE,OWNER,GROUP,MODE,ALIGNMENT,MIN-IO,OPT-IO,PHY-SEC,LOG-SEC,ROTA,SCHED,RQ-SIZE,DISC-ALN,DISC-GRAN,DISC-MAX,DISC-ZERO,WSAME,WWN,RAND,PKNAME,HCTL,TRAN,REV,VENDOR' on Centos 7.7
        """
        self.assertEqual(jc.parsers.lsblk.parse(self.centos_7_7_lsblk_allcols, quiet=True), self.centos_7_7_lsblk_allcols_json)

    def test_lsblk_allcols_ubuntu_18_4(self):
        """
        Test 'lsblk -o +KNAME,FSTYPE,LABEL,UUID,PARTLABEL,PARTUUID,RA,MODEL,SERIAL,STATE,OWNER,GROUP,MODE,ALIGNMENT,MIN-IO,OPT-IO,PHY-SEC,LOG-SEC,ROTA,SCHED,RQ-SIZE,DISC-ALN,DISC-GRAN,DISC-MAX,DISC-ZERO,WSAME,WWN,RAND,PKNAME,HCTL,TRAN,REV,VENDOR' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.lsblk.parse(self.ubuntu_18_4_lsblk_allcols, quiet=True), self.ubuntu_18_4_lsblk_allcols_json)

    def test_lsblk_multiple_mountpoints(self):
        """
        Test 'lsblk' with multiple mountpoints
        """
        data = '''NAME                 MAJ:MIN RM          SIZE RO TYPE MOUNTPOINTS
sda                    8:0    0 5368709120000  0 disk
|-sda1                 8:1    0       1048576  0 part
|-sda2                 8:2    0    1073741824  0 part /boot
|-sda3                 8:3    0    1073741824  0 part /boot/efi
`-sda4                 8:4    0   51536461824  0 part
  |-almalinux-root   253:0    0   36075208704  0 lvm  /
  |-almalinux-docker 253:1    0    1073741824  0 lvm  /opt/docker
  |-almalinux-home   253:2    0    5368709120  0 lvm  /home
  `-almalinux-opt    253:3    0    9017753600  0 lvm  /var/lib/kafka
                                                      /opt
sr0                   11:0    1    1073741312  0 rom'''
        expected = [{"name":"sda","maj_min":"8:0","rm":False,"size":"5368709120000","ro":False,"type":"disk","mountpoints":[],"size_bytes":5368709120000},{"name":"sda1","maj_min":"8:1","rm":False,"size":"1048576","ro":False,"type":"part","mountpoints":[],"size_bytes":1048576},{"name":"sda2","maj_min":"8:2","rm":False,"size":"1073741824","ro":False,"type":"part","mountpoints":["/boot"],"size_bytes":1073741824},{"name":"sda3","maj_min":"8:3","rm":False,"size":"1073741824","ro":False,"type":"part","mountpoints":["/boot/efi"],"size_bytes":1073741824},{"name":"sda4","maj_min":"8:4","rm":False,"size":"51536461824","ro":False,"type":"part","mountpoints":[],"size_bytes":51536461824},{"name":"almalinux-root","maj_min":"253:0","rm":False,"size":"36075208704","ro":False,"type":"lvm","mountpoints":["/"],"size_bytes":36075208704},{"name":"almalinux-docker","maj_min":"253:1","rm":False,"size":"1073741824","ro":False,"type":"lvm","mountpoints":["/opt/docker"],"size_bytes":1073741824},{"name":"almalinux-home","maj_min":"253:2","rm":False,"size":"5368709120","ro":False,"type":"lvm","mountpoints":["/home"],"size_bytes":5368709120},{"name":"almalinux-opt","maj_min":"253:3","rm":False,"size":"9017753600","ro":False,"type":"lvm","mountpoints":["/var/lib/kafka","/opt"],"size_bytes":9017753600},{"name":"sr0","maj_min":"11:0","rm":True,"size":"1073741312","ro":False,"type":"rom","mountpoints":[],"size_bytes":1073741312}]
        self.assertEqual(jc.parsers.lsblk.parse(data, quiet=True), expected)

if __name__ == '__main__':
    unittest.main()
