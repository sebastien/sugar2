let A = 1 ; let B = 2 ; let C = 3 ; let E = 4; let F = 5

# BUG: A and B should be equal, in the bug not takes priority over 'or'
var AA = A or  not B  or C != D  or E != F
var AB = A or (not B) or C != D  or E != F
assert AA == AB

## NOTE: These forms are not output the same way between Sugar1 and Sugar2,
## but they individually have the same effect (but D != E)
## NOTE: Sugar1 gets it wrong again here
var BA = A == 0 or  B and C == 0
var BB = A == 0 or (B and C) == 0

assert AA = BB

var C = 1 * 2 + 3
var D = 1 + 2 * 3

# NOTE: Here, sugar2 does get the unary operation right, not sugar1
var E = not 1 or  A
var F = not 1 and A
# FIXME: This is wrong
var G = not 1 + A
