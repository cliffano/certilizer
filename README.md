<img align="right" src="https://raw.github.com/cliffano/certilizer/main/avatar.jpg" alt="Avatar"/>

[![Build Status](https://github.com/cliffano/certilizer/workflows/CI/badge.svg)](https://github.com/cliffano/certilizer/actions?query=workflow%3ACI)
[![Security Status](https://snyk.io/test/github/cliffano/certilizer/badge.svg)](https://snyk.io/test/github/cliffano/certilizer)
[![Published Version](https://img.shields.io/pypi/v/certilizer.svg)](https://pypi.python.org/pypi/certilizer)
<br/>

Certilizer
----------

Certilizer is a Python CLI for generating report of SSL certificates from multiple endpoints specified in a YAML configuration.

Installation
------------

    pip3 install certilizer

Usage
-----

Create a configuration file, e.g. `certilizer.yaml`:

    ---
    endpoints:
      - host: apple.com
        port: 443
      - host: google.com
        port: 443
      - host: microsoft.com
        port: 443
 
And then run `certilizer` CLI and pass the configuration file path:

    certilizer --conf-file certilizer.yaml

It will write the log messages to stdout:

    [certilizer] INFO Loading configuration file certilizer.yaml
    [certilizer] INFO TODO

Configuration
-------------

Configuration properties:

| Property | Type | Description | Example |
|----------|------|-------------|---------|
| `endpoints[]` | Array | A list of one or more endpoints with ... | |
| `endpoints[].host` | String | The name of the tagset. | `apple.com` |
| `endpoints[].port` | String | The name of the tagset. | `443` |

Colophon
--------

[Developer's Guide](https://cliffano.github.io/developers_guide.html#python)

Build reports:

* [Lint report](https://cliffano.github.io/certilizer/lint/pylint/index.html)
* [Code complexity report](https://cliffano.github.io/certilizer/complexity/wily/index.html)
* [Unit tests report](https://cliffano.github.io/certilizer/test/pytest/index.html)
* [Test coverage report](https://cliffano.github.io/certilizer/coverage/coverage/index.html)
* [Integration tests report](https://cliffano.github.io/certilizer/test-integration/pytest/index.html)
* [API Documentation](https://cliffano.github.io/certilizer/doc/sphinx/index.html)
