import os
import unittest
import json
import jc.parsers.yaml

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/yaml-istio-sc.yaml'), 'r') as f:
            self.generic_yaml_istio_sc = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/yaml-istio-sidecar.yaml'), 'r') as f:
            self.generic_yaml_istio_sidecar = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/yaml-istio-sc.json'), 'r') as f:
            self.generic_yaml_istio_sc_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/yaml-istio-sidecar.json'), 'r') as f:
            self.generic_yaml_istio_sidecar_json = json.loads(f.read())

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


if __name__ == '__main__':
    unittest.main()
