"""A module for reporting the certificate details
depending on output configurations.
"""
import os
from tabulate import tabulate
import pandas as pd

class Reporter():
    """A class for producing certificate details report.
    """

    def __init__(self, out_format: str, out_file: str) -> None:
        """Initialise the Reporter object."""
        self.out_format = out_format
        self.out_file = out_file

    def write_cert(self, cert_data: list) -> None:
        """Write the errors to the output file or stdout."""

        data_frame = pd.DataFrame(cert_data).sort_values(by=['Expiry Date'])
        output = tabulate(
            data_frame,
            showindex=False,
            headers='keys',
            tablefmt=self.out_format
        )

        if self.out_format == 'html':
            output = self._html(output)

        if self.out_file:
            with open(self.out_file, 'w', encoding='utf-8') as (stream):
                stream.write(output)
        else:
            print(output)

    def write_error(self, error_data: list) -> None:
        """Write the errors to the output file or stdout."""

        data_frame = pd.DataFrame(error_data)
        output = tabulate(
            data_frame,
            showindex=False,
            headers='keys',
            tablefmt=self.out_format
        )

        if self.out_format == 'html':
            output = self._html(output)

        if self.out_file:
            head, tail = os.path.split(self.out_file)
            tail = f'error-{tail}'
            with open(os.path.join(head, tail), 'w', encoding='utf-8') as (stream):
                stream.write(output)
        else:
            print(output)

    def _html(self, table) -> str:
        """Return the complete HTML page with the table as content."""

        table = table.replace(
            '<table>', '<table class="table table-striped table-bordered table-hover">')
        table = table.replace('<th>', '<th class="text-center table-dark">')
        return f'<html>\
            <head>\
            <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css" type="text/css">\
            <meta name="generator" content="Certilizer">\
            </head>\
            <body>\
            {table}\
            </body>\
            </html>'
