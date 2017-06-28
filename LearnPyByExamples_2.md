# 看例子，学 Python（二）

## 模块

文件 `mymath.py` 定义了函数 `fib` 和 `fac`，`mymath.py` 就是一个模块。

> A module is a file containing Python definitions and statements.

### 自定义模块

导入模块：
```
>>> import mymath
```
`mymath.py` 须在当前目录。

查看模块帮助：
```
>>> help(mymath)
Help on module mymath:

NAME
    mymath

FUNCTIONS
    fib(n)
...
```
列出模块属性：
```
>>> dir(mymath)
['__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'fac', 'fib']
```
访问模块属性：
```
>>> mymath.__name__
'mymath'
>>> mymath.__doc__
>>>
```
模块暂时还没有 `docstring`，所以 `mymath.__doc__` 为空。
访问函数属性：
```
>>> mymath.fac
<function fac at 0x00000000026DBA60>
>>> mymath.__dict__['fac']
<function fac at 0x00000000026DBA60>
```
两种方式效果一样。`__dict__`（字典）隐含于每个对象中，模块对象也不例外。

为模块 `mymath` 添加 `docstring`：
```python
"""My math utilities."""

def fib(n):
    ...
```
那么，下次调用 `help` 就能显示这个 `docstring` 了：
```
>>> help(mymath)
Help on module mymath:

NAME
    mymath - My math utilities.
...
```

### 内建模块

Python 自带了 `math` 模块，来研究一下：
```
>>> import math
>>> help(math)
Help on built-in module math:

NAME
    math
...
```
列出属性：
```
>>> dir(math)
['__doc__', '__loader__', ..., 'factorial', ...]
```
可见内建模块 `math` 也提供了阶乘（factorial），看看它怎么用：
```
>>> help(math.factorial)
Help on built-in function factorial in module math:

factorial(...)
    factorial(x) -> Integral

    Find x!. Raise a ValueError if x is negative or non-integral.
```
调用试试：
```
>>> math.factorial(4)
24
>>> math.factorial(-1)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: factorial() not defined for negative values
>>>
```
内建函数在异常处理方面做得会比较好。
值得注意的是，内建模块并不一定由 Python 文件定义，比如 Python 的安装目录下其实并没有 `math.py`。

## doctest

顾名思义，`docstring` 里嵌测试用例，就是 `doctest`。
好处是，既可做文档又可做测试，也避免了注释里的示例代码失效的问题。
为 `fac` 添加 `doctest`：
```python
def fac(n):
    """
    >>> fac(4)
    24
    """
    ...
```
这就像交互环境下的输入输出一样。`>>>` 打头的是输入，紧接着的便是输出。
下面来运行试试：
```
$ python -m doctest -v mymath.py
Trying:
    fac(4)
Expecting:
    24
ok
2 items had no tests:
    mymath
    mymath.fib
1 items passed all tests:
   1 tests in mymath.fac
1 tests in 3 items.
1 passed and 0 failed.
Test passed.
```
`-m` 指定使用 Python 的内建模块 `doctest`，`-v` 表示显示详细信息。
这只是运行 `doctest` 的方式之一，还可以添加代码到 `mymath.py` 的 `main` 函数：
```python
if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
```
后续就不必指定命令行参数 `-m` `-v` 了。

作为练习，我们可以为 `fib` 添加 `doctest`：
```python
def fib(n):
    """Get the nth Fibonacci number.

    >>> fib(0)
    0
    >>> fib(1)
    1
    >>> fib(2)
    1
    >>> fib(6)
    8
    """
   ...
```

## 字典

对应于官方教程 [5.5. Dictionaries][3]。
前面介绍模块时，提到了对象的特殊属性 `__dict__` ，它其实就是一个字典（dict）。
Python 的字典，类似于 C++ 或 Java 的 `map`，是存储键值映射关系的一种数据结构。我们且不去关心它的实现细节，是平衡二叉树还是哈希表，目前并不重要。

### Char Counter

第一个例子，实现函数 `char_counter`，以字典的形式，返回字符串中每个字符出现的次数。
函数的 `doctest` 已经写出来了，你只要让它通过即可。
```python
def char_counter(chars):
    """Count the number of each character.

    >>> d = char_counter('banana')
    >>> d['a']
    3
    >>> d['b']
    1
    >>> d['n']
    2
    """
    pass
```

#### 第一版
```python
def char_counter(chars):
    counter = {}  # 初始化为空字典
    for c in chars:
        counter[c] += 1  # KeyError!
    return counter
```
`counter[c] += 1` 一句将引发 `KeyError` 异常，因为它没有考虑字典中键不存在的情况。

#### 第二版
```python
def char_counter(chars):
    counter = {}
    for c in chars:
        if c in counter:
            counter[c] += 1
        else:
            counter[c] = 1
    return counter
```
此版处理了键不存在的问题，但是 `if...else` 总归显得不够优雅，Python 是一门简洁优雅的语言，应该有更好的方法。

#### 第三版
```python
def char_counter(chars):
    counter = {}
    for c in chars:
        counter[c] = counter.get(c, 0) + 1
    return counter
```
通过字典的 `get` 方法，保证当键不存在时，也能得到妥善初始化了的值。

### Word Counter

Word Counter 与 Char Counter 类似，以字典形式返回一段文本中每个单词出现的次数。

给定一段文本如下：
```python
text = """Remember me when I am gone away,
Gone far away into the silent land;
When you can no more hold me by the hand,
Nor I half turn to go yet turning stay.
Remember me when no more day by day
You tell me of our future that you plann'd:
Only remember me; you understand
It will be late to counsel then or pray.
Yet if you should forget me for a while
And afterwards remember, do not grieve:
For if the darkness and corruption leave
A vestige of the thoughts that once I had,
Better by far you should forget and smile
Than that you should remember and be sad."""
```

首先通过 `str.split` 把 `text` 分割成单词的列表，然后计数的过程就跟 Char Counter 一样了，各位可以当做练习。

不难发现，Char Counter 和 Word Counter 在算法上有相似的地方，所以 Python 其实已经提供了这样一个算法。
```
>>> import collections
>>> help(collections.Counter)
Help on class Counter in module collections:

class Counter(builtins.dict)
 |  Dict subclass for counting hashable items.  Sometimes called a bag
 |  or multiset.  Elements are stored as dictionary keys and their counts
 |  are stored as dictionary values.
...
```
根据帮助信息，`Counter` 是一个类，并且继承自 `dict`。姑且跳过类定义的语法，篇幅所限。
使用 `collections.Counter`：
```python
from collections import Counter
counter = Counter(text.split())
print(counter['you'])  # 6
```

既然继承自字典，`Counter` 必定提供了一些额外的方法，比如获取出现频率最高的几个键值对：
```python
print(counter.most_common(3))
# [('you', 6), ('me', 5), ('the', 4)]
```
这就涉及了一个对字典以值来排序的问题。
怎么对字典以值来排序呢？确实有几种方式，下面以 Char Counter 为例。

### 使用 dict.get

首先，排序用 `sorted`。
```
>>> help(sorted)
...
sorted(iterable, key=None, reverse=False)
```
输入是一个 `iterable`，可以用 `for` 迭代的便是 `iterable` 的，字典当然也是。
但是如果直接对字典排序，便是以键来排序：
```python
counter = char_counter('banana')
print(sorted(counter))
# ['a', 'b', 'n']
```
为了以值来排序，可以为 `sorted` 指定 `key`：
```python
counter = char_counter('banana')
print(sorted(counter, key=counter.get))
# ['b', 'n', 'a']
```
这样 `sorted` 在比较时，就不是比较键，而是比较 `counter.get(键)`。
然而这样的排序结果并不是我们想要的，因为它只有键而没有值。

### 使用 itemgetter

字典的 `items` 方法返回「键值对」列表，我们可以对这个列表按值排序。
```python
print(counter.items())
# dict_items([('b', 1), ('a', 3), ('n', 2)])
```
这个列表里的每个元素都是一个键值对，由元组（tuple）表示。元组相当于只读的列表，后面会有介绍。
```python
from operator import itemgetter
print(sorted(counter.items(), key=itemgetter(1)))
# [('b', 1), ('n', 2), ('a', 3)]
```
指定 `sorted` 的 `key` 为 `itemgetter(1)`，便以每个键值对元组下标为 1 的元素进行排序。

最后，不妨来看一下 `dict.items` 的帮助：
```
>>> help(dict.items)

items(...)
    D.items() -> list of D's (key, value) pairs, as 2-tuples
```

### 使用 lambda

除了 `itemgetter`，还可以用 `lambda`。
简单来说，`lambda` 就是匿名函数（没有名字的函数），短小精悍，临时创建临时使用，一般作为参数传递，没必要有名字。

方式一：
```python
sorted(counter.items(), key=lambda x: x[1])
```
`x` 为键值对元组。

方式二：
```python
sorted(counter.items(), key=lambda (k,v): v)
```
直接在参数上把元组展开。

方式三：
```python
sorted(counter.items(), key=lambda (k,v): (v,k))
```
交互键值顺序，元组在比较时，依次比较里面的每个元素。

### 降序排序

降序排序，只需指定 `reverse` 参数即可：
```python
sorted(counter.items(), key=itemgetter(1), reverse=True)
```

## 元组

元组（tuple）是只读的列表，虽然在底层实现上有很大不同。

```
>>> a = (1, "hello")
>>> a[0]
1
>>> a[0] = 2
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'tuple' object does not support item assignment
```

可将其它序列类型（str, list）转换成元组：
```
>>> s = tuple("abcde")
>>> s
('a', 'b', 'c', 'd', 'e')
```
