import json
from pathlib import Path

import jc


FIXTURES = Path(__file__).parent / 'fixtures'


def test_upsc_cyberpower_fixture():
    output = (FIXTURES / 'upsc--cyberpower.out').read_text(encoding='utf-8')
    expected = json.loads(
        (FIXTURES / 'upsc--cyberpower.json').read_text(encoding='utf-8')
    )

    assert jc.parse('upsc', output) == expected


def test_upsc_raw_mode_preserves_strings():
    output = b'''battery.charge: 100
battery.voltage: 24.0
device.serial: 000000000000
driver.version.internal: 0.41
ups.test.result: Waiting: on battery
'''

    assert jc.parse('upsc', output, raw=True) == {
        'battery_charge': '100',
        'battery_voltage': '24.0',
        'device_serial': '000000000000',
        'driver_version_internal': '0.41',
        'ups_test_result': 'Waiting: on battery',
    }


def test_upsc_ignores_blank_and_malformed_lines():
    output = '''
not a variable
ups.status: OL
:
'''

    assert jc.parse('upsc', output) == {'ups_status': 'OL'}


def test_upsc_empty_input():
    assert jc.parse('upsc', '') == {}
