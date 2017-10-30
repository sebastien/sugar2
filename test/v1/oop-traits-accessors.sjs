@trait TA

	@property _value = "XXX"

	@getter value
		return _value

	@setter value value
		self _value = value

@class A: TA

	@method m
		return value

@class B: TA

	@setter value value
		self _value = "B" + value




# BUG: Getter/setters would be not be inherited
assert (new A() value, "XXX")

# BUG: Redefining a settter would remove the preceding getter
assert (new B() value, "XXX")
