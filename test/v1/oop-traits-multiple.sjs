@trait TA
	@property ta = "TA"

@trait TAA: TA
	@property taa = "TAA"
	@constructor
		console log ("HELLO")

@trait TAAA: TAA

@class A: TAAA
	@property a = "A"

