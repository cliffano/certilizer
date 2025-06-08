"""A module for reporting the certificate details
depending on output configurations.
"""

import os
import re
import pandas as pd
from tabulate import tabulate
from dominate import document
from dominate.tags import meta, link
from dominate.util import raw


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
            output = self._html(data_frame, _colour_rows_styler)
        else:
            output = self._text(data_frame)

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
            output = self._html(data_frame, _colour_rows_styler)
        else:
            output = self._text(data_frame)

        if self.out_file:
            head, tail = os.path.split(self.out_file)
            tail = f"error-{tail}"
            self.out_file = os.path.join(head, tail)

        self._write_output(output)

    def _html(self, data_frame, colour_rows_styler) -> str:
        """Return the HTML page with table having data frame as content."""

        styled_data_frame = data_frame.style.apply(
            colour_rows_styler, axis=1
        ).set_table_attributes('class="table table-striped table-bordered table-hover"')
        table = styled_data_frame.to_html(doctype_html=False, index=False)
        table = re.sub(r"col_heading", "text-center table-active col_heading", table)

        doc = document(title="Certilizer Report")
        with doc.head:
            meta(charset="utf-8")
            meta(name="generator", content="Certilizer")
            link(
                rel="stylesheet",
                href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.6/dist/css/bootstrap.min.css",
            )
        doc.body.add(raw(table))
        return doc.render()

    def _text(self, data_frame) -> str:
        """Return the text representation of the data frame table."""
        return tabulate(
            data_frame, showindex=False, headers="keys", tablefmt=self.out_format
        )

    def _write_output(self, output: str) -> None:
        """Write the output to the file or stdout."""
        if self.out_file:
            with open(self.out_file, "w", encoding="utf-8") as (stream):
                stream.write(output)
        else:
            print(output)
