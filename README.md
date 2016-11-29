Sugar Programming Language
==========================

Sugar is a *transpiler* that targets JavaScript and Python, it is intended
to be a syntax sugar overlay on top of the target language/platform, and as
such does not provide a cross-platform abstraction layer.

The language itself is designed to help developers focus on software
architecture, to minimize discrepencies in code presentation and ease the
development of software engineering tools.

The syntax has the following characteristics

- Tab-based indentation
- Optional parentheses for first argument (`f 10`)
- Space to denote decomposition (`a b` instead of `a.b`)
- Structural elements prefixed by `@`, like `@module`, `@class`, etc‥
- Explicit `end` for constructs
- Collections operators ('::' to iterate, '::=' to map, '::?' to filter)

Sugar requires Python (2 or 3) and a C compiler to compile its parser (implemented
using [libparsing](https://github.com/sebastien/libparsing).

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

Iterating

:	```
 	```

Mapping

:	```
 	```

Filtering

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

While (loops)

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

Documentation
-------------

Comments

:	```
	```

Docstrings

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

Guards

:	```
	```


