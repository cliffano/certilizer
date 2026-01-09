# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals,too-many-arguments,too-many-positional-arguments
from datetime import datetime
import ssl
from unittest.mock import patch, call, MagicMock
import unittest

from click.testing import CliRunner

from certilizer import run, cli


class TestCertilizer(unittest.TestCase):

    @patch("certilizer.Reporter")
    @patch("certilizer.Cert")
    @patch("certilizer.socket.create_connection")
    @patch("certilizer.ssl.create_default_context")
    @patch("certilizer.CFGRW")
    @patch("certilizer.init")
    def test_run_with_successful_endpoint(
        self,
        func_init,
        func_cfgrw,
        func_create_default_context,
        func_create_connection,
        func_cert,
        func_reporter,
    ):

        mock_logger = MagicMock()
        func_init.return_value = mock_logger

        func_cfgrw.return_value.read.return_value = {
            "endpoints": [
                {
                    "name": "example",
                    "host": "example.com",
                    "port": 443,
                    "ssl_verify": True,
                }
            ]
        }

        mock_context = MagicMock()
        func_create_default_context.return_value = mock_context

        mock_socket = MagicMock()
        mock_socket.__enter__.return_value = mock_socket
        func_create_connection.return_value = mock_socket

        mock_ssock = MagicMock()
        mock_ssock.__enter__.return_value = mock_ssock
        mock_ssock.getpeercert.return_value = {"serialNumber": "raw"}
        mock_context.wrap_socket.return_value = mock_ssock

        expiry_date = datetime(2030, 1, 1, 12, 0, 0)
        func_cert.return_value.get_serial_number.return_value = "serial"
        func_cert.return_value.get_common_name.return_value = "common-name"
        func_cert.return_value.get_alternative_names.return_value = "alt-names"
        func_cert.return_value.get_issuer.return_value = "issuer"
        func_cert.return_value.get_expiry_date.return_value = expiry_date
        func_cert.return_value.get_ocsp.return_value = "ocsp"
        func_cert.return_value.get_ca_issuer.return_value = "ca-issuer"
        func_cert.return_value.get_crl_dist_points.return_value = "crl-dist"

        mock_reporter = MagicMock()
        func_reporter.return_value = mock_reporter

        run(
            conf_file="certilizer.yaml",
            out_format="text",
            out_file=None,
            max_col_size=100,
            expiry_threshold_in_days=90,
        )

        mock_logger.info.assert_has_calls(
            [
                call("Loading configuration file certilizer.yaml..."),
                call("Retrieving certificate from endpoint example.com:443 ..."),
                call("Generating report using text format..."),
            ]
        )
        self.assertEqual(mock_logger.error.call_count, 0)

        func_reporter.assert_called_once_with("text", None, 100, 90)
        mock_reporter.write_cert.assert_called_once_with(
            {
                "Name": ["example"],
                "Endpoint": ["example.com:443"],
                "Serial Number": ["serial"],
                "Common Name": ["common-name"],
                "Alternative Names": ["alt-names"],
                "Issuer": ["issuer"],
                "Expiry Date": [expiry_date],
                "OCSP": ["ocsp"],
                "CA Issuer": ["ca-issuer"],
                "CRL Dist Points": ["crl-dist"],
            }
        )
        mock_reporter.write_error.assert_not_called()

    @patch("certilizer.Reporter")
    @patch("certilizer.Cert")
    @patch("certilizer.socket.create_connection")
    @patch("certilizer.ssl.create_default_context")
    @patch("certilizer.CFGRW")
    @patch("certilizer.init")
    def test_run_with_false_ssl_verify(
        self,
        func_init,
        func_cfgrw,
        func_create_default_context,
        func_create_connection,
        func_cert,
        func_reporter,
    ):

        mock_logger = MagicMock()
        func_init.return_value = mock_logger

        func_cfgrw.return_value.read.return_value = {
            "endpoints": [
                {
                    "name": "example",
                    "host": "example.com",
                    "port": 443,
                    "ssl_verify": False,
                }
            ]
        }

        mock_context = MagicMock()
        func_create_default_context.return_value = mock_context

        mock_socket = MagicMock()
        mock_socket.__enter__.return_value = mock_socket
        func_create_connection.return_value = mock_socket

        mock_ssock = MagicMock()
        mock_ssock.__enter__.return_value = mock_ssock
        mock_ssock.getpeercert.return_value = {"serialNumber": "raw"}
        mock_context.wrap_socket.return_value = mock_ssock

        expiry_date = datetime(2030, 1, 1, 12, 0, 0)
        func_cert.return_value.get_serial_number.return_value = "serial"
        func_cert.return_value.get_common_name.return_value = "common-name"
        func_cert.return_value.get_alternative_names.return_value = "alt-names"
        func_cert.return_value.get_issuer.return_value = "issuer"
        func_cert.return_value.get_expiry_date.return_value = expiry_date
        func_cert.return_value.get_ocsp.return_value = "ocsp"
        func_cert.return_value.get_ca_issuer.return_value = "ca-issuer"
        func_cert.return_value.get_crl_dist_points.return_value = "crl-dist"

        mock_reporter = MagicMock()
        func_reporter.return_value = mock_reporter

        run(
            conf_file="certilizer.yaml",
            out_format="text",
            out_file=None,
            max_col_size=100,
            expiry_threshold_in_days=90,
        )

        self.assertFalse(mock_context.check_hostname)
        self.assertEqual(mock_context.verify_mode, ssl.CERT_NONE)

        func_reporter.assert_called_once_with("text", None, 100, 90)
        mock_reporter.write_error.assert_not_called()

    @patch("certilizer.Reporter")
    @patch("certilizer.socket.create_connection")
    @patch("certilizer.ssl.create_default_context")
    @patch("certilizer.CFGRW")
    @patch("certilizer.init")
    def test_run_with_endpoint_error(
        self,
        func_init,
        func_cfgrw,
        func_create_default_context,
        func_create_connection,
        func_reporter,
    ):

        mock_logger = MagicMock()
        func_init.return_value = mock_logger

        func_cfgrw.return_value.read.return_value = {
            "endpoints": [{"name": "example", "host": "example.com", "port": 443}]
        }

        mock_context = MagicMock()
        func_create_default_context.return_value = mock_context

        mock_socket = MagicMock()
        mock_socket.__enter__.return_value = mock_socket
        func_create_connection.return_value = mock_socket

        mock_ssock = MagicMock()
        mock_ssock.__enter__.side_effect = RuntimeError("ssl failure")
        mock_context.wrap_socket.return_value = mock_ssock

        mock_reporter = MagicMock()
        func_reporter.return_value = mock_reporter

        run(
            conf_file="certilizer.yaml",
            out_format="html",
            out_file="report.html",
            max_col_size=50,
            expiry_threshold_in_days=30,
        )

        mock_logger.info.assert_has_calls(
            [
                call("Loading configuration file certilizer.yaml..."),
                call("Retrieving certificate from endpoint example.com:443 ..."),
                call("Generating report using html format..."),
            ]
        )
        mock_logger.error.assert_has_calls([call("An error occurred: ssl failure")])

        func_reporter.assert_called_once_with("html", "report.html", 50, 30)
        mock_reporter.write_cert.assert_called_once()
        mock_reporter.write_error.assert_called_once_with(
            {
                "Name": ["example"],
                "Endpoint": ["example.com:443"],
                "Error": ["ssl failure"],
            }
        )

    @patch("certilizer.run")
    def test_cli(self, func_run):

        func_run.return_value = None

        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "--conf-file",
                "conf.yaml",
                "--out-format",
                "json",
                "--out-file",
                "report.json",
                "--max-col-size",
                "120",
                "--expiry-threshold-in-days",
                "60",
            ],
        )

        self.assertFalse(result.exception)
        self.assertEqual(result.exit_code, 0)
        func_run.assert_called_once_with("conf.yaml", "json", "report.json", 120, 60)


if __name__ == "__main__":
    unittest.main()
