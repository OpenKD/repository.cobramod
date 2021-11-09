# -*- coding: utf-8 -*-
# Module: default
# Author: asciidisco
# Created on: 24.07.2017
# License: MIT https://goo.gl/WA1kby

"""Setup"""

from __future__ import unicode_literals
from os.path import abspath, dirname, join
from re import search
from sys import exit, version, version_info
from setuptools import find_packages, setup

REQUIRED_PYTHON_VERSION = (2, 7)
PACKAGES = find_packages()
INSTALL_DEPENDENCIES = []
SETUP_DEPENDENCIES = []
TEST_DEPENDENCIES = [
    'nose',
    'Kodistubs',
    'httpretty',
    'mock',
]
EXTRA_DEPENDENCIES = {
    'dev': [
        'nose',
        'flake8',
        'codeclimate-test-reporter',
        'pylint',
        'mccabe',
        'pycodestyle',
        'pyflakes',
        'Kodistubs',
        'httpretty',
        'mock',
        'requests',
        'beautifulsoup4',
        'pyDes',
        'radon',
        'Sphinx',
        'sphinx_rtd_theme',
        'm2r',
        'kodi-release-helper',
        'dennis',
        'blessings',
        'demjson',
        'restructuredtext_lint',
        'yamllint',
    ]
}


def get_addon_data():
    """Loads the Kodi plugin data from addon.xml"""
    root_dir = dirname(abspath(__file__))
    pathname = join(root_dir, 'addon.xml')
    with open(pathname, 'rb') as addon_xml:
        addon_xml_contents = addon_xml.read()
        _id = search(
            r'(?<!xml )id="(.+?)"',
            addon_xml_contents).group(1)
        author = search(
            r'(?<!xml )provider-name="(.+?)"',
            addon_xml_contents).group(1)
        name = search(
            r'(?<!xml )name="(.+?)"',
            addon_xml_contents).group(1)
        version = search(
            r'(?<!xml )version="(.+?)"',
            addon_xml_contents).group(1)
        desc = search(
            r'(?<!xml )description lang="en_GB">(.+?)<',
            addon_xml_contents).group(1)
        email = search(
            r'(?<!xml )email>(.+?)<',
            addon_xml_contents).group(1)
        source = search(
            r'(?<!xml )email>(.+?)<',
            addon_xml_contents).group(1)
        return {
            'id': _id,
            'author': author,
            'name': name,
            'version': version,
            'desc': desc,
            'email': email,
            'source': source,
        }


if version_info < REQUIRED_PYTHON_VERSION:
    exit('Python >= 2.7 is required. Your version:\n{0}'.format(version))

if __name__ == '__main__':
    ADDON_DATA = get_addon_data()
    setup(
        name=ADDON_DATA.get('name'),
        version=ADDON_DATA.get('version'),
        author=ADDON_DATA.get('author'),
        author_email=ADDON_DATA.get('email'),
        description=ADDON_DATA.get('desc'),
        packages=PACKAGES,
        include_package_data=True,
        install_requires=INSTALL_DEPENDENCIES,
        setup_requires=SETUP_DEPENDENCIES,
        tests_require=TEST_DEPENDENCIES,
        extras_require=EXTRA_DEPENDENCIES,
        test_suite='nose.collector',
    )
