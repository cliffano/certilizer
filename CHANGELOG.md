# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

## 1.2.0 - 2025-09-05
### Added
- Add CodeQL scanning workflow and badge
- Add ssl_verify YAML configuration property [#2]
- Add JSON and YAML output formats

### Changed
- Certificate OCSP is now optional [#4]
- Enforce min TLS to v1.2

## 1.1.0 - 2025-06-14
### Added
- Add --version flag to show version info

## 1.0.0 - 2025-06-09
### Added
- Add Python 3.12 support
- Add colour-coded row background based on cert expiry date [#1]
- Add CLI arg --expiry-threshold-in-days [#3]

### Changed
- Use Poetry to manage project
- Switch dependency versioning to allow compatible with version
- Use PieMaker for Makefile build

### Removed
- Remove Python 3.8 support

## 0.12.0 - 2023-09-07
### Added
- Add --max-col-size flag to limit column size in report output

## 0.11.0 - 2023-09-06
### Added
- Add message logging for error during certificate retrieval
- Add name field to certificate report

### Removed
- Hide index from report output tables

### Fixed
- Fix error report generation when output file is not on current working directory

## 0.10.3 - 2023-09-04
### Fixed
- Fix missing tabulate dependency

## 0.10.2 - 2023-09-04
### Fixed
- Reflect 0.10.1 fix in setup.py

## 0.10.1 - 2023-09-04
### Fixed
- Fix installation error with Cython 3.0.0a10 via PyYAML 6.0.1 upgrade

## 0.10.0 - 2023-09-04
### Added
- Initial version
