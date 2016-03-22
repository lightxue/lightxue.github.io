---
layout: post
title: Python源码寻宝记——挖坑不埋
date: 2016-03-22 20:34:21 +0800
comments: true
categories: Python
keywords: Python, python internals, how python works, python source code, python implenment, python源码剖析, python源码, python代码分析, python实现, python解释器实现
description: 发掘Python解释器中有趣的源码
---

作为pythonista，不禁感慨Python的易用与强大。时不时会想，这个好用的语法是怎么实现的，那个神奇库是怎么回事。后来开始翻Python源码，读感兴趣的部分的实现时，像是找到了个四次元口袋。这里有奇思妙想的算法实现，也有精妙绝伦的性能优化，还有天马行空的语法原理。源码的风格也和Python所倡导的一样，简洁优雅，阅读的时候心情十分愉悦。

记下源码里有趣的地方，是件有意思的事。但按这个博客一直以来自娱自乐的尿性，注定了这个系列是只会把坑越挖越大。这里不要脸地承认了，这就是在挖坑。

这个系列分析的Python源码版本是2.7.11和3.5.1，当前最新版。在[这里][1]可以找到下载链接。

本文的目的是灌水+挖坑+索引这系列文章。开始寻宝吧。

[Python源码寻宝记——地图](/python-internals-locate-source-code)


[1]: https://www.python.org/downloads/


