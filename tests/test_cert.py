# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
import unittest
from certilizer import Cert


class TestCert(unittest.TestCase):

    def test_get_ocsp_when_ocsp_exists(self):
        cert = Cert({"OCSP": ["http://ocsp.example.com"]})
        self.assertEqual(cert.get_ocsp(), "http://ocsp.example.com")

    def test_get_ocsp_when_ocsp_does_not_exist(self):
        cert = Cert({})
        self.assertEqual(cert.get_ocsp(), "")
