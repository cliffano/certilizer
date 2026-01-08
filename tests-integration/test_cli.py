# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
import unittest
from unittest.mock import patch
from click.testing import CliRunner

from certilizer import cli


class TestInit(unittest.TestCase):

    @patch("certilizer.run")
    def test_cli_help(self, func_run):

        func_run.return_value = None

        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Usage: cli [OPTIONS]", result.output)
        self.assertIn("Show this message and exit.", result.output)
        func_run.assert_not_called()

    @patch("certilizer.run")
    def test_cli_with_no_arg(self, func_run):

        func_run.return_value = None

        runner = CliRunner()
        result = runner.invoke(cli, [])

        self.assertEqual(result.exit_code, 0)
        func_run.assert_called_once_with("certilizer.yaml", "text", None, 100, 90)

    @patch("certilizer.run")
    def test_cli_with_invalid_arg(self, func_run):

        func_run.return_value = None

        runner = CliRunner()
        result = runner.invoke(cli, ["--some-invalid-arg"])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Error: No such option: --some-invalid-arg", result.output)
        func_run.assert_not_called()

    @patch("certilizer.run")
    def test_cli_with_defaults(self, func_run):

        func_run.return_value = None

        runner = CliRunner()
        result = runner.invoke(cli, [])

        self.assertFalse(result.exception)
        self.assertEqual(result.exit_code, 0)
        func_run.assert_called_once_with("certilizer.yaml", "text", None, 100, 90)

    @patch("certilizer.run")
    def test_cli_with_custom_options(self, func_run):

        func_run.return_value = None

        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "--conf-file",
                "tests-integration/fixtures/certilizer.yaml",
                "--out-format",
                "html",
                "--out-file",
                "/tmp/report.html",
                "--max-col-size",
                "50",
                "--expiry-threshold-in-days",
                "120",
            ],
        )

        self.assertFalse(result.exception)
        self.assertEqual(result.exit_code, 0)
        func_run.assert_called_once_with(
            "tests-integration/fixtures/certilizer.yaml",
            "html",
            "/tmp/report.html",
            50,
            120,
        )
