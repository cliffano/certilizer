# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
import unittest
from certilizer import run

class TestInit(unittest.TestCase):

    def test_run_without_aws_region(self):
        run('tests-integration/fixtures/certilizer.yaml', 'simple', None)
