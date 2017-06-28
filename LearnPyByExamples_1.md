# 看例子，学 Python（一）

很难说，这篇代码比文字还多的文章，是否适合初学者。
它源于个人笔记，涉及的多是简单核心的概念，也许需要一些编程基础才能快速理解。
内容方面，力求循序渐进，避开细枝末节，注重原理和示例的连续性，尽量不罗列特性，点到即止。

**说明：本文仅限于 Python 3。**

## Hello, Python!

从 `Hello, Python!` 开始，通过一系列不同实现，简单介绍字符串、函数等概念。

### 第一版

```python
print("Hello, Python!")
```

`print` 是一个内置函数；在 Python 2 里，`print` 是一个语句（statement）。
字符串由引号表示，这一点与其它语言类似。
语句末尾不需要结尾符（比如 C 系列语言的分号）。

### 第二版

```python
print("Hello, " + "Python!")
print("Hello, " * 3 + "Python!")
```

字面字符串即为对象。
操作符 `+` 和 `*` 都对字符串做了重载。

### 第三版

```python
print('Hello, "Python"!')
```

字符串可以用双引号，也可以用单引号。顺带也可看出 Python 并没有字符类型（char）。
通过单、双引号的恰当使用，可以避免不必要的字符转义（escape）。上例若改用双引号，则里面的 `"` 就需要转义了：
```python
print("Hello, \"Python\"!")
```

### 第四版

```python
def say_hello():
    print('Hello, Python!')
```

函数定义由 `def` 关键字指定。
函数的命名习惯上为小写下划线（`xxx\_yyy\_zzz`），变量名也是，类名则是驼峰状（`XxxYyyZzz`）。
Python 以【缩进】组织代码块，没有 C 系列语言的花括号，也没有 Ruby 那样的 `end` 语句。
使用缩进的优点是，代码风格比较单一，也就比较统一，没有诸如 `{` 是否另起一行的争论；缺点是无法自动缩进，不但给编辑器出了难题，也使代码分享变得相对困难，因为缩进一变，程序就不对了。

## Python 概览

对应于官方教程第三章。
简单介绍字符串、列表等概念，为后续内容做准备。

### 字符串

下面由 `>>>` 打头的代码，表示是在交互模式下的演示。
打开命令行，键入 python，即可进入交互模式。

```
>>> s = "Hello!"
>>> s
'Hello!'
```

#### 内建函数 len

字符串并没有方法（size 或 length）返回长度，取而代之的是内建函数 `len`：
```
>>> len("Hello!")
6
```
其它序列类型（sequence type）也是如此。

#### 遍历

作为一种序列类型，字符串可以直接用 `for` 遍历。
```
>>> for c in "Hello!": print(c)
...
H
e
l
l
o
!
```
注意这里的变量 `c`，虽然表示的是单个字符，其实却是字符串。前面已经说过，Python 没有字符类型。

#### 类型

通过几个内建函数，在交互模式下做一些试验。

函数 `type`：查看对象类型：
```
>>> type("Hello!")
<type 'str'>
```

函数 `help`：查看类型或函数的帮助信息：
```
>>> help(str)
Help on class str in module builtins:

class str(object)
 |  str(object='') -> str
<省略>
```

查看 `help` 自己的帮助信息：
```
>>> help(help)
Help on _Helper in module _sitebuiltins object:
<省略>
```

函数 `dir`：列出类的属性：
```
>>> dir(str)
['__add__', '__class__', '__contains__', <省略>]
```

不妨看看 `dir` 又是什么：
```
>>> help(dir)
Help on built-in function dir in module builtins:
<省略>
```

类型之间可以比较：
```
>>> type("hello") == str
True
```
但是一般不这么用，一般用 `isinstance`，因为后者会考虑到类的继承关系：
```
>>> isinstance("hello", str)
True
```

不出意外，类型自身也有类型：
```
>>> type(str)
<class 'type'>
```

这几个内建函数，非常称手，后面会经常用到。

#### 不可变性

尝试像 C/C++ 那样对单个字符赋值：
```
>>> s = "Hello!"
>>> s[-1] = '.'  # -1 表示倒数第一个（也即最后一个）字符的下标
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'str' object does not support item assignment
```
错误信息显示：`str` 对象不支持元素赋值。

方法 `replace` 也一样，不会改变原来的字符串，而是返回一个替换后的新字符串：
```
>>> help(str.replace)

replace(...)
    S.replace(old, new[, count]) -> string

    Return a copy of string S with all occurrences of substring
    old replaced by new.  If the optional argument count is
    given, only the first count occurrences are replaced.
```

```python
>>> s = "Hello!"
>>> s.replace('!', '.')
"Hello."
>>> s
"Hello!"  # 原对象并没有改变
```

### 列表

列表（list）是最常用的数据结构，类似于 C++ 的 `std::vector`。

#### 定义

```
>>> squares = [1, 4, 9, 16, 25]
>>> squares
[1, 4, 9, 16, 25]
>>> type(squares)
<class 'list'>
```

#### 索引

列表的底层实现并非链表（linked list），所以索引的性能还是不错的。
比较特别的地方在于，索引的下标可以为负数，比如前面提到 `-1` 表示倒数第一个元素。
```
>>> squares[0]
1
>>> squares[-1]
25
```

#### 切片

切片（slice）截取列表的一段。
```
>>> squares[1:4]
[4, 9, 16]
```
字符串也可以切片。
当然，切片返回新序列，原序列保持不变。

#### 拷贝

因为 Python 的对象是引用计数的，所以要拷贝一个列表，不能简单的赋值，但是可以用切片间接实现：
```
>>> squares[:]
[1, 4, 9, 16, 25]
```
不指定起始和结束下标，就切片整个列表。相当于 `squares[0:]` 或 `squares[0:len(squares)]`。

#### 拼接

拼接两个列表，直接相加即可。
```
>>> squares + [36, 48]
[1, 4, 9, 16, 25, 36, 48]
```
如前所述，Python 有操作符重载的概念，与 C++ 不无相似之处。

#### 可变性

与字符串不同，列表是可变的，可以被修改。
```
>>> squares[6] = 49
>>> squares.append(64)
>>> squares.pop()
49
>>> squares
[1, 4, 9, 16, 25, 36]

```

## 编程初步

以「斐波那契数列」为例，介绍基本的控制语句、函数定义。

### 斐波那契数列

```
0, 1, 1, 2, 3, 5, 8, ...
a  b
   a, b
      a, b
```

### 交互模式下的演示

打印 100 以内的数列：
```
>>> a, b = 0, 1
>>> while a < 100:
...     print(a, end='')
...     a, b = b, a+b
...
0 1 1 2 3 5 8 13 21 34 55 89 >>>
```

以下几点值得一提：
- Python 支持多变量赋值（multiple assignment），比如 `a, b = 0, 1`，可以简化代码，更让 swap 操作变得异常简单：`a, b = b, a`。
- `while` 语句与其它语言类似。
- `print` 函数指定 `end` 参数为空就不再换行了，`end` 缺省为 `'\n'`。

### 函数定义

函数由关键字 `def` 定义。
把刚才写在交互模式下代码，封装成 `fib` 函数，并移到文件 `mymath.py` 中：
```python
def fib(n):
    "Print a Fibonacci series up to n."

    a, b = 0, 1
    while a < n:
        print(a, end='')
        a, b = b, a+b
```
那么，`mymath` 就是一个模块（module）。
关于模块，Python 是这样定义的：
> A module is a file containing Python definitions and statements.

### 函数对象

对于模块，我们暂时先不做深究，知道通过 `import` 语句来使用即可，就好像 Java 的 `import` 或 C++ 的 `#include` 一样。
```
>>> import mymath
>>> mymath.fib
<function fib at 0x7fd1d6ec25f0>
>>> mymath.fib(100)
0 1 1 2 3 5 8 13 21 34 55 89
>>> fib = mymath.fib
>>> fib(100)
0 1 1 2 3 5 8 13 21 34 55 89
```
函数也是对象，可以赋值给变量，作为参数传递。这比 C/C++ 里的函数指针更强大。

### 文档字符串 (docstring)

前面定义 `fib` 时，函数体前有一个字符串：`Print a Fibonacci series up to n`，不知道你注意没有？
它就是文档字符串，既可以充当注释，又是函数对象的一部分，你可以通过属性 `__doc__` 访问：
```
>>> fib.__doc__
'Print a Fibonacci series up to n.'
```
文档字符串的功能不言而喻，它为函数 `help` 提供了萃取信息的通道。
```
>>> help(fib)
Help on function fib in module mymath:

fib(n)
    Print a Fibonacci series up to n.
```
如果文档字符串有多行，可以使用三重引号的字符串：
```python
def fib(n):
    """Print a Fibonacci series up to n.
    E.g., fib(10) prints:
        0 1 1 2 3 5 8
    """
```

### 函数返回值

只要是函数，都有返回值，没有明确指定返回值的，就返回 `None`。
`None` 是 Python 的空值，相当于 C++ 的 `NULL` 或 Java 的 `null`。
```
>>> fib(0)
>>> print(fib(0))
None
```

### 让 fib 返回列表

直接打印结果的函数，并不是一个好的设计，对于 `fib` 来说，把结果以列表返回要实用得多。

```python
def fib(n):
    result = []
    a, b = 0, 1
    while a < n:
        result.append(a)
        a, b = b, a+b
    return result
```

### 另一种实现

改写 `fib` 函数，返回数列中的第 N 个数。

```python
def fib(n):
    a, b = 0, 1
    if n <= 0:
        return 0
    if n == 1:
        return 1
    while n > 1:
        a, b = b, a+b
        n -= 1
    return b
```

Python 的 `if else` 缩写为 `elif`。
Python 没有 `++` 或 `--` 操作符，但是有 `+=` 和 `-=`。

### 递归版

递归和循环比较，递归易理解，循环更高效。

```python
def fib(n):
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return fib(n-1) + fib(n-2)
```

### 阶乘（练习）

各位可以暂停一下，拿阶乘（factorial）练练手，下面先给出轮廓：
```python
def fac(n):
    """ ...
    >>> fac(4)
    24
    """
    pass
```
`pass` 是占位符，用来标记空代码块，纯粹为了通过“编译”。

参考实现：
```python
def fac(n):
    """C-style implementation"""
    result = 1
    while n > 1:
        result = result * n
        n -= 1
    return result
```

### 使用 range 实现阶乘

`range` 表示一段范围，比如 `range(2, n)` 就表示从 `2` 一直到 `n-1`（不包括 `n`）。
```python
def fac(n):
    result = 1
    for i in range(2, n+1):
        result *= i
    return result
```

### for

回到前面遍历字符串的演示：
```
>>> s = "Hello!"
>>> for c in s: print(c)
```

如果需要索引，用 `enumerate`：
```
>>> for i, c in enumerate(s):
...     print("s[{}] = {}".format(i, c))
...
s[0] = H
s[1] = e
s[2] = l
s[3] = l
s[4] = o
s[5] = !
```

用 `range` 也能达到目的：
```
>>> for i in range(len(s)):
...     print("s[{}] = {}".format(i, c))
```

### range

再看几个 `range` 的例子：
```
>>> range(10)  # 起点默认为 0
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> range(0, 10)
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> range(0, 10, 3)  # 步长为 3
[0, 3, 6, 9]
```

最后再来看一下 `range` 的帮助信息：
```
>>> help(range)

range(...)
    range(stop) -> list of integers
    range(start, stop[, step]) -> list of integers
    <省略>
```

如前所述，函数 `help` 是非常称手的。
