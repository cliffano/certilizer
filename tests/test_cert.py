# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
import unittest
from certilizer import Cert


class TestCert(unittest.TestCase):

    def test_get_serial_number(self):
        cert = Cert({"serialNumber": "1234567890"})
        self.assertEqual(cert.get_serial_number(), "1234567890")

    def test_get_common_name_when_common_name_exists(self):
        cert = Cert({"subject": [[("commonName", "example.com")]]})
        self.assertEqual(cert.get_common_name(), "example.com")

    def test_get_common_name_when_common_name_does_not_exist(self):
        cert = Cert({"subject": [[("organizationName", "Example Inc.")]]})
        self.assertEqual(cert.get_common_name(), None)

    def test_get_alternative_names_when_alt_names_exist(self):
        cert = Cert(
            {"subjectAltName": [["DNS", "example.com"], ["DNS", "www.example.com"]]}
        )
        self.assertEqual(cert.get_alternative_names(), "example.com, www.example.com")

    def test_get_alternative_names_when_alt_names_do_not_exist(self):
        cert = Cert({"subjectAltName": []})
        self.assertEqual(cert.get_alternative_names(), None)

    def test_get_ocsp_when_ocsp_exists(self):
        cert = Cert({"OCSP": ["http://ocsp.example.com"]})
        self.assertEqual(cert.get_ocsp(), "http://ocsp.example.com")

    def test_get_ocsp_when_ocsp_does_not_exist(self):
        cert = Cert({})
        self.assertEqual(cert.get_ocsp(), "")
