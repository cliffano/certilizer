"""A module for processing certificate details to be produced by the
reporter, based on the information retrieved from the endpoints'
SSL/TLS certificates.
"""
from datetime import datetime

class Cert():
    """A class for processing reportable certificate details
    from the peer cert.
    """

    def __init__(self, peer_cert: dict):
        """Initialise the Cert object."""
        self.peer_cert = peer_cert

    def get_serial_number(self) -> str:
        """Return the certificate's serial number."""

        serial_number = self.peer_cert['serialNumber']

        return serial_number

    def get_common_name(self) -> str:
        """Return the certificate's subject common name.
        None will be returned if the common name is not found.
        """

        common_name = None

        subject = self.peer_cert['subject']
        for item in subject:
            if item[0][0] == 'commonName':
                common_name = item[0][1]
                break

        return common_name

    def get_alternative_names(self) -> str:
        """Return the certificate's alternative names.
        If there are multiple alternative names, they will be
        returned as a comma-separated string.
        If there's no alternative names, an empty array will be returned.
        """

        alt_names = []

        subject_alt_name = self.peer_cert['subjectAltName']
        for item in subject_alt_name:
            if item[0] == 'DNS':
                alt_name = item[1]
                alt_names.append(alt_name)

        return ', '.join(alt_names)

    def get_issuer(self) -> str:
        """Return the certificate's issuer.
        The format will be 'organizationName (countryName) - commonName'.
        """

        country_name = None
        org_name = None
        common_name = None

        issuer = self.peer_cert['issuer']
        for item in issuer:
            if item[0][0] == 'countryName':
                country_name = item[0][1]
            if item[0][0] == 'organizationName':
                org_name = item[0][1]
            if item[0][0] == 'commonName':
                common_name = item[0][1]

        issuer_info = f'{org_name} ({country_name}) - {common_name}'
        return issuer_info

    def get_expiry_date(self) -> str:
        """Return the certificate's expiry date.
        The format will be '%b %d %H:%M:%S %Y %Z'.
        """

        not_after = self.peer_cert['notAfter']
        expiry_date = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')

        return expiry_date

    def get_ocsp(self) -> str:
        """Return the certificate's OCSP URL.
        If there are multiple OCSP URLs, they will be
        returned as a comma-separated string.
        """

        ocsp =  ', '.join(self.peer_cert['OCSP'])

        return ocsp

    def get_ca_issuer(self) -> str:
        """Return the certificate's CA issuer.
        If there are multiple CA issuers, they will be
        returned as a comma-separated string.
        """

        ca_issuer = ', '.join(self.peer_cert['caIssuers'])

        return ca_issuer

    def get_crl_dist_points(self) -> str:
        """Return the certificate's CRL distribution points.
        If there are multiple CRL distribution points, they will be
        returned as a comma-separated string.
        """

        crl_dist_points = ', '.join(self.peer_cert['crlDistributionPoints'])

        return crl_dist_points
