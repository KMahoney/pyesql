import re
from os.path import basename


class ParseError(Exception):
    """An error was encountered in the SQL source"""
    pass


WHITESPACE_RE = re.compile('^\s*$')
NAME_RE = re.compile('^\s*--\s*name:')
DOC_RE = re.compile('^\s*--\s*')


class LineParser(object):
    def __init__(self, source):
        self.lines = iter(source.splitlines())
        self.linecount = 0
        self.next()

    def next(self):
        try:
            self.line = next(self.lines)
        except StopIteration:
            self.line = None
        else:
            self.linecount += 1

    def eof(self):
        return self.line is None

    def skip_whitespace(self):
        while not self.eof() and WHITESPACE_RE.match(self.line):
            self.next()


def parse_query(parser):
    parser.skip_whitespace()

    # Parse name
    if parser.eof() or not NAME_RE.match(parser.line):
        raise ParseError("{}: Expecting '-- name: <query-name>'".format(parser.linecount))

    name = re.sub(NAME_RE, '', parser.line).strip()
    parser.next()
    parser.skip_whitespace()

    if parser.eof():
        raise ParseError('{}: Expecting documentation or query body for query {}'.format(parser.linecount, name))

    # Parse docstring
    doc_lines = []
    while not parser.eof() and DOC_RE.match(parser.line):
        doc_lines.append(re.sub(DOC_RE, '', parser.line))
        parser.next()
    doc = '\n'.join(doc_lines)

    parser.skip_whitespace()

    if parser.eof() or NAME_RE.match(parser.line):
        raise ParseError('{}: Expecting query body for query {}'.format(parser.linecount, name))

    # Parse body
    body_lines = []
    while not parser.eof() and not NAME_RE.match(parser.line):
        body_lines.append(parser.line)
        parser.next()
    body = '\n'.join(body_lines)

    return name, doc, body


def parse_queries(source):
    queries = {}
    parser = LineParser(source)
    while not parser.eof():
        name, doc, body = parse_query(parser)
        queries[name] = (doc, body)
        parser.skip_whitespace()
    return queries


def _make_query_fn(doc, body):
    def inner(self, *args, **kwargs):
        cursor = self.connection.cursor()
        cursor.execute(body, kwargs)
        return cursor.fetchall()
    inner.__doc__ = doc
    return inner


def parse_source(name, source):
    """Parse a SQL source string into a python object.

    Takes a source SQL string and parses it into a new class named
    `name`. The class is initialised with a database connection
    and has a method for each SQL statement.

    Each SQL statement should take the form::

        -- name: <name>
        -- optional documentation
        BODY %(parameter)s

    For example given the SQL source::

        -- name: test1
        -- documentation test1
        SELECT * FROM test

        -- name: test2
        SELECT * FROM test WHERE x = %(y)s

    we can produce this object::

        Example = parse_object('Example', source)
        connection = MySQLdb.connect(...)
        example = Example(connection)
        example.test1()
        example.test2(y=1)

    :param str name: Name of the returned type
    :param str source: Source SQL
    :return: A new Python type
    :raises ParseError: If the Source SQL does not conform

    """
    queries = parse_queries(source)
    obj = {k: _make_query_fn(*v) for k, v in queries.items()}

    def __init__(self, connection):
        self.connection = connection
    obj['__init__'] = __init__

    return type(name, (), obj)


def parse_file(filename, name=None):
    """Parse a SQL source file into a python object.

    Reads `filename` in to memory and returns a new class named after
    the filename. See :py:func:`pyesql.parse_source` for details on the
    returned class.

    :param str filename: Source SQL filename
    :param str name: Optional name of the returned type. Uses filename by default.
    :return: A new Python type
    :raises ParseError: If the Source SQL does not conform

    """
    with open(filename) as f:
        source = f.read()
    return parse_source(name or basename(filename), source)
