#!/usr/bin/python3 
# coding=utf-8
import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='slider_task',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',  # example license
    description='oTree Slider Task.',
    long_description=README,
    url='http://github.com/chkgk/slider_task',
    author='Christian König genannt Kersting',
    author_email='christian.koenig@awi.uni-heidelberg.de',
)