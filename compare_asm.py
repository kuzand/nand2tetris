import sys


def compare_files(file1, file2):
	f1 = open(file1, 'r')
	f2 = open(file2, 'r')

	for i, (l1, l2) in enumerate(zip(f1, f2)):
		if l1.strip() != l2.strip():
		    raise Exception(f"Comparison error at line {i + 1}: {l1.strip()} != {l2.strip()}")
	print("Comparison succedded!")

	f1.close()
	f2.close()
	

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python3 {sys.argv[0]} <file1> <file2>")
        sys.exit(1)
    
    compare_files(sys.argv[1], sys.argv[2])
