import os
import unittest
import json
import jc.parsers.xml

# fix for whether tests are run directly or via runtests.sh
try:
    from ._vendor.packaging import version
except:
    from _vendor.packaging import version  # type: ignore

# check the version of installed xmltodict library
try:
    import xmltodict
    XMLTODICT_INSTALLED = True
    XMLTODICT_0_13_0_OR_HIGHER = version.parse(xmltodict.__version__) >= version.parse('0.13.0')  # type: ignore
except:
    XMLTODICT_INSTALLED = False


THIS_DIR = os.path.dirname(os.path.abspath(__file__))

@unittest.skipIf(not XMLTODICT_INSTALLED, 'xmltodict library not installed')
class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/xml-cd_catalog.xml'), 'r', encoding='utf-8') as f:
        generic_xml_cd_catalog = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/xml-foodmenu.xml'), 'r', encoding='utf-8') as f:
        generic_xml_foodmenu = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/xml-nmap.xml'), 'r', encoding='utf-8') as f:
        generic_xml_nmap = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/xml-cd_catalog.json'), 'r', encoding='utf-8') as f:
        generic_xml_cd_catalog_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/xml-foodmenu.json'), 'r', encoding='utf-8') as f:
        generic_xml_foodmenu_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/xml-nmap.json'), 'r', encoding='utf-8') as f:
        generic_xml_nmap_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/xml-nmap-nocomment.json'), 'r', encoding='utf-8') as f:
        generic_xml_nmap_nocomment_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/xml-nmap-raw.json'), 'r', encoding='utf-8') as f:
        generic_xml_nmap_r_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/xml-nmap-raw-nocomment.json'), 'r', encoding='utf-8') as f:
        generic_xml_nmap_r_nocomment_json = json.loads(f.read())


    def test_xml_nodata(self):
        """
        Test xml parser with no data
        """
        self.assertEqual(jc.parsers.xml.parse('', quiet=True), [])

    def test_xml_nodata_r(self):
        """
        Test xml parser with no data and raw output
        """
        self.assertEqual(jc.parsers.xml.parse('', raw=True, quiet=True), [])

    def test_xml_cd_catalog(self):
        """
        Test the cd catalog xml file
        """
        self.assertEqual(jc.parsers.xml.parse(self.generic_xml_cd_catalog, quiet=True), self.generic_xml_cd_catalog_json)

    def test_xml_foodmenu(self):
        """
        Test the food menu xml file
        """
        self.assertEqual(jc.parsers.xml.parse(self.generic_xml_foodmenu, quiet=True), self.generic_xml_foodmenu_json)

    def test_xml_nmap(self):
        """
        Test nmap xml output
        """
        if XMLTODICT_0_13_0_OR_HIGHER:
            self.assertEqual(jc.parsers.xml.parse(self.generic_xml_nmap, quiet=True), self.generic_xml_nmap_json)
        else:
            print('\n### Using older version of xmltodict library. Testing without comment support. ### ... ')
            self.assertEqual(jc.parsers.xml.parse(self.generic_xml_nmap, quiet=True), self.generic_xml_nmap_nocomment_json)

    def test_xml_nmap_r(self):
        """
        Test nmap xml raw output
        """
        if XMLTODICT_0_13_0_OR_HIGHER:
            self.assertEqual(jc.parsers.xml.parse(self.generic_xml_nmap, raw=True, quiet=True), self.generic_xml_nmap_r_json)
        else:
            print('\n### Using older version of xmltodict library. Testing without comment support. ### ... ')
            self.assertEqual(jc.parsers.xml.parse(self.generic_xml_nmap, raw=True, quiet=True), self.generic_xml_nmap_r_nocomment_json)


if __name__ == '__main__':
    unittest.main()
