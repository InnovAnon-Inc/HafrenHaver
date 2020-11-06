#! /usr/bin/env python3

#from pathlib           import Path
from os                import path
from setuptools        import find_packages, setup
#from setuptools.config import read_configuration
#from subprocess        import run

#conf_file = path.join (path.dirname (__file__), "setup.cfg")
#conf_dict = read_configuration (conf_file)

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read (fname):
    dirname = path.dirname (__file__)
    with open (path.join (dirname, fname)) as f: result = f.read ()
    assert result
    return result

def get_version (): return read ("VERSION")
#    vers_name = "VERSION"
#    vers_file = path.join (path.dirname (__file__), vers_name)
#    vers_file = Path (vers_file)
#    if vers_file.is_file ():
#        with open (vers_file, 'r') as f: result = f.read ()
#        #result = str (result)
#        #print ("result: %s", result)
#        assert result
#        if not result: raise Error ()
#        return result
#    result = run (["scripts/version.sh"])
#    result.check_returncode ()
#    result = str (result.stdout)
#    #print ("result: %s", result)
#    assert result
#    if not result: raise Error ()
#    return result

from glob    import glob
from os.path import basename
from os.path import splitext

setup (
   name='HafrenHaver', # TODO can use spaces ?
   version=get_version (),
   description=('Goes on and on about the River Severn'),
   author='Innovations Anonymous',
   author_email='InnovAnon-Inc@protonmail.com',
   license='unlicense',
   keywords=['InnovAnon', 'Innovations', 'Anonymous', 'Hafren Haver'],
   url='https://InnovAnon-Inc.github.io/HafrenHaver',
   long_description=read ('README.md'),
   long_description_content_type="text/markdown",
   packages=find_packages ('src', exclude=[".gitignore", "README.md", "cache"]),
   package_dir={ '' : 'src' },
   py_modules=[splitext (basename (path))[0] for path in glob ('src/*.py')],
   include_package_data=True,
   zip_safe=False,
   scripts=[
            'scripts/sloc.sh',
            'scripts/watch_sloc.sh',
            'scripts/version.sh',
           ],
   classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        'Programming Language :: Python :: Implementation :: CPython',
        #'Programming Language :: Python :: Implementation :: PyPy',

        #"Operating System :: OS Independent",
        'Operating System :: Unix',
        'Operating System :: POSIX',

        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Unlicense",
        "Topic :: Utilities",
        'Intended Audience :: Developers',
    ],
    python_requires='>=3.6',
    install_requires=[ #external packages as dependencies
        #'ast',
        'astor',
        #'bitarray',        # Python.h
        #'bjorklund',       # internal to our project
        #'cartopy',         # Python.h, mysql_config
        'datetime',
        #'enum',
        #'ephem',           # Python.h
        #'functools',       # Python.h
        #'gasp',
        'geocoder',
        'geopy',
        'hilbertcurve',
        #'inspect',
        #'itertools',
        #'math',
        #'matplotlib',      # Python.h
        'nltk',
        #'numba',           # Python.h, mysql_config
        'numpy',
        #'os',
        'pathlib',
        #'pattern',         # ?
        #'PIL',
        'podsixnet',
        #'pyaudio',         # Python.h
        #'pyephem_sunpath', # ephem
        'pygame',
        #'queue',
        #'random',
        #'re',
        'requests',
        #'scipy',           # ?
        #'shutil',
        'skyfield',
        #'speech_recognition',
        #'struct',
        #'sys',
        'tatsu',
        #'tensorflow',
        #'threading',
        #'tkinter',
        'wave',
        #'wavebender',
        #'weakref',
        #'weatherbit',
    ],
    extras_require={  # Optional
        #'dev': ['check-manifest'],
        #'test': ['coverage'],
        'test' : ['pytest', 'pytest-html', 'pytest-xdist'],
        'site' : ['sphinx', 'sphinx_theme'], # sphinx.ext.todo, sphinx.ext.githubpages
        'dist' : ['setuptools', 'wheel', 'twine'],
    },
    setup_requires=['pytest-runner'],
    #dependency_links=["http://peak.telecommunity.com/snapshots/",],
    package_data={  # Optional
    #    'sample': ['package_data.dat'],
        'version': ['scripts/VERSION.in'],
    },
    #entry_points={  # Optional
    #    'console_scripts': [
    #        'sample=sample:main',
    #    ],
    #},
    project_urls={  # Optional
        'Source'     : 'https://github.com/InnovAnon-Inc/HafrenHaver',
        'Bug Reports': 'https://github.com/InnovAnon-Inc/HafrenHaver/issues',
        #'Changelog'  : 'https://github.com/InnovAnon-Inc/HafrenHaver/blob/master/CHANGELOG.rst',
        'CIS'        : 'https://app.circleci.com/pipelines/github/InnovAnon-Inc/HafrenHaver',
        'Funding'    : 'https://www.patreon.com/InnovAnon',
        'Say Thanks!': 'https://saythanks.io/to/InnovAnon-Inc%40protonmail.com',
    },
)

