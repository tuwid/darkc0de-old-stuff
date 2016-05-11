Tools for C code manipulation
=============================

The fusil.c_tools module contains many tools to manipulation C code.

String manipulation
-------------------

   >>> from fusil.c_tools import quoteString, encodeUTF32
   >>> quoteString('Hello World\n\0')
   '"Hello World\\n\\0"'
   >>> encodeUTF32("Hello")
   'H\x00\x00\x00e\x00\x00\x00l\x00\x00\x00l\x00\x00\x00o\x00\x00\x00'

encodeUTF32() use host endian.

Generate C script
-----------------

Hello World!
++++++++++++

   >>> from fusil.c_tools import CodeC
   >>> from sys import stdout
   >>> hello = CodeC()
   >>> hello.includes.append('<stdio.h>')
   >>> main = hello.addMain()
   >>> main.callFunction('printf', [quoteString("Hello World\n")])
   >>> for line in hello.lines():
   ...     if line:
   ...         print line
   #include <stdio.h>
   int main() {
       printf(
           "Hello World\n"
       );
       return 0;
   }

FunctionC
+++++++++

addMain() is an helper to create main() function, but you can write your own
functions with addFunction() method:

   >>> from fusil.c_tools import FunctionC
   >>> testcode = CodeC()
   >>> test = testcode.addFunction( FunctionC('test', type='int') )
   >>> test.variables.append('int x')
   >>> test.add('x = 1+1')
   >>> test.add('return x')
   >>> for line in testcode.lines():
   ...     if line:
   ...         print line
   int test() {
       int x;
       x = 1+1;
       return x;
   }

You can get the function with:

   >>> hello['main']
   <FunctionC "int main()">
   >>> testcode['test']
   <FunctionC "int test()">

Write to a file
===============

To write a code to a file, use write() method:

   >>> from pprint import pprint
   >>> hello.write(open('hello.c', 'w'))
   >>> pprint(open('hello.c').readlines())
   ['#include <stdio.h>\n',
    '\n',
    'int main() {\n',
    '    printf(\n',
    '        "Hello World\\n"\n',
    '    );\n',
    '\n',
    '    return 0;\n',
    '}\n',
    '\n']

Compile the code
==================

To compile the code, use compile() method:

   >>> from os import system, WEXITSTATUS
   >>> from fusil.mockup import NullLogger
   >>> null = NullLogger()
   >>> hello = CodeC()
   >>> main = hello.addMain(footer='return 2*3*7;')
   >>> hello.compile(null, 'hello.c', 'hello')
   >>> WEXITSTATUS(system('./hello'))
   42

Misc attributes
===============

You can customize write() output:

 * 'indent' is the indententation string (default: 4 spaces)
 * 'eol' is the end of line string (default: "\n")

Set gnu_source to True to get::

   #define _GNU_SOURCE

FuzzyFunctionC
==============

Ok, let's play with fuzzing! FuzzFunctionC has methods to generate values.

   >>> from fusil.c_tools import FuzzyFunctionC
   >>> fuzzy = CodeC()
   >>> main = fuzzy.addFunction(FuzzyFunctionC('main', type='int'))

Methods to generate data:

 * createInt32()
 * createInt()
 * createString()
 * createRandomBytes()

Example:

   >>> main.add('return %s' % main.createInt())

