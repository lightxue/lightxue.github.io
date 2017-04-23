---
title: Python判断整数相加溢出
date: 2013-07-13 22:50:32 +0800
slug: python-ingeger-overflow
category: Python
tags: Python, C, algorithm
keywords: 溢出, Python, 源码, 整数溢出, integer overflow
description: 剖析Python源码，分析Python如何判断整数溢出
---

在Python解释器的源码里看到一段有趣的代码，它实现了Python两个整数相加时如果溢出则用更大的数据类型保存整数。具体代码的如下。

<!-- more -->

```c
// Python解释器是C语言实现的
static PyObject *
int_add(PyIntObject *v, PyIntObject *w)
{
    register long a, b, x;
    CONVERT_TO_LONG(v, a);
    CONVERT_TO_LONG(w, b);
    /* casts in the line below avoid undefined behaviour on overflow */
    x = (long)((unsigned long)a + b); // 重点是这行
    if ((x^a) >= 0 || (x^b) >= 0)     // 和这行
        return PyInt_FromLong(x);
    return PyLong_Type.tp_as_number->nb_add((PyObject *)v, (PyObject *)w);
}
```

`((x^a) >= 0 || (x^b) >= 0)`如果是false，就是发生了溢出。这段代码咋看跟溢出没关系，细看还是挺有名堂的。这个if要判断的是符号位。我们知道，整型的最后一个bit如果是0，那么这个数大于等于0；如果是1，这个数小于0。这个表达式的`>= 0`判断的就是是否最后一个bit是否是0。

我们知道，^是异或运算：

```c
0 ^ 0 == 0
0 ^ 1 == 1
1 ^ 0 == 1
1 ^ 1 == 0
```

简而言之就是两个bit相同得0，两个bit不同得1。也就是说`((x^a) >= 0 || (x^b) >= 0)`判断的是x与a的符号位相同或x与b的符号位相同。换而言之，x只要跟a和b任意一个数的符号位相同则为true。这跟溢出有什么关系？

我们知道，一个long能表达的数的范围是有限制的，两个long相加的情况不外乎下面6种：

```c
//  没有溢出的情况
非负数 + 非负数 = 非负数
非负数 + 负数 = 负/非负数
负数 + 非负数 = 负/非负数
负数 + 负数 = 负数

// 溢出的情况
非负数 + 非负数 = 负数
负数 + 负数 = 非负数
```

可以看到，没有溢出的情况刚好x和a、b其中一个的符号位相同，而溢出的情况x跟a、b的符号位都不同。所以`((x^a) >= 0 || (x^b) >= 0)`就刚好能判断出来a+b有没有溢出。

好神奇，我和我的小伙伴们都惊呆了！

有个地方不提一下这个讨论就不完整了。大家可能都注意到代码中的注释了：casts in the line below avoid undefined behaviour on overflow。在[wikipedia](http://en.wikipedia.org/wiki/Integer_overflow)上看到的解释是这样的：

> Since an arithmetic operation may produce a result larger than the maximum representable value, a potential error condition may result. In the C programming language, signed integer overflow causes undefined behavior, while unsigned integer overflow causes the number to be reduced modulo a power of two, meaning that unsigned integers "wrap around" on overflow.

如果是a和b都是signed long，溢出后结果是不确定的，看编译器的实现。如果a或b是unsigned long(相加时另一个也会转成unsigned long)，相加结果再转回long跟上面讨论的6种情况就一样了。

最后留个问题吧，怎么判断两个数相减溢出了呢:-)

补充：

axu给了我另一种判断整数溢出的判断

```c
t = a + b;
if ((a<0 == b<0) && (t<0 != a<0))
    // overflow
```

细看其实思路跟上面说的一样，于是弃之不理。望仔看到这段代码后竟然想到去优化这它。

```c
t = a + b;
if (((a^b) >= 0) && ((a^t) < 0))
    // overflow
```

确实比上面的解法有所提升。认真思考的心态值得学习，赞一下望仔。
