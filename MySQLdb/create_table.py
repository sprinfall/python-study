# coding: utf-8

import MySQLdb as mdb

con = mdb.connect('localhost', 'root', 'chopin', 'test')

with con:
    cur = con.cursor()
    cur.execute('drop table if exists writers')
    cur.execute('create table writers(id int primary key auto_increment,\
            name varchar(25)) default charset utf8')
    cur.execute('insert into writers(name) values("Jack London")')
    cur.execute('insert into writers(name) values("Honore de Balzac")')
    cur.execute('insert into writers(name) values("Lion Feuchtwanger")')
    cur.execute('insert into writers(name) values("Emile Zola")')
    cur.execute('insert into writers(name) values("Truman Capote")')
    cur.execute('insert into writers(name) values("曹雪芹")')
