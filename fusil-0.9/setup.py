#!/usr/bin/env python
from imp import load_source
from os import path
from sys import argv

CLASSIFIERS = [
    'Intended Audience :: Developers',
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Operating System :: OS Independent',
    'Natural Language :: English',
    'Programming Language :: Python',
]

MODULES = [
    "fusil", "fusil.mas", "fusil.linux", "fusil.process", "fusil.network",
]

def main():
    if "--setuptools" in argv:
        argv.remove("--setuptools")
        from setuptools import setup
    else:
        from distutils.core import setup

    fusil = load_source("version", path.join("fusil", "version.py"))
    PACKAGES = {}
    for name in MODULES:
        PACKAGES[name] = name.replace(".", "/")

    install_options = {
        "name": fusil.PACKAGE,
        "version": fusil.VERSION,
        "url": fusil.WEBSITE,
        "download_url": fusil.WEBSITE,
        "author": "Victor Stinner",
        "description": "Fuzzing framework",
        "long_description": open('README').read(),
        "classifiers": CLASSIFIERS,
        "license": fusil.LICENSE,
        "packages": PACKAGES.keys(),
        "package_dir": PACKAGES,
        "scripts": ("scripts/fusil",),
    }
    setup(**install_options)

if __name__ == "__main__":
    main()

