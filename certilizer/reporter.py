# pylint: disable=too-few-public-methods
"""A module for reporting the certificate details
depending on output configurations.
"""
from tabulate import tabulate
import pandas as pd

class Reporter():
    """A class for producing certificate details report.
    """

    def __init__(self, out_format: str, out_file: str) -> None:
        """Initialise the Reporter object."""
        self.out_format = out_format
        self.out_file = out_file

    def write(self, data: list) -> None:
        """Write the report to the output file or stdout."""

        data_frame = pd.DataFrame(data).sort_values(by=['Expiry Date'])
        # pd.set_option('max_colwidth', 20)
        output = tabulate(
            data_frame,
            headers='keys',
            tablefmt=self.out_format
        )

        if self.out_file:
            with open(self.out_file, 'w', encoding='utf-8') as (stream):
                stream.write(output)
        else:
            print(output)
