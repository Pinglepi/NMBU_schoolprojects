# -*- coding: utf-8 -*-

"""
Setup file taken from chutes project by Hans Ekkhard Plesser

To create a package, run

python setup.py sdist

in the directory containing this file.

To create a zip archive in addition to a tar.gz archive, run

python setup.py sdist --formats=gztar,zip

The package will be placed in directory dist.

To install from the package, unpack it, move into the unpacked directory and
run

python setup.py install          # default location
python setup.py install --user   # per-user default location

See also
    https://docs.python.org/3.8/distributing
    https://docs.python.org/3.8/installing
    https://packaging.python.org/tutorials/distributing-packages/
"""

from setuptools import setup
import codecs
import os

__author__ = 'August N Steinset and Sunniva E Daae Steiro'
__email__ = 'augustei@nmbu.no and sunnivas@nmbu.no'


def read_readme():
    """
    Read README.md for use as long description.

    Based on PyPA Sample Project https://github.com/pypa/sampleproject

    :return: Multiline string containing contents of README.md
    """

    # build absolute path to directory containing setup.py
    here = os.path.abspath(os.path.dirname(__file__))

    # read the README.md file
    # using codes.open ensures that the file is read properly when using
    # UTF-8 encoding, e.g., for non-ASCII characters
    with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()

    return long_description


setup(
      name='BioSim',
      version='0.1.0',
      packages=['biosim'],
      description='An simulation of an island with animals',
      long_description=read_readme(),
      author='Sunniva Steiro and August Steinset, NMBU',
      author_email='sunnivas@nmbu.no and augustei@nmbu.no',
      requires=['matplotlib'],
      scripts=['examples/run_sim.py'],
      keywords='simulation',
      license='MIT License',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        ]
)
