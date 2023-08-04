#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="jsonschema-minmax",
    version="1.0",
    description="A Draft2020-21 metaschema and python-jsonschema extension to allow defining and validating relative min/max constraints",
    author="Vidminas Mikucionis",
    author_email="5411598+Vidminas@users.noreply.github.com",
    license="MIT",
    url="https://github.com/Vidminas/python-jsonschema-minmax",
    py_modules=["src"],
    install_requires=[
        "referencing >= 0.30.0",
        "jsonschema >= 4.18.4",
    ],
)
