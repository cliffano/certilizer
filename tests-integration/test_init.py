# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
import unittest
from certilizer import run

class TestInit(unittest.TestCase):

    def test_run_with_config_file(self):
        run('tests-integration/fixtures/certilizer.yaml', 'simple', None)
