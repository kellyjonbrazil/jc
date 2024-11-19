import os
import unittest
import json
import jc.parsers.yaml

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    import ruamel.yaml
    RUAMELYAML_INSTALLED = True
except:
    RUAMELYAML_INSTALLED = False


@unittest.skipIf(not RUAMELYAML_INSTALLED, 'ruamel.yaml library not installed')
class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/yaml-istio-sc.yaml'), 'r', encoding='utf-8') as f:
        generic_yaml_istio_sc = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/yaml-istio-sidecar.yaml'), 'r', encoding='utf-8') as f:
        generic_yaml_istio_sidecar = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/yaml-istio-sc.json'), 'r', encoding='utf-8') as f:
        generic_yaml_istio_sc_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/yaml-istio-sidecar.json'), 'r', encoding='utf-8') as f:
        generic_yaml_istio_sidecar_json = json.loads(f.read())


    def test_yaml_nodata(self):
        """
        Test the YAML parser with no data
        """
        self.assertEqual(jc.parsers.yaml.parse('', quiet=True), [])

    def test_yaml_istio_sc(self):
        """
        Test the Istio SC yaml file
        """
        self.assertEqual(jc.parsers.yaml.parse(self.generic_yaml_istio_sc, quiet=True), self.generic_yaml_istio_sc_json)

    def test_yaml_istio_sidecar(self):
        """
        Test the Istio Sidecar yaml file
        """
        self.assertEqual(jc.parsers.yaml.parse(self.generic_yaml_istio_sidecar, quiet=True), self.generic_yaml_istio_sidecar_json)

    def test_yaml_datetime(self):
        """
        Test yaml file with datetime object (should convert to a string)
        """
        data = 'deploymentTime: 2022-04-18T11:12:47'
        expected = [{"deploymentTime":"2022-04-18T11:12:47"}]
        self.assertEqual(jc.parsers.yaml.parse(data, quiet=True), expected)

    def test_yaml_equalsign(self):
        """
        Test yaml file with a value that starts with a literal equal sign "=" (should convert to a string)
        """
        data = 'key: ='
        expected = [{"key":"="}]
        self.assertEqual(jc.parsers.yaml.parse(data, quiet=True), expected)


if __name__ == '__main__':
    unittest.main()
