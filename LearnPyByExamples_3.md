# 看例子，学 Python（三）

## 包

创建一个目录 `myutil`，把 `mymath.py` 挪到里面，再添加一个空文件 `__init__.py`：
```
myutil/
    __init__.py
    mymath.py
```
`myutil` 便是一个包（package）。

### import

最直接的用法：
```
>>> import myutil.mymath
>>> myutil.mymath.fac(4)
24
```
缺点是调用 `fac` 时太长，包和模块作为前缀都要写全。但是写成 `import myutil.mymath.fac` 也是不对的。
通过 `import` 的语法（syntax）：
```
import <包>.<包>.<包|模块>
```
可以看出：
- 最后一项（item）可以是包也可以是模块，前面的必须是包；
- 最后一项不可以是类、函数或变量的定义。

根据语法来看，可以 import 一个包：
```
>>> import myutil
>>> help(myutil)
...
```
但是这样并没有什么实际用处，因为无法就此调用具体的函数（类、变量）：
```
>>> myutil.mymath.fac(4)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: module 'myutil' has no attribute 'mymath'
```

### from...import

如果要避免调用时带着一串前缀，可以用 `from...import`：
```
>>> from myutil.mymath import fac
>>> fac(4)  # 不再需要前缀
24
```
一次 import 多个时以逗号分割：
```
>>> from myutil.mymath import fib, fac
```
一次 import 所有：
```
>>> from myutil.mymath import *
```

`from...import...` 避免了前缀，但是也污染了名字，使用时需权衡。

## 高阶函数

高阶函数（higher-order）就是操作或返回其它函数的函数。
下面是几个经典的高阶函数，其它稍微函数式一点的语言里一般也有。

## reduce（规约）

用 `reduce` 重写阶乘：
```python
import operator, functools
def fac(n):
    return functools.reduce(operator.mul, range(1, n+1))
```

用 `reduce` 求和:
```python
def sum(n):
    return functools.reduce(operator.add, range(1, n+1))
```

Python 的 `reduce` 就相当于 C++ 的 `accumulate`（C++17 已经新增 `reduce`）。
```cpp
std::vector<int> v{1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
int sum = std::accumulate(v.begin(), v.end(), 0);  // 求和
int product = std::accumulate(v.begin(), v.end(), 1, std::multiplies<int>());  // 求积
```

## map（映射）

```
>>> list(map(bool, [None, 0, "", u"", list(), tuple(), dict(), set(), frozenset()]))
[False, False, False, False, False, False, False, False, False]
```
None、0、空字符串、以及没有元素的容器对象都可视为 `False`，反之为 `True`。

## filter（过滤）

```
>>> list(filter(bool, [None, 0, "", 1]))
[1]
```

## 数据模型

### == vs. is

`==` 判断值是否相等，`is` 判断两个变量是否为同一个对象。
这就好像 Java 里的 `==` 和 `equals` 一样。
下面是一些例子：
```
>>> a, b = 1, 1
>>> a == b
True
>>> a is b
True
```
`a == b` 比较好理解，`a is b` 是因为 Python 对整数做了优化，`a` 和 `b` 都指向同一个预先分配的对象（其值为 1）。
可以理解为 `is` 比较的是对象的内存地址。
内建函数 `id()` 返回对象的唯一标识，可以理解为内存地址。
```
>>> id(a), id(b)
(35169392, 35169392)
```
甚至可以拿到一个对象的引用计数（reference count）：
```
>>> import sys
>>> sys.getrefcount(a)
99
>>> sys.getrefcount(b)
99
```
引用计数为 99 有点意外，其实是因为很多装载的内建模块都用到了整数 1。
不妨看看其它整数如何：
```
>>> sys.getrefcount(0)
169
>>> sys.getrefcount(255)
4
```

对 Python 来说，变量只是名字，它的类型和值取决于它所绑定的对象。我们可以把 `a` `b` 绑定到其它对象：
```
>>> a, b = "hello", "hello"
>>> a is b
True
```
同样，`a is b` 是因为 Python 对字符串做了优化。

值得一提的是，这种优化（也即引用计数）可能只针对 CPython，对于 Python 的其它实现可能就不是这样了。你的程序不该依赖于这些特定于解释器的实现。

整数和字符串有一个共同点，即它们都是不可变的（immutable），现在来看看可变对象，比如列表：
```
>>> c, d = [a, b], [a, b]
>>> c == d
True
>>> c is d
False
```
可见虽然 `c` 和 `d` 具有相等的值，但对象是不同的两个。

这些就是 Python 的数据模型（Data Model），虽然不是全部。

### 对象

Python 的每一个对象（object）都有以下三个部分：
- 身份（identity）
- 类型（type）
- 值（value）

身份：
- 不可改变（unchangeable）（一旦对象创建了就不会改变）
- 对应于内存地址
- 通过操作符 `is` 进行比较: a is b
- 函数 `id()` 返回对象唯一的整形标识（内存地址)

类型：
- 不可改变（unchangeable）
- 函数 `type()` 返回对象类型

值：
- 可变的（mutable）：字典，列表
- 不可变的（immutable）：数字，字符串，元组

最后，对象不会被显式地销毁（explicitly destroyed）。
对 CPython 来说，对象由引用计数管理，计数为 0 时对象会自动销毁。

### 练习

最后留一道练习。

给定：
```
>>> c = []
>>> d = []
>>> c is d
False
```
请问：
```
>>> e = f = []
>>> e is f
???
```
