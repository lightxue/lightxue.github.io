---
title: strlen的实现方法
date: 2013-12-07 22:23:46 +0800
author: John Smith
slug: strlen-implementation
category: C
tags: C
keywords: strlen, C, algorithm
description: 解析一段牛逼的strlen实现
---

感谢[John Smith](https://plus.google.com/u/0/102034236640204820044)来稿，笔风太有趣了，能当本博的专栏作家吗？
<!-- more -->

```c
size_t strlen(const char* str)
{
    size_t len = 0;
    while (*str++)
        len++;
    return len;
}
```

这大概是通常的写法，或者是像C语言程序设计的示例
```c
int strlen(char* s)
{
    char *p = s;
    while(*p++)
        ;
    return p - s;
}
```

和某B偶然说到这个函数，那B说面试的时候老大问了strlen的写法，他当时用了一种
比较快速的方法。第一反应这货还有快速实现？怎么搞都得遍历完这个字符串，O(n)没跑了，你丫忽悠我。

答曰不是，然后上网去搜了一个glibc的strlen实现。大概如下：
```c
size_t strlen (const char *str)
{
    const char *char_ptr;
    const unsigned long int *longword_ptr;
    unsigned long int longword, magic_bits, himagic, lomagic;

    for (char_ptr = str; ((unsigned long int) char_ptr
            & (sizeof (longword) - 1)) != 0;
                ++char_ptr)
        if (*char_ptr == '\0')
            return char_ptr - str;

    longword_ptr = (unsigned long int *) char_ptr;

    magic_bits = 0x7efefeffL;
    himagic = 0x80808080L;
    lomagic = 0x01010101L;
    if (sizeof (longword) > 4)
    {
        magic_bits = ((0x7efefefeL << 16) << 16) | 0xfefefeffL;
        himagic = ((himagic << 16) << 16) | himagic;
        lomagic = ((lomagic << 16) << 16) | lomagic;
    }
    if (sizeof (longword) > 8)
        abort ();

    for (;;)
    {
        longword = *longword_ptr++;

        if (((longword - lomagic) & himagic) != 0)
        {
            const char *cp = (const char *) (longword_ptr - 1);

            if (cp[0] == 0)
                return cp - str;
            if (cp[1] == 0)
                return cp - str + 1;
            if (cp[2] == 0)
                return cp - str + 2;
            if (cp[3] == 0)
                return cp - str + 3;
            if (sizeof (longword) > 4)
            {
                if (cp[4] == 0)
                    return cp - str + 4;
                if (cp[5] == 0)
                    return cp - str + 5;
                if (cp[6] == 0)
                    return cp - str + 6;
                if (cp[7] == 0)
                    return cp - str + 7;
            }
        }
    }
}
```

艹，这么长(你这么想了，你一定这么想了)。

大概看了下，主要思想是一次取4/8个字节的数据进行判断。减少了将数据从内存搬到寄存器的指令次数。碉堡了，简直碉堡了。

以32位机器为例。

第一步地址4字节对齐。将地址与上`0x03`，抹掉前面的bits，留下最后两位，检查是否为0，为0则地址是4字节对齐的退出循环，否则地址+1。

第二步4字节作步长，检查取到的4字节中是否有`\0`，有的话，return 长度，没有继续往后走。检查是否有`\0`，是通过 `(x - 0x01010101L) & 0x80808080L != 0`来做的。至于为啥可以这么做，自行列竖式试验下就知道了。如果有`\0`，遍历那4个字节，看具体是哪个字节是`\0`。

至此，实现方式已经清楚了。

但是这种方式实际上对于非ascii字符串是有问题的，会误判。所谓步子迈大了容易扯着tama。 unicode，GBK啥的，虽然函数不会出错，但是效率退化到和普通遍历一样了。 GBK是这样编码的好像，比如两字节表示一个字，这种情况下第一个字节肯定是大于等于128。就是说第一个字节最高位是1，这样 `(x - 0x01010101L) & 0x80808080L != 0`判断是否有`\0`就失效了，就算上面的判断为true，那4个字节也没有`\0`，代码会遍历那4个字节，发现实际上没有`\0`，不退出，继续往后走直到找到`\0`。

理论上对于ascii字符串，glibc的实现可以达到3X的效率提升，仔细想想 Is it worthwhile?

who knows? ╮(╯_╰)╭, it all depends.

现在的电脑，内存带宽大概在5GB/s(我胡邹的)，`mov VAR, %eax`这条指令大约消耗十几到几十个时钟周期(这也是胡诌的)。做这样的优化是否有意义不太好说，真是超级无所谓的事情。对程序员来说，就知道大概有这么一种思想，可以这么做，聊以自慰罢了。

----喂喂，你是认真的么

----我错了，我说谎了，最大作用是可以和别人拿来zhuangbility。。。

顺便说一下，CRC32算法也用到这种的思想了(同上)。一次取4字节数据进行计算 + 打表。可以达到原本计算方法几十倍速度的提升吧，大概。。。有兴趣自行wikipedia。

以上

john_smith，2013-12-07，一边听着柿姐的<虎视眈眈>，一边看里番，一边想着中午吃什么，一边写这个。

无所谓，真是超级无所谓的事情。

