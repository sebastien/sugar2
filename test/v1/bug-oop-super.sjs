# @class A
# 	@method a
#
# @class B: A
#
# 	@constructor
# 		# BUG: Super is called twice
# 		super ("XXX")

@class A
	@event Foo
	@event Bar
	@constructor
		Foo !+ {console log "Foo"}
		Bar !+ {console log "Bar"}
