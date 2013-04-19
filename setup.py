import os
from setuptools import setup, find_packages

required = [
    "docopt==0.6.1"
]

test = [
    "pytest==2.3.4",
    "tox==1.4.3"
]

dev = [
    "ipython==0.13.2",
    "readline"
]

readme = ''

# TODO: Figure out why this file is missing when running `tox`
if os.path.isfile('README.md'):
    readme = open('README.md').read()

setup(name='doku',
      version='0.1',
      description='A general sudoku library with a cli interface',
      long_description=readme,
      author='Collin Watson',
      author_email='collinwat@gmail.com',
      url='https://github.com/collinwat/doku',
      license='MIT',
      install_requires=required,
      packages=find_packages(exclude=['tests']),
      extras_require={
          'dev': dev,
          'test': test
      },
      entry_points={
          'console_scripts': [
              'doku = doku.cli:main',
          ]
      },
      classifiers=[
          'Development Status :: 4 - Alpha'
      ])
