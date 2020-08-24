#!/usr/bin/python -tt

import re
import sys
import os
from collections import defaultdict

def main():

	wigName = sys.argv[1]
	# wigfile1 containes the number of unique target genomes the reference mapped to
	# wigfile2 contains the total number of sequences including duplicates: the "height" of the MAF block

	aligned = defaultdict(int) 
	currScaff = ""
	alignedPosCounter = defaultdict(int)

	with open(wigName, 'r') as wig1:
		for line in wig1:
			line = line.strip()
			if line.startswith("fixedStep"):
				#encountered new scaffold
				line = line.split()
				scaff = line[1]
				scaff = scaff.replace("chrom=", "")
				currScaff = scaff
			else:
				if int(line) == 1:
					aligned[currScaff] += 1
	wig1.close()

	fn = wigName
	fn = fn.split("/")
	fn = fn[-1] 
	fn = fn.replace(".wig","")
	o = open(fn, 'w')
	for scaff in aligned:
		print(scaff, aligned[scaff], file=o)
	o.close()

if __name__ == '__main__':
	main()
