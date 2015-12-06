from pyesql import parse_file
import MySQLdb

Example = parse_file('example.sql')
conn = MySQLdb.connect(db='test')
example = Example(conn)

try:
    example.create_table()
except:
    pass

example.clean_test()

example.insert_test(a='test1', b=1)
example.insert_test(a='test2', b=2)
example.insert_test(a='test3', b=3)
assert conn.insert_id() == 3

conn.commit()

assert example.all_test() == ((1, 'test1', 1), (2, 'test2', 2), (3, 'test3', 3))
