---
layout: post
title: Python源码寻宝记——地图
date: 2016-03-22 23:44:21 +0800
comments: true
categories: Python
keywords: Python, python internals, how python works, python source code, python implenment, python locate source code, python find source code, python get source code, python 源码, python 定位, python 位置, python 代码
description: 找到Python解释器特定逻辑的源码位置
---

如果读源码的方式是打开源码包，一个个文件，一行行开始读。这种阅读源码方式太枯燥了。另一种方式，对Python的设计有了基本的了解后，找感兴趣的部分去阅读。兴致高，目的性强，内容少，阅读的过程会轻松有趣得过。

对Python设计基本了解包括对总体架构设计，对象系统实现原理，字节码的生成和解释过程有大致的了解。哪天闲得不行，可以写写这方面的文章。

感兴趣的部分源码怎么找？这个就是此文的主题了——如何找到特定逻辑的源码。

## 下载源码

Python官方给的下载源码的方式在[这里](https://docs.python.org/devguide/setup.html#getting-the-source-code)。如果不想用Mercurial，也可以直接去[这里](https://www.python.org/downloads/)下对应的版本的Gzipped source tarball。

## 目录结构

官方有源码目录的介绍，在[这里](https://docs.python.org/devguide/setup.html#directory-structure)。重点说一下常见的目录。

- Grammar。EBNF描述的语法规则在这个目录下。
- Include。整个解释器所有的头文件放在这个目录下。
- Lib。纯Python实现的标准库。
- Modules。C实现的标准库。
- Objects。所有的内置类型的实现。
- Python。Python虚拟机的核心代码。

## 源码定位

感兴趣的地方不一样，定位的方式也不一样。介绍一下常见的几种。

### 语法定义

这个好说，去`Grammar`目录看语法规则吧。语法规则由Zephyr Abstract Syntax Definition Language定义，[SPARK](http://pages.cpsc.ucalgary.ca/~aycock/spark/)解析的。

### 内置对象

找某个内置对象是怎么实现的，就直接去`Include`里看声明和`Object`看实现。

比如想知道`list.sort()`是怎么实现的。那么在`Include/listobject.h`里可以知道列表是怎么用`ob_item`表示数据的，在`Objects/listobject.c`的`list_methods`里看到了`sort()`是由`listsort()`实现的.`listsort()`的实现刚好也在`Objects/listobject.c`里。就这样找到了`list.sort()`的源码了。

### 标准库

想找标准库的实现，分两种情况。大部分情况，标准库是纯Python实现的。还有一小部分标准库是C实现的。

纯Python实现的标准库，可以不用直接去`Lib`下面找。Python内置了很好用的工具叫`inspect`。比如想知道`timeit.timeit()`的源码在哪，可以这么查。

```python
python
>>> import inspect
>>> import timeit
>>> inspect.getsourcefile(timeit.timeit)
```

`inspect`只对纯Python实现的库有效，拿C实现的标准库一点招没有。

C实现的标准库也有类似于`inspect`这种好用的方案，叫[cinspect](https://github.com/punchagan/cinspect)，不过我没有尝试过。C的标准库不多，命名也比较容易懂。所以直接去`Modules`找一般很容易找到。

如果不想对着文件名猜某个模块是不是在这实现，就需要工具来帮忙了。这里推荐一下速度比`grep`快得多的[ack](http://beyondgrep.com/)。举个盒子，想找`time`的源码，可以执行这个命令。

```bash
> cd Modules
> 
# Python 2
> ack 'Py_InitModule3\("time"'
timemodule.c
854:    m = Py_InitModule3("time", time_methods, module_doc);

# Python 3
> ack 'PyModuleDef' -A 5 | ack '"time"'
timemodule.c-1331-    "time",
```

`Modules/timemodule.c`就是`time`模块实现的地方。`Py_InitModule3`是Python 2 注册模块的宏，`PyModuleDef`是Python 3 模块定义的结构体的名字。这两个地方都要填上模块名作参数向解释器注册模块。所以这么搜模块名，一搜一个准。

### 语法实现

想知道某个语法怎么实现的去哪找呢？这时候就要去解读字节码，找到对应语法的字节码，并去`ceval.c`看具体实现。

比如想看关键字`in`的实现，执行下面的代码可以看到`in`的字节码是`COMPARE_OP`。

```python
>>> import dis
>>> exp = '0 in (1, 2)'
>>> code = compile(exp, '', 'eval')
>>> dis.dis(code)
  1           0 LOAD_CONST               0 (0)
              3 LOAD_CONST               3 ((1, 2))
              6 COMPARE_OP               6 (in)
              9 RETURN_VALUE
```

具体各个字节码的意思可以去[这里](https://docs.python.org/2/library/dis.html#python-bytecode-instructions)看解释。拿到了字节码后去`Python/ceval.c`里找`COMPARE_OP`的实现，会看到关键字`in`的实现在`PySequence_Contains`函数里。`ceval.c`里实现了字节码解析的eval loop，是整个源码中至关重要的部分。

### 其它情况

上面说的几种方法应该包含了大部分的情况，但也有些时候需要别的方法，比如找垃圾回收的实现。这里推荐一本深入剖析Python 2 源码的书，[《Python源码剖析》](https://book.douban.com/subject/3117898/)。这本书详细介绍了Python源码里各个重要的地方，非常值得一看。

如果书里没有提到的地方，想快速定位源码位置，我的招式已经全部分用完了，剩下的只有问Google，问Stack Overflow，邮件大牛，或是自己去啃源码。

以上就是Python寻宝需要的地图。看这个系列更多文章，请到[Python源码寻宝记——挖坑不埋篇](/python-internals-introductory)。

