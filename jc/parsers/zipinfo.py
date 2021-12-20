"""jc - JSON CLI output utility `zipinfo` command output parser

Options supported:
- none

Note: The default listing format.

Usage (cli):

    $ zipinfo <archive> | jc --zipinfo

    or

    $ jc zipinfo

Usage (module):

    import jc.parsers.zipinfo
    result = jc.parsers.zipinfo.parse(zipinfo_command_output)

Schema:

    {
      "archive": [
        {
          "name":               string,
          "size":               integer,
          "size_unit":          string,
          "number_entries":     integer,
          "number_files":       integer,
          "bytes_uncompressed": integer,
          "bytes_compressed":   integer,
          "contents": [
            {
              "flags":       string,
              "zipversion":  float,
              "zipunder":    string
              "size":        integer,
              "type":        string,
              "method":      string,
              "date":        string,
              "time":        string,
              "filename":    string
            }
          ] 
        }
      ]
    }

Examples:

    $ zipinfo log4j-core-2.16.0.jar | jc --zipinfo -p

    {
      "archive": [
        {
          "name": "log4j-core-2.16.0.jar",
          "size": "1789565",
          "size_unit": "bytes,",
          "number_entries": "1218",
          "number_files": "1218",
          "bytes_uncompressed": "3974141",
          "bytes_compressed": "1515455",
          "contents": [
            {
              "flags": "-rw-r--r--",
              "zipversion": "2.0",
              "zipunder": "unx",
              "size": "19810",
              "type": "bl",
              "method": "defN",
              "date": "21-Dec-12",
              "time": "23:35",
              "filename": "META-INF/MANIFEST.MF"
            },
    ...

"""
import jc.utils
import jc.parsers.universal


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '0.01'
    description = '`zipinfo` command parser'
    author = 'Matt J'
    author_email = 'https://github.com/listuser'

    # compatible options: linux
    compatible = ['linux']
    magic_commands = ['zipinfo']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema.
    """

    return proc_data


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
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    datalines = data.splitlines()
    datalist = list(filter(None, datalines))
 
    if jc.utils.has_data(data):

        archive_info = [] 

        # 1st line
        line = datalist.pop(0)
        parsed_line = line.split()
        name = parsed_line[1]

        # 2nd line
        line = datalist.pop(0)
        parsed_line = line.split()
        size = parsed_line[3]
        size_unit = parsed_line[4]
        number_entries = parsed_line[-1]

        # last line
        line = datalist.pop(-1)
        parsed_line = line.split()
        number_files = parsed_line[0]
        bytes_uncompressed = parsed_line[2]
        bytes_compressed = parsed_line[5]

        # Add header row for parsing
        datalist[:0] = ['flags zipversion zipunder size type method date time filename']

        contents_list = jc.parsers.universal.simple_table_parse(datalist)

        archive_info.append({'name': name,
                             'size': size,
                             'size_unit': size_unit,
                             'number_entries': number_entries,
                             'number_files': number_files,
                             'bytes_uncompressed': bytes_uncompressed,
                             'bytes_compressed': bytes_compressed,
                             'contents': contents_list})

        raw_output['archive'] = archive_info

    return raw_output if raw else _process(raw_output)
