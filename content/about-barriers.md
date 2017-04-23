---
title: 关于barrier
date: 2015-04-10 16:50:24 +0800
author: John Smith
slug: about-barries
category: C
tags: C
---

再次收到John Smith的来稿，为了你这篇稿子，我停笔一年了呀。

memory barrier内存屏障，一种非常底层的同步原语，是memory ordering的一部分。
使用内存屏障可以阻止编译器或cpu对内存的乱序访问，其中阻止编译时期重排的叫做
compiler barrier，阻止运行时期重排的叫做memory barrier。

<!-- more -->

## 一. compiler barrier
```c
#define barrier()   __asm__ __volatile__("":::"memory")
```

看开源项目代码可能偶尔会看上面这样的内嵌汇编:

1. 内嵌汇编的格式为`__asm__` ("asm statement" : outputs : inputs : registers-modified)
2. `__asm__`用于提示编译器在这里插入汇编代码
3. `__volatile__`用于告诉编译器，严禁将此处的汇编代码和其他语句进行重排优化，所得即所见
4. `"":::`空的汇编语句，实际上不做任何事情
5. `"memory"`强制编译器假设RAM所有内存单元均被汇编指令修改，cpu的registers和cache的缓存数据将invalidate，cpu不得不在需要的时候重新从内存读取数据
6. 这条语句实际上不生成任何代码，但是会让gcc在barrier()之后刷新寄存器对变量的分配

举个例子，考虑下面这段代码:
```c
for ( ;; )
{
    struct task_struct *owner;

    owner = lock->owner;
    if (owner && !mutex_spin_on_owner(lock, owner))
        break;
    /* ... */
}
```

这段代码含义大概是自旋的去获取一个mutex, 乍看一下没有问题。但是optimize编译下，compiler发现
循环里面完全没有去修改`lock->owner`嘛，没必要每次都取值。然后这段代码可能会优化为这样:

```c
owner = lock->owner;
for ( ;; )
{
    if (owner && !mutex_spin_on_owner(lock, owner))
        break;
}
```

这肯定不是你想要的结果，而且极有可能出现死循环。

多线程情况下，编译器优化有可能会忽略`lock->owner`会被其他线程修改的情况。compiler barrier可以告诉编译器这里禁止优化，每次都从内存里面取`lock->owner`的值。修改后：

```c
for ( ;; )
{
    struct task_struct *owner;
    barrier();

    owner = lock->owner;
    if (owner && !mutex_spin_on_owner(lock, owner))
        break;
    /* ... */
}
```

注：这里不用compiler barrier，`onwer = (volatile struct task_struct *)(lock->owner)`;
直接强转为volatile指针也可以解决问题。

## 二. memory barrier

```c
#define mb()        __asm__ __volatile__("lock; addl $0, 0(%%rsp)":::"memory")
#define rmb()       mb()
#define wmb()       __asm__ __volatile__("":::"memory")
```

上面三个分别是读写内存屏障，读内存屏障和写内存屏障，在常见的x86/x64体系下，通常使用`lock`指令前缀
加上一个空操作来实现memory barrier, 注意当然不能是真的nop指令，linux中采用`addl $0, 0(%esp)`。

memory barrier可以保证运行时期的内存访问次序不被重排，保证程序的执行看上去满足顺序一致性。`volatile`关键字无法做到这一点，所以`volatile`不能保证是一个memory barrier。

另外也不能指望独立的memory barrier能不做很多事情，mb往往是成对出现的。

考虑下面这种情况，机器有两个核心，x和y都被初始化为0：
```c
CPU 0                   CPU 1

x = 1;                  r1 = y;
mb();                   mb();
y = 1;                  r2 = x;
```

CPU 0和CPU 1走完所有语句之后，总共有下面三种可能:

1. r1 == 0 && r2 == 0: CPU 0在CPU1执行完之后才开始

2. r1 == 0 && r2 == 1: CPU 0和CPU 1物理上并行执行

3. r1 == 1 && r2 == 1: CPU 1在CPU 0执行完之后才开始

只有`r1 == 1 && r2 == 0`这种输出被禁止了，如果这种情况真的出现，那你可以报警了。
这种情况仅仅当CPU 0或CPU 1出现乱序执行的时候才会出现，mb就是为了禁止乱序执行的。
目前Intel的CPU都遵循处理一致性，所有的写操作都遵循程序顺序，不会越过前面的读写操作，不过由于未来可能
会采用更弱的内存一致性模型，在代码里面适当的加上mb保证内存事件的次序仍然是必要的。

