import os
import unittest
import json
from typing import Dict
import jc.parsers.proc_vmallocinfo

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'proc_vmallocinfo': (
                'fixtures/linux-proc/vmallocinfo',
                'fixtures/linux-proc/vmallocinfo.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_proc_vmallocinfo_nodata(self):
        """
        Test 'proc_vmallocinfo' with no data
        """
        self.assertEqual(jc.parsers.proc_vmallocinfo.parse('', quiet=True), [])

    def test_proc_vmallocinfo(self):
        """
        Test '/proc/vmallocinfo'
        """
        self.assertEqual(jc.parsers.proc_vmallocinfo.parse(self.f_in['proc_vmallocinfo'], quiet=True),
                                                           self.f_json['proc_vmallocinfo'])


    def test_proc_vmallocinfo_details_stay_on_their_record(self):
        """
        Test '/proc/vmallocinfo' with phys= and pages= on the lines of their records
        """
        data = (
            '0xffffb3c1c0000000-0xffffb3c1c0005000   20480 map_irq_stack+0x93/0xe0 vmap\n'
            '0xffffb3c1c0005000-0xffffb3c1c0007000    8192 acpi_os_map_iomem+0x1ac/0x1c0 phys=0x00000000bfefe000 ioremap\n'
            '0xffffb3c1c0007000-0xffffb3c1c0009000    8192 alloc_pages+0x1/0x2 pages=2 vmalloc N0=2 key=a=b\n'
        )
        result = jc.parsers.proc_vmallocinfo.parse(data, quiet=True)
        self.assertEqual(result, [
            {'start': '0xffffb3c1c0000000', 'end': '0xffffb3c1c0005000', 'size': 20480,
             'caller': 'map_irq_stack+0x93/0xe0', 'options': ['vmap']},
            {'start': '0xffffb3c1c0005000', 'end': '0xffffb3c1c0007000', 'size': 8192,
             'caller': 'acpi_os_map_iomem+0x1ac/0x1c0', 'options': ['ioremap'], 'phys': '0x00000000bfefe000'},
            {'start': '0xffffb3c1c0007000', 'end': '0xffffb3c1c0009000', 'size': 8192,
             'caller': 'alloc_pages+0x1/0x2', 'options': ['vmalloc'], 'pages': 2, 'N0': 2, 'key': 'a=b'}
        ])


if __name__ == '__main__':
    unittest.main()
