import unittest

from jc.parsers import php_fpm


PHP_FPM_OUTPUT = """[25-Feb-2024 20:25:25] NOTICE: [global]
[25-Feb-2024 20:25:25] NOTICE:  pid = /run/php/php8.2-fpm.pid
[25-Feb-2024 20:25:25] NOTICE:  log_level = unknown value
[25-Feb-2024 20:25:25] NOTICE:
[25-Feb-2024 20:29:38] NOTICE: [www]
[25-Feb-2024 20:29:38] NOTICE:  user = www-data
[25-Feb-2024 20:29:38] NOTICE:  security.limit_extensions = .php .phar
[25-Feb-2024 20:29:38] NOTICE: configuration file /etc/php/8.2/fpm/php-fpm.conf test is successful
"""


EXPECTED = {
    'global': {
        'pid': '/run/php/php8.2-fpm.pid',
        'log_level': 'unknown value',
    },
    'www': {
        'user': 'www-data',
        'security.limit_extensions': '.php .phar',
    },
}


class PhpFpmTests(unittest.TestCase):
    def test_parses_php_fpm_82_output(self):
        self.assertEqual(php_fpm.parse(PHP_FPM_OUTPUT), EXPECTED)

    def test_accepts_bytes_and_raw_mode(self):
        self.assertEqual(
            EXPECTED,
            php_fpm.parse(PHP_FPM_OUTPUT.encode('utf-8'), raw=True),
        )

    def test_supports_arbitrary_pool_names_and_equals_in_values(self):
        sample = (
            '[01-Mar-2024 10:00:00] NOTICE: [api]\n'
            '[01-Mar-2024 10:00:00] NOTICE:  listen = 127.0.0.1:9000\n'
            '[01-Mar-2024 10:00:00] NOTICE:  env[QUERY] = one=two\n'
            '[01-Mar-2024 10:00:00] NOTICE:  process.dumpable = no\n'
        )
        self.assertEqual(
            php_fpm.parse(sample),
            {
                'api': {
                    'listen': '127.0.0.1:9000',
                    'env[QUERY]': 'one=two',
                    'process.dumpable': 'no',
                }
            },
        )

    def test_ignores_unrelated_diagnostics(self):
        sample = (
            'unrelated stderr output\n'
            '[01-Mar-2024 10:00:00] ERROR: unable to load configuration\n'
            '[01-Mar-2024 10:00:00] NOTICE: configuration file /tmp/fpm.conf test is successful\n'
        )
