# BUG: A and B should be equal, in the bug not takes priority over 'or'
var A = A or  not B  or C != D  or E != F
var B = A or (not B) or C != D  or E != F
#
## NOTE: These forms are not output the same way between Sugar1 and Sugar2,
## but they individually have the same effect (but D != E)
## NOTE: Sugar1 gets it wrong again here
var D = A == 0 or  B and C == 0
var E = A == 0 or (B and C) == 0

var G = 1 * 2 + 3
var H = 1 + 2 * 3

# NOTE: Here, sugar2 does get the unary operation right, not sugar1
var I = not 1 or  A
var I = not 1 and A
var I = not 1 + A
