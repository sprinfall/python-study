# coding: utf-8

import MySQLdb as mdb

# MySQLdb的connection对象可以当做context manager使用.
# 如果结合with语句的话, commit和rollback都将自动完成.

try:
    con = mdb.connect('localhost', 'root', 'chopin', 'test')

    cur = con.cursor()
    # A transaction is started when the cursor is created.

    cur.execute('drop table if exists writers')
    # MyISAM doesn't support transaction.
    cur.execute('create table writers(id int primary key auto_increment,\
            name varchar(25)) engine=innodb')

    cur.execute('insert into writers(name) values("Jack London")')
    cur.execute('insert into writers(name) values("Honore de Balzac")')
    cur.execute('insert into writers(name) values("Lion Feuchtwanger")')
    cur.execute('insert into writers(name) values("Emile Zola")')
    cur.execute('insert into writers(name) values("Truman Capote")')

    # We must end a transaction with either commit() or rollback().
    con.commit()

except mdb.Error, e:
    if con:
        con.rollback()

    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

finally:
    if con:
        con.close()

