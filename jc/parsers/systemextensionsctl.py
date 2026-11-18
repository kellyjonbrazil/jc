"""jc - JSON Convert `systemextensionsctl list` command output parser

Usage:

    $ systemextensionsctl list | jc --systemextensionsctl

Compatibility:

    macOS

Example:

    $ systemextensionsctl list | jc --systemextensionsctl -p
    {
      "total_extensions": 1,
      "sections": [
        {
          "category": "com.apple.system_extension.network_extension",
          "description": "Go to 'System Settings > General > Login Items & Extensions > Network Extensions' to modify these system extension(s)",
          "entries": [
            {
              "enabled": true,
              "active": true,
              "teamID": "XXX",
              "bundleID": "YYY",
              "version": "QQQ",
              "name": "ZZZ",
              "state": ["activated", "enabled"]
            }
          ]
        }
      ]
    }
"""

import jc.utils
import jc.parsers.universal
import re
from typing import List, Dict, Tuple, Optional, Iterator, Any


class info:
    version = "1.0"
    description = "`systemextensionsctl list` command parser"
    author = "Ron Green"
    author_email = "11993626+georgettica@users.noreply.github.com"
    compatible = ["darwin"]
    magic_commands = ["systemextensionsctl"]


def parse(data: str, raw: bool = False, quiet: bool = False) -> Dict[str, Any]:
    """
    Parses the output of `systemextensionsctl list` command.

    Parameters:
        data:   (str)  Text data to parse
        raw:    (bool) Whether to return raw data
        quiet:  (bool) Suppress error messages

    Returns:
        Dict[str, Any]: Dictionary with parsed data
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    if not jc.utils.has_data(data):
        return {}

    lines = data.strip().splitlines()
    total_extensions, remaining_lines = extract_total_extensions(lines)

    if total_extensions is None:
        return {}
    elif total_extensions == 0:
        return {"total_extensions": 0, "sections": []}

    sections = process_sections(remaining_lines, total_extensions)
    return {"total_extensions": total_extensions, "sections": sections}


def extract_total_extensions(lines: List[str]) -> Tuple[Optional[int], List[str]]:
    """
    Extracts the total number of extensions from the command output.

    Parameters:
        lines: List[str] - List of lines from the command output

    Returns:
        Tuple[Optional[int], List[str]]: Total number of extensions and remaining lines
    """
    total_extensions = None
    remaining_lines = []
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.endswith("extension(s)"):
            match = re.match(r"(\d+)\s+extension\(s\)", stripped_line)
            if match:
                total_extensions = int(match.group(1))
        else:
            remaining_lines.append(line)
    return total_extensions, remaining_lines


def process_sections(lines: List[str], total_extensions: int) -> List[Dict[str, Any]]:
    """
    Processes the sections of the command output.

    Parameters:
        lines: List[str] - List of lines from the command output
        total_extensions: int - Total number of extensions

    Returns:
        List[Dict[str, Any]]: List of section dictionaries
    """
    sections = []
    section = None
    headers = None
    line_iter = iter(lines)

    for line in line_iter:
        stripped_line = line.strip()
        if stripped_line.startswith("--- ") and total_extensions > 0:
            section, headers = create_section(stripped_line, line_iter)
            if section and headers:
                sections.append(section)
        elif section and headers:
            entry = parse_entry(stripped_line, headers)
            if entry:
                section["entries"].append(entry)

    return sections


def create_section(
    line: str, line_iter: Iterator[str]
) -> Tuple[Dict[str, Any], Optional[List[str]]]:
    """
    Creates a section dictionary from a section header line.

    Parameters:
        line: str - The section header line
        line_iter: Iterator[str] - Iterator of the remaining lines

    Returns:
        Tuple[Dict[str, Any], Optional[List[str]]]: Section dictionary and headers list
    """
    category, description = extract_category_description(line)
    section = {"category": category, "description": description, "entries": []}
    try:
        headers_line = next(line_iter).strip()
        expected_headers = [
            "enabled",
            "active",
            "teamID",
            "bundleID (version)",
            "name",
            "[state]",
        ]
        actual_headers = [h.strip().lower() for h in headers_line.split("\t")]
        if all(header.lower() in actual_headers for header in expected_headers):
            headers = [h.strip() for h in headers_line.split("\t")]
            return section, headers
    except StopIteration:
        pass
    return section, None


def extract_category_description(line: str) -> Tuple[str, str]:
    """
    Extracts category and description from a section header line.

    Parameters:
        line: str - The section header line

    Returns:
        Tuple[str, str]: Category and description
    """
    category_and_desc = line[4:]
    if "(" in category_and_desc and ")" in category_and_desc:
        category = category_and_desc.split("(")[0].strip()
        description = category_and_desc[
            category_and_desc.find("(") + 1 : category_and_desc.rfind(")")
        ].strip()
    else:
        category = category_and_desc.strip()
        description = ""
    return category, description


def parse_entry(line: str, headers: List[str]) -> Optional[Dict[str, Any]]:
    """
    Parses a single entry line into a dictionary.

    Parameters:
        line: str - The entry line
        headers: List[str] - List of header names

    Returns:
        Optional[Dict[str, Any]]: Dictionary representing the entry or None
    """
    if not line:
        return None
    fields = line.split("\t")
    fields += [""] * (len(headers) - len(fields))  # Pad fields if necessary
    entry = dict(zip(headers, [f.strip() for f in fields]))
    entry = process_entry_fields(entry)
    return entry


def process_entry_fields(entry: Dict[str, Any]) -> Dict[str, Any]:
    """
    Processes and cleans individual fields of an entry.

    Parameters:
        entry: Dict[str, Any] - The entry dictionary

    Returns:
        Dict[str, Any]: Processed entry dictionary
    """
    # Process 'bundleID (version)'
    if "bundleID (version)" in entry:
        bundleID_version = entry.pop("bundleID (version)")
        match = re.match(r"(.+)\s+\((.+)\)", bundleID_version)
        if match:
            entry["bundleID"] = match.group(1).strip()
            entry["version"] = match.group(2).strip()
        else:
            entry["bundleID"] = bundleID_version.strip()
            entry["version"] = ""

    # Process '[state]'
    if "[state]" in entry:
        state = entry.pop("[state]")
        state = state.strip("[]").split()
        entry["state"] = state

    # Convert 'enabled' and 'active' to boolean
    entry["enabled"] = entry.get("enabled") == "*"
    entry["active"] = entry.get("active") == "*"

    return entry
