<img align="right" src="https://raw.github.com/cliffano/certilizer/main/avatar.jpg" alt="Avatar"/>

[![Build Status](https://github.com/cliffano/certilizer/workflows/CI/badge.svg)](https://github.com/cliffano/certilizer/actions?query=workflow%3ACI)
[![Code Scanning Status](https://github.com/cliffano/certilizer/workflows/CodeQL/badge.svg)](https://github.com/cliffano/certilizer/actions?query=workflow%3ACodeQL)
[![Dependencies Status](https://img.shields.io/librariesio/release/pypi/certilizer)](https://libraries.io/pypi/certilizer)
[![Security Status](https://snyk.io/test/github/cliffano/certilizer/badge.svg)](https://snyk.io/test/github/cliffano/certilizer)
[![Published Version](https://img.shields.io/pypi/v/certilizer.svg)](https://pypi.python.org/pypi/certilizer)
<br/>

Certilizer
----------

Certilizer is a Python CLI for generating report of SSL/TLS certificates from multiple endpoints specified in a YAML configuration.

Certificates which will expire within N days (default 90 days, configurable via `--expiry-threshold-in-days` flag) will be highlighted in yellow. Expired certificates will be shown in red. And remaining certificates are shown in green.

![Screenshot of certificate report in HTML format](/screenshots/cert-report-html.png "Certificate report in HTML format")

Any error with certificates inspection will be included in an error report and highlighted in red.

![Screenshot of error report in HTML format](/screenshots/error-report-html.png "Error report in HTML format")

Installation
------------

    pip3 install certilizer

Usage
-----

Create a configuration file, e.g. `certilizer.yaml`:

    ---
    endpoints:
      - name: Google
        host: google.com
        port: 443
      - name: Apple
        host: apple.com
        port: 443
      - name: Twitter
        host: twitter.com
        port: 443
      - name: Facebook
        host: facebook.com
        port: 443
      - name: Nvidia
        host: nvidia.com
        port: 443
      - name: Microsoft
        host: microsoft.com
        port: 443
      - name: Amazon
        host: amazon.com
        port: 443
      - name: Inexisting
        host: someinexisting.website
        port: 443
      - name: Expired
        host: someexpired.website
        port: 443
        ssl_verify: false
 
And then run `certilizer` CLI and pass the configuration file path:

    certilizer --conf-file certilizer.yaml

It will write the log messages to stdout:

    [certilizer] INFO Loading configuration file certilizer.yaml...
    [certilizer] INFO Retrieving certificate from endpoint google.com:443 ...
    [certilizer] INFO Retrieving certificate from endpoint apple.com:443 ...
    [certilizer] INFO Retrieving certificate from endpoint twitter.com:443 ...
    [certilizer] INFO Retrieving certificate from endpoint facebook.com:443 ...
    [certilizer] INFO Retrieving certificate from endpoint nvidia.com:443 ...
    [certilizer] INFO Retrieving certificate from endpoint microsoft.com:443 ...
    [certilizer] INFO Retrieving certificate from endpoint amazon.com:443 ...
    [certilizer] INFO Retrieving certificate from endpoint someinexisting.website:443 ...
    [certilizer] ERROR An error occurred: [Errno -2] Name or service not known
    [certilizer] INFO Retrieving certificate from endpoint someexpired.website:443 ...
    [certilizer] ERROR An error occurred: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: Hostname mismatch, certificate is not valid
    [certilizer] INFO Generating report using text format...

By default, the certificate and error reports are written to stdout:

    Name       Endpoint           Serial Number         Common Name     Alternative Names     Issuer                Expiry Date          OCSP                  CA Issuer             CRL Dist Points
    ---------  -----------------  --------------------  --------------  --------------------  --------------------  -------------------  --------------------  --------------------  --------------------
    Facebook   facebook.com:443   06A4928C3D26F9659015  *.facebook.com  *.facebook.com, *.fa  DigiCert Inc (US) -   2023-09-17 23:59:59  http://ocsp.digicert  http://cacerts.digic  http://crl3.digicert
    Apple      apple.com:443      0E8AAA2BDAE0D2588F9D  apple.com       apple.com             Apple Inc. (US) - Ap  2023-10-30 20:25:16  http://ocsp.apple.co  http://certs.apple.c  http://crl.apple.com
    Google     google.com:443     37E9827AAED77BA210C2  *.google.com    *.google.com, *.appe  Google Trust Service  2023-11-06 08:16:27  http://ocsp.pki.goog  http://pki.goog/repo  http://crls.pki.goog
    Amazon     amazon.com:443     0E59F266F05E2A38079B  *.peg.a2z.com   amazon.co.uk, uedata  DigiCert Inc (US) -   2024-03-22 23:59:59  http://ocsp.digicert  http://cacerts.digic  http://crl3.digicert
    Microsoft  microsoft.com:443  3300C2BD1DF0B5A974D0  microsoft.com   microsoft.com, s.mic  Microsoft Corporatio  2024-06-27 23:59:59  http://oneocsp.micro  http://www.microsoft  http://www.microsoft
    Nvidia     nvidia.com:443     0FD72A4984819E27089A  nvidia.com      nvidia.com, *.nvidia  Amazon (US) - Amazon  2024-08-16 23:59:59  http://ocsp.r2m02.am  http://crt.r2m02.ama  http://crl.r2m02.ama
    Twitter    twitter.com:443    08A77EDA927285B76DFD  twitter.com     twitter.com, www.twi  DigiCert Inc (US) -   2024-08-19 23:59:59  http://ocsp.digicert  http://cacerts.digic  http://crl3.digicert
    Name                  Endpoint              Error
    --------------------  --------------------  --------------------
    someinexisting.websi  someinexisting.websi  [Errno -2] Name or s

Alternatively, the report format can be customised using `--out-format` flag, and the report can be written to a file using `--out-file` flag:

    certilizer --conf-file certilizer.yaml --out-format html --out-file some-certilizer-report.html

If the `--out-file` arg is not provided, the report will be written to stdout.

The threshold for expiry date can be configured using `--expiry-threshold-in-days` flag. By default, this is set to 90 days.

The column size can be set via `--max-col-size` flag which will determine how many characters will be included for each of the column values.

The certificate report can also be formatted in JSON or YAML, which is useful for further processing need.

JSON:

    [
      {
        "Name":"Facebook",
        "Endpoint":"facebook.com:443",
        "Serial Number":"0DDB92187FCE7567449EF61C9628140B",
        "Common Name":"*.facebook.com",
        "Alternative Names":"*.facebook.com, *.facebook.net, *.fbcdn.net, *.fbsbx.com, *.m.facebook.com, *.messenger.com, *.xx.fb",
        "Issuer":"DigiCert Inc (US) - DigiCert Global G2 TLS RSA SHA256 2020 CA1",
        "Expiry Date":1767052799000,
        "OCSP":"http:\/\/ocsp.digicert.com",
        "CA Issuer":"http:\/\/cacerts.digicert.com\/DigiCertGlobalG2TLSRSASHA2562020CA1-1.crt",
        "CRL Dist Points":"http:\/\/crl3.digicert.com\/DigiCertGlobalG2TLSRSASHA2562020CA1-1.crl, http:\/\/crl4.digicert.com\/DigiCer"
      },
      {
        "Name":"Apple",
        "Endpoint":"apple.com:443",
        "Serial Number":"3B983CAF5477B941342653A584074CBD",
        "Common Name":"apple.com",
        "Alternative Names":"apple.com",
        "Issuer":"Apple Inc. (US) - Apple Public EV Server ECC CA 1 - G1",
        "Expiry Date":1770753015000,
        "OCSP":"http:\/\/ocsp.apple.com\/ocsp03-apevsecc1g101",
        "CA Issuer":"http:\/\/certs.apple.com\/apevsecc1g1.der",
        "CRL Dist Points":"http:\/\/crl.apple.com\/apevsecc1g1.crl"
      },
      ...
    ]

YAML:

    - Alternative Names: '*.facebook.com, *.facebook.net, *.fbcdn.net, *.fbsbx.com, *.m.facebook.com,
        *.messenger.com, *.xx.fb'
      CA Issuer: http://cacerts.digicert.com/DigiCertGlobalG2TLSRSASHA2562020CA1-1.crt
      CRL Dist Points: http://crl3.digicert.com/DigiCertGlobalG2TLSRSASHA2562020CA1-1.crl,
        http://crl4.digicert.com/DigiCer
      Common Name: '*.facebook.com'
      Endpoint: facebook.com:443
      Expiry Date: !!python/object/apply:pandas._libs.tslibs.timestamps._unpickle_timestamp
      - 1767052799000000000
      - null
      - null
      - 10
      Issuer: DigiCert Inc (US) - DigiCert Global G2 TLS RSA SHA256 2020 CA1
      Name: Facebook
      OCSP: http://ocsp.digicert.com
      Serial Number: 0DDB92187FCE7567449EF61C9628140B
    - Alternative Names: apple.com
      CA Issuer: http://certs.apple.com/apevsecc1g1.der
      CRL Dist Points: http://crl.apple.com/apevsecc1g1.crl
      Common Name: apple.com
      Endpoint: apple.com:443
      Expiry Date: !!python/object/apply:pandas._libs.tslibs.timestamps._unpickle_timestamp
      - 1770753015000000000
      - null
      - null
      - 10
      Issuer: Apple Inc. (US) - Apple Public EV Server ECC CA 1 - G1
      Name: Apple
      OCSP: http://ocsp.apple.com/ocsp03-apevsecc1g101
      Serial Number: 3B983CAF5477B941342653A584074CBD

Configuration
-------------

Configuration properties that should be added to the YAML configuration file:

| Property | Type | Description | Example |
|----------|------|-------------|---------|
| `endpoints[]` | Array | A list of one or more cert endpoints with ... | |
| `endpoints[].name` | String | The name of the endpoint. | `443` |
| `endpoints[].host` | String | The cert endpoint host name. | `apple.com` |
| `endpoints[].port` | Int | The cert endpoint port number. | `443` |
| `endpoints[].ssl_verify` | String | Verify SSL when set to true. | `true` |

Colophon
--------

[Developer's Guide](https://cliffano.github.io/developers_guide.html#python)

Build reports:

* [Lint report](https://cliffano.github.io/certilizer/lint/pylint/index.html)
* [Code complexity report](https://cliffano.github.io/certilizer/complexity/radon/index.html)
* [Unit tests report](https://cliffano.github.io/certilizer/test/pytest/index.html)
* [Test coverage report](https://cliffano.github.io/certilizer/coverage/coverage/index.html)
* [Integration tests report](https://cliffano.github.io/certilizer/test-integration/pytest/index.html)
* [API Documentation](https://cliffano.github.io/certilizer/doc/sphinx/index.html)

Related projects:

* [Packer Certilizer](https://github.com/cliffano/packer-certilizer) - Packer builder of machine image for running Certilizer SSL/TLS certificates reporting tool