# pylint: disable=too-many-locals,broad-exception-caught
"""
certilizer
==========
Generate report of SSL/TLS certificates from a list of endpoints defined
in a YAML configuration file.

This library provides a CLI tool to generate a report of SSL/TLS certificate's
details (serial number, common name, alternative names, issuer, expiry date,
OCSP, CA issuer, CRL distribution points), retrieved directly from an endpoint.
"""
import ssl
import socket
import click
from .cert import Cert
from .config import load as load_config
from .logger import init
from .reporter import Reporter

def run(conf_file: str, out_format: str, out_file: str) -> None:
    """Run Certiliser by:
    - Loading configuration file
    - Retrieving certificate from each endpoint
    - Generating report using specified format
    """

    logger = init()
    context = ssl.create_default_context()

    logger.info(f'Loading configuration file {conf_file}...')
    conf = load_config(conf_file)

    data = {
        'Endpoint': [],
        'Serial Number': [],
        'Common Name': [],
        'Alternative Names': [],
        'Issuer': [],
        'Expiry Date': [],
        'OCSP': [],
        'CA Issuer': [],
        'CRL Dist Points': []
    }

    error_data = {
        'Name': [],
        'Endpoint': [],
        'Error': []
    }

    for endpoint in conf['endpoints']:

        host = endpoint['host']
        port = endpoint['port']

        logger.info(f'Retrieving certificate from endpoint {host}:{port} ...')

        try:

            with socket.create_connection((host, port)) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:

                    peer_cert = ssock.getpeercert()
                    cert = Cert(peer_cert)

                    data['Endpoint'].append(f'{host}:{port}')
                    data['Serial Number'].append(cert.get_serial_number())
                    data['Common Name'].append(cert.get_common_name())
                    data['Alternative Names'].append(cert.get_alternative_names()[:20])
                    data['Issuer'].append(cert.get_issuer())
                    data['Expiry Date'].append(cert.get_expiry_date())
                    data['OCSP'].append(cert.get_ocsp()[:20])
                    data['CA Issuer'].append(cert.get_ca_issuer()[:20])
                    data['CRL Dist Points'].append(cert.get_crl_dist_points()[:20])

        except KeyboardInterrupt:
            logger.info('Keyboard interrupt detected')

        except Exception as exception:
            error_data['Name'].append(endpoint['name'])
            error_data['Endpoint'].append(f'{host}:{port}')
            error_data['Error'].append(str(exception))

    logger.info(f'Generating report using {out_format} format...')
    reporter = Reporter(out_format, out_file)
    reporter.write_cert(data)
    if error_data['Name']:
        reporter.write_error(error_data)

@click.command()
@click.option('--conf-file', default='certilizer.yaml', help='Configuration file path')
@click.option('--out-format', default='simple', help='Output format, based on table format \
              supported by Tabulate https://pypi.org/project/tabulate/')
@click.option('--out-file', help='When specified, output will be written to this file')
def cli(conf_file: str, out_format: str, out_file: str) -> None:
    """CLI tool for generating report of SSL/TLS certificates from a list of endpoints defined
    in a YAML configuration file.
    """
    run(conf_file, out_format, out_file)
