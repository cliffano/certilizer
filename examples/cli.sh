#!/bin/sh
set -o errexit
set -o nounset

echo "\n\n========================================"
echo "Show help guide: certilizer --help"
echo "Show help guide: certilizer --help"
certilizer --help

echo "\n\n========================================"
echo "Run command with default config file: certilizer"
certilizer

echo "\n\n========================================"
echo "Run command with specified config file:"
echo "certilizer --conf-file certilizer.yaml"
certilizer --conf-file certilizer.yaml

echo "\n\n========================================"
echo "Run command with specified config file, output format, and output file:"
echo "certilizer --conf-file certilizer.yaml --out-format html --out-file ../stage/test-integration/example-output.html"
certilizer --conf-file certilizer.yaml --out-format html --out-file ../stage/test-integration/example-output.html