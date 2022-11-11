import os
import unittest
import json
import jc.parsers.git_log

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log.out'), 'r', encoding='utf-8') as f:
        git_log = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-short.out'), 'r', encoding='utf-8') as f:
        git_log_short = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-short-stat.out'), 'r', encoding='utf-8') as f:
        git_log_short_stat = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-short-shortstat.out'), 'r', encoding='utf-8') as f:
        git_log_short_shortstat = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-medium.out'), 'r', encoding='utf-8') as f:
        git_log_medium = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-medium-stat.out'), 'r', encoding='utf-8') as f:
        git_log_medium_stat = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-medium-shortstat.out'), 'r', encoding='utf-8') as f:
        git_log_medium_shortstat = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-full.out'), 'r', encoding='utf-8') as f:
        git_log_full = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-full-stat.out'), 'r', encoding='utf-8') as f:
        git_log_full_stat = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-full-shortstat.out'), 'r', encoding='utf-8') as f:
        git_log_full_shortstat = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-fuller.out'), 'r', encoding='utf-8') as f:
        git_log_fuller = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-fuller-stat.out'), 'r', encoding='utf-8') as f:
        git_log_fuller_stat = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-fuller-shortstat.out'), 'r', encoding='utf-8') as f:
        git_log_fuller_shortstat = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-oneline.out'), 'r', encoding='utf-8') as f:
        git_log_oneline = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-oneline-stat.out'), 'r', encoding='utf-8') as f:
        git_log_oneline_stat = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-oneline-shortstat.out'), 'r', encoding='utf-8') as f:
        git_log_oneline_shortstat = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-hash-in-message-fix.out'), 'r', encoding='utf-8') as f:
        git_log_fuller_hash_in_message_fix = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-is-hash-regex-fix.out'), 'r', encoding='utf-8') as f:
        git_log_fuller_is_hash_regex_fix = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-blank-author-fix.out'), 'r', encoding='utf-8') as f:
        git_log_blank_author_fix = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log.json'), 'r', encoding='utf-8') as f:
        git_log_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-short.json'), 'r', encoding='utf-8') as f:
        git_log_short_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-short-stat.json'), 'r', encoding='utf-8') as f:
        git_log_short_stat_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-short-shortstat.json'), 'r', encoding='utf-8') as f:
        git_log_short_shortstat_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-medium.json'), 'r', encoding='utf-8') as f:
        git_log_medium_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-medium-stat.json'), 'r', encoding='utf-8') as f:
        git_log_medium_stat_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-medium-shortstat.json'), 'r', encoding='utf-8') as f:
        git_log_medium_shortstat_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-full.json'), 'r', encoding='utf-8') as f:
        git_log_full_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-full-stat.json'), 'r', encoding='utf-8') as f:
        git_log_full_stat_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-full-shortstat.json'), 'r', encoding='utf-8') as f:
        git_log_full_shortstat_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-fuller.json'), 'r', encoding='utf-8') as f:
        git_log_fuller_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-fuller-stat.json'), 'r', encoding='utf-8') as f:
        git_log_fuller_stat_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-fuller-shortstat.json'), 'r', encoding='utf-8') as f:
        git_log_fuller_shortstat_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-oneline.json'), 'r', encoding='utf-8') as f:
        git_log_oneline_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-oneline-stat.json'), 'r', encoding='utf-8') as f:
        git_log_oneline_stat_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-oneline-shortstat.json'), 'r', encoding='utf-8') as f:
        git_log_oneline_shortstat_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-hash-in-message-fix.json'), 'r', encoding='utf-8') as f:
        git_log_fuller_hash_in_message_fix_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-is-hash-regex-fix.json'), 'r', encoding='utf-8') as f:
        git_log_fuller_is_hash_regex_fix_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/git-log-blank-author-fix.json'), 'r', encoding='utf-8') as f:
        git_log_blank_author_fix_json = json.loads(f.read())


    def test_git_log_nodata(self):
        """
        Test 'git_log' with no data
        """
        self.assertEqual(jc.parsers.git_log.parse('', quiet=True), [])

    def test_git_log(self):
        """
        Test 'git_log'
        """
        self.assertEqual(jc.parsers.git_log.parse(self.git_log, quiet=True), self.git_log_json)

    def test_git_log_short(self):
        """
        Test 'git_log --format=short'
        """
        self.assertEqual(jc.parsers.git_log.parse(self.git_log_short, quiet=True), self.git_log_short_json)

    def test_git_log_short_stat(self):
        """
        Test 'git_log --format=short --stat'
        """
        self.assertEqual(jc.parsers.git_log.parse(self.git_log_short_stat, quiet=True), self.git_log_short_stat_json)

    def test_git_log_short_shortstat(self):
        """
        Test 'git_log --format=short --shortstat'
        """
        self.assertEqual(jc.parsers.git_log.parse(self.git_log_short_shortstat, quiet=True), self.git_log_short_shortstat_json)

    def test_git_log_medium(self):
        """
        Test 'git_log --format=medium'
        """
        self.assertEqual(jc.parsers.git_log.parse(self.git_log_medium, quiet=True), self.git_log_medium_json)

    def test_git_log_medium_stat(self):
        """
        Test 'git_log --format=medium --stat'
        """
        self.assertEqual(jc.parsers.git_log.parse(self.git_log_medium_stat, quiet=True), self.git_log_medium_stat_json)

    def test_git_log_medium_shortstat(self):
        """
        Test 'git_log --format=medium --shortstat'
        """
        self.assertEqual(jc.parsers.git_log.parse(self.git_log_medium_shortstat, quiet=True), self.git_log_medium_shortstat_json)

    def test_git_log_full(self):
        """
        Test 'git_log --format=full'
        """
        self.assertEqual(jc.parsers.git_log.parse(self.git_log_full, quiet=True), self.git_log_full_json)

    def test_git_log_full_stat(self):
        """
        Test 'git_log --format=full --stat'
        """
        self.assertEqual(jc.parsers.git_log.parse(self.git_log_full_stat, quiet=True), self.git_log_full_stat_json)

    def test_git_log_full_shortstat(self):
        """
        Test 'git_log --format=full --shortstat'
        """
        self.assertEqual(jc.parsers.git_log.parse(self.git_log_full_shortstat, quiet=True), self.git_log_full_shortstat_json)

    def test_git_log_fuller(self):
        """
        Test 'git_log --format=fuller'
        """
        self.assertEqual(jc.parsers.git_log.parse(self.git_log_fuller, quiet=True), self.git_log_fuller_json)

    def test_git_log_fuller_stat(self):
        """
        Test 'git_log --format=fuller --stat'
        """
        self.assertEqual(jc.parsers.git_log.parse(self.git_log_fuller_stat, quiet=True), self.git_log_fuller_stat_json)

    def test_git_log_fuller_shortstat(self):
        """
        Test 'git_log --format=fuller --shortstat'
        """
        self.assertEqual(jc.parsers.git_log.parse(self.git_log_fuller_shortstat, quiet=True), self.git_log_fuller_shortstat_json)

    def test_git_log_oneline(self):
        """
        Test 'git_log --format=oneline'
        """
        self.assertEqual(jc.parsers.git_log.parse(self.git_log_oneline, quiet=True), self.git_log_oneline_json)

    def test_git_log_oneline_stat(self):
        """
        Test 'git_log --format=oneline --stat'
        """
        self.assertEqual(jc.parsers.git_log.parse(self.git_log_oneline_stat, quiet=True), self.git_log_oneline_stat_json)

    def test_git_log_oneline_shortstat(self):
        """
        Test 'git_log --format=oneline --shortstat'
        """
        self.assertEqual(jc.parsers.git_log.parse(self.git_log_oneline_shortstat, quiet=True), self.git_log_oneline_shortstat_json)

    def test_git_log_fuller_hash_in_message_fix(self):
        """
        Test 'git_log --format=fuller --stat' fix for when a commit message
        contains a line that is only a commit hash value.
        """
        self.assertEqual(jc.parsers.git_log.parse(self.git_log_fuller_hash_in_message_fix, quiet=True), self.git_log_fuller_hash_in_message_fix_json)

    def test_git_log_fuller_is_hash_fix(self):
        """
        Test 'git_log --format=fuller --stat' fix for when a commit message
        contains a line that evaluated as true to an older _is_hash regex
        """
        self.assertEqual(jc.parsers.git_log.parse(self.git_log_fuller_is_hash_regex_fix, quiet=True), self.git_log_fuller_is_hash_regex_fix_json)

    def test_git_log_blank_author_fix(self):
        """
        Test 'git_log' fix for when a commit author has a blank name,
        empty email, or both
        """
        self.assertEqual(jc.parsers.git_log.parse(self.git_log_blank_author_fix, quiet=True), self.git_log_blank_author_fix_json)


if __name__ == '__main__':
    unittest.main()
