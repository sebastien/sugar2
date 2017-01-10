# BUG: Bitwise operators are not converted
v = (v << 8) || (byte ())
v = (v << 8) && (byte ())
