import os
import json
import unittest
import jc.parsers.systemextensionsctl

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # Input data from fixtures
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/systemextensionsctl.out'), 'r', encoding='utf-8') as f:
        systemextensionsctl_output = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/systemextensionsctl-empty.out'), 'r', encoding='utf-8') as f:
        systemextensionsctl_empty_output = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/systemextensionsctl-no-extensions.out'), 'r', encoding='utf-8') as f:
        systemextensionsctl_no_extensions_output = f.read()

    # Expected output data from fixtures
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/systemextensionsctl.json'), 'r', encoding='utf-8') as f:
        systemextensionsctl_expected = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/systemextensionsctl-empty.json'), 'r', encoding='utf-8') as f:
        systemextensionsctl_empty_expected = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/systemextensionsctl-no-extensions.json'), 'r', encoding='utf-8') as f:
        systemextensionsctl_no_extensions_expected = json.loads(f.read())

    def test_systemextensionsctl(self):
        """
        Test 'systemextensionsctl list' with placeholder data
        """
        self.assertEqual(
            jc.parsers.systemextensionsctl.parse(
                self.systemextensionsctl_output, quiet=True),
            self.systemextensionsctl_expected
        )

    def test_systemextensionsctl_empty(self):
        """
        Test 'systemextensionsctl list' with empty input
        """
        self.assertEqual(
            jc.parsers.systemextensionsctl.parse(
                self.systemextensionsctl_empty_output, quiet=True),
            self.systemextensionsctl_empty_expected
        )

    def test_systemextensionsctl_no_extensions(self):
        """
        Test 'systemextensionsctl list' with no extensions
        """
        self.assertEqual(
            jc.parsers.systemextensionsctl.parse(
                self.systemextensionsctl_no_extensions_output, quiet=True),
            self.systemextensionsctl_no_extensions_expected
        )

    def test_systemextensionsctl_nodata(self):
        """
        Test 'systemextensionsctl list' with no data
        """
        self.assertEqual(jc.parsers.systemextensionsctl.parse('', quiet=True), {})

    def test_systemextensionsctl_incorrect_format(self):
        """
        Test 'systemextensionsctl list' with incorrect format
        """
        incorrect_data = 'This is not the correct format.'
        self.assertEqual(
            jc.parsers.systemextensionsctl.parse(incorrect_data, quiet=True), {}
        )

    def test_systemextensionsctl_trailing_newline(self):
        """
        Test 'systemextensionsctl list' with trailing newline
        """
        cmd_output = self.systemextensionsctl_output + '\n'
        self.assertEqual(
            jc.parsers.systemextensionsctl.parse(cmd_output, quiet=True),
            self.systemextensionsctl_expected
        )


if __name__ == '__main__':
    unittest.main()
