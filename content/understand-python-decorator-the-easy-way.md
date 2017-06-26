---
title: 简单地理解Python的装饰器
date: 2017-06-26 01:00:00 +0800
slug: understand-python-decorator-the-easy-way
category: Python
tags: Python
keywords: Python, python decorator, python装饰器, 装饰器, 装饰器原理, python语法糖, python类, python 类 装饰器, functoos wraps, 链 装饰器, 装饰器 参数, 装饰器 可变参数
description: 用简单的方式轻松地理解Python的装饰器
---

Python有大量强大又贴心的特性，如果要列个最受欢迎排行榜，那么装饰器绝对会在其中。

刚接触装饰器，会觉得代码不多却难以理解。其实装饰器的语法本身挺简单的，复杂是因为同时混杂了其它的概念。下面我们一起抛去无关概念，简单地理解下Python的装饰器。

<!-- more -->

## 装饰器的原理

在解释器下跑个装饰器的例子，直观地感受一下。

```python
# make_bold就是装饰器，实现方式这里略去
>>> @make_bold
... def get_content():
...     return 'hello world'
...
>>> get_content()
'<b>hello world</b>'
```

被`make_bold`装饰的`get_content`，调用后返回结果会自动被`b`标签包住。怎么做到的呢，简单4步就能明白了。

### 1. 函数是对象

我们定义个`get_content`函数。这时`get_content`也是个对象，它能做所有对象的操作。

```python
def get_content():
    return 'hello world'
```

它有`id`，有`type`，有值。

```text
>>> id(get_content)
140090200473112
>>> type(get_content)
<class 'function'>
>>> get_content
<function get_content at 0x7f694aa2be18>
```

跟其他对象一样可以被赋值给其它变量。

```python
>>> func_name = get_content
>>> func_name()
'hello world'
```

它可以当参数传递，也可以当返回值

```python
>>> def foo(bar):
...     print(bar())
...     return bar
...
>>> func = foo(get_content)
hello world
>>> func()
'hello world'
```

### 2. 自定义函数对象

我们可以用`class`来构造函数对象。有成员函数`__call__`的就是函数对象了，函数对象被调用时正是调用的`__call__`。

```python
class FuncObj(object):
    def __init__(self, name):
        print('Initialize')
        self.name= name

    def __call__(self):
        print('Hi', self.name)
```

我们来调用看看。可以看到，**函数对象的使用分两步：构造和调用**(同学们注意了，这是考点)。

```python
>>> fo = FuncObj('python')
Initialize
>>> fo()
Hi python
```

### 3. `@`是个语法糖

装饰器的`@`没有做什么特别的事，不用它也可以实现一样的功能，只不过需要更多的代码。

```python
@make_bold
def get_content():
    return 'hello world'

# 上面的代码等价于下面的

def get_content():
    return 'hello world'
get_content = make_bold(get_content)
```

`make_bold`是个函数，要求入参是函数对象，返回值是函数对象。`@`的语法糖其实是省去了上面最后一行代码，使可读性更好。用了装饰器后，每次调用`get_content`，真正调用的是`make_bold`返回的函数对象。

### 4. 用类实现装饰器

入参是函数对象，返回是函数对象，如果第2步里的类的构造函数改成入参是个函数对象，不就正好符合要求吗？我们来试试实现`make_bold`。

```python
class make_bold(object):
    def __init__(self, func):
        print('Initialize')
        self.func = func

    def __call__(self):
        print('Call')
        return '<b>{}</b>'.format(self.func())
```

大功告成，看看能不能用。

```python
>>> @make_bold
... def get_content():
...     return 'hello world'
...
Initialize
>>> get_content()
Call
'<b>hello world</b>'
```

成功实现装饰器！是不是很简单？

这里分析一下之前强调的**构造**和**调用**两个过程。我们去掉`@`语法糖好理解一些。

```python
# 构造，使用装饰器时构造函数对象，调用了__init__
>>> get_content = make_bold(get_content)
Initialize

# 调用，实际上直接调用的是make_bold构造出来的函数对象
>>> get_content()
Call
'<b>hello world</b>'
```

到这里就彻底清楚了，完结撒花，可以关掉网页了~~~(如果只是想知道装饰器原理的话)

## 函数版装饰器

阅读源码时，经常见到用嵌套函数实现的装饰器，怎么理解？同样仅需4步。

### 1. `def`的函数对象初始化

用`class`实现的函数对象很容易看到什么时候**构造**的，那`def`定义的函数对象什么时候**构造**的呢？

```python
# 这里的全局变量删去了无关的内容
>>> globals()
{}
>>> def func():
...     pass
...
>>> globals()
{'func': <function func at 0x10f5baf28>}
```

不像一些编译型语言，程序在启动时函数已经构造那好了。上面的例子可以看到，执行到`def`会才构造出一个函数对象，并赋值给变量`make_bold`。

这段代码和下面的代码效果是很像的。

```python
class NoName(object):
    def __call__(self):
        pass

func = NoName()
```

### 2. 嵌套函数

Python的函数可以嵌套定义。

```python
def outer():
    print('Before def:', locals())
    def inner():
        pass
    print('After def:', locals())
    return inner
```

`inner`是在`outer`内定义的，所以算`outer`的局部变量。执行到`def inner`时函数对象才创建，因此每次调用`outer`都会创建一个新的`inner`。下面可以看出，每次返回的`inner`是不同的。

```text
>>> outer()
Before def: {}
After def: {'inner': <function outer.<locals>.inner at 0x7f0b18fa0048>}
<function outer.<locals>.inner at 0x7f0b18fa0048>
>>> outer()
Before def: {}
After def: {'inner': <function outer.<locals>.inner at 0x7f0b18fa00d0>}
<function outer.<locals>.inner at 0x7f0b18fa00d0>
```

### 3. 闭包

嵌套函数有什么特别之处？因为有闭包。

```python
def outer():
    msg = 'hello world'
    def inner():
        print(msg)
    return inner
```

下面的试验表明，`inner`可以访问到`outer`的局部变量`msg`。

```python
>>> func = outer()
>>> func()
hello world
```

闭包有2个特点

1. `inner`能访问`outer`及其祖先函数的命名空间内的变量(局部变量，函数参数)。
2. 调用`outer`已经返回了，但是它的命名空间被返回的`inner`对象引用，所以还不会被回收。

这部分想深入可以去了解Python的LEGB规则。

### 4. 用函数实现装饰器

装饰器要求入参是函数对象，返回值是函数对象，嵌套函数完全能胜任。

```python
def make_bold(func):
    print('Initialize')
    def wrapper():
        print('Call')
        return '<b>{}</b>'.format(func())
    return wrapper
```

用法跟类实现的装饰器一样。可以去掉`@`语法糖分析下**构造**和**调用**的时机。

```python
>>> @make_bold
... def get_content():
...     return 'hello world'
...
Initialize
>>> get_content()
Call
'<b>hello world</b>'
```

因为返回的`wrapper`还在引用着，所以存在于`make_bold`命名空间的`func`不会消失。`make_bold`可以装饰多个函数，`wrapper`不会调用混淆，因为每次调用`make_bold`，都会有创建新的命名空间和新的`wrapper`。

到此函数实现装饰器也理清楚了，完结撒花，可以关掉网页了~~~(后面是使用装饰的常见问题)

## 常见问题

### 1. 怎么实现带参数的装饰器？

带参数的装饰器，有时会异常的好用。我们看个例子。

```python
>>> @make_header(2)
... def get_content():
...     return 'hello world'
...
>>> get_content()
'<h2>hello world</h2>'
```

怎么做到的呢？其实这跟装饰器语法没什么关系。去掉`@`语法糖会变得很容易理解。

```python
@make_header(2)
def get_content():
    return 'hello world'

# 等价于

def get_content():
    return 'hello world'
unnamed_decorator = make_header(2)
get_content = unnamed_decorator(get_content)
```

上面代码中的`unnamed_decorator`才是真正的装饰器，`make_header`是个普通的函数，它的返回值是装饰器。

来看一下实现的代码。

```python
def make_header(level):
    print('Create decorator')
    
    # 这部分跟通常的装饰器一样，只是wrapper通过闭包访问了变量level
    def decorator(func):
        print('Initialize')
        def wrapper():
            print('Call')
            return '<h{0}>{1}</h{0}>'.format(level, func())
        return wrapper

    # make_header返回装饰器
    return decorator
```

看了实现代码，装饰器的**构造**和**调用**的时序已经很清楚了。

```python
>>> @make_header(2)
... def get_content():
...     return 'hello world'
...
Create decorator
Initialize
>>> get_content()
Call
'<h2>hello world</h2>'
```

### 2. 如何装饰有参数的函数？

为了有条理地理解装饰器，之前例子里的被装饰函数有意设计成无参的。我们来看个例子。

```python
@make_bold
def get_login_tip(name):
    return 'Welcome back, {}'.format(name)
```

最直接的想法是把`get_login_tip`的参数透传下去。

```python
class make_bold(object):
    def __init__(self, func):
        self.func = func

    def __call__(self, name):
        return '<b>{}</b>'.format(self.func(name))
```

如果被装饰的函数参数是明确固定的，这么写是没有问题的。但是`make_bold`明显不是这种场景。它既需要装饰没有参数的`get_content`，又需要装饰有参数的`get_login_tip`。这时候就需要可变参数了。

```python
class make_bold(object):
    def __init__(self, func):
        self.func = func
    def __call__(self, *args, **kwargs):
        return '<b>{}</b>'.format(self.func(*args, **kwargs))
```

当装饰器不关心被装饰函数的参数，或是被装饰函数的参数多种多样的时候，可变参数非常合适。可变参数不属于装饰器的语法内容，这里就不深入探讨了。

### 3. 一个函数能否被多个装饰器装饰？

下面这么写合法吗？

```python
@make_italic
@make_bold
def get_content():
    return 'hello world'
```

合法。上面的的代码和下面等价，留意一下装饰的顺序。

```python
def get_content():
    return 'hello world'
get_content = make_bold(get_content) # 先装饰离函数定义近的
get_content = make_italic(get_content)
```

### 4. `functools.wraps`有什么用？

Python的装饰器倍感贴心的地方是对调用方透明。调用方完全不知道也不需要知道调用的函数被装饰了。这样我们就能在调用方的代码完全不改动的前提下，给函数patch功能。

为了对调用方透明，装饰器返回的对象要伪装成被装饰的函数。伪装得越像，对调用方来说差异越小。有时光伪装函数名和参数是不够的，因为Python的函数对象有一些元信息调用方可能读取了。为了连这些元信息也伪装上，`functools.wraps`出场了。它能用于把被调用函数的`__module__`，`__name__`，`__qualname__`，`__doc__`，`__annotations__`赋值给装饰器返回的函数对象。

```python
import functools

def make_bold(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return '<b>{}</b>'.format(func(*args, **kwargs))
    return wrapper
```

对比一下效果。

```python
>>> @make_bold
... def get_content():
...     '''Return page content'''
...     return 'hello world'

# 不用functools.wraps的结果
>>> get_content.__name__
'wrapper'
>>> get_content.__doc__
>>>

# 用functools.wraps的结果
>>> get_content.__name__
'get_content'
>>> get_content.__doc__
'Return page content'
```

实现装饰器时往往不知道调用方会怎么用，所以养成好习惯加上`functools.wraps`吧。

这次是真·完结了，有疑问请留言，撒花吧~~~
