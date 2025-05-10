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
        self.test_files_processed_json = [f'{file}-processed.json' for file in self.TEST_FILES_NAME]

    def test_amixer_sget_nodata(self):
        """
        Test 'amixer' with no data
        """
        self.assertEqual(jc.parsers.amixer.parse('', quiet=True), {})

    def test_amixer_sget(self):
        for file_out, file_json, file_processed_json in zip(self.test_files_out, self.test_files_json,
                                                            self.test_files_processed_json):
            with open(file_out, 'r') as f:
                amixer_sget_raw_output = f.read()
            with open(file_json, 'r') as f:
                expected_amixer_sget_json_output = f.read()
                expected_amixer_sget_json_map = json.loads(expected_amixer_sget_json_output)
            with open(file_processed_json, 'r') as f:
                expected_amixer_sget_processed_json_output = f.read()
                expected_amixer_sget_processed_json_map = json.loads(expected_amixer_sget_processed_json_output)

            # Tests for raw=True
            amixer_sget_json_map = jc.parse(self.AMIXER_CMD, amixer_sget_raw_output, raw=True,
                                                  quiet=True)
            self.assertEqual(amixer_sget_json_map, expected_amixer_sget_json_map)
            # Tests for raw=False process
            amixer_sget_json_processed_map = jc.parse(self.AMIXER_CMD, amixer_sget_raw_output, raw=False,
                                                            quiet=True)
            self.assertEqual(amixer_sget_json_processed_map, expected_amixer_sget_processed_json_map)

    def test_amixer_missing_db(self):
        data = '''Simple mixer control 'Master',0
  Capabilities: pvolume pswitch pswitch-joined
  Playback channels: Front Left - Front Right
  Limits: Playback 0 - 65536
  Mono:
  Front Left: Playback 55039 [84%] [on]
  Front Right: Playback 54383 [83%] [on]
Simple mixer control 'Capture',0
  Capabilities: cvolume cswitch cswitch-joined
  Capture channels: Front Left - Front Right
  Limits: Capture 0 - 65536
  Front Left: Capture 24672 [38%] [on]
  Front Right: Capture 24672 [38%] [on]'''
        expected = {"control_name":"Master","capabilities":["cvolume","cswitch","cswitch-joined"],"playback_channels":["Front Left","Front Right"],"limits":{"playback_min":0,"playback_max":65536},"front_left":{"playback_value":24672,"percentage":38,"db":0.0,"status":True},"front_right":{"playback_value":24672,"percentage":38,"db":0.0,"status":True}}
        self.assertEqual(expected, jc.parsers.amixer.parse(data, quiet=True))

if __name__ == '__main__':
    unittest.main()
