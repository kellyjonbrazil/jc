import os
import json
import unittest
import jc.parsers.git_log_s

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# To create streaming output use:
# $ cat git_log.out | jc --git-log-s | jello -c > git-log-streaming.json


class MyTests(unittest.TestCase):

    def setUp(self):
        pass
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log.out'), 'r', encoding='utf-8') as f:
            self.generic_git_log = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-short.out'), 'r', encoding='utf-8') as f:
            self.generic_git_log_short = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-short-stat.out'), 'r', encoding='utf-8') as f:
            self.generic_git_log_short_stat = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-short-shortstat.out'), 'r', encoding='utf-8') as f:
            self.generic_git_log_short_shortstat = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-medium.out'), 'r', encoding='utf-8') as f:
            self.generic_git_log_medium = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-medium-stat.out'), 'r', encoding='utf-8') as f:
            self.generic_git_log_medium_stat = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-medium-shortstat.out'), 'r', encoding='utf-8') as f:
            self.generic_git_log_medium_shortstat = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-full.out'), 'r', encoding='utf-8') as f:
            self.generic_git_log_full = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-full-stat.out'), 'r', encoding='utf-8') as f:
            self.generic_git_log_full_stat = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-full-shortstat.out'), 'r', encoding='utf-8') as f:
            self.generic_git_log_full_shortstat = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-fuller.out'), 'r', encoding='utf-8') as f:
            self.generic_git_log_fuller = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-fuller-stat.out'), 'r', encoding='utf-8') as f:
            self.generic_git_log_fuller_stat = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-fuller-shortstat.out'), 'r', encoding='utf-8') as f:
            self.generic_git_log_fuller_shortstat = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-oneline.out'), 'r', encoding='utf-8') as f:
            self.generic_git_log_oneline = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-oneline-stat.out'), 'r', encoding='utf-8') as f:
            self.generic_git_log_oneline_stat = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-oneline-shortstat.out'), 'r', encoding='utf-8') as f:
            self.generic_git_log_oneline_shortstat = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-streaming.json'), 'r', encoding='utf-8') as f:
            self.generic_git_log_streaming_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-short-streaming.json'), 'r', encoding='utf-8') as f:
            self.generic_git_log_short_streaming_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-short-stat-streaming.json'), 'r', encoding='utf-8') as f:
            self.generic_git_log_short_stat_streaming_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-short-shortstat-streaming.json'), 'r', encoding='utf-8') as f:
            self.generic_git_log_short_shortstat_streaming_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-medium-streaming.json'), 'r', encoding='utf-8') as f:
            self.generic_git_log_medium_streaming_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-medium-stat-streaming.json'), 'r', encoding='utf-8') as f:
            self.generic_git_log_medium_stat_streaming_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-medium-shortstat-streaming.json'), 'r', encoding='utf-8') as f:
            self.generic_git_log_medium_shortstat_streaming_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-full-streaming.json'), 'r', encoding='utf-8') as f:
            self.generic_git_log_full_streaming_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-full-stat-streaming.json'), 'r', encoding='utf-8') as f:
            self.generic_git_log_full_stat_streaming_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-full-shortstat-streaming.json'), 'r', encoding='utf-8') as f:
            self.generic_git_log_full_shortstat_streaming_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-fuller-streaming.json'), 'r', encoding='utf-8') as f:
            self.generic_git_log_fuller_streaming_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-fuller-stat-streaming.json'), 'r', encoding='utf-8') as f:
            self.generic_git_log_fuller_stat_streaming_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-fuller-shortstat-streaming.json'), 'r', encoding='utf-8') as f:
            self.generic_git_log_fuller_shortstat_streaming_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-oneline-streaming.json'), 'r', encoding='utf-8') as f:
            self.generic_git_log_oneline_streaming_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-oneline-stat-streaming.json'), 'r', encoding='utf-8') as f:
            self.generic_git_log_oneline_stat_streaming_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-oneline-shortstat-streaming.json'), 'r', encoding='utf-8') as f:
            self.generic_git_log_oneline_shortstat_streaming_json = json.loads(f.read())

    def test_git_log_s_nodata(self):
        """
        Test 'git_log' with no data
        """
        self.assertEqual(list(jc.parsers.git_log_s.parse([], quiet=True)), [])

    def test_git_log_s(self):
        """
        Test 'git_log'
        """
        self.assertEqual(list(jc.parsers.git_log_s.parse(self.generic_git_log.splitlines(), quiet=True)), self.generic_git_log_streaming_json)

    def test_git_log_short_s(self):
        """
        Test 'git_log --format=short'
        """
        self.assertEqual(list(jc.parsers.git_log_s.parse(self.generic_git_log_short.splitlines(), quiet=True)), self.generic_git_log_short_streaming_json)

    def test_git_log_short_stat_s(self):
        """
        Test 'git_log --format=short --stat'
        """
        self.assertEqual(list(jc.parsers.git_log_s.parse(self.generic_git_log_short_stat.splitlines(), quiet=True)), self.generic_git_log_short_stat_streaming_json)

    def test_git_log_short_shortstat_s(self):
        """
        Test 'git_log --format=short --shortstat'
        """
        self.assertEqual(list(jc.parsers.git_log_s.parse(self.generic_git_log_short_shortstat.splitlines(), quiet=True)), self.generic_git_log_short_shortstat_streaming_json)

    def test_git_log_medium_s(self):
        """
        Test 'git_log --format=medium'
        """
        self.assertEqual(list(jc.parsers.git_log_s.parse(self.generic_git_log_medium.splitlines(), quiet=True)), self.generic_git_log_medium_streaming_json)

    def test_git_log_medium_stat_s(self):
        """
        Test 'git_log --format=medium --stat'
        """
        self.assertEqual(list(jc.parsers.git_log_s.parse(self.generic_git_log_medium_stat.splitlines(), quiet=True)), self.generic_git_log_medium_stat_streaming_json)

    def test_git_log_medium_shortstat_s(self):
        """
        Test 'git_log --format=medium --shortstat'
        """
        self.assertEqual(list(jc.parsers.git_log_s.parse(self.generic_git_log_medium_shortstat.splitlines(), quiet=True)), self.generic_git_log_medium_shortstat_streaming_json)

    def test_git_log_full_s(self):
        """
        Test 'git_log --format=full'
        """
        self.assertEqual(list(jc.parsers.git_log_s.parse(self.generic_git_log_full.splitlines(), quiet=True)), self.generic_git_log_full_streaming_json)

    def test_git_log_full_stat_s(self):
        """
        Test 'git_log --format=full --stat'
        """
        self.assertEqual(list(jc.parsers.git_log_s.parse(self.generic_git_log_full_stat.splitlines(), quiet=True)), self.generic_git_log_full_stat_streaming_json)

    def test_git_log_full_shortstat_s(self):
        """
        Test 'git_log --format=full --shortstat'
        """
        self.assertEqual(list(jc.parsers.git_log_s.parse(self.generic_git_log_full_shortstat.splitlines(), quiet=True)), self.generic_git_log_full_shortstat_streaming_json)

    def test_git_log_fuller_s(self):
        """
        Test 'git_log --format=fuller'
        """
        self.assertEqual(list(jc.parsers.git_log_s.parse(self.generic_git_log_fuller.splitlines(), quiet=True)), self.generic_git_log_fuller_streaming_json)

    def test_git_log_fulerl_stat_s(self):
        """
        Test 'git_log --format=fuller --stat'
        """
        self.assertEqual(list(jc.parsers.git_log_s.parse(self.generic_git_log_fuller_stat.splitlines(), quiet=True)), self.generic_git_log_fuller_stat_streaming_json)

    def test_git_log_fuller_shortstat_s(self):
        """
        Test 'git_log --format=fuller --shortstat'
        """
        self.assertEqual(list(jc.parsers.git_log_s.parse(self.generic_git_log_fuller_shortstat.splitlines(), quiet=True)), self.generic_git_log_fuller_shortstat_streaming_json)

    def test_git_log_oneline_s(self):
        """
        Test 'git_log --format=oneline'
        """
        self.assertEqual(list(jc.parsers.git_log_s.parse(self.generic_git_log_oneline.splitlines(), quiet=True)), self.generic_git_log_oneline_streaming_json)

    def test_git_log_oneline_stat_s(self):
        """
        Test 'git_log --format=oneline --stat'
        """
        self.assertEqual(list(jc.parsers.git_log_s.parse(self.generic_git_log_oneline_stat.splitlines(), quiet=True)), self.generic_git_log_oneline_stat_streaming_json)

    def test_git_log_oneline_shortstat_s(self):
        """
        Test 'git_log --format=oneline --shortstat'
        """
        self.assertEqual(list(jc.parsers.git_log_s.parse(self.generic_git_log_oneline_shortstat.splitlines(), quiet=True)), self.generic_git_log_oneline_shortstat_streaming_json)


if __name__ == '__main__':
    unittest.main()
