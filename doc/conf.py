# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

import os
import sys
sys.path.insert (0, os.path.abspath ('../src'))

# -- Project information -----------------------------------------------------

project = 'Hafren Haver'
copyright = '2020, Innovations Anonymous'
author = 'Innovations Anonymous'

from pathlib    import Path
from os         import path
#from subprocess import run

def read ():
    vers_name = "VERSION.in"
    vers_file = path.join (path.dirname (__file__), "..", "scripts", vers_name)
    vers_file = Path (vers_file)
    with open (vers_file, 'r') as f: result = f.read ()
    assert result
    return result

def get_version ():
    vers_name = "VERSION"
    vers_file = path.join (path.dirname (__file__), "..", vers_name)
    vers_file = Path (vers_file)
    with open (vers_file, 'r') as f: result = f.read ()
#    if vers_file.is_file ():
#        with open (vers_file, 'r') as f: result = f.read ()
#        #print ("result: %s" % result)
#        assert result
#        if not result: raise Error ()
#        return result
#    result = run (["../scripts/version.sh"])
#    result.check_returncode ()
#    result = str (result.stdout)
    #print ("result: %s" % result)
    assert result
    if not result: raise Error ()
    return result

version = read ()
# The full version, including alpha/beta/rc tags
release = get_version ()


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.doctest',
    'sphinx.ext.githubpages',
    #'sphinx.ext.graphviz',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.intersphinx',
    #'sphinx.ext.linkcode',
    'sphinx.ext.imgmath',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
]
autosummary_generate = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

html_logo = '_static/logo.png'

source_suffix = ['.rst', '.md']
master_doc = 'index'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

pygments_style = 'sphinx'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
import sphinx_theme
#html_theme = 'alabaster'
html_theme = 'stanford_theme'
html_theme_path = [sphinx_theme.get_html_theme_path ('stanford-theme')]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

