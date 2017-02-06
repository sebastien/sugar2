# Match statement
match value
	== "pouet"
		2
	type? String
		21
	type? Value
		4
	type? Number and _ > 10
		5
	type? Number and _ < 10
		6
	> 0
		7
	*
		9

# Match statement
match value
	== "pouet"
		2
	type? String
		21
	type? Value
		4
	type? Number and _ > 10
		5
	type? Number and _ < 10
		6
	> 0
		7
	*
		9



# Match Expression
let a = 10 match
	> 1
		1
	< 5
		2
	*
		3
