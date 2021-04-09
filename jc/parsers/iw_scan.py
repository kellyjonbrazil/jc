"""jc - JSON CLI output utility `iw dev <device> scan` command output parser

This parser is considered beta quality. Not all fields are parsed and there are not enough samples to test.

Usage (cli):

    $ iw dev wlan0 scan | jc --iw-scan

    or

    $ jc iw dev wlan0 scan

Usage (module):

    import jc.parsers.iw-scan
    result = jc.parsers.iw-scan.parse(iw-scan_command_output)

Schema:

    [
      {
        "foo":     string/integer/float,         # best guess based on value
        "bar":     string/integer/float,
        "baz":     string/integer/float
      }
    ]

Examples:

    $ iw dev wlan0 scan | jc --iw-scan -p
    [
      {
        "bssid": "71:31:72:65:e1:a2",
        "interface": "wlan0",
        "freq": 2462,
        "capability": "ESS Privacy ShortSlotTime (0x0411)",
        "ssid": "WLAN-1234",
        "supported_rates": [
          1.0,
          2.0,
          5.5,
          11.0,
          18.0,
          24.0,
          36.0,
          54.0
        ],
        "erp": "<no flags>",
        "erp_d4.0": "<no flags>",
        "rsn": "Version: 1",
        "group_cipher": "CCMP",
        "pairwise_ciphers": "CCMP",
        "authentication_suites": "PSK",
        "capabilities": "0x186c",
        "extended_supported_rates": [
          6.0,
          9.0,
          12.0,
          48.0
        ],
        "ht_rx_mcs_rate_indexes_supported": "0-15",
        "primary_channel": 11,
        "secondary_channel_offset": "no secondary",
        "rifs": 1,
        "ht_protection": "no",
        "non-gf_present": 1,
        "obss_non-gf_present": 0,
        "dual_beacon": 0,
        "dual_cts_protection": 0,
        "stbc_beacon": 0,
        "l-sig_txop_prot": 0,
        "pco_active": 0,
        "pco_phase": 0,
        "bss_width_channel_transition_delay_factor": 5,
        "extended_capabilities": "HT Information Exchange Supported",
        "wmm": "Parameter version 1",
        "be": "CW 15-1023, AIFSN 3",
        "bk": "CW 15-1023, AIFSN 7",
        "vi": "CW 7-15, AIFSN 2, TXOP 3008 usec",
        "vo": "CW 3-7, AIFSN 2, TXOP 1504 usec",
        "wps": "Version: 1.0",
        "wi-fi_protected_setup_state": "2 (Configured)",
        "selected_registrar": "0x0",
        "response_type": "3 (AP)",
        "uuid": "00000000-0000-0003-0000-75317074f1a2",
        "manufacturer": "Corporation",
        "model": "VGV8539JW",
        "model_number": "1.47.000",
        "serial_number": "J144024542",
        "primary_device_type": "6-0050f204-1",
        "device_name": "Wireless Router(WFA)",
        "config_methods": "Label, PBC",
        "rf_bands": "0x3",
        "tsf_usec": 212098649788,
        "sta_channel_width_mhz": 20,
        "passive_dwell_tus": 20,
        "active_dwell_tus": 10,
        "channel_width_trigger_scan_interval_s": 300,
        "scan_passive_total_per_channel_tus": 200,
        "scan_active_total_per_channel_tus": 20,
        "beacon_interval_tus": 100,
        "signal_dbm": -80.0,
        "last_seen_ms": 11420,
        "selected_rates": [
          1.0,
          2.0,
          5.5,
          11.0
        ],
        "obss_scan_activity_threshold_percent": 0.25,
        "ds_parameter_set_channel": 11,
        "max_amsdu_length_bytes": 7935,
        "minimum_rx_ampdu_time_spacing_usec": 16
      },
      ...
    ]
"""
import re
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '0.6'
    description = '`iw dev [device] scan` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Enhancements by Philipp Schmitt (https://pschmitt.dev/)'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux']
    magic_commands = ['iw dev']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema.
    """

    # convert ints and floats for top-level keys
    for item in proc_data:
        for key in item:
            try:
                item[key] = int(item[key])
            except (Exception):
                try:
                    item[key] = float(item[key])
                except (Exception):
                    pass
            # convert ints and floats for lists
            if isinstance(item[key], list):
                new_list = []
                for list_item in item[key]:
                    try:
                        new_list.append(int(list_item))
                    except (Exception):
                        try:
                            new_list.append(float(list_item))
                        except (Exception):
                            pass
                item[key] = new_list

    return proc_data


def _post_parse(data):
    # remove empty items
    cleandata = []
    for ssid in data:
        ssid = {k: v for k, v in ssid.items() if v}
        cleandata.append(ssid)

    # remove asterisks from begining of values
    for ssid in cleandata:
        for key in ssid:
            if ssid[key].startswith('*'):
                ssid[key] = ssid[key][1:].strip()

    for item in cleandata:
        if 'country' in item:
            country_split = item['country'].split()
            item['country'] = country_split[0]
            if len(country_split) > 1:
                item['environment'] = country_split[2]

        if 'tsf' in item:
            item['tsf_usec'] = item['tsf'].split()[0]
            del item['tsf']

        if 'sta_channel_width' in item:
            item['sta_channel_width_mhz'] = item['sta_channel_width'].replace(' MHz', '')
            del item['sta_channel_width']

        if 'passive_dwell' in item:
            item['passive_dwell_tus'] = item['passive_dwell'].replace(' TUs', '')
            del item['passive_dwell']

        if 'active_dwell' in item:
            item['active_dwell_tus'] = item['active_dwell'].replace(' TUs', '')
            del item['active_dwell']

        if 'channel_width_trigger_scan_interval' in item:
            item['channel_width_trigger_scan_interval_s'] = item['channel_width_trigger_scan_interval'].replace(' s', '')
            del item['channel_width_trigger_scan_interval']

        if 'scan_passive_total_per_channel' in item:
            item['scan_passive_total_per_channel_tus'] = item['scan_passive_total_per_channel'].replace(' TUs', '')
            del item['scan_passive_total_per_channel']

        if 'scan_active_total_per_channel' in item:
            item['scan_active_total_per_channel_tus'] = item['scan_active_total_per_channel'].replace(' TUs', '')
            del item['scan_active_total_per_channel']

        if 'beacon_interval' in item:
            item['beacon_interval_tus'] = item['beacon_interval'].replace(' TUs', '')
            del item['beacon_interval']

        if 'signal' in item:
            item['signal_dbm'] = item['signal'].replace(' dBm', '')
            del item['signal']

        if 'last_seen' in item:
            item['last_seen_ms'] = item['last_seen'].replace(' ms ago', '')
            del item['last_seen']

        if 'supported_rates' in item:
            selected_rates = []
            for rate in item['supported_rates'].split():
                if rate.endswith('*'):
                    selected_rates.append(rate.replace('*', ''))
            item['selected_rates'] = selected_rates
            item['supported_rates'] = item['supported_rates'].replace('*', '').split()

        if 'extended_supported_rates' in item:
            item['extended_supported_rates'] = item['extended_supported_rates'].split()

        if 'obss_scan_activity_threshold' in item:
            item['obss_scan_activity_threshold_percent'] = item['obss_scan_activity_threshold'].replace(' %', '')
            del item['obss_scan_activity_threshold']

        if 'ds_parameter_set' in item:
            item['ds_parameter_set_channel'] = item['ds_parameter_set'].replace('channel ', '')
            del item['ds_parameter_set']

        if 'max_amsdu_length' in item:
            item['max_amsdu_length_bytes'] = item['max_amsdu_length'].replace(' bytes', '')
            del item['max_amsdu_length']

        if 'available_admission_capacity' in item:
            item['available_admission_capacity'] = item['available_admission_capacity'].replace(' [*32us]', '')

        if 'power_constraint' in item:
            item['power_constraint_db'] = item['power_constraint'].replace(' dB', '')
            del item['power_constraint']

        if 'minimum_rx_ampdu_time_spacing' in item:
            item['minimum_rx_ampdu_time_spacing_usec'] = item['minimum_rx_ampdu_time_spacing'].split()[0]
            del item['minimum_rx_ampdu_time_spacing']

        if 'vht_rx_highest_supported' in item:
            item['vht_rx_highest_supported_mbps'] = item['vht_rx_highest_supported'].replace(' Mbps', '')
            del item['vht_rx_highest_supported']

        if 'vht_tx_highest_supported' in item:
            item['vht_tx_highest_supported_mbps'] = item['vht_tx_highest_supported'].replace(' Mbps', '')
            del item['vht_tx_highest_supported']

    return _process(cleandata)


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = []
    section = {}

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            if line.startswith('BSS'):
                if section:
                    raw_output.append(section)
                    section = {}

                split_line = line.replace('(', ' ').replace(')', ' ').split()
                section['bssid'] = split_line[1]
                section['interface'] = split_line[3]

                continue

            if re.match(r"^\s+.+", line):
                # ignore problematic lines
                if 'Maximum RX AMPDU length' in line:
                    continue

                split_line = line.split(':', maxsplit=1)
                if len(split_line) == 2:
                    split_line[0] = split_line[0].lower().replace('*', '').replace('(', '').replace(')', '').replace(',', '').replace('-', '_').strip().replace(' ', '_')
                    section[split_line[0]] = split_line[1].strip()

                continue

    if section:
        raw_output.append(section)

    if raw:
        return raw_output
    else:
        return _post_parse(raw_output)
