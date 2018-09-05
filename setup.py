# -*- coding: utf-8 -*-
# setup.py
# author : Antoine Passemiers

from setuptools import setup

setup(
    name='rmm',
    version='1.0.0',
    description='Realistic mouse movements',
    url='https://github.com/AntoinePassemiers/Realistic-Mouse',
    author='Antoine Passemiers',
    author_email='apassemi@ulb.ac.be',
    packages=['rmm'],
    package_data={'rmm': ['data/*.*']})
