#!/usr/bin/env python
"""
esmbc
~~~~~

Calculates total ship volume of supplied ships and quantity pairs.

:copyright: (c) 2012 Stuart Baker
:license: GNU GPL Version 3, see LICENSE

"""
from distutils.core import setup

setup(name='esmbc',
      version='0.1',
      description='EVE Online Ship Maintenance Bay Calculator',
      license='GPL3',
      author='Stuart Baker',
      author_email='sdb@stuartdb.com',
      url='https://github.com/stuartdb/esmbc',
      platforms='any',
      py_modules=['esmbc', 'test_esmbc'],
      data_files=[('data', ['data/ships.json', 'data/test_ships.json'])],
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Games/Entertainment'
        ]
      )
