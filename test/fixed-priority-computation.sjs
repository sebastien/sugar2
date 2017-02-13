AA = typeof(jQuery) != "undefined" and jQuery or extend modules select $
AB = ((typeof(jQuery) != "undefined") and jQuery) or (extend modules select $)
assert (AA == AB)

# FIXME: Ideally, this should not have parens
B = (yr + mo + da + ho + mn + se + ms)

CA = not period or period is FOREVER or not period[0] or not period[1]
CB = (not period) or period is FOREVER or (not period[0]) or (not period[1])
assert (CA == CB)

# if a + 1 == B or C
# 	pass
# end
