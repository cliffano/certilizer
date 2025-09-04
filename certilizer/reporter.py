"""A module for reporting the certificate details
depending on output configurations.
"""

import os
import pandas as pd
from .formatters.html import format_report as format_html
from .formatters.text import format_report as format_text


class Reporter:
    """A class for producing certificate details report."""

    def __init__(
        self,
        out_format: str,
        out_file: str,
        max_col_size: int,
        expiry_threshold_in_days: int,
    ) -> None:
        """Initialise the Reporter object."""
        self.out_format = out_format
        self.out_file = out_file
        self.max_col_size = max_col_size
        self.expiry_threshold_in_days = expiry_threshold_in_days

    def write_cert(self, cert_data: list) -> None:
        """Write the errors to the output file or stdout."""

        data_frame = pd.DataFrame(cert_data).sort_values(by=["Expiry Date"])

        if self.max_col_size:
            data_frame = data_frame.map(
                lambda x: x[0 : self.max_col_size] if isinstance(x, str) else x
            )

        def _colour_rows_styler(row):
            today = pd.Timestamp.today()
            threshold_date = today + pd.DateOffset(days=self.expiry_threshold_in_days)
            if row["Expiry Date"] <= today:
                style = ["background-color: LightPink"] * len(row)
            elif row["Expiry Date"] <= threshold_date:
                style = ["background-color: LightYellow"] * len(row)
            else:
                style = ["background-color: LightGreen"] * len(row)
            return style

        if self.out_format == "html":
            output = format_html(data_frame, _colour_rows_styler)
        else:
            output = format_text(data_frame)

        self._write_output(output)

    def write_error(self, error_data: list) -> None:
        """Write the errors to the output file or stdout."""

        data_frame = pd.DataFrame(error_data)

        if self.max_col_size:
            data_frame = data_frame.map(
                lambda x: x[0 : self.max_col_size] if isinstance(x, str) else x
            )

        def _colour_rows_styler(row):
            return ["background-color: LightPink"] * len(row)

        if self.out_format == "html":
            output = format_html(data_frame, _colour_rows_styler)
        else:
            output = format_text(data_frame)

        if self.out_file:
            head, tail = os.path.split(self.out_file)
            tail = f"error-{tail}"
            self.out_file = os.path.join(head, tail)

        self._write_output(output)

    def _write_output(self, output: str) -> None:
        """Write the output to the file or stdout."""
        if self.out_file:
            with open(self.out_file, "w", encoding="utf-8") as (stream):
                stream.write(output)
        else:
            print(output)
