__author__ = 'alexander.berlind'

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
      long_description = fh.read()

setup(name='me-mover',
      version='3.1.0',
      packages=find_packages(exclude=['tests', 'tests.*']),
      author='Alexander Berlind',
      url='https://github.com/Alecktos/me-mover.git',
      description="Organize movies and tv-shows",
      long_description=long_description,
      long_description_content_type="text/markdown",
      license='MIT',
      entry_points={
            'console_scripts': ['me-mover = memover.main:main']
      },
      install_requires=[
            'watchdog'
      ],
      python_requires='>=3.7'
)
