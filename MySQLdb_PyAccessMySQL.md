**环境**：MySQL 5.6.27, Ubuntu 15.10 64-bit

个人笔记，可读性较差。寻教程请移步：[MySQL Python tutorial][1]

**官方简介**
> MySQLdb is an thread-compatible interface to the popular MySQL
> database server that provides the Python database API.

## 安装

### 通过 pip 安装

```
$ apt-get install python-dev libmysqlclient-dev
$ pip install MySQL-python
```
详见：[How to install Python MySQLdb module using pip?][2]

### 通过 apt 安装
```
$ sudo apt-get install python-mysqldb
```

## 模块 _mysql

MySQLdb 安装好后，有两个模块或方式可用。模块 `_mysql` 提供的是类似于 MySQL C 接口的 API，而模块 `MySQLdb` 在 `_mysql` 基础上又做了进一步封装，使之符合 Python 的数据库 API 规范。推荐使用后者。

使用 `_mysql` 的例子：
```python
import _mysql
import sys

try:
    con = _mysql.connect('localhost', 'root', '******', 'test')

    con.query('select version()')
    result = con.use_result()

    print 'MySQL version: %s' % result.fetch_row()[0]

except _mysql.Error, e:
    print 'Error %d: %s' % (e.args[0], e.args[1])
    sys.exit(1)

finally:
    if con:
        con.close()
```

改用 `MySQLdb`：
```python
import MySQLdb as mdb
import sys

try:
    con = mdb.connect('localhost', 'root', '******', 'test')

    cur = con.cursor()
    cur.execute('select version()')

    ver = cur.fetchone()

    print 'MySQL version: %s' % ver

except mdb.Error, e:
    print 'Error %d: %s' % (e.args[0], e.args[1])
    sys.exit(1)

finally:
    if con:
        con.close()
```

## 创建表，插入数据
 
```python
# coding: utf-8

import MySQLdb as mdb

con = mdb.connect('localhost', 'root', '******', 'test')

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
```

## 查询

### 一次取回所有结果：`fetchall`
```python
import MySQLdb as mdb

con = mdb.connect('localhost', 'root', '******', 'test')

with con:
    cur = con.cursor()
    cur.execute('select * from writers')

    # 结果集 rows 为元组（tuple）的元组，每一个元组代表了表中的一行。
    rows = cur.fetchall()
    for row in rows:
        print row
```

### 挨个取回结果：`fetchone`
```python
import MySQLdb as mdb

con = mdb.connect('localhost', 'root', '******', 'test')

with con:
    cur = con.cursor()
    cur.execute('select * from writers')

    for i in range(cur.rowcount):
        row = cur.fetchone()
        print row
```

### 使用字典 Cursor
```python
import MySQLdb as mdb

con = mdb.connect('localhost', 'root', '******', 'test')

def test_dict_cursor():
    with con:
        cur = con.cursor(mdb.cursors.DictCursor) # 字典 cursor
        cur.execute('select * from writers limit 4')

        # rows 为字典的元组
        rows = cur.fetchall()
        for row in rows:
            print row['id'], row['name'] # 通过列名访问结果
```

### 打印列名

```python
import MySQLdb as mdb

con = mdb.connect('localhost', 'root', '******', 'test')

with con:
    cur = con.cursor()
    cur.execute('select * from writers limit 4')

    rows = cur.fetchall()
        
    # 元组的元组，每一个元组对应一个结果列，元组的第一个元素为列名。
    desc = cur.description

    # 打印前两个结果列的列名。
    print '%s %3s' % (desc[0][0], desc[1][0])

    for row in rows:
        print '%2s %3s' % row
```

## Prepared Statements

Prepared Statements 可以提高安全性和性能，特别是对于多次重复执行的查询。Python 的数据库 API 规范建议了 5 种不同的方式来构造 Prepared Statements，MySQLdb 只支持其中的一种，代码类似于 `ANSI printf` 的格式化操作。

Prepared Statements 在 ORM 库（比如 SQLAlchemy）中应该会有更完善的支持。

**注（2016-01-10）：**
这里的 Prepared Statements 只是客户端的模拟，跟 MySQL Server 的 Prepared Statements 是两码事，所以并不能提高性能或安全性。（详见 [C API Prepared Statements][3]）

```python
import MySQLdb as mdb

con = mdb.connect('localhost', 'root', '******', 'test')

with con:
    cur = con.cursor()

    cur.execute("update writers set name = %s where id = %s",
            ("Guy de Maupasant", "4"))

    print "Number of rows updated:", cur.rowcount
```

## 事务

前面的例子一直使用 `with` 语句来管理链接 (connection) 对象，避免了 `commit` 的直接调用。

一旦 cursor 创建，一个事务也就开始，结束时必须调用 `commit` 或 `rollback`。`commit` 提交修改，`rollback` 回滚。如果结合 `with` 语句使用的话，`commit` 和 `rollback` 都将自动完成，因为 MySQLdb 的链接对象可以当作 context manager 使用。

```python
# coding: utf-8

import MySQLdb as mdb

try:
    con = mdb.connect('localhost', 'root', '******', 'test')

    # Cursor 创建，事务开始。
    cur = con.cursor()

    cur.execute('drop table if exists writers')
    # MyISAM doesn't support transaction.
    cur.execute('create table writers(id int primary key auto_increment,\
            name varchar(25)) engine=innodb')

    cur.execute('insert into writers(name) values("Jack London")')
    cur.execute('insert into writers(name) values("Honore de Balzac")')
    cur.execute('insert into writers(name) values("Lion Feuchtwanger")')
    cur.execute('insert into writers(name) values("Emile Zola")')
    cur.execute('insert into writers(name) values("Truman Capote")')

    # 显式地调用 commit 来结束一个事务。
    con.commit()

except mdb.Error, e:
    # 异常发生时，调用 rollback 进行回滚。
    if con:
        con.rollback()

    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

finally:
    if con:
        con.close()
```

## Cursor 有必要 close 吗？

原则上讲，不需要显式地调用 cursor 对象的 `close` 方法，因为当 cursor 对象生命期结束时，`close` 方法会被自动调用。源码如下：

```python
class BaseCursor(object):
    def __del__(self):
        self.close()
        self.errorhandler = None
        self._result = None
```

不过，还是建议主动调用 `close`，这样至少代码的行为更加明显。


  [1]: http://zetcode.com/db/mysqlpython/
  [2]: http://stackoverflow.com/questions/25865270/how-to-install-python-mysqldb-module-using-pip
  [3]: http://dev.mysql.com/doc/refman/5.6/en/c-api-prepared-statements.html