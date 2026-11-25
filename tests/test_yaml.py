import os
import unittest
import json
import datetime
import jc.parsers.yaml
from jc.exceptions import ParseError

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    import ruamel.yaml
    RUAMELYAML_INSTALLED = True
except ImportError:
    RUAMELYAML_INSTALLED = False


@unittest.skipIf(not RUAMELYAML_INSTALLED, 'ruamel.yaml library not installed')
class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/yaml-istio-sc.yaml'), 'r', encoding='utf-8') as f:
        generic_yaml_istio_sc = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/yaml-istio-sidecar.yaml'), 'r', encoding='utf-8') as f:
        generic_yaml_istio_sidecar = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/yaml-anchors.yaml'), 'r', encoding='utf-8') as f:
        generic_yaml_anchors = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/yaml-istio-sc.json'), 'r', encoding='utf-8') as f:
        generic_yaml_istio_sc_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/yaml-istio-sidecar.json'), 'r', encoding='utf-8') as f:
        generic_yaml_istio_sidecar_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/yaml-anchors.json'), 'r', encoding='utf-8') as f:
        generic_yaml_anchors_json = json.loads(f.read())


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

    def test_yaml_anchors(self):
        """
        Test yaml file with anchors, aliases and merge keys
        """
        self.assertEqual(jc.parsers.yaml.parse(self.generic_yaml_anchors, quiet=True), self.generic_yaml_anchors_json)

    def test_yaml_repeated_aliases(self):
        """
        Test yaml file with a mapping referenced many times
        """
        data = 'd: &d {a: 1, b: [x, y]}\nl: [' + ', '.join(['*d'] * 500) + ']\n'
        result = jc.parsers.yaml.parse(data, quiet=True)
        self.assertEqual(len(result[0]['l']), 500)
        self.assertEqual(result[0]['l'][499], {'a': 1, 'b': ['x', 'y']})

    def test_yaml_alias_expansion_limit(self):
        """
        Test yaml file with nested aliases that expand far beyond the input size
        """
        lines = ['a0: &a0 [x, x, x, x, x, x, x, x, x, x]']
        for i in range(1, 10):
            lines.append('a%d: &a%d [%s]' % (i, i, ', '.join(['*a%d' % (i - 1)] * 10)))
        data = '\n'.join(lines) + '\n'
        self.assertRaises(ParseError, jc.parsers.yaml.parse, data, quiet=True)
        self.assertRaises(ParseError, jc.parsers.yaml.parse, data, raw=True, quiet=True)

    def test_yaml_no_side_effects(self):
        """
        Test 'yaml' leaves the ruamel.yaml classes unchanged for other code
        in the same process
        """
        data = 'a: 2022-04-18\nb: =\n'
        # official_plug_ins() was added in ruamel.yaml 0.15.x
        plug_ins = getattr(ruamel.yaml.YAML, 'official_plug_ins', None)
        constructors = ruamel.yaml.constructor.RoundTripConstructor.yaml_constructors.copy()
        self.assertEqual(jc.parsers.yaml.parse(data, quiet=True), [{'a': '2022-04-18', 'b': '='}])
        self.assertIs(getattr(ruamel.yaml.YAML, 'official_plug_ins', None), plug_ins)
        self.assertEqual(ruamel.yaml.constructor.RoundTripConstructor.yaml_constructors, constructors)
        self.assertEqual(ruamel.yaml.YAML().load('a: 2022-04-18\n')['a'], datetime.date(2022, 4, 18))

    def test_yaml_non_finite(self):
        """
        Test 'yaml' with nan and inf values: they are null
        """
        data = 'a: .nan\nb: -.inf\nc: [.inf, 1.5, 1e400]\nd: !!float .NaN\ne: 2.5\nf: nan\n'
        expected = [{'a': None, 'b': None, 'c': [None, 1.5, None], 'd': None, 'e': 2.5, 'f': 'nan'}]
        self.assertEqual(jc.parsers.yaml.parse(data, quiet=True), expected)


if __name__ == '__main__':
    unittest.main()
