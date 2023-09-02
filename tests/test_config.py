# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
from unittest.mock import patch, mock_open
import unittest.mock
import unittest
from certilizer.config import load

CONFIG = '''
---
endpoints:
  - host: apple.com
    port: 443
  - host: google.com
    port: 443
  - host: microsoft.com
    port: 443
'''

class TestConfig(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data=CONFIG)
    def test_load_with_properties(self, func_open): # pylint: disable=unused-argument
        with open('certilizer.yaml', 'r', encoding='utf8') as file_handle:
            assert file_handle.read() == CONFIG

        config = load('certilizer.yaml')
        self.assertEqual(len(config['endpoints']), 3)
        self.assertEqual(config['endpoints'][0]['host'], 'apple.com')
        self.assertEqual(config['endpoints'][0]['port'], 443)
        self.assertEqual(config['endpoints'][1]['host'], 'google.com')
        self.assertEqual(config['endpoints'][1]['port'], 443)
        self.assertEqual(config['endpoints'][2]['host'], 'microsoft.com')
        self.assertEqual(config['endpoints'][2]['port'], 443)
