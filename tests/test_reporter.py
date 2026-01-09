# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals,unused-variable
import os
import io
import asyncio
import unittest
from unittest.mock import MagicMock, patch
import pandas as pd

from certilizer.reporter import Reporter

# Silence dominaate 'There is no current event loop' warning
asyncio.set_event_loop(asyncio.new_event_loop())


class TestReporter(unittest.TestCase):

    @patch("certilizer.reporter.PandasReporter")
    def test_write_cert(self, mock_reporter_cls):
        reporter = Reporter(
            out_format="html",
            out_file="somereport.html",
            max_col_size=20,
            expiry_threshold_in_days=30,
        )

        cert_data = [
            {"Domain": "b.example", "Expiry Date": pd.Timestamp("2030-01-02")},
            {"Domain": "a.example", "Expiry Date": pd.Timestamp("2030-01-01")},
        ]

        mock_report = MagicMock()
        mock_reporter_cls.return_value = mock_report

        reporter.write_cert(cert_data)

        mock_report.report.assert_called_once()
        args, kwargs = mock_report.report.call_args
        data_frame = args[0]
        options = args[2]

        self.assertListEqual(list(data_frame["Domain"]), ["a.example", "b.example"])
        self.assertEqual(options["max_col_size"], 20)
        self.assertEqual(options["out_file"], "somereport.html")
        self.assertEqual(options["title"], "Certificate Expiry Report")
        self.assertEqual(options["generator"], "Certilizer")
        self.assertTrue(callable(options["rows_styler"]))

    def test_write_cert_with_pandasreporter(self):
        reporter = Reporter(
            out_format="html",
            out_file=None,
            max_col_size=50,
            expiry_threshold_in_days=30,
        )

        today = pd.Timestamp.today().normalize()
        cert_data = [
            {
                "Domain": "expired.example.com",
                "Expiry Date": today - pd.Timedelta(days=1),
            },
            {"Domain": "soon.example.com", "Expiry Date": today + pd.Timedelta(days=5)},
            {
                "Domain": "future.example.com",
                "Expiry Date": today + pd.Timedelta(days=60),
            },
        ]

        buffer = io.StringIO()
        with patch("sys.stdout", buffer):
            reporter.write_cert(cert_data)

        html_output = buffer.getvalue()
        self.assertIn("Certificate Expiry Report", html_output)
        self.assertIn("expired.example", html_output)
        self.assertIn("soon.example", html_output)
        self.assertIn("future.example", html_output)
        self.assertIn("LightPink", html_output)
        self.assertIn("LightYellow", html_output)
        self.assertIn("LightGreen", html_output)

    @patch("certilizer.reporter.PandasReporter")
    def test_write_error_with_out_file(self, mock_reporter_cls):
        reporter = Reporter(
            out_format="html",
            out_file=os.path.join("/tmp", "somereport.html"),
            max_col_size=20,
            expiry_threshold_in_days=30,
        )

        error_data = [{"Domain": "a.example", "Error": "timeout"}]

        mock_report = MagicMock()
        mock_reporter_cls.return_value = mock_report

        reporter.write_error(error_data)

        mock_report.report.assert_called_once()
        args, kwargs = mock_report.report.call_args
        options = args[2]

        self.assertEqual(
            options["out_file"], os.path.join("/tmp", "error-somereport.html")
        )
        self.assertEqual(options["title"], "Certificate Expiry Error Report")
        self.assertEqual(options["generator"], "Certilizer")
        self.assertTrue(callable(options["rows_styler"]))

    @patch("certilizer.reporter.PandasReporter")
    def test_write_error_without_out_file(self, mock_reporter_cls):
        reporter = Reporter(
            out_format="html",
            out_file=None,
            max_col_size=20,
            expiry_threshold_in_days=30,
        )

        error_data = [{"Domain": "a.example", "Error": "timeout"}]

        mock_report = MagicMock()
        mock_reporter_cls.return_value = mock_report

        reporter.write_error(error_data)

        mock_report.report.assert_called_once()
        args, kwargs = mock_report.report.call_args
        options = args[2]

        self.assertIsNone(options["out_file"])

    def test_write_error_with_pandasreporter(self):
        reporter = Reporter(
            out_format="html",
            out_file=None,
            max_col_size=50,
            expiry_threshold_in_days=30,
        )

        error_data = [
            {"Domain": "err1.example.com", "Error": "timeout"},
            {"Domain": "err2.example.com", "Error": "connection refused"},
        ]

        buffer = io.StringIO()
        with patch("sys.stdout", buffer):
            reporter.write_error(error_data)

        html_output = buffer.getvalue()
        self.assertIn("Certificate Expiry Error Report", html_output)
        self.assertIn("err1.example.com", html_output)
        self.assertIn("err2.example.com", html_output)
        self.assertIn("LightPink", html_output)


if __name__ == "__main__":
    unittest.main()
