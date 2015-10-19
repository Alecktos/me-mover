__author__ = 'alexander.persson'

from setuptools import setup

setup(name='episodeMover',
      version='0.1dev',
      packages=['episodeMover'],
      author='Alexander Persson',
      url='https://github.com/Alecktos/Directory-Tree-File-Mover',
      license='MIT',
      entry_points={
            'console_scripts': ['episodeMover = episodeMover.directory_tree_file_mover:main']
      }
)
