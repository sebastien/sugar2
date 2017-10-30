@feature sugar  2
@feature ecmascript

@class B

	# BUG: The ES backend would output the following line as
	# f (typeof this.id === typeof undefined) {this.id = self.nextID();}
	@property id = nextID ()

	@method nextID
		pass


@where

	let b0 = new B ()
	b id == 0
	let b1 = new B ()
	b id == 1

# EOF
