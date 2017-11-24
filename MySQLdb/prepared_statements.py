
import MySQLdb as mdb

con = mdb.connect('localhost', 'root', 'chopin', 'test')

with con:
    cur = con.cursor()

    cur.execute("update writers set name = %s where id = %s",
            ("Guy de Maupasant", "4"))

    print "Number of rows updated:", cur.rowcount

