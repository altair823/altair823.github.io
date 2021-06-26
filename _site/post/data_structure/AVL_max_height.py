import sys
def N(h):
	if h == 0:
		return 0
	elif h == 1:
		return 1
	else:
		return N(h-1) + N(h-2) + 1

print(N(int(sys.argv[1])))
