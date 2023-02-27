"""
Module for working with PNP ID REGISTRY
"""

import csv
import string
from html.parser import HTMLParser
from urllib import request

__all__ = ["Registry"]


class WebPnpIdParser(HTMLParser):
    """Parser pnp id from https://uefi.org/PNP_ID_List

    Examples:
        p = WebPnpIdParser()
        p.feed(html_data)
        p.result
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._find_table = False
        self._find_row = False
        # first -- company name, second -- pnp id, third -- approved date
        self._last_field = []
        # key -- pnp id, value -- tuple (company_name, approved_date)
        self.result = {}

    def handle_starttag(self, tag, attrs):
        if tag == "tbody":
            self._find_table = True
        elif self._find_table and tag == "tr":
            self._find_row = True

    def handle_endtag(self, tag):
        if tag == "tbody":
            self._find_table = False
        elif self._find_table and tag == "tr":
            self._find_row = False
            # add table row to result
            self.result[self._last_field[1]] = (
                self._last_field[0],
                self._last_field[-1],
            )
            self._last_field.clear()

    def handle_data(self, data):
        # skip processing until table is found
        if not self._find_table:
            return

        if self._find_row:
            data = data.strip()
            if data:
                self._last_field.append(data)

    def error(self, message):
        super().close()


class Registry(dict):
    """Registry pnp id data dictionary

    key   -- pnp_id
    value -- company name
    """

    @classmethod
    def from_web(cls, filter_by_id: str = None):
        """Get registry from https://uefi.org/PNP_ID_List

        Args:
            filter_by_id (str), optional: filter registry by id

        Raises:

        Returns:

        """
        url = "https://uefi.org/PNP_ID_List"
        if filter_by_id:
            url += "?search={}".format(filter_by_id)

        with request.urlopen(url) as req:
            parse = WebPnpIdParser()
            parse.feed(req.read().decode())

            registry = cls()
            for key, value in parse.result.items():
                # skip invalid search value
                if filter_by_id and key != filter_by_id:
                    continue
                registry[key] = value[0]
        return registry

    @classmethod
    def from_csv(cls, csv_path: str, filter_by_id: str = None):
        """Get registry by csv local file

        Args:
            csv_path (str): path to csv file
            filter_by_id (str), optional: filter registry by id

        Raises:

        Returns:

        """
        registry = cls()
        with open(csv_path, "r") as file:
            reader = csv.reader(file)
            for line in reader:
                # filter
                if filter_by_id and filter_by_id != line[0]:
                    continue
                registry[line[0]] = line[1]
        return registry

    def to_csv(self, csv_path: str):
        """Dump registry to csv file"""
        with open(csv_path, "w") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(self.items())
        return self

    def get_company_from_id(self, pnp_id: str) -> str:
        """Convert PNP id to company name"""
        return self.get(pnp_id, "Unknown")

    def get_company_from_raw(self, raw: int) -> str:
        """Convert raw edid value to company name"""
        tmp = [(raw >> 10) & 31, (raw >> 5) & 31, raw & 31]
        pnp_id = "".join(string.ascii_uppercase[n - 1] for n in tmp)
        return self.get_company_from_id(pnp_id)
