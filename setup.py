from setuptools import find_packages, setup
import os
import sys


setup(
    name='src',
    packages=find_packages(),
    version='0.1.0',
    description='Packaging the repos',
    author='reka',
    license='',
)

p = os.path.abspath('..')
if p not in sys.path:
    sys.path.append(p)

