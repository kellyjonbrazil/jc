import unittest
import jc.parsers.amixer
import os
import json

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class AmixerTests(unittest.TestCase):
    AMIXER_CMD = 'amixer'
    UBUNTU_22_04_TEST_FIXTURES_PATH = f'{THIS_DIR}/fixtures/ubuntu-22.04/'
    AMIXER_CONTROL_PATH = f'{UBUNTU_22_04_TEST_FIXTURES_PATH}amixer-control-'
    TEST_FILES_NAME = [
        f"{AMIXER_CONTROL_PATH}capture",
        f'{AMIXER_CONTROL_PATH}headphone',
        f'{AMIXER_CONTROL_PATH}master',
        f'{AMIXER_CONTROL_PATH}speakers',
    ]

    def setUp(self):
        self.test_files_out = [f'{file}.out' for file in self.TEST_FILES_NAME]
        self.test_files_json = [f'{file}.json' for file in self.TEST_FILES_NAME]

    def test_amixer_sget(self):
        for file_out, file_json in zip(self.test_files_out, self.test_files_json):
            with open(file_out, 'r') as f:
                amixer_sget_raw_output: str = f.read()
            with open(file_json, 'r') as f:
                expected_amixer_sget_json_output: str = f.read()
                expected_amixer_sget_json_map: dict = json.loads(expected_amixer_sget_json_output)
            amixer_sget_json_map: dict = jc.parse(self.AMIXER_CMD, amixer_sget_raw_output)
            self.assertEqual(amixer_sget_json_map, expected_amixer_sget_json_map)



if __name__ == '__main__':
    unittest.main()
