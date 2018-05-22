@class A

	@event success
	@event failure
	@event foo

	@method succeed
		self ! success (self)

	@method fail reason
		self ! failure (reason)

	@method foo a, b
		self ! failure (a, b)

	@method bind callback
		self !+ failure (callback)

	@method unbind callback
		self !- failure (callback)

	@method once callback
		self !! failure (callback)

	@method custom event, callback
		self !+ (event) (callback)

