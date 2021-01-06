"""jc - JSON CLI output utility `iw DEV scan` command output parser

<<Short iw-scan description and caveats>>

Usage (cli):

    $ iw dev wlan0 scan | jc --iw-scan

    or

    $ jc iw dev wlan0 scan

Usage (module):

    import jc.parsers.iw-scan
    result = jc.parsers.iw-scan.parse(iw-scan_command_output)

Compatibility:

    'linux'

Examples:

    $ iw-scan | jc --iw-scan -p
    []

    $ iw-scan | jc --iw-scan -p -r
    []
"""
import jc.utils


class info():
    version = '0.5'
    description = 'iw dev <device> scan command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux']
    magic_commands = ['iw dev']


__version__ = info.version


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data with the following schema:

        [
          {
            "iw-scan":     string,
            "bar":     boolean,
            "baz":     integer
          }
        ]
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

def post_parse(data):
    # remove empty items
    cleandata = []
    for ssid in data:
        ssid = { k : v for k, v in ssid.items() if v}
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

    return process(cleandata)

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
                section['mac_address'] = split_line[1]
                section['interface'] = split_line[3]

                continue

            if line.startswith('    '):
                # ignore problematic lines
                if 'Maximum RX AMPDU length' in line:
                    continue

                split_line = line.split(':', maxsplit=1)
                if len(split_line) == 2:
                    split_line[0] = split_line[0].lower().replace('*', '').replace('(', '').replace(')', '').replace(',', '').strip().replace(' ', '_')
                    section[split_line[0]] = split_line[1].strip()

                continue



    if section:
        raw_output.append(section)

    if raw:
        return raw_output
    else:
        return post_parse(raw_output)
