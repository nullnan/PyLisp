# PyLisp
A Lisp interpreter written in Python.  

Reference: [Lisp之根源](http://daiyuwen.freeshell.org/gb/rol/roots_of_lisp.html)

## Introduction

根据 *Root of Lisp* 中的描述，实现了七个基本运算符，可以运行文章中大部分的代码。但是很多细节不知道有没有实现对。

参照了部分 Scheme 实现了数字和字符串，不过还没有添加相关函数。

作用域只有一个全局的域，在函数内会继承全局域然后新建一个，函数中的自由变量根据调用者确定，貌似这叫动态作用域？

## Usage

#### 执行测试用例

```bash
$ cd test && python all_tests.py
```

#### 运行简单的 REPL

```bash
$ python lisp_repl.py
```

目前有几个问题

- REPL 不支持多行输入
- 出现错误时不能显示完整的堆栈信息

## TODO

- [ ] 实现词法作用域
- [ ] 实现变量绑定
- [ ] 实现闭包
- [ ] 读取lisp文件来执行
