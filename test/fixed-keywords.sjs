# BUG: continue, pass and break were not understood as keywords, but variables
for a in 0..10
	if a < 5
		continue
	else
		break
	end
end

for a in 0..10
	pass
end
