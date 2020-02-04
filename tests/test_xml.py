import os
import unittest
import json
import jc.parsers.xml

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/xml-cd_catalog.xml'), 'r') as f:
            self.generic_xml_cd_catalog = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/xml-foodmenu.xml'), 'r') as f:
            self.generic_xml_foodmenu = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/xml-cd_catalog.json'), 'r') as f:
            self.generic_xml_cd_catalog_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/xml-foodmenu.json'), 'r') as f:
            self.generic_xml_foodmenu_json = json.loads(f.read())

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


if __name__ == '__main__':
    unittest.main()
