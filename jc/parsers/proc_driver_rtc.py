r"""jc - JSON Convert `/proc/driver/rtc` file parser

Usage (cli):

    $ cat /proc/driver/rtc | jc --proc

or

    $ jc /proc/driver/rtc

or

    $ cat /proc/driver/rtc | jc --proc-driver-rtc

Usage (module):

    import jc
    result = jc.parse('proc', proc_driver_rtc_file)

or

    import jc
    result = jc.parse('proc_driver_rtc', proc_driver_rtc_file)

Schema:

"yes" and "no" values are converted to `true`/`false`. Integer conversions
are attempted. If you do not want this behavior, then use `--raw` (cli) or
`raw=True` (module).

    {
      "rtc_time":                       string,
      "rtc_date":                       string,
      "alrm_time":                      string,
      "alrm_date":                      string,
      "alarm_IRQ":                      boolean,
      "alrm_pending":                   boolean,
      "update IRQ enabled":             boolean,
      "periodic IRQ enabled":           boolean,
      "periodic IRQ frequency":         integer,
      "max user IRQ frequency":         integer,
      "24hr":                           boolean,
      "periodic_IRQ":                   boolean,
      "update_IRQ":                     boolean,
      "HPET_emulated":                  boolean,
      "BCD":                            boolean,
      "DST_enable":                     boolean,
      "periodic_freq":                  integer,
      "batt_status":                    string
    }

Examples:

    $ cat /proc/driver/rtc | jc --proc -p
    {
      "rtc_time": "16:09:21",
      "rtc_date": "2022-09-03",
      "alrm_time": "00:00:00",
      "alrm_date": "2022-09-03",
      "alarm_IRQ": false,
      "alrm_pending": false,
      "update IRQ enabled": false,
      "periodic IRQ enabled": false,
      "periodic IRQ frequency": 1024,
      "max user IRQ frequency": 64,
      "24hr": true,
      "periodic_IRQ": false,
      "update_IRQ": false,
      "HPET_emulated": true,
      "BCD": true,
      "DST_enable": false,
      "periodic_freq": 1024,
      "batt_status": "okay"
    }

    $ cat /proc/driver/rtc | jc --proc -p -r
    {
      "rtc_time": "16:09:21",
      "rtc_date": "2022-09-03",
      "alrm_time": "00:00:00",
      "alrm_date": "2022-09-03",
      "alarm_IRQ": "no",
      "alrm_pending": "no",
      "update IRQ enabled": "no",
      "periodic IRQ enabled": "no",
      "periodic IRQ frequency": "1024",
      "max user IRQ frequency": "64",
      "24hr": "yes",
      "periodic_IRQ": "no",
      "update_IRQ": "no",
      "HPET_emulated": "yes",
      "BCD": "yes",
      "DST_enable": "no",
      "periodic_freq": "1024",
      "batt_status": "okay"
    }
"""
from typing import Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`/proc/driver/rtc` file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    tags = ['file']
    hidden = True


__version__ = info.version


def _process(proc_data: Dict) -> Dict:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured to conform to the schema.
    """
    for key, val in proc_data.items():
        try:
            proc_data[key] = int(val)
        except:
            pass

        if val == 'yes':
            proc_data[key] = True

        if val == 'no':
            proc_data[key] = False

    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> Dict:
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: Dict = {}

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            split_line = line.split(':', maxsplit=1)
            key = split_line[0].strip()
            val = split_line[1].rsplit(maxsplit=1)[0]
            raw_output[key] = val

    return raw_output if raw else _process(raw_output)
