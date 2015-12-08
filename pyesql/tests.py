from unittest import TestCase
from pyesql.parser import LineParser, parse_query, ParseError, parse_queries, parse_source


class TestParseQuery(TestCase):
    def test_simple_query(self):
        query = """
        -- name: test
        QUERY BODY
        """
        q = parse_query(LineParser(query))
        self.assertEqual(q.name, 'test')
        self.assertFalse(q.statement)
        self.assertEqual(q.doc, '')
        self.assertEqual(q.body.strip(), 'QUERY BODY')

    def test_statement(self):
        query = """
        -- name: test!
        QUERY BODY
        """
        q = parse_query(LineParser(query))
        self.assertEqual(q.name, 'test')
        self.assertTrue(q.statement)
        self.assertEqual(q.doc, '')
        self.assertEqual(q.body.strip(), 'QUERY BODY')

    def test_multiline_query(self):
        query = """
        -- name: test
        QUERY BODY 1

        QUERY BODY 2

        QUERY BODY 3
        """
        q = parse_query(LineParser(query))
        self.assertEqual(q.name, 'test')
        self.assertEqual(q.doc, '')
        self.assertEqual([l.strip() for l in q.body.splitlines()],
                         ['QUERY BODY 1', '', 'QUERY BODY 2', '', 'QUERY BODY 3', ''])

    def test_include_comment_query(self):
        query = """
        -- name: test
        QUERY BODY 1
        -- comment
        QUERY BODY 2
        """
        q = parse_query(LineParser(query))
        self.assertEqual(q.name, 'test')
        self.assertEqual(q.doc, '')
        self.assertEqual([l.strip() for l in q.body.splitlines()],
                         ['QUERY BODY 1', '-- comment', 'QUERY BODY 2', ''])

    def test_doc_query(self):
        query = """
        -- name: test
        -- documentation1
        -- documentation2
        QUERY BODY
        """
        q = parse_query(LineParser(query))
        self.assertEqual(q.name, 'test')
        self.assertEqual(q.doc.strip(), 'documentation1\ndocumentation2')
        self.assertEqual(q.body.strip(), 'QUERY BODY')

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
        self.assertEqual(queries['test1'].doc.strip(), 'doc1')
        self.assertEqual(queries['test1'].body.strip(), 'QUERY BODY 1')
        self.assertEqual(queries['test2'].doc.strip(), 'doc2')
        self.assertEqual(queries['test2'].body.strip(), 'QUERY BODY 2')

    def test_no_endline(self):
        query = """
        -- name: test1
        -- doc1
        QUERY BODY 1

        -- name: test2
        -- doc2
        QUERY BODY 2"""
        queries = parse_queries(query)
        self.assertEqual(queries['test1'].doc.strip(), 'doc1')
        self.assertEqual(queries['test1'].body.strip(), 'QUERY BODY 1')
        self.assertEqual(queries['test2'].doc.strip(), 'doc2')
        self.assertEqual(queries['test2'].body.strip(), 'QUERY BODY 2')


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
