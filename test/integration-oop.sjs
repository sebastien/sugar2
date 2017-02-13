@feature sugar 2
@module  oop
| An integration test that exercises class/instance attributes and methods
| as well as super.

@class A

	@shared   TYPE = "A"

	@property type = "a"

	@operation GetTYPE
		return TYPE

	@method getTYPE
		return TYPE

	@method getType
		return type

@class B: A

	@shared   TYPE = "B"
	@property type = "b"

	@operation SuperGetTYPE
		return super GetTYPE ()

	@operation superGetTYPE
		return super getTYPE ()

	@operation superGetType
		return super getType ()

@where
	let a = new A ()
	let b = new B ()

	a GetTYPE () == "A"
	a getTYPE () == "A"
	a getType () == "a"

	b GetTYPE () == "B"
	b getTYPE () == "B"
	b getType () == "b"

	b SuperGetTYPE () == "B"
	b superGetTYPE () == "B"
	b superGetType () == "b"













