"""
Pyesql is a Python clone of Yesql (https://github.com/krisajenkins/yesql)

Source: https://github.com/KMahoney/pyesql

Differences from Yesql:

- Python does not distinguish between a statement and a query, so there is no need for the `!` suffix.
- Instead of the `?` and `:param` syntax, Pyesql uses the `%(param)s` syntax

"""

from pyesql.parser import parse_file, parse_source, ParseError

__all__ = ['parse_file', 'parse_source', 'ParseError', 'VERSION']

VERSION = '0.0.1'
