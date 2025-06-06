#!/usr/bin/env bash
set -o errexit
set -o nounset

printf "\n\n========================================\n"
printf "Show help guide: certilizer --help\n"
certilizer --help

printf "\n\n========================================\n"
printf "Run command with default config file: certilizer\n"
certilizer

printf "\n\n========================================\n"
printf "Run command with specified config file:\n"
certilizer --conf-file certilizer.yaml

printf "\n\n========================================\n"
printf "Run command with specified config file, output format, and output file:\n"
certilizer --conf-file certilizer.yaml --out-format html --out-file ../stage/test-integration/example-output.html