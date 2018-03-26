# 浅析 Python 的类、继承和多态

## 类的定义

假如要定义一个类 `Point`，表示二维的坐标点：
```python
# point.py
class Point:
    def __init__(self, x=0, y=0):
        self.x, self.y = x, y
```
最最基本的就是 `__init__` 方法，相当于 C++ / Java 的构造函数。带双下划线 `__` 的方法都是特殊方法，除了 `__init__` 还有很多，后面会有介绍。

参数 `self` 相当于 C++ 的 `this`，表示当前实例，所有方法都有这个参数，但是调用时并不需要指定。
```
>>> from point import *
>>> p = Point(10, 10)  # __init__ 被调用
>>> type(p)
<class 'point.Point'>
>>> p.x, p.y
(10, 10)
```
几乎所有的特殊方法（包括 `__init__`）都是隐式调用的（不直接调用）。

对一切皆对象的 Python 来说，类自己当然也是对象：
```
>>> type(Point)
<class 'type'>
>>> dir(Point)
['__class__', '__delattr__', '__dict__', ..., '__init__', ...]
>>> Point.__class__
<class 'type'>
```
`Point` 是 `type` 的一个实例，这和 `p` 是 `Point` 的一个实例是一回事。

现添加方法 `set`：
```python
class Point:
    ...
    def set(self, x, y):
        self.x, self.y = x, y
```
```
>>> p = Point(10, 10)
>>> p.set(0, 0)
>>> p.x, p.y
(0, 0)
```
`p.set(...)` 其实只是一个语法糖，你也可以写成 `Point.set(p, ...)`，这样就能明显看出 `p` 就是 `self` 参数了：
```
>>> Point.set(p, 0, 0)
>>> p.x, p.y
(0, 0)
```

值得注意的是，`self` 并不是关键字，甚至可以用其它名字替代，比如 `this`：
```python
class Point:
    ...
    def set(this, x, y):
        this.x, this.y = x, y
```
与 C++ 不同的是，“成员变量”必须要加 `self.` 前缀，否则就变成类的属性（相当于 C++ 静态成员），而不是对象的属性了。

### 访问控制

Python 没有 `public / protected / private` 这样的访问控制，如果你非要表示“私有”，习惯是加双下划线前缀。
```python
class Point:
    def __init__(self, x=0, y=0):
        self.__x, self.__y = x, y

    def set(self, x, y):
        self.__x, self.__y = x, y

    def __f(self):
        pass
```
`__x`、`__y` 和 `__f` 就相当于私有了：
```
>>> p = Point(10, 10)
>>> p.__x
...
AttributeError: 'Point' object has no attribute '__x'
>>> p.__f()
...
AttributeError: 'Point' object has no attribute '__f'
```

### \_\_repr__

尝试打印 `Point` 实例：
```
>>> p = Point(10, 10)
>>> p
<point.Point object at 0x000000000272AA20>
```
通常，这并不是我们想要的输出，我们想要的是：
```
>>> p
Point(10, 10)
```
添加特殊方法 `__repr__` 即可实现：
```python
class Point:
    def __repr__(self):
        return 'Point({}, {})'.format(self.__x, self.__y)
```
不难看出，交互模式在打印 `p` 时其实是调用了 `repr(p)`：
```
>>> repr(p)
'Point(10, 10)'
```

### \_\_str__

如果没有提供 `__str__`，`str()` 缺省使用 `repr()` 的结果。
这两者都是对象的字符串形式的表示，但还是有点差别的。简单来说，`repr()` 的结果面向的是解释器，通常都是合法的 Python 代码，比如 `Point(10, 10)`；而 `str()` 的结果面向用户，更简洁，比如 `(10, 10)`。

按照这个原则，我们为 `Point` 提供 `__str__` 的定义如下：
```python
class Point:
    def __str__(self):
        return '({}, {})'.format(self.__x, self.__y)
```

### \_\_add__

两个坐标点相加是个很合理的需求。
```
>>> p1 = Point(10, 10)
>>> p2 = Point(10, 10)
>>> p3 = p1 + p2
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unsupported operand type(s) for +: 'Point' and 'Point'
```
添加特殊方法 `__add__` 即可做到：
```python
class Point:
    def __add__(self, other):
        return Point(self.__x + other.__x, self.__y + other.__y)
```
```
>>> p3 = p1 + p2
>>> p3
Point(20, 20)
```
这就像 C++ 里的操作符重载一样。
Python 的内建类型，比如字符串、列表，都“重载”了 `+` 操作符。

特殊方法还有很多，这里就不逐一介绍了。

## 继承

举一个教科书中最常见的例子。`Circle` 和 `Rectangle` 继承自 `Shape`，不同的图形，面积（`area`）计算方式不同。
```python
# shape.py

class Shape:
    def area(self):
        return 0.0
        
class Circle(Shape):
    def __init__(self, r=0.0):
        self.r = r

    def area(self):
        return math.pi * self.r * self.r

class Rectangle(Shape):
    def __init__(self, a, b):
        self.a, self.b = a, b

    def area(self):
        return self.a * self.b
```

用法比较直接：
```
>>> from shape import *
>>> circle = Circle(3.0)
>>> circle.area()
28.274333882308138
>>> rectangle = Rectangle(2.0, 3.0)
>>> rectangle.area()
6.0
```

如果 `Circle` 没有定义自己的 `area`：
```python
class Circle(Shape):
    pass
```
那么它将继承父类 `Shape` 的 `area`：
```
>>> Shape.area is Circle.area
True
```
一旦 `Circle` 定义了自己的 `area`，从 `Shape` 继承而来的那个 `area` 就被重写（`overwrite`）了：
```
>>> from shape import *
>>> Shape.area is Circle.area
False
```
通过类的字典更能明显地看清这一点：
```
>>> Shape.__dict__['area']
<function Shape.area at 0x0000000001FDB9D8>
>>> Circle.__dict__['area']
<function Circle.area at 0x0000000001FDBB70>
```
所以，子类重写父类的方法，其实只是把相同的属性名绑定到了不同的函数对象。可见 Python 是没有覆写（`override`）的概念的。

同理，即使 `Shape` 没有定义 `area` 也是可以的，`Shape` 作为“接口”，并不能得到语法的保证。

甚至可以动态的添加方法：
```python
class Circle(Shape):
    ...
    #  def area(self):
        #  return math.pi * self.r * self.r

# 为 Circle 添加 area 方法。
Circle.area = lambda self: math.pi * self.r * self.r
```
动态语言一般都是这么灵活，Python 也不例外。

Python 官方教程「9. Classes」第一句就是：
> Compared with other programming languages, Python’s class mechanism adds classes with a minimum of new syntax and semantics.

Python 以最少的新的语法和语义实现了类机制，这一点确实让人惊叹，但是也让 C++ / Java 程序员感到颇为不适。

### 多态

如前所述，Python 没有覆写（`override`）的概念。严格来讲，Python 并不支持「多态」。

为了解决继承结构中接口和实现的问题，或者说为了更好的用 Python 面向接口编程（设计模式所提倡的），我们需要人为的设一些规范。

请考虑 `Shape.area()` 除了简单的返回 `0.0`，有没有更好的实现？

以内建模块 `asyncio` 为例，`AbstractEventLoop` 原则上是一个接口，类似于 Java 中的接口或 C++ 中的纯虚类，但是 Python 并没有语法去保证这一点，为了尽量体现 `AbstractEventLoop` 是一个接口，首先在名字上标志它是抽象的（Abstract），然后让每个方法都抛出异常 `NotImplementedError`。
```python
class AbstractEventLoop:
    def run_forever(self):
        raise NotImplementedError
    ...
```

纵然如此，你是无法禁止用户实例化 `AbstractEventLoop` 的：
```python
loop = asyncio.AbstractEventLoop()
try:
    loop.run_forever()
except NotImplementedError:
    pass
```
C++ 可以通过纯虚函数或设构造函数为 `protected` 来避免接口被实例化，Java 就更不用说了，接口就是接口，有完整的语法支持。

你也无法强制子类必须实现“接口”中定义的每一个方法，C++ 的纯虚函数可以强制这一点（Java 更不必说）。

就算子类「自以为」实现了“接口”中的方法，也不能保证方法的名字没有写错，C++ 的 `override` 关键字可以保证这一点（Java 更不必说）。

静态类型的缺失，让 Python 很难实现 C++ / Java 那样严格的多态检查机制。所以面向接口的编程，对 Python 来说，更多的要依靠程序员的素养。

回到 `Shape` 的例子，仿照 `asyncio`，我们把“接口”改成这样：
```python
class AbstractShape:
    def area(self):
        raise NotImplementedError
```
这样，它才更像一个接口。

### super

有时候，需要在子类中调用父类的方法。

比如图形都有颜色这个属性，所以不妨加一个参数 `color` 到 `__init__`：
```python
class AbstractShape:
    def __init__(self, color):
        self.color = color
```
那么子类的 `__init__()` 势必也要跟着改动：
```python
class Circle(AbstractShape):
    def __init__(self, color, r=0.0):
        super().__init__(color)
        self.r = r
```
通过 `super` 把 `color` 传给父类的 `__init__()`。其实不用 `super` 也行：
```python
class Circle(AbstractShape):
    def __init__(self, color, r=0.0):
        AbstractShape.__init__(self, color)
        self.r = r
```
但是 `super` 是推荐的做法，因为它避免了硬编码，也能处理多继承的情况。


**另见：**
- https://segmentfault.com/a/1190000010046025
