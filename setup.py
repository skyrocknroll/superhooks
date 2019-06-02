##############################################################################
# This software is subject to the provisions of the BSD-like license at
# http://www.repoze.org/LICENSE.txt.  A copy of the license should accompany
# this distribution.  THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL
# EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND
# FITNESS FOR A PARTICULAR PURPOSE
#
##############################################################################

import os
import sys

py_version = sys.version_info[:2]

if py_version < (2, 6):
    raise RuntimeError('On Python 2, superhooks requires Python 2.6 or later')
elif (3, 0) < py_version < (3, 2):
    raise RuntimeError('On Python 3, superhooks requires Python 3.2 or later')

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.md')).read()
except (IOError, OSError):
    README = ''
try:
    CHANGES = open(os.path.join(here, 'CHANGES.md')).read()
except (IOError, OSError):
    CHANGES = ''
# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    os.system('python2 setup.py sdist bdist_wheel')
    os.system('python3 setup.py sdist bdist_wheel')
    os.system('twine upload dist/superhooks*.tar.gz')
    os.system('twine upload dist/superhooks*.whl')
    sys.exit()

setup(name='superhooks',
      version='0.5',
      license='BSD-derived (http://www.repoze.org/LICENSE.txt)',
      description='superhooks plugin for supervisord',
      long_description=README + '\n\n' + CHANGES,
      long_description_content_type='text/markdown',
      classifiers=[
          "Development Status :: 3 - Alpha",
          'Environment :: No Input/Output (Daemon)',
          'Intended Audience :: System Administrators',
          'Natural Language :: English',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Topic :: System :: Boot',
          'Topic :: System :: Monitoring',
          'Topic :: System :: Systems Administration',
      ],
      author='Yuvaraj Loganathan',
      author_email='uvaraj6@gmail.com',
      url="https://github.com/skyrocknroll/superhooks",
      maintainer="Yuvaraj Loganathan",
      maintainer_email="uvaraj6@gmail.com",
      keywords='supervisor web hooks monitoring',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'superlance',
          'supervisor',
          'requests',
      ],
      tests_require=[
          'supervisor',
          'superlance',
          'mock',

      ],
      test_suite='superhooks.tests',
      entry_points="""\
      [console_scripts]
      superhooks = superhooks.superhooks:main
      """
      )
