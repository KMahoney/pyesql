from unittest import TestCase
from pyesql.parser import LineParser, parse_query, ParseError, parse_queries, parse_source


class TestParseQuery(TestCase):
    def test_simple_query(self):
        query = """
        -- name: test
        QUERY BODY
        """
        name, doc, body = parse_query(LineParser(query))
        self.assertEqual(name, 'test')
        self.assertEqual(doc, '')
        self.assertEqual(body.strip(), 'QUERY BODY')

    def test_multiline_query(self):
        query = """
        -- name: test
        QUERY BODY 1

        QUERY BODY 2

        QUERY BODY 3
        """
        name, doc, body = parse_query(LineParser(query))
        self.assertEqual(name, 'test')
        self.assertEqual(doc, '')
        self.assertEqual([l.strip() for l in body.splitlines()],
                         ['QUERY BODY 1', '', 'QUERY BODY 2', '', 'QUERY BODY 3', ''])

    def test_include_comment_query(self):
        query = """
        -- name: test
        QUERY BODY 1
        -- comment
        QUERY BODY 2
        """
        name, doc, body = parse_query(LineParser(query))
        self.assertEqual(name, 'test')
        self.assertEqual(doc, '')
        self.assertEqual([l.strip() for l in body.splitlines()],
                         ['QUERY BODY 1', '-- comment', 'QUERY BODY 2', ''])

    def test_doc_query(self):
        query = """
        -- name: test
        -- documentation1
        -- documentation2
        QUERY BODY
        """
        name, doc, body = parse_query(LineParser(query))
        self.assertEqual(name, 'test')
        self.assertEqual(doc.strip(), 'documentation1\ndocumentation2')
        self.assertEqual(body.strip(), 'QUERY BODY')

    def test_no_body(self):
        query = """
        -- name: test
        -- documentation1
        -- documentation2
        """
        with self.assertRaises(ParseError):
            parse_query(LineParser(query))

    def test_no_doc_or_body(self):
        query = """
        -- name: test
        """
        with self.assertRaises(ParseError):
            parse_query(LineParser(query))

    def test_empty(self):
        with self.assertRaises(ParseError):
            parse_query(LineParser(""))


class TestParseQueries(TestCase):
    def test_multi_queries(self):
        query = """
        -- name: test1
        -- doc1
        QUERY BODY 1

        -- name: test2
        -- doc2
        QUERY BODY 2
        """
        queries = parse_queries(query)
        self.assertEqual(queries['test1'][0].strip(), 'doc1')
        self.assertEqual(queries['test1'][1].strip(), 'QUERY BODY 1')
        self.assertEqual(queries['test2'][0].strip(), 'doc2')
        self.assertEqual(queries['test2'][1].strip(), 'QUERY BODY 2')

    def test_no_endline(self):
        query = """
        -- name: test1
        -- doc1
        QUERY BODY 1

        -- name: test2
        -- doc2
        QUERY BODY 2"""
        queries = parse_queries(query)
        self.assertEqual(queries['test1'][0].strip(), 'doc1')
        self.assertEqual(queries['test1'][1].strip(), 'QUERY BODY 1')
        self.assertEqual(queries['test2'][0].strip(), 'doc2')
        self.assertEqual(queries['test2'][1].strip(), 'QUERY BODY 2')


class TestObject(TestCase):
    def test_multi_queries(self):
        query = """
        -- name: test1
        -- doc1
        QUERY BODY 1

        -- name: test2
        -- doc2
        QUERY BODY 2
        """
        test_class = parse_source('Test', query)
        test = test_class(None)
        self.assertTrue(hasattr(test, '__init__'))
        self.assertTrue(hasattr(test, 'test1'))
        self.assertTrue(hasattr(test, 'test2'))
