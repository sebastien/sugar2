Sugar Programming Language
==========================

Sugar is a *transpiler* that targets JavaScript and Python, it is intended
to be a *syntax sugar overlay* on top of the target language/platform, and as
such does not provide a cross-platform abstraction layer.

The language is designed with the following priorities in mind:

- Favor decomposition and reuse using OOP constructs
- Encourage functional-style programming for data processing
- Minimize discrepancies in code presentation between developers
- Provide a foundation for building software/code engineering tools
- Remove superflous syntax

Here's an example of Sugar code:

```sugar
@module hello

@class Hello
| A simple object-oriented hello world

	@property message = "hello, "

	@method greet name:String
		print (message + name)

```

It's good to note the following decisions were made regarding the syntax:

- Indentation is with *tabs only*. It makes it easier for people to adjust
  the indentation size in their editor and makes tools parsing Sugar code
  easier.

- Structural elements are prefixed by `@`, like `@module`, `@class`, etc‥, which makes it easy to parse
  the structure without having to worry about the whole language (ie. fast ctags) while
  also preventing names/keyword clashes.

- Space is used to denote decomposition (`a b` instead of `a.b`)

Sugar requires Python (2 or 3) and a C compiler to compile its parser (implemented
using [libparsing](https://github.com/sebastien/libparsing) and using
[λfactory](https://github.com/sebastien/lambdafactory) as a backend). Sugar also works
on PyPy.

Sugar currently comes with 3 backends:

- JavaScript
- ECMAScript
- Python

Installing
==========

```shell
pip install --user sugar2
```

Usage
=====

Compile a Sugar file to JavaScript

:	```shell
	sugar2 -c hello.sjs
	```

Compile a Sugar file to Python

:	```shell
	sugar2 -clpy hello.sjs
	```

Compile a Sugar file to a directory

:	```shell
	sugar2 -cl -o. hello.sjs
	```

Add a library (LIBRARY) path to search for Sugar modules

:	```shell
	sugar2 -cl -LLIBRARY hello.sjs
	```

Syntax
======

Litterals
---------

Numbers

:	```
	```

Strings

:	```
	```

Lists:

:	```
	```

Maps:

:	```
	```

Operations
----------

Variable declaration

:	```
 	```

Destructuring

:	```
 	```

Chaining

:	```
 	```

Continuing

:	```
 	```

Iterating

:	```
 	```

Mapping

:	```
 	```

Filtering

:	```
 	```

Folding

:	```
 	```


Invocation

:	```
	```

Asynchronous invocation

:	```
	```

Control structures
------------------

If/else (conditionals)

:	```
 	```

For loops

:	```
 	```

While loops


:	```
 	```

Return (termination)

:	```
	```

Breaking

:	```
 	```

Continue

:	```
	```

Pattern matching

:	```
 	```



Documentation
-------------

Comments

:	```
	```

Docstrings

:	```
	```

Examples

:	```
	```
Unit testing

:	```
	```

Litterate programming

:	```
	```

Constructs
---------

Closures

:	```
	```

Functions

:	```
	```

Module

:	```
	```

Classes

:	```
	```

Traits

:	```
	```

Singletons

:	```
	```

Guards

:	```
	```

Decorators

:	```
	``

Types
---------

Enumeration

:	```
 	```

Types

:	```
	```


