"""jc - JSON CLI output utility `MANIFEST.MF` file parser

Usage (cli):

    $ cat MANIFEST.MF | jc --jar-manifest

Usage (module):

    import jc.parsers.jar_manifest
    result = jc.parsers.jar_manifest.parse(jar_manifest_file_output)

Schema:

    [
      {
        "key1":     string,
        "key2":     string
      }
    ]

Examples:

    $ cat MANIFEST.MF | jc --jar-manifest -p
    $ unzip -c apache-log4j-2.16.0-bin/log4j-core-2.16.0.jar META-INF/MANIFEST.MF | jc --jar-manifest -p
    $ unzip -c 'apache-log4j-2.16.0-bin/*.jar' META-INF/MANIFEST.MF | jc --jar-manifest -p

    $ cat MANIFEST.MF | jc --jar-manifest -p

    [
      {
        "Import_Package": "com.conversantmedia.util.concurrent;resolution:=optional,com.fasterxml.jackson.annotation;version=\"[2.12,3)\";resolution:=optional,com.fasterxml.jackson.core;version=\"[2.12,3)\";resolution:=optional,com.fasterxml.jackson.core.type;version=\"[2.12,3)\";resolution:=optional,com.fasterxml.jackson.cor...",
        "Export_Package": "org.apache.logging.log4j.core;uses:=\"org.apache.logging.log4j,org.apache.logging.log4j.core.config,org.apache.logging.log4j.core.impl,org.apache.logging.log4j.core.layout,org.apache.logging.log4j.core.time,org.apache.logging.log4j.message,org.apache.logging.log4j.spi,org.apache.logging.log4j.status...",
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

    $ unzip -c 'apache-log4j-2.16.0-bin/*.jar' META-INF/MANIFEST.MF | jc --jar-manifest -p

    [
      ...
      {
        "Archive": "apache-log4j-2.16.0-bin/log4j-spring-boot-2.16.0-sources.jar",
        "Manifest_Version": "1.0",
        "Built_By": "matt",
        "Created_By": "Apache Maven 3.8.4",
        "Build_Jdk": "1.8.0_312"
      },
      {
        "Archive": "apache-log4j-2.16.0-bin/log4j-spring-boot-2.16.0-javadoc.jar",
        "Manifest_Version": "1.0",
        "Built_By": "matt",
        "Created_By": "Apache Maven 3.8.4",
        "Build_Jdk": "1.8.0_312"
      },
      {
        "Bundle_SymbolicName": "org.apache.logging.log4j.spring-cloud-config-client.logging.log4j.core.util;version=\"[2.16,3)\",org.springframework.boot.autoconfigure.condition,org.springframework.cloud.context.environment,org.springframework.context,org.springframework.stereotype",
        "Export_Package": "org.apache.logging.log4j.spring.cloud.config.controller;version=\"2.16.0\"ient",
        "Archive": "apache-log4j-2.16.0-bin/log4j-spring-cloud-config-client-2.16.0.jar",
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
    version = '0.01'
    description = 'MANIFEST.MF file parser'
    author = 'Matt J'
    author_email = 'https://github.com/listuser'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']


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

    raw_output = []
    archives = []

    if jc.utils.has_data(data):
        datalines = data.splitlines()

        # remove last line of multi-archive output since it is not needed
        if datalines[-1].endswith('archives were successfully processed.'):
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

            manifests = []
            this_manifest = {}
            plines = []

            for i, line in enumerate(archive_item):
                last = archive_item[-1]

                # remove line since it is not needed and starts with "space"
                if (re.match(r'^\s+inflating\s*:\s*META-INF/MANIFEST.MF', line, re.IGNORECASE)):
                    archive_item.pop(i)
                    continue

                # if line starts with "space"
                # begin key multiline value pair concatenation
                if (re.match(r'\s', line)):

                    # expectation is this "if" sets a key once
                    if (not this_manifest):
                        # previous line contains a key
                        k, v = archive_item[i - 1].split(":", maxsplit=1)
                        v = v + line
                        v = re.sub(r'\s', '', v)
                        this_manifest = {k: v}
                        plines.append(i - 1)
                        plines.append(i)

                    # continue key multiline value pair concatenation
                    else:
                        plines.append(i)
                        linecmp = line
                        for k, v in this_manifest.items():
                            line = v + line
                            line = re.sub(r'\s', '', line)
                        this_manifest.update({k:line})

                        if linecmp is not last:
                            nextline = archive_item[i + 1]
                            # if next line starts with not "space",
                            # end key multiline value pair concatenation
                            if (re.match(r'\S', nextline)):
                                manifests.append(this_manifest)
                                this_manifest = False
                            else:
                                manifests.append(this_manifest)

            # pop key multiline value pair lines
            if plines:
                for p in reversed(plines):
                    archive_item.pop(p)

            # all other key value pairs
            for i, line in enumerate(archive_item):
                k, v = line.split(":", maxsplit=1)
                v = v.strip()
                manifests.append({k: v})

            if manifests:
                this_manifest = {}
                for d in manifests:
                    for k, v in d.items():
                        k = re.sub(r'\s', '', k)
                        k = re.sub(r'-', '_', k)
                        this_manifest.update({k: v})
                raw_output.append(this_manifest)

    return raw_output if raw else _process(raw_output)
