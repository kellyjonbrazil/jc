"""
EDID helper
"""

from subprocess import CalledProcessError, check_output
from typing import List

__all__ = ["EdidHelper"]


class EdidHelper:
    """Class for working with EDID data"""

    @staticmethod
    def hex2bytes(hex_data: str) -> bytes:
        """Convert hex EDID string to bytes

        Args:
            hex_data (str): hex edid string

        Returns:
            bytes: edid byte string
        """
        # delete edid 1.3 additional block
        if len(hex_data) > 256:
            hex_data = hex_data[:256]

        numbers = []
        for i in range(0, len(hex_data), 2):
            pair = hex_data[i : i + 2]
            numbers.append(int(pair, 16))
        return bytes(numbers)

    @classmethod
    def get_edids(cls) -> List[bytes]:
        """Get edids from xrandr

        Raises:
            `RuntimeError`: if error with retrieving xrandr util data

        Returns:
            List[bytes]: list with edids
        """
        try:
            output = check_output(["xrandr", "--verbose"])
        except (CalledProcessError, FileNotFoundError) as err:
            raise RuntimeError(
                "Error retrieving xrandr util data: {}".format(err)
            ) from None

        edids = []
        lines = output.splitlines()
        for i, line in enumerate(lines):
            line = line.decode().strip()
            if line.startswith("EDID:"):
                selection = lines[i + 1 : i + 9]
                selection = list(s.decode().strip() for s in selection)
                selection = "".join(selection)
                bytes_section = cls.hex2bytes(selection)
                edids.append(bytes_section)
        return edids
