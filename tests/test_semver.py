import unittest
import jc.parsers.semver


class MyTests(unittest.TestCase):
    def test_semver_nodata(self):
        """
        Test 'semver' with no data
        """
        self.assertEqual(jc.parsers.semver.parse('', quiet=True), {})


    def test_semver_good_strings(self):
        good_strings = {
            '0.0.4': {'major': 0, 'minor': 0, 'patch': 4, 'prerelease': None, 'build': None},
            '1.2.3': {'major': 1, 'minor': 2, 'patch': 3, 'prerelease': None, 'build': None},
            '10.20.30': {'major': 10, 'minor': 20, 'patch': 30, 'prerelease': None, 'build': None},
            '1.1.2-prerelease+meta': {'major': 1, 'minor': 1, 'patch': 2, 'prerelease': 'prerelease', 'build': 'meta'},
            '1.1.2+meta': {'major': 1, 'minor': 1, 'patch': 2, 'prerelease': None, 'build': 'meta'},
            '1.1.2+meta-valid': {'major': 1, 'minor': 1, 'patch': 2, 'prerelease': None, 'build': 'meta-valid'},
            '1.0.0-alpha': {'major': 1, 'minor': 0, 'patch': 0, 'prerelease': 'alpha', 'build': None},
            '1.0.0-beta': {'major': 1, 'minor': 0, 'patch': 0, 'prerelease': 'beta', 'build': None},
            '1.0.0-alpha.beta': {'major': 1, 'minor': 0, 'patch': 0, 'prerelease': 'alpha.beta', 'build': None},
            '1.0.0-alpha.beta.1': {'major': 1, 'minor': 0, 'patch': 0, 'prerelease': 'alpha.beta.1', 'build': None},
            '1.0.0-alpha.1': {'major': 1, 'minor': 0, 'patch': 0, 'prerelease': 'alpha.1', 'build': None},
            '1.0.0-alpha0.valid': {'major': 1, 'minor': 0, 'patch': 0, 'prerelease': 'alpha0.valid', 'build': None},
            '1.0.0-alpha.0valid': {'major': 1, 'minor': 0, 'patch': 0, 'prerelease': 'alpha.0valid', 'build': None},
            '1.0.0-alpha-a.b-c-somethinglong+build.1-aef.1-its-okay': {'major': 1, 'minor': 0, 'patch': 0, 'prerelease': 'alpha-a.b-c-somethinglong', 'build': 'build.1-aef.1-its-okay'},
            '1.0.0-rc.1+build.1': {'major': 1, 'minor': 0, 'patch': 0, 'prerelease': 'rc.1', 'build': 'build.1'},
            '2.0.0-rc.1+build.123': {'major': 2, 'minor': 0, 'patch': 0, 'prerelease': 'rc.1', 'build': 'build.123'},
            '1.2.3-beta': {'major': 1, 'minor': 2, 'patch': 3, 'prerelease': 'beta', 'build': None},
            '10.2.3-DEV-SNAPSHOT': {'major': 10, 'minor': 2, 'patch': 3, 'prerelease': 'DEV-SNAPSHOT', 'build': None},
            '1.2.3-SNAPSHOT-123': {'major': 1, 'minor': 2, 'patch': 3, 'prerelease': 'SNAPSHOT-123', 'build': None},
            '1.0.0': {'major': 1, 'minor': 0, 'patch': 0, 'prerelease': None, 'build': None},
            '2.0.0': {'major': 2, 'minor': 0, 'patch': 0, 'prerelease': None, 'build': None},
            '1.1.7': {'major': 1, 'minor': 1, 'patch': 7, 'prerelease': None, 'build': None},
            '2.0.0+build.1848': {'major': 2, 'minor': 0, 'patch': 0, 'prerelease': None, 'build': 'build.1848'},
            '2.0.1-alpha.1227': {'major': 2, 'minor': 0, 'patch': 1, 'prerelease': 'alpha.1227', 'build': None},
            '1.0.0-alpha+beta': {'major': 1, 'minor': 0, 'patch': 0, 'prerelease': 'alpha', 'build': 'beta'},
            '1.2.3----RC-SNAPSHOT.12.9.1--.12+788': {'major': 1, 'minor': 2, 'patch': 3, 'prerelease': '---RC-SNAPSHOT.12.9.1--.12', 'build': '788'},
            '1.2.3----R-S.12.9.1--.12+meta': {'major': 1, 'minor': 2, 'patch': 3, 'prerelease': '---R-S.12.9.1--.12', 'build': 'meta'},
            '1.2.3----RC-SNAPSHOT.12.9.1--.12': {'major': 1, 'minor': 2, 'patch': 3, 'prerelease': '---RC-SNAPSHOT.12.9.1--.12', 'build': None},
            '1.0.0+0.build.1-rc.10000aaa-kk-0.1': {'major': 1, 'minor': 0, 'patch': 0, 'prerelease': None, 'build': '0.build.1-rc.10000aaa-kk-0.1'},
            '99999999999999999999999.999999999999999999.99999999999999999': {'major': 99999999999999999999999, 'minor': 999999999999999999, 'patch': 99999999999999999, 'prerelease': None, 'build': None},
            '1.0.0-0A.is.legal': {'major': 1, 'minor': 0, 'patch': 0, 'prerelease': '0A.is.legal', 'build': None}
        }

        for ver_string, expected in good_strings.items():
            self.assertEqual(jc.parsers.semver.parse(ver_string, quiet=True), expected)


    def test_semver_bad_strings(self):
        bad_strings = [
            '1',
            '1.2',
            '1.2.3-0123',
            '1.2.3-0123.0123',
            '1.1.2+.123',
            '+invalid',
            '-invalid',
            '-invalid+invalid',
            '-invalid.01',
            'alpha',
            'alpha.beta',
            'alpha.beta.1',
            'alpha.1',
            'alpha+beta',
            'alpha_beta',
            'alpha.',
            'alpha..',
            'beta',
            '1.0.0-alpha_beta',
            '-alpha.',
            '1.0.0-alpha..',
            '1.0.0-alpha..1',
            '1.0.0-alpha...1',
            '1.0.0-alpha....1',
            '1.0.0-alpha.....1',
            '1.0.0-alpha......1',
            '1.0.0-alpha.......1',
            '01.1.1',
            '1.01.1',
            '1.1.01',
            '1.2',
            '1.2.3.DEV',
            '1.2-SNAPSHOT',
            '1.2.31.2.3----RC-SNAPSHOT.12.09.1--..12+788',
            '1.2-RC-SNAPSHOT',
            '-1.0.3-gamma+b7718',
            '+justmeta',
            '9.8.7+meta+meta',
            '9.8.7-whatever+meta+meta',
            '99999999999999999999999.999999999999999999.99999999999999999----RC-SNAPSHOT.12.09.1--------------------------------..12'
        ]

        for item in bad_strings:
            self.assertEqual(jc.parsers.semver.parse(item, quiet=True), {})


if __name__ == '__main__':
    unittest.main()
