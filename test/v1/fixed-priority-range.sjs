# BUG: This is interpreted as 0..(10 :: f), because ‥ is an enumeration
# and :: and iteration, so they don't appear as computations.
# NOTE: It's easier to run it through -Diterate
0..A :: f
