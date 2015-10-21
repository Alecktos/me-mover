__author__ = 'alexander.persson'

from setuptools import setup

setup(name='episode-mover',
      version='0.1dev',
      packages=['episodeMover'],
      author='Alexander Persson',
      url='https://github.com/Alecktos/Directory-Tree-File-Mover',
      license='MIT',
      entry_points={
            'console_scripts': ['episode-mover = episodeMover.directory_tree_file_mover:main']
      }
)
