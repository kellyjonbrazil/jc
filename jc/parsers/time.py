"""jc - JSON CLI output utility `/usr/bin/time` command output parser

Output from `/usr/bin/time` is sent to `STDERR`, so the `-o` option can be used to redirect the output to a file that can be read by `jc`.

Alternatively, the output from `/usr/bin/time` can be redirected to `STDOUT` so `jc` can receive it.

Note: `/usr/bin/time` is similar but different from the Bash builtin `time` command.

Usage (cli):

    $ /usr/bin/time -o timefile.out sleep 2.5; cat timefile.out | jc --time -p

Usage (module):

    import jc.parsers.time
    result = jc.parsers.time.parse(time_command_output)

Schema:

    Source: https://www.freebsd.org/cgi/man.cgi?query=getrusage
            https://man7.org/linux/man-pages/man1/time.1.html

    {
      "real_time":                          float,
      "user_time":                          float,
      "system_time":                        float,
      "elapsed_time":                       string,
      "elapsed_time_hours":                 integer,
      "elapsed_time_minutes":               integer,
      "elapsed_time_seconds":               integer,
      "elapsed_time_centiseconds":          integer,
      "elapsed_time_total_seconds":         float,
      "cpu_percent":                        integer,   # null if ?
      "average_shared_text_size":           integer,
      "average_unshared_data_size":         integer,
      "average_unshared_stack_size":        integer,
      "average_shared_memory_size":         integer,
      "maximum_resident_set_size":          integer,
      "block_input_operations":             integer,   # aka File system inputs
      "block_output_operations":            integer,   # aka File system outputs
      "major_pagefaults":                   integer,
      "minor_pagefaults":                   integer,
      "swaps":                              integer,
      "page_reclaims":                      integer,
      "page_faults":                        integer,
      "messages_sent":                      integer,
      "messages_received":                  integer,
      "signals_received":                   integer,
      "voluntary_context_switches":         integer,
      "involuntary_context_switches":       integer
      "command_being_timed":                string,
      "average_stack_size":                 integer,
      "average_total_size":                 integer,
      "average_resident_set_size":          integer,
      "signals_delivered":                  integer,
      "page_size":                          integer,
      "exit_status":                        integer
    }

Examples:

    $ /usr/bin/time --verbose -o timefile.out sleep 2.5; cat timefile.out | jc --time -p
    {
      "command_being_timed": "sleep 2.5",
      "user_time": 0.0,
      "system_time": 0.0,
      "cpu_percent": 0,
      "elapsed_time": "0:02.50",
      "average_shared_text_size": 0,
      "average_unshared_data_size": 0,
      "average_stack_size": 0,
      "average_total_size": 0,
      "maximum_resident_set_size": 2084,
      "average_resident_set_size": 0,
      "major_pagefaults": 0,
      "minor_pagefaults": 72,
      "voluntary_context_switches": 2,
      "involuntary_context_switches": 1,
      "swaps": 0,
      "block_input_operations": 0,
      "block_output_operations": 0,
      "messages_sent": 0,
      "messages_received": 0,
      "signals_delivered": 0,
      "page_size": 4096,
      "exit_status": 0,
      "elapsed_time_hours": 0,
      "elapsed_time_minutes": 0,
      "elapsed_time_seconds": 2,
      "elapsed_time_centiseconds": 50,
      "elapsed_time_total_seconds": 2.5
    }

    $ /usr/bin/time --verbose -o timefile.out sleep 2.5; cat timefile.out | jc --time -p -r
    {
      "command_being_timed": "\"sleep 2.5\"",
      "user_time": "0.00",
      "system_time": "0.00",
      "cpu_percent": "0",
      "elapsed_time": "0:02.50",
      "average_shared_text_size": "0",
      "average_unshared_data_size": "0",
      "average_stack_size": "0",
      "average_total_size": "0",
      "maximum_resident_set_size": "2084",
      "average_resident_set_size": "0",
      "major_pagefaults": "0",
      "minor_pagefaults": "72",
      "voluntary_context_switches": "2",
      "involuntary_context_switches": "0",
      "swaps": "0",
      "block_input_operations": "0",
      "block_output_operations": "0",
      "messages_sent": "0",
      "messages_received": "0",
      "signals_delivered": "0",
      "page_size": "4096",
      "exit_status": "0"
    }
"""
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.2'
    description = '`/usr/bin/time` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'aix', 'freebsd']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        Dictionary. Structured data to conform to the schema.
    """
    if 'command_being_timed' in proc_data:
        proc_data['command_being_timed'] = proc_data['command_being_timed'][1:-1]

    if 'elapsed_time' in proc_data:
        proc_data['elapsed_time'] = proc_data['elapsed_time'].replace('.', ':')
        *hours, minutes, seconds, centiseconds = proc_data['elapsed_time'].split(':')
        proc_data['elapsed_time'] = proc_data['elapsed_time'][::-1].replace(':', '.', 1)[::-1]
        if hours:
            proc_data['elapsed_time_hours'] = jc.utils.convert_to_int(hours[0])
        else:
            proc_data['elapsed_time_hours'] = 0
        proc_data['elapsed_time_minutes'] = jc.utils.convert_to_int(minutes)
        proc_data['elapsed_time_seconds'] = jc.utils.convert_to_int(seconds)
        proc_data['elapsed_time_centiseconds'] = jc.utils.convert_to_int(centiseconds)
        proc_data['elapsed_time_total_seconds'] = (proc_data['elapsed_time_hours'] * 3600) + \
                                                  (proc_data['elapsed_time_minutes'] * 60) + \
                                                  (proc_data['elapsed_time_seconds']) + \
                                                  (proc_data['elapsed_time_centiseconds'] / 100)

    # convert ints and floats
    int_list = ['cpu_percent', 'average_shared_text_size', 'average_unshared_data_size', 'average_unshared_stack_size',
                'average_shared_memory_size', 'maximum_resident_set_size', 'block_input_operations',
                'block_output_operations', 'major_pagefaults', 'minor_pagefaults', 'swaps', 'page_reclaims',
                'page_faults', 'messages_sent', 'messages_received', 'signals_received', 'voluntary_context_switches',
                'involuntary_context_switches', 'average_stack_size', 'average_total_size', 'average_resident_set_size',
                'signals_delivered', 'page_size', 'exit_status']
    float_list = ['real_time', 'user_time', 'system_time']
    for key in proc_data:
        if key in int_list:
            proc_data[key] = jc.utils.convert_to_int(proc_data[key])
        if key in float_list:
            proc_data[key] = jc.utils.convert_to_float(proc_data[key])

    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = {}

    if jc.utils.has_data(data):
        time_type = None     # linux_brief, linux_long, bsd_brief, bsd_long, posix

        for line in filter(None, data.splitlines()):
            # linux default style:
            # 0.00user 0.00system 0:03.00elapsed 0%CPU (0avgtext+0avgdata 2148maxresident)k
            # 0inputs+0outputs (0major+71minor)pagefaults 0swaps
            if time_type != 'linux_brief' and 'elapsed' in line:
                time_type = 'linux_brief'

            # BSD/OSX default style:
            #         0.00 real         0.00 user         0.00 sys
            elif time_type != 'bsd_brief' and ' user ' in line:
                time_type = 'bsd_brief'

            elif time_type != 'linux_long' and 'Command' in line:
                time_type = 'linux_long'

            elif time_type != 'bsd_long' and 'maximum resident set size' in line:
                time_type = 'bsd_long'

            # POSIX compliant output:
            # real         0.00
            # user         0.00
            # sys          0.00
            elif time_type != 'posix' and line.startswith('real '):
                time_type = 'posix'

            # start parsing lines
            if time_type == 'linux_brief':
                if 'elapsed' in line:
                    line_num = 0
                else:
                    line_num = 1

                new_line = line.replace('+', ' ').replace('(', ' ').replace(')', ' ')\
                               .replace('user', ' ').replace('system', ' ').replace('elapsed', ' ')\
                               .replace('elapsed', ' ').replace('%CPU', ' ').replace('avgtext', ' ')\
                               .replace('avgdata', ' ').replace('maxresident', ' ').replace('inputs', ' ')\
                               .replace('outputs', ' ').replace('major', ' ').replace('minor', ' ')\
                               .replace('pagefaults', ' ').replace('swaps', ' ').replace('k', ' ')

                linux_brief_line = new_line.split()

                if line_num == 0:
                    raw_output['user_time'] = linux_brief_line[0]
                    raw_output['system_time'] = linux_brief_line[1]
                    raw_output['elapsed_time'] = linux_brief_line[2]
                    raw_output['cpu_percent'] = None if linux_brief_line[3] == '?' else linux_brief_line[3]
                    raw_output['average_shared_text'] = linux_brief_line[4]
                    raw_output['average_unshared_data_size'] = linux_brief_line[5]
                    raw_output['maximum_resident_set_size'] = linux_brief_line[6]
                else:
                    raw_output['block_input_operations'] = linux_brief_line[0]
                    raw_output['block_output_operations'] = linux_brief_line[1]
                    raw_output['major_pagefaults'] = linux_brief_line[2]
                    raw_output['minor_pagefaults'] = linux_brief_line[3]
                    raw_output['swaps'] = linux_brief_line[4]

            if time_type == 'posix':
                posix_line = line.split()
                if 'real' in line:
                    raw_output['real_time'] = posix_line[1]
                if 'user' in line:
                    raw_output['user_time'] = posix_line[1]
                if 'sys' in line:
                    raw_output['system_time'] = posix_line[1]

            if time_type == 'bsd_brief':
                bsd_brief_line = line.split()
                raw_output['real_time'] = bsd_brief_line[0]
                raw_output['user_time'] = bsd_brief_line[2]
                raw_output['system_time'] = bsd_brief_line[4]

            if time_type == 'bsd_long':
                bsd_long_line = line.split(maxsplit=1)
                key = bsd_long_line[1].replace(' ', '_')

                # fixup some key names
                if key == 'average_shared_text':
                    key = 'average_shared_text_size'

                value = bsd_long_line[0]
                raw_output[key] = value

            if time_type == 'linux_long':
                # cleanup key names: (h:mm:ss or m:ss)
                # line = line.replace('h:mm:ss', '', 1).replace('m:ss', '')
                linux_long_line = line.split(': ', maxsplit=1)
                key = linux_long_line[0].strip().lower().replace(' ', '_').replace('(', '').replace(')', '')\
                                        .replace('/', '_').replace(':', '_').replace('_kbytes', '')\
                                        .replace('_seconds', '').replace('socket_', '').replace('_bytes', '')

                # fixup some key names
                if key == 'file_system_inputs':
                    key = 'block_input_operations'

                if key == 'file_system_outputs':
                    key = 'block_output_operations'

                if key == 'percent_of_cpu_this_job_got':
                    key = 'cpu_percent'

                if key == 'elapsed_wall_clock_time_h_mm_ss_or_m_ss':
                    key = 'elapsed_time'

                if key == 'major_requiring_i_o_page_faults':
                    key = 'major_pagefaults'

                if key == 'minor_reclaiming_a_frame_page_faults':
                    key = 'minor_pagefaults'

                value = linux_long_line[1].replace('%', '')
                raw_output[key] = value

    if raw:
        return raw_output
    else:
        return _process(raw_output)
