import sys

def count_node(h):
	
	if h == 0:
		return 0
	elif h == 1:
		return 1
	else:
		return count_node(h-1) + 2**((h-1)//2)

print(count_node(int(sys.argv[1])))
