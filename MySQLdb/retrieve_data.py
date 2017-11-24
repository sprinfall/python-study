import MySQLdb as mdb

con = mdb.connect('localhost', 'root', 'chopin', 'test')

def test_fetchall():
    with con:
        cur = con.cursor()
        cur.execute('select * from writers')

        # Result set.
        # A tuple of tuples. Each of the inner tuples represent a row in the table.
        rows = cur.fetchall()
        for row in rows:
            # TODO: How to display utf8 encoded strings in MySQL?
            print row[0], unicode(row[1], 'utf-8')

def test_fetch_one_by_one():
    with con:
        cur = con.cursor()
        cur.execute('select * from writers')

        # Fetch row one by one.
        for i in range(cur.rowcount):
            row = cur.fetchone()
            print row

def test_dict_cursor():
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute('select * from writers limit 4')

        rows = cur.fetchall()
        for row in rows:
            print row['id'], row['name']

def test_column_headers():
    with con:
        cur = con.cursor()
        cur.execute('select * from writers limit 4')

        rows = cur.fetchall()
        desc = cur.description

        print '%s %3s' % (desc[0][0], desc[1][0])

        for row in rows:
            print '%2s %3s' % row

if __name__ == '__main__':
    test_fetchall()
#     test_fetch_one_by_one()
#     test_dict_cursor()
#     test_column_headers()

