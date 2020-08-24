#!/usr/bin/python -tt

"""
"""

import re
import sys
import os
from Bio import AlignIO
import copy
from collections import defaultdict

def main():

	fn = sys.argv[1]
	reference = sys.argv[2]
	target = sys.argv[3]
	winSize = 100
	f = AlignIO.parse(fn, "maf")

	aligned = []    
	diverged = []    
	winPositions = []    
	alignedPosCounter = -1
	mafStackHeights = defaultdict(int)
	count = 0
	for multiple_alignment in f:
		# length of reference seq in alignment, should be same as others
		if len(multiple_alignment) == 2:
			mafStackHeights[len(multiple_alignment)] += 1
			refName = multiple_alignment[0].name.split(".")
			targetName = multiple_alignment[1].name.split(".")
			# sanity check
			if refName[0] == reference and targetName[0] == target:
				count += 1
				#print(multiple_alignment[0].name, multiple_alignment[1].name)	
				refSeq = multiple_alignment[0]._seq.upper()
				targetSeq = multiple_alignment[1]._seq.upper() 
				startPos = multiple_alignment[0].annotations["start"]
				posInRef = startPos - 1 # this is used to keep track of reference coordinates, in original sequence (i.e. don't count gaps!!!), since these positions will be used to overlap with gene regions detected using the original fasta
				# you subtract 1 so that posInRef == startPos when i == 0 (below)
				for i in range(len(refSeq)):
					if refSeq[i] != "-":
						posInRef += 1
					# only consider aligned positions
					if refSeq[i] != "-" and targetSeq[i] != "-":
						if refSeq[i] != "N" and targetSeq[i] != "N":
							alignedPosCounter += 1
							win = int(alignedPosCounter/winSize)

							if len(aligned) < (win+1):
								aligned.append(1)
								diverged.append(0) # only add 1 if position also SNP (tested below)
								winPositions.append([])
								winPositions[win].append(posInRef)
							else:
								aligned[win] += 1
								winPositions[win].append(posInRef)

							if refSeq[i] != targetSeq[i]:
								diverged[win] += 1
	f.close()

	name = fn
	name = name.replace(".maf","")
	scaffold = name
	name = name + "_slidingWindow.txt"
	o = open(name, 'w')

	for i in range(len(aligned)):
		print(scaffold, winPositions[i][0], winPositions[i][-1], aligned[i], diverged[i], file=o)
	o.close()	
	
	print(count)
	for key in mafStackHeights:
		print(key, mafStackHeights[key])
		
if __name__ == '__main__':
  main()
