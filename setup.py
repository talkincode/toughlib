#!/usr/bin/python


from setuptools import setup, find_packages
import toughlib

version = toughlib.__version__

install_requires = [
    'six>=1.8.0',
    'Twisted>=13.0.0',
    'SQLAlchemy',
    'treq',
    'cyclone',
    'pycrypto'
]
install_requires_empty = []

package_data={}


setup(name='toughlib',
      version=version,
      author='jamiesun',
      author_email='jamiesun.net@gmail.com',
      url='https://github.com/talkincode/toughlib',
      license='MIT',
      description='toughstruct python tools',
      long_description=open('README.md').read(),
      classifiers=[
       'Development Status :: 6 - Mature',
       'Intended Audience :: Developers',
       'Programming Language :: Python :: 2.6',
       'Programming Language :: Python :: 2.7',
       'Topic :: Software Development :: Libraries :: Python Modules',
       ],
      packages=find_packages(),
      package_data=package_data,
      keywords=['toughstruct','toughradius'],
      zip_safe=True,
      include_package_data=True,
      install_requires=install_requires,
)