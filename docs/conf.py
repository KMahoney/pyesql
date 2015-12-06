import sys
import os

sys.path.insert(0, os.path.abspath('..'))

from pyesql import VERSION

extensions = ['sphinx.ext.autodoc']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'pyesql'
copyright = u'2015, Kevin Mahoney'
author = u'Kevin Mahoney'
version = VERSION
release = VERSION
language = None
exclude_patterns = ['_build']
pygments_style = 'sphinx'
todo_include_todos = False

htmlhelp_basename = 'pyesqldoc'
html_theme = 'alabaster'
html_sidebars = {'**': []}
html_use_modindex = False
html_use_index = False
