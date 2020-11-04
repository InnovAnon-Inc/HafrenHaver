#! /usr/bin/env python3

from pathlib           import Path
from os                import path
from setuptools        import find_packages, setup
from setuptools.config import read_configuration
from subprocess        import run

conf_file = path.join (path.dirname (__file__), "setup.cfg")
conf_dict = read_configuration (conf_file)

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read (fname):
    dirname = path.dirname (__file__)
    with open (path.join (dirname, fname)) as f: return f.read ()

def get_version ():
    vers_name = "VERSION"
    vers_file = path.join (path.dirname (__file__), vers_name)
    vers_file = Path (vers_file)
    if vers_file.is_file ():
        with open (vers_file) as f: result = f.read ()
        #result = str (result)
        print ("result: %s", result)
        return result
    result = run (["scripts/version.sh"])
    result = str (result)
    print ("result: %s", result)
    return result

setup (
   name='HafrenHaver', # TODO can use spaces ?
   version=get_version (),
   description=('Goes on and on about the River Severn'),
   author='Innovations Anonymous',
   author_email='InnovAnon-Inc@protonmail.com',
   license='unlicense', # TODO can read LICENSE ?
   keywords='Innovations Anonymous Hafren Haver',
   url='https://InnovAnon-Inc.github.io/HafrenHaver',
   long_description=read ('README.md'),
   long_description_content_type="text/markdown",
   #packages=['src'],  #same as name
   packages=find_packages (exclude=[".gitignore", "README.md", "LICENSE.md", "doc", "tests"]),
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

