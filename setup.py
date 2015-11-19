# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

version = '0.0.1'

setup(
    name='transactions',
    version=version,
    description='App for transactions',
    author='Wayzon',
    author_email='info@wayzon.in',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=("frappe",),
)
