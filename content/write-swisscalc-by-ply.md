---
title: 使用PLY编写多功能计算器
date: 2013-11-24 22:00:52 +0800
slug: write-swisscalc-by-ply
category: Python
keywords: Python, PLY, LALR, 解释器, 计算器, SwissCalc, 词法解析, 语法解析, calculator, BNF, 结合性, 命名空间
description: 用PLY实现程序员专用的Vim计算器，解释了一些PLY用法和编译原理知识
---

最近用[PLY](http://www.dabeaz.com/ply/ply.html)(Python Lex-Yacc)写了个Vim插件：[SwissCalc](https://github.com/lightxue/SwissCalc)。借这个机会复习了下编译原理的一些知识。下面介绍一下用PLY写SwissCalc的过程吧。

<!-- more -->

## 程序结构

程序分成3个部分

* 计算器(autoload/swisscalc.py)
* 内置函数(autoload/builtin.py)
* 用户自定义函数(autoload/custom.py)

这里主要分析计算器部分。

计算器部分有两个类：Parser和Calc。Parser是Calc的父类，对外提供计算器接口，处理一些传入参数，决定一些中间文件的路径等等。Calc是计算器的主要逻辑，一部分负责解释表达式，一部分负责管理计算器内部的逻辑，比如变量命令空间、函数命名空间、环境变量。Calc是计算器最有趣的地方。词法、语法解释就在解释表达式的部分。

## 词法解析

词法解析是把表达式(字符序列)识别成token序列。比如`v=13+13`经过记法解析会变成`v` `=` `13` `+` `13`。词法解析的过程归根结底是自动机扫描字符串。幸运的是现在的词法解析工具都不需要直接写自动机，大都是用正则表达式，PLY也一样。

PLY的词法解析在SwissCalc里这么用。

1.Parser里创建lexer对象，把lexer的命名空间指向类的命令空间。
```python
self.lexer = lex.lex(module=self, debug=self.debug)
```

2.在Calc中，指定token的类型。
```python
tokens = (
    'ident',
    'newline',
    'binint', 'octint', 'hexint', 'decint',
    'string',
    'pointfloat', 'exponentfloat',
    'add', 'subtract', 'multiply', 'divide',
    'modulo', 'power', 'factorial',
    'lshift', 'rshift', 'and', 'not', 'or', 'xor',
    'assign',
    'addassign', 'subassign', 'mulassign', 'divassign',
    'modassign', 'powassign',
    'lsftassign', 'rsftassign',
    'andassign', 'orassign', 'xorassign',
    'lparen', 'rparen', 'comma',
)
```

这里的变量名`tokens`是固定的，别的名字PLY不认。

3.每种token类型写上对应的正则表达式。
```python
t_ignore = ' \t'
t_ident = r'[a-zA-Z_][a-zA-Z0-9_]*'

def t_hexint(self, t):
    r'0[xX][0-9a-fA-F]+'
    t.value = int(t.value, 16)
    return t

_escapeseq = r'\\.'
_stringchar = (r"[^\\']", r'[^\\"]')
_singlequote = "'(%s|%s)*'" % (_escapeseq, _stringchar[0])
_doublequote = '"(%s|%s)*"' % (_escapeseq, _stringchar[1])
_string = r'[rR]?((%s)|(%s))' % (_singlequote, _doublequote)
@TOKEN(_string)
def t_string(self, t):
    if t.value[0] in 'rR':
        t.value = t.value[2:-1]
    else:
        t.value = t.value[1:-1].decode('string-escape')
    return t

def t_error(self, t):
    t.lexer.skip(1)
    raise SyntaxError("illegal character '%s'" % (t.value[0]))

...
```

这里变量名一样是有要求的。上面`tokens`里的类型名前面加上`t_`就是这个类型对应正则表达式的变量名。PLY会通过反射来查找这些变量。像`t_ident`是变量名的表达式，符合这个正则的字符串会被切出来当变量名。切出来的数据还是字符串。

如果有些特殊需求，比如想让token类型是整数，那么就不能像`t_ident`那样只写正则表达式了，要像`t_hexint`那样写成函数。函数的docstring还是正则表达式，token是函数的返回值。这样在函数里就能把字符串类型转成整型了。像行号计数、错误处理都可以用函数去实现。

如果正则表达式比较复杂，写docstring不方便，可以像`t_string`那样，先把正则表达式拼接好，然后再用`@TOKEN(_string)`设置`t_string`的正则表达式。

`t_ignore`是PLY内置的token类型，这种token在解析到的时候会被丢弃。`t_error`函数词法解析错误的时候调用。

经过这3个步骤词法分析就做好了。这个过程写正则挺有意思的。像字符串的表达式怎么识别内部有转义的引号这种有趣的问题是会有的(没有开玩笑哦，这个计算器是支持字符串的)。Parser里有个函数叫`_lexme`，参数是表达式，结果是token序列。如果有兴趣可以用它了解一下词法分析的输入和输出。

## 语法解析

语法解析是写SwissCalc最爽的一部分。语法解析是根据token序列解析出语法树。有了语法树，对表达式的语义分析就容易很多了。如果不用PLY，自己手写语法分析还是挺有挑战的(如果打算这么做，推荐使用[递归下降法](http://en.wikipedia.org/wiki/Recursive_descent_parser)，可操作性比较强)。用PLY整个语法解析的工作变得轻松不少，基本上只要操作产生式就行。根据产生式分析表达式过程PLY包办了，这是语法解析最复杂的部分，有很多坑。这里要感谢一下PLY，不然写个计算器都不知道要花我多少时间。

PLY支持[LALR](http://en.wikipedia.org/wiki/Recursive_descent_parser)和[SLR](http://en.wikipedia.org/wiki/Simple_LR_parser)，默认使用LALR，SwissCalc也是用的LALR。LALR和SLR怎么实现的我半懂不懂，感兴趣可以翻翻龙书，如果能翻得下去的话……

写[产生式](http://en.wikipedia.org/wiki/Formal_grammar)也是件很有趣的事。PLY产生式用的[BNF](http://en.wikipedia.org/wiki/BNF_grammar)，这里不详细介绍了。写产生式花了我一些时间，因为计算机到底需要哪些语法，功能要支持到什么程度就在这时候决定了。要让计算器强大一些，又要适当控制使用的复杂度，很多东西需要取舍。写完产生式其实计算器要做成什么样已经非常清晰了。

PLY的语法分析使用分这几个步骤。

1.在Parser里初始化yacc。
```python
yacc.yacc(module=self,
          debug=self.debug,
          debugfile=self.debugfile,
          tabmodule=self.tabmodule,
          outputdir=self.basedir)
```

2.编写产生式，像这样的。
```python
expression : expression add expression
           | expression subtract expression
           | expression multiply expression
           | expression divide expression
           | expression or expression
           | expression xor expression
           | expression and expression
           | expression lshift expression
           | expression rshift expression
           | expression modulo expression
           | expression power expression

expression : float
           | ident

float      : pointfloat
           | exponentfloat
```

注意，产生式出来的语法树，叶子节点肯定要是词法解析的token，比如上面的`ident` `pointfloat` `exponentfloat`。

3.指定运算符的结合性和优先级。

结合性举个例子。`2 ** 2 ** 3`，如果是这么算`(2 ** 2) ** 3`，结果是64，那么`**`是左结合的。如果`2 ** (2 ** 3)`结果是256，那么`**`是右结合的。结合性的指定决定了LALR解析时遇到同优先级的操作符是要shift还是要reduce。

优先级就不多说了，像我上面那么写`expression`，需要指定乘法比加法优先级高才能确保`2 + 2 * 3`这样的表达式结果是8而不是12。

结合性和优先级像下面这么指定。同理，变量名`precedence`是固定的。优先级从低到高，同一个元组内的操作级等级相同，元组第一个元素是结合性。
```python
precedence = (
    ('left', 'and', 'or', 'xor'),
    ('left', 'lshift', 'rshift'),
    ('left', 'add', 'subtract'),
    ('left', 'multiply', 'divide', 'modulo'),
    ('right','usub', 'uadd', 'not'),
    ('left', 'factorial'),
    ('left', 'power'),
    )
```

4.每一条产生式编写对应的函数，做语义分析。
```python
def p_expression_binop(self, p):
    '''
    expression : expression add expression
               | expression subtract expression
               | expression multiply expression
               | expression divide expression
               | expression or expression
               | expression xor expression
               | expression and expression
               | expression lshift expression
               | expression rshift expression
               | expression modulo expression
               | expression power expression
    '''
    if p[2] == '/':
        p[3] = float(p[3])

    if p[2] in self.common_binops:
        p[0] = self.common_binops[p[2]](p[1], p[3])
    else:
        p[0] = self.int_binops[p[2]](int(p[1]), int(p[3]))
```

像上面这个函数，函数名无所谓，但必须要有`p_`开头，参数必须 只有一个，docstring是产生式。参数`p`就像个元组一样，从0开始顺序对应表达式里的各个单词。上面的函数，就是计算器里的二元操作，`p[0]`保存计算结果，`p[2]`是运算符，`p[1]`和`p[3]`是需要操作的数。

`p_error`在语法解析错误的时候会调用，在里面做一些错误处理。

以上4步就能把语法解析的工作做完了。设定SwissCalc世界观还是相当愉悦的。

## 其它

做完词法、语法解析的工作，计算器基本完工了。SwissCalc有一些特别的功能，值得说一下。

### 命名空间

SwissCalc的变量和函数命名空间各用一个字典来实现。内置函数和用户自定义函数用这种方式导进来。
```python
import builtin
import custom

self.funcs['vars'] = self.show_names
self.funcs['funcs'] = self.show_funcs
self.funcs['ff'] = self.find_func
self.funcs['find_func'] = self.find_func
self.funcs['env'] = self.env
self.funcs['setenv'] = self.setenv
self.funcs['help'] = self.helper

self.funcs.update(builtin.funcs)
cusfuncs = {var : getattr(custom, var)
                for var in dir(custom)
                    if callable(getattr(custom, var))}
self.funcs.update(cusfuncs)
```

上面代码中的`vars` `funcs` `help`等都是一些需要操作变量和函数的命名空间的函数，以提供一些自省的功能。比如`help`能看函数的帮助。
```python
def helper(self, func):
    '''
    help(func_name)

    print the document of the function which name is func_name
    '''
    if func not in self.funcs:
        raise SyntaxError('function: %s not found' % func)
    doc = self.funcs[func].__doc__
    if doc:
        print doc
```

### 整数截断

Python的整数精度是无限大的，只要内存存得下。但是SwissCalc为了模拟整数运算溢出的情况，要把整数截断成用户定义的字长。
```python
def truncint(self, val):
    val = int(val)
    signed = int(self._env['signed'] > 0)
    bits = 1 << (self._env['word'] * 8)
    return (val & (bits - 1)) - bool(val & (bits >> 1)) * signed * bits
```

### 重定向标准输出

内置函数和用户自定义函数有可能需要标准输出。但是SwissCalc是Vim插件，直接操作标准输出是不会输出到Vim的buffer里的。需要把标准输出的数据接住，然后用Vim提供的方式放到Vim的buffer里。
```python
import cStringIO

try:
    sys.stdout = mystdout = cStringIO.StringIO()
    self.exeval = ''
    yacc.parse(s)
except SyntaxError as err:
    self.exeval = 'SyntaxError: %s' % (err)
except Exception as err:
    self.exeval = 'RuntimeError: %s' % (err)

sys.stdout = sys.__stdout__
outstr = mystdout.getvalue()
```

## 总结

以上就是怎么用PLY实现[SwissCalc v1.0.0](https://github.com/lightxue/SwissCalc/tree/v1.0.0)(1.0.0? 我这么懒难道还会有更高版本吗？)。
