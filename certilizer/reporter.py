"""A module for reporting the certificate details
depending on output configurations.
"""

import os
from pandasreporter import PandasReporter
import pandas as pd


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

        data_frame = pd.DataFrame(cert_data).sort_values(by=["Expiry Date"])

        reporter = PandasReporter()
        reporter.report(
            data_frame,
            self.out_format,
            {
                "max_col_size": self.max_col_size,
                "out_file": self.out_file,
                "rows_styler": _colour_rows_styler,
                "title": "Certificate Expiry Report",
                "generator": "Certilizer",
            },
        )

    def write_error(self, error_data: list) -> None:
        """Write the errors to the output file or stdout."""

        def _colour_rows_styler(row):
            return ["background-color: LightPink"] * len(row)

        if self.out_file:
            head, tail = os.path.split(self.out_file)
            tail = f"error-{tail}"
            self.out_file = os.path.join(head, tail)

        data_frame = pd.DataFrame(error_data)

        reporter = PandasReporter()
        reporter.report(
            data_frame,
            self.out_format,
            {
                "max_col_size": self.max_col_size,
                "out_file": self.out_file,
                "rows_styler": _colour_rows_styler,
                "title": "Certificate Expiry Error Report",
                "generator": "Certilizer",
            },
        )
