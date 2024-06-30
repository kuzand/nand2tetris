import sys

f1 = open(sys.argv[1], 'r')
f2 = open(sys.argv[2], 'r')

for i, (l1, l2) in enumerate(zip(f1, f2)):
    if l1 != l2:
        raise Exception(f"Comparison error at line {i}: {l1} != {l2}")
print("Comparison succedded!")
f1.close()
f2.close()
