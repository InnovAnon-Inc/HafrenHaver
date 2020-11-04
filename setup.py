#! /usr/bin/env python3

from os                import path
from setuptools        import find_packages, setup
from setuptools.config import read_configuration

conf_file = path.join (path.dirname (__file__), "setup.cfg")
conf_dict = read_configuration (conf_file)

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read (fname): return open (path.join (path.dirname (__file__), fname)).read ()

setup (
   name='HafrenHaver',
   # TODO create version.txt if not exists, then read()
   version='1.0.2',
   description=('Goes on and on about the River Severn'),
   author='InnovAnon, Inc.',
   author_email='InnovAnon-Inc@protonmail.com',
   license='unlicense',
   keywords='Innovations Anonymous Hafren Haver',
   url='https://InnovAnon-Inc.github.io/HafrenHaver',
   long_description=read ('README.md'),
   long_description_content_type="text/markdown",
   #packages=['src'],  #same as name
   packages=find_packages (exclude=[".gitignore", "README.md", "LICENSE.md", "docs", "tests"]),
   scripts=[
            'scripts/sloc.sh',
            'scripts/watch_sloc.sh',
           ],
   classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
    ],
    python_requires='>=3.6',
    #install_requires=['bar', 'greek'], #external packages as dependencies
    #extras_require={  # Optional
        #'dev': ['check-manifest'],
        #'test': ['coverage'],
        #'doc'  : ['sphinx'],
        #'dev'  : ['setuptools', 'wheel', 'twine'],
        #'test' : [],
    #},
    #dependency_links=["http://peak.telecommunity.com/snapshots/",],
    #package_data={  # Optional
    #    'sample': ['package_data.dat'],
    #},
    #entry_points={  # Optional
    #    'console_scripts': [
    #        'sample=sample:main',
    #    ],
    #},
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/InnovAnon-Inc/HafrenHaver/issues',
        'Funding'    : 'https://www.patreon.com/InnovAnon',
        'Say Thanks!': 'https://saythanks.io/to/InnovAnon-Inc%40protonmail.com',
        'Source'     : 'https://github.com/InnovAnon-Inc/HafrenHaver',
        'CIS'        : 'https://app.circleci.com/pipelines/github/InnovAnon-Inc/HafrenHaver',
    },
)

