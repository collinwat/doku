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

description = ""
readme = open('README.rst')
description = readme.read()
readme.close()

setup(name='doku',
      version='0.1',
      description='A general sudoku library with a cli interface',
      long_description=description,
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
              'xpsudoku = xpsudoku.cli:main',
          ]
      },
      classifiers=[
          'Development Status :: 4 - Alpha'
      ])
