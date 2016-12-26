__author__ = 'alexander.persson'

from setuptools import setup

setup(name='me-mover',
      version='0.2dev',
      packages=['memover'],
      author='Alexander Persson',
      url='https://github.com/Alecktos/Directory-Tree-File-Mover',
      license='MIT',
      entry_points={
            'console_scripts': ['me-mover = memover.main:main']
      }
)
