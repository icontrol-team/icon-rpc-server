#!/usr/bin/env python
import os
import re

from setuptools import setup, find_packages, Command
from setuptools.command.build_py import build_py
from setuptools.command.develop import develop

version = os.environ.get('VERSION')

if version is None:
    with open(os.path.join('.', 'VERSION')) as version_file:
        version = version_file.read().strip()

install_requires = []
setup_requires = []

with open('requirements.txt') as requirements:
    regex = re.compile('(grpcio)|(protobuf).+')
    for line in requirements:
        req = line.strip()
        install_requires.append(req)
        if regex.search(req):
            setup_requires.append(req)


class BuildPackageProtos(Command):
    """Command to generate project *_pb2.py modules from proto files."""

    description = 'build grpc protobuf modules'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import grpc_tools.command
        grpc_tools.command.build_package_protos(self.distribution.package_dir[''])


class BuildPyCommand(build_py):
    def run(self):
        self.run_command('build_proto_modules')
        build_py.run(self)


class DevelopCommand(develop):
    def run(self):
        self.run_command('build_proto_modules')
        develop.run(self)


setup_options = {
    'name': 'iconrpcserver',
    'version': version,
    'description': 'ICON RPC Server',
    'long_description': open('README.md').read(),
    'long_description_content_type': 'text/markdown',
    'url': 'https://github.com/icon-project/icon-rpc-server',
    'author': 'ICON Foundation',
    'author_email': 'foo@icon.foundation',
    'packages': find_packages(exclude=['tests*', 'docs']),
    'package_dir': {'': '.'},
    'package_data': {'iconrpcserver': ['icon_rpcserver_config.json']},
    'py_modules': ['iconrpcserver', ''],
    'license': "Apache License 2.0",
    'setup_requires': setup_requires,
    'install_requires': install_requires,
    'extras_require': {
        'tests': ['pytest>=4.6.3', "pytest-asyncio", "pytest-mock"],
    },
    'test_suite': 'tests',
    'entry_points': {
        'console_scripts': [
            'iconrpcserver=iconrpcserver:main'
        ],
    },
    'cmdclass': {
        'build_proto_modules': BuildPackageProtos,
        'build_py': BuildPyCommand,
        'develop': DevelopCommand
    },
    'classifiers': [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only'
    ]
}

setup(**setup_options)
