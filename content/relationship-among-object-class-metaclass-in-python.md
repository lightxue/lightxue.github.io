---
title: Python中对象、类型、元类之间的关系
date: 2013-11-01 23:29:48 +0800
slug: relationship-among-object-class-metaclass-in-python
category: Python
tags: Python
keywords: Python, object, class, type, metaclass, 对象, 类型, 元类
description: 解释Python中对象、类型和元类之前的关系
---


Python里的对象、类型和元类的关系很微妙也很有意思。

1989年圣诞节期间，[上帝](http://www.python.org/~guido/)很无聊，于是创造了一个世界。

<!-- more -->

## 对象

在这个世界的运转有几条定律。

> 1.一切都是对象

对象(object)是这个世界的基本组成单位，所有的的事物都由对象构成。

什么是对象？不同的语言对对象的定义不尽相同。在Python的世界里，对象是数据的一种抽象表示。如果看了Python源码，事情就很好解释了，所有能通过PyObject类型的指针访问的都是对象。整数、字符串、元组、列表、字典、函数、模块、包，栈等都是对象。

[圣经](http://www.python.org/doc/)中[提到](http://docs.python.org/2/reference/datamodel.html#objects-values-and-types)，

> 2.所有对象都有三种特性: id、类型、值

id是一个对象的编号，每个对象天生都有一个与众不同的编号(目前实现是对象的地址).用`id()`能看到对象的id
```python
>>> id(1)
140657675012776
```


每个对象都会有类型(type)，类型就像是商品上印的生产厂商一样，标识自己被谁生产出来。用`type()`可以看到对象的类型
```python
>>> type(1)
<type 'int'>
>>> class A(object): pass
... 
>>> a = A()
>>> type(a)
<class '__main__.A'>
```

值是对象的价值所在。各种各样的对象保存着各种各样的值，Python的世界才会如此多彩。有的对象值永远不会变，叫不可变对象(immutable)；有的对象值可以变，叫可变对象(mutable)。

再说一次：Python世界里，一切都是对象

## 类型

类(class)就是生产出对象的模具(本文只讨论[new-style class](http://docs.python.org/2/reference/datamodel.html#new-style-and-classic-classes)，classic class不在讨论范围内)。上面说到，每个对象天生都会有个铭牌，写着自己的类型。在Python里，类(class)和型(type)指的是同一件东西。汉字真是精妙，类和型放在一块念是多么的自然。

> 3.每个对象都是由对应的类创建出来的

由这个定律很容易理解上文说到的，每个对象都有对应类型。类很像工厂里生产产品的模具，它负责对象的创建，决定了对象将被塑造成什么样，有什么属性、函数。

类可以继承和派生。虽然有点勉强，但姑且这么理解吧。类型B继承类型A，就像相当于模具B是以模型A为原型做出来的。生产出模具B的不是模具A，但模具B是模仿模具A而生产出来的，模具B生产出来的对象拥有模具A生产出来的对象类似的特性。模具B如果以模具A为原型生产出来，模具B身上会络上模具A的版权标识(☺就当做版权保护吧)。用`B.__bases__`可以看模具B的印记。聪明的你可能已经注意到了，bases是复数，也就是说模具B可以以多个模具为原型，即多重继承。
```python
>>> class A(object): pass
...
>>> class B(A): pass
...
>>> A.__bases__
(<type 'object'>,)
>>> B.__bases__
(<class '__main__.A'>,)
```

这里注意，模具的版权标识跟对象的类型不一样。每个对象都会有类型，表示自己是哪个模具生产出来的。而模具的版权标识只有模具才会有，标识表示的是这个模具的设计原型哪个模具，并不表示这个模具是由这个原理模具生产出来的。

这里必须要提一下一个特殊的模具，堪称模具之母的模具：object。这个object不是上文说的对象，上文的对象是一个抽象的概念，这里的object是一个具体的模具。所有的模具(除了object自己)沿着印记向上追溯，最后肯定到object。也就是说，所有除了object自己以外的类，都直接或间接地继承了object，无论是内置的(buit-in)还是自定义的(user-defined)。另一方面看，所有对象都直接或间接由模具object生产出来。如果有兴趣的话，用`type()`把想查看对象的类型找到，再用`__baess__`向上查找，最后肯定会到object。从源码的角度看，object就是上文提到的PyObject。这跟Python里所有的对象都能用PyObject的指针访问是有关系的。

## 元类

定律1说到，一切都是对象，类型也是对象。相比很多语言，这一点非常特别。
```python
>>> id(A)
140548933792976
>>> type(A)
<type 'type'>
>>> dir(A)
['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__']
```

可以看到，类型也像其他对象那样，有id，有类型，有值。它可以当变量、类成员、函数参数。有意思吧？更有意思的在后头。

定律3说到，任何对象都是由类型创建出来的。那类型这种对象是由谁创建出来的呢？继续拿模具来说，生产模具的模具是谁呢？模具的模具：元类(metaclass)。元类跟其它模具不同之处在于，它生产出来的是不是一般的对象，是模具。是不是很神奇？有了元类我们就可以在程序运行时动态生成类了。我们可以根据各种数据和配置，动态地定制我们所需要的类。这里不讨论元类的使用方法。不过元类除了能生产模具之外，跟其它模具相比无其它特别的地方。

有趣的问题又来了，根据定律1，元类也是对象吧，元类是谁生产出来的？元类是模具，生产模具的模具还是元类，所以元类的类型也应该是元类。继续追问下去，元类的元类的元类也是元类……这么追溯到源头(再强调一下，本文只讨论new-style class)，就是一个特殊的元类：type。什么？type不是个查看类型的函数吗？通过`help(type)`可以知道，type是个类。`type()`如果传1个对象进去，type会返回这个对象的类型，这是我们熟知的用法；如果传3个对象进去，会生产出一个新的类出来。为什么会把两个功能放到一个类里做呢？可能是历史原因吧。再追问下去，这个终极的元类的类型是什么呢？上帝为了世界设定的统一，使type的类型是它自己。模具把自己生产出来了？这个下面讨论。

type引来的问题不只这些。
```python
>>> object
<type 'object'>
>>> type
<type 'type'>
>>> type(object)
<type 'type'>
>>> type(type)
<type 'type'>
>>> type.__bases__
(<type 'object'>,)
```

我们看到，type这个模具是object为原型造的，而生产object的模具却是type。鸡先生蛋还是蛋先生鸡？Python这个世界是运行在虚拟机上的。世界创建之初虚拟机就把type和object都造出来了。object一出世，生产的模具就写着是type；type一出世，模板的版权印记就记着object。他们一开始就存在了，无所谓谁先谁后。同理，type是不是自己把自己创建也来的问题也一样。

## 总结

![对象、类型、元类之间的关系](/images/relationship-among-object-class-metaclass-in-python/python_types_map.png)

[此文](http://www.cafepy.com/article/python_types_and_objects/python_types_and_objects.html)把对象、类型、元类的关系画成了这幅图。三个框分别表示元类、类型、一般对象。把虚线看成产品与模具的关系，实线看成模具与原型的关系，是不是一目了然？
