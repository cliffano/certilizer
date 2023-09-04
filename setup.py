import os
import setuptools
from setuptools import sic
import yaml

info_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'conf/info.yaml')
with open(info_file, 'r', encoding='utf8') as info_fh:
    info = yaml.load(info_fh, Loader=yaml.FullLoader)

readme_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'README.md')
with open(readme_file, 'r', encoding='utf8') as readme_fh:
    readme = readme_fh.read()

setuptools.setup(
    name='certilizer',
    description='Generate report of SSL/TLS certificates from a list of endpoints defined in a YAML configuration file',
    version=sic(info['version']),
    author='Cliffano Subagio',
    author_email='cliffano@gmail.com',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/cliffano/certilizer',
    keywords=['certilizer', 'report', 'ssl', 'tls', 'certificate'],
    packages=setuptools.find_packages(),
    include_package_data=True,
    py_modules=['certilizer'],
    entry_points={
        'console_scripts': [
            'certilizer = certilizer:cli',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=[
        'click==8.1.3',
        'conflog==1.5.1',
        'pandas==2.0.3',
        'PyYAML==6.0.1',
        'tabulate==0.9.0'
    ],
)
