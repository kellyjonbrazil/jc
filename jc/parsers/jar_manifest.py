r"""jc - JSON Convert Java `MANIFEST.MF` file parser

Usage (cli):

    $ cat MANIFEST.MF | jc --jar-manifest

Usage (module):

    import jc
    result = jc.parse('jar_manifest', jar_manifest_file_output)

Schema:

    [
      {
        "key1":     string,
        "key2":     string
      }
    ]

Examples:

    $ cat MANIFEST.MF | jc --jar-manifest -p
    $ unzip -c log4j-core-2.16.0.jar META-INF/MANIFEST.MF | \\
      jc --jar-manifest -p
    $ unzip -c 'apache-log4j-2.16.0-bin/*.jar' META-INF/MANIFEST.MF | \\
      jc --jar-manifest -p

    $ cat MANIFEST.MF | jc --jar-manifest -p
    [
      {
        "Import_Package": "com.conversantmedia.util.concurrent;resoluti...",
        "Export_Package": "org.apache.logging.log4j.core;uses:=\"org.ap...",
        "Manifest_Version": "1.0",
        "Bundle_License": "https://www.apache.org/licenses/LICENSE-2.0.txt",
        "Bundle_SymbolicName": "org.apache.logging.log4j.core",
        "Built_By": "matt",
        "Bnd_LastModified": "1639373735804",
        "Implementation_Vendor_Id": "org.apache.logging.log4j",
        "Specification_Title": "Apache Log4j Core",
        "Log4jReleaseManager": "Matt Sicker",
        ...
      }
    ]

    $ unzip -c 'apache-log4j-2.16.0-bin/*.jar' META-INF/MANIFEST.MF | \\
      jc --jar-manifest -p
    [
      ...
      {
        "Archive": "apache-log4j-2.16.0-bin/log4j-spring-boot-2.16.0-so...",
        "Manifest_Version": "1.0",
        "Built_By": "matt",
        "Created_By": "Apache Maven 3.8.4",
        "Build_Jdk": "1.8.0_312"
      },
      {
        "Archive": "apache-log4j-2.16.0-bin/log4j-spring-boot-2.16.0-ja...",
        "Manifest_Version": "1.0",
        "Built_By": "matt",
        "Created_By": "Apache Maven 3.8.4",
        "Build_Jdk": "1.8.0_312"
      },
      {
        "Bundle_SymbolicName": "org.apache.logging.log4j.spring-cloud-c...",
        "Export_Package": "org.apache.logging.log4j.spring.cloud.config...",
        "Archive": "apache-log4j-2.16.0-bin/log4j-spring-cloud-config-c...",
        "Manifest_Version": "1.0",
        "Bundle_License": "https://www.apache.org/licenses/LICENSE-2.0.txt",
        ...
      }
      ...
    ]
"""
import jc.utils
import re


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '0.2'
    description = 'Java MANIFEST.MF file parser'
    author = 'Matt J'
    author_email = 'https://github.com/listuser'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['file']


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
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = []
    archives = []

    if jc.utils.has_data(data):
        datalines = jc.utils.splitlines(data, split_cr=True)

        # remove last line of multi-archive output since it is not needed.
        # match the whole unzip summary line so other text that ends with
        # the same words is kept
        if re.match(r'\d+ archives? (?:was|were) successfully processed\.$', datalines[-1]):
            datalines.pop(-1)

        # extract each archive into its own list of lines.
        # archives are separated by a blank line
        this_archive = []
        for row in datalines:
            if row == '':
                archives.append(this_archive)
                this_archive = []
                continue

            this_archive.append(row)

        if this_archive:
            archives.append(this_archive)

        # iterate through list of archives and parse
        for archive_item in archives:
            if not archive_item:
                continue

            attributes = []
            unzip_status_line = False

            # an unzip "inflating" status line is only recognized when it
            # directly follows the unindented "Archive:" line that starts
            # the section.
            unzip_header = bool(re.match(r'Archive\s*:', archive_item[0]))

            for i, line in enumerate(archive_item):
                # a line starting with a single space continues the
                # previous attribute. Drop the one space and append the
                # rest directly to that attribute's value.
                if line.startswith(' '):
                    if (i == 1 and unzip_header and
                            re.match(r'\s+\w+\s*:\s*META-INF/MANIFEST\.MF', line, re.IGNORECASE)):
                        unzip_status_line = True
                        continue

                    if attributes:
                        attributes[-1][1].append(line[1:])
                    continue

                k, v = line.split(":", maxsplit=1)
                attributes.append((k, [v]))

            if attributes:
                this_manifest = {}
                raw_keys = {}
                for index, (raw_key, parts) in enumerate(attributes):
                    k = re.sub(r'\s', '', raw_key)
                    k = re.sub(r'-', '_', k)

                    if k in raw_keys:
                        # a manifest attribute named "Archive" must not
                        # replace the file name from the unzip header line
                        if unzip_status_line and raw_keys[k] == 0:
                            continue

                        # keys that only differ in "-" and "_" (e.g.
                        # Main-Class and Main_Class): keep the first one
                        if attributes[raw_keys[k]][0] != raw_key:
                            continue

                    raw_keys[k] = index
                    this_manifest[k] = ''.join(parts).strip()
                raw_output.append(this_manifest)

    return raw_output if raw else _process(raw_output)
