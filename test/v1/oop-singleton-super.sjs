# BUG: S.a super reference only works for a method declared in a class
@class A
	@method a
		return "a"

@singleton S: A

	@method a
		return super a ()
