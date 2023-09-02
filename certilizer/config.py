"""Configuration loader.
"""
import yaml

def load(conf_file: str):
    """Load configuration values from file.
    """

    with open(conf_file, 'r', encoding='utf-8') as (stream):
        conf = yaml.safe_load(stream)

    return conf
