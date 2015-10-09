__author__ = 'alexander.persson'

from setuptools import setup

setup(name='directoryTreeFileMover',
      version='0.1dev',
      packages=['directoryTreeFileMover'],
      author='Alexander Persson',
      url='https://github.com/Alecktos/Directory-Tree-File-Mover',
      license='MIT',
      entry_points={
            'console_scripts': ['directoryTreeFileMover = directoryTreeFileMover.directory_tree_file_mover:main']
      }
)
