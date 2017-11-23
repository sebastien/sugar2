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

Symbols

:
	```
	True                  # Boolean true
	False                 # Boolean false
	None                  # Nothing / nul
	Undefined             # Undefined

	NaN                   # Not a number
	Infinity              # Infinity
	```

Numbers

:	```
	1                     # Natural number
	1.0                   # Real number
	10.5s                 # Time (supports ms, s, m, h, d, w)
	90.5deg               # Degrees
	```

Strings

:	```
	"Hello, world"        # Double-quoted string (default)
	'c'                   # Single-quoted string (chars and alternate notation)
	"Here is a quote \""  # Escaping
	```

Lists:

:	```
	[]                    # Empty list
	[0, 1, 2]             # List on one line
	[                     # Multi-line strings have either `,` or `\n` as delimiter
		0
		1, 2              
		3
	]
	```

Tuples:

:	Tuples are immutable lists

	```
	(,)                    # Empty tuple
	(0, 1, 2)              # The rest is the same as lists
	(                     
		0
		1, 2              
		3
	)
	```

Maps:

:	```
	{}                     # Empty map
	{one:1, two:2}         # Inline map
	{                      # Multiline map
		one: 1
		two: 2
	}
	{"o n e":1}            # Explicit string for map key
	{(1 + 10):1} == {11:1} # Key expression
	```

Operations
----------

Variable declaration

:	```
	var name               # Variable declaration
	var name = 10          # ‥ with assignment
	var a, b = [10, 20]    # ‥ with decomposition
 	```

	While `var` declares the slot as variable (mutable) the `let` keyword
	declares the slot as *immutable* (it cannot be re-assigned later):

	```
	let a = 10
	a     = 20             # ERROR → a is immutable
 	```

Destructuring

:	Destructuring allows to quickly extract and assign components
	within a composite value. Any unresolved value will be assigned
	`Undefined`

	```
	a, b = [10, 20]               # a=10, b=20
	a, b = [10]                   # a=10, b=Undefined
	a, b | c = [10, 20, 30, 40]   # a=10, b=20, c=[30,40]
	{a,b} = {a:10, b:20}          # a=10, b=20
	{a,b} = {a:10}                # a=10, b=Undefined
 	```

Chaining

:	Chaining is a variant of line continuation where expressions
	will all be applied on the same value.

	```
	a () :
		b ()
		c ()
	```

	is equivalent to

	```
	let _ = a ()
	_ b ()
	_ c ()
	```
	
 	chains can also be nested

	```
	a:
		b ()
		c () :
			d ()
	```
	
	which equals to

	```
	var _ = a
	a b ()
	_ = a c ()
	_ d ()
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


