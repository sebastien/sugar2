@feature sugar 2
@module reference
| This exercises the

@class A

	@property type = "A"

	@method doSomething
		return "a:" + type

	@method getDoSomething
		return doSomething

	@method getDoSomethingFromIteration
		for i in 0..10
			return doSomething

	@method getDoSomethingFromClosure
		return {_|doSomething} ()

@class A: B

	@property type = "B"

	@method doSomething
		return "b:" + type

	@method getSuperDoSomething
		return super doSomething

	@method getSuperDoSomethingFromIteration
		for i in 0..10
			return super doSomething

	@method getSuperDoSomethingFromClosure
		return {_|super doSomething} ()

@where

	let a = new A ()
	let b = new B ()

	a doSomething                 ()    == "a.A"
	a getDoSomething              () () == "a.A"
	a getDoSomethingFromIteration () () == "a.A"
	a getDoSomethingFromClosure   () () == "a.A"

	a doSomething                 ()    == "b.B"
	a getDoSomething              () () == "b.B"
	a getDoSomethingFromIteration () () == "b.B"
	a getDoSomethingFromClosure   () () == "b.B"

	a getSuperDoSomething              () () == "a.B"
	a getSuperDoSomethingFromIteration () () == "a.B"
	a getSuperDoSomethingFromClosure   () () == "a.B"

# EOF
