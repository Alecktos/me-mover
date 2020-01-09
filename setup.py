__author__ = 'alexander.berlind'

from setuptools import setup

setup(name='me-mover',
      version='3.0',
      packages=['memover'],
      author='Alexander Berlind',
      url='https://github.com/Alecktos/me-mover.git',
      license='MIT',
      entry_points={
            'console_scripts': ['me-mover = memover.main:main']
      },
      install_requires=[
            'watchdog'
      ]
)
