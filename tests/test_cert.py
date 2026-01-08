# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
import unittest
from datetime import datetime
from certilizer import Cert


class TestCert(unittest.TestCase):

    def test_get_serial_number(self):
        cert = Cert({"serialNumber": "1234567890"})
        self.assertEqual(cert.get_serial_number(), "1234567890")

    def test_get_common_name_when_common_name_exists(self):
        cert = Cert({"subject": [[("commonName", "example.com")]]})
        self.assertEqual(cert.get_common_name(), "example.com")

    def test_get_common_name_when_common_name_does_not_exist(self):
        cert = Cert({"subject": [[("organizationName", "Some Org")]]})
        self.assertEqual(cert.get_common_name(), None)

    def test_get_alternative_names_when_alt_names_exist(self):
        cert = Cert(
            {"subjectAltName": [["DNS", "example.com"], ["DNS", "www.example.com"]]}
        )
        self.assertEqual(cert.get_alternative_names(), "example.com, www.example.com")

    def test_get_alternative_names_when_alt_names_do_not_exist(self):
        cert = Cert({"subjectAltName": []})
        self.assertEqual(cert.get_alternative_names(), None)

    def test_get_issuer_when_fields_exist(self):
        cert = Cert(
            {
                "issuer": [
                    [("countryName", "AU")],
                    [("organizationName", "Some Org")],
                    [("commonName", "Some CA")],
                ]
            }
        )
        self.assertEqual(cert.get_issuer(), "Some Org (AU) - Some CA")

    def test_get_issuer_when_fields_are_partial(self):
        cert = Cert({"issuer": [[("commonName", "Some CA")]]})
        self.assertEqual(cert.get_issuer(), "None (None) - Some CA")

    def test_get_issuer_when_issuer_missing(self):
        cert = Cert({})
        with self.assertRaises(KeyError):
            cert.get_issuer()

    def test_get_expiry_date_when_not_after_exists(self):
        cert = Cert({"notAfter": "Jan 01 12:00:00 2030 GMT"})
        self.assertEqual(
            cert.get_expiry_date(),
            datetime(2030, 1, 1, 12, 0, 0),
        )

    def test_get_expiry_date_when_not_after_not_exist(self):
        cert = Cert({})
        with self.assertRaises(KeyError):
            cert.get_expiry_date()

    def test_get_expiry_date_when_not_after_invalid_format(self):
        cert = Cert({"notAfter": "2030-01-01"})
        with self.assertRaises(ValueError):
            cert.get_expiry_date()

    def test_get_ocsp_when_ocsp_exists(self):
        cert = Cert({"OCSP": ["http://ocsp.example.com"]})
        self.assertEqual(cert.get_ocsp(), "http://ocsp.example.com")

    def test_get_ocsp_when_ocsp_does_not_exist(self):
        cert = Cert({})
        self.assertEqual(cert.get_ocsp(), "")

    def test_get_ca_issuer_when_ca_issuer_exists(self):
        cert = Cert({"caIssuers": ["http://ca.example.com"]})
        self.assertEqual(cert.get_ca_issuer(), "http://ca.example.com")

    def test_get_ca_issuer_when_ca_issuers_are_empty(self):
        cert = Cert({"caIssuers": []})
        self.assertEqual(cert.get_ca_issuer(), "")

    def test_get_ca_issuer_when_ca_issuers_do_not_exist(self):
        cert = Cert({})
        with self.assertRaises(KeyError):
            cert.get_ca_issuer()

    def test_get_crl_dist_points_when_points_exist(self):
        cert = Cert(
            {
                "crlDistributionPoints": [
                    "http://crl1.example.com",
                    "http://crl2.example.com",
                ]
            }
        )
        self.assertEqual(
            cert.get_crl_dist_points(),
            "http://crl1.example.com, http://crl2.example.com",
        )

    def test_get_crl_dist_points_when_points_are_empty(self):
        cert = Cert({"crlDistributionPoints": []})
        self.assertEqual(cert.get_crl_dist_points(), "")

    def test_get_crl_dist_points_when_points_do_not_exist(self):
        cert = Cert({})
        with self.assertRaises(KeyError):
            cert.get_crl_dist_points()
