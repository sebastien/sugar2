let A = 1 if b else 2
let B = 1 if b
let C = 1 else 2
let D = 1 if b else 2
# NOTE: This does not make much sense, but parses anyway
let E = 1 if b if c if d else 2 else 3 else 4
