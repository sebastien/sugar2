Sugar Programming Language
==========================

Sugar is a *transpiler* that targets JavaScript and Python, it is intended
to be a syntax sugar overlay on top of the target language/platform, and as
such does not provide a cross-platform abstraction layer.

The language itself is designed to help developers focus on software
architecture, to minimize discrepencies in code presentation and ease the
development of software engineering tools. In essence, Sugar is meant
to provide a consistent, tool and human-friendly syntax that minimize errors
and maximizes expressivity.

Here's an example of Sugar code:

```sugar
@module hello

@class Hello
| A simple object-oriented hello world

	@property message = "hello, "

	@method greet name:String
		print (message + name)
	@end

@end
```

this gets translated to the following JavaScript, using the [extend](http://github.com/sebastien/extend) library.

```javascript
// 8< ---[hello.js]---
var hello=(typeof(extend)!='undefined' && extend && extend.module && extend.module("hello")) || hello || {};
(function(hello){
var self=hello, __module__=hello
hello.Hello = extend.Class({
	// A simple object-oriented hello world
	name:'hello.Hello', parent:undefined,
	properties:{
		message:undefined
	},
	initialize:function(){
		var self=this;
		if (typeof(self.message)=='undefined') {self.message = "hello, ";};
	},
	methods:{
		greet:function(name){
			var self=this;
			extend.print((self.message + name));
		}
	}
})
hello.init = 	function(){
		var self=hello;
		new __module__.Hello().greet("world")
	}
if (typeof(__module__.init)!="undefined") {__module__.init();}
})(hello);
```

and the following Python (no dependency)

```python
#8< ---[hello.py]---
#!/usr/bin/env python
import sys
__module__ = sys.modules[__name__]
__module_name__ = 'hello'
class Hello:
	"""A simple object-oriented hello world"""
	def __init__( self, *args, **kwargs ):
		"""Constructor wrapper to intialize class attributes"""
		self.message = 'hello, '
	def greet(self, name):
		print ((self.message + name))
	

def __module_init__():
	Hello().greet('world')
__module_init__()
```

The syntax has the following characteristics

- Tab-based indentation
- Optional parentheses for first argument (`f 10`)
- Space to denote decomposition (`a b` instead of `a.b`)
- Structural elements prefixed by `@`, like `@module`, `@class`, etc‥
- Explicit `end` for constructs
- Collections operators ('::' to iterate, '::=' to map, '::?' to filter)

Sugar requires Python (2 or 3) and a C compiler to compile its parser (implemented
using [libparsing](https://github.com/sebastien/libparsing) and using
[λfactory](https://github.com/sebastien/lambdafactory) as a backend). Sugar also works
on PyPy.

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


