#!/usr/bin/env python

""" 
The first step with working with gffutils involves importing the gff file into a local sqlite3 file-based database.
"""

import sys
import re
import os
from Bio import AlignIO
from collections import defaultdict

def overlaps(a, b):
        """
        Return the amount of overlap, in bp
        between a and b.
        If >0, the number of bp of overlap
        If 0,  they are book-ended.
        If <0, the distance in bp between them
        """
        return min(a[1], b[1]) - max(a[0], b[0]) 

def main():

	fn = sys.argv[1]
	reference = sys.argv[2]
	target = sys.argv[3]
	start = int(sys.argv[4])
	end = int(sys.argv[5])
	f = AlignIO.parse(fn, "maf")

	scaffold = fn.replace(".maf", "")
	alnBasesOverlap = 0
	divergence = 0
	for multiple_alignment in f:
		
		"""
		if len(multiple_alignment) >= 3:
			tmp = []
			for i in multiple_alignment:
				tmp.append(i.name.split("."))
			print(tmp)
		"""

		if len(multiple_alignment) > 1:
			refCount = 0
			targetCount = 0

			refName = multiple_alignment[0].name.split(".")
			"""
			for i in range(len(multiple_alignment)):
				name = multiple_alignment[i].name.split(".")
				if name[0] == reference:
					refCount += 1
				if name[0] == target:
					targetCount += 1
			print(refCount, targetCount)
			"""
			# if paralogs, just get first target sequence for now; could look at all later
			# with hal2maf run with --noDupes, Ref seqs will never be aligned to other Ref seqs, 
			# but may still be aligned to multiple target seqs
			targetName = multiple_alignment[1].name.split(".")
			"""
			for i in range(len(multiple_alignment)):
				targetName = multiple_alignment[i].name.split(".")
				if targetName[0] == target:
					break
			"""
			# sanity check
			if refName[0] == reference and targetName[0] == target:
				refSeq = multiple_alignment[0]._seq.upper()
				targetSeq = multiple_alignment[1]._seq.upper() 
				refSeqLen = len(str(refSeq).replace("-","")) # ungapped length of reference sequence
				refStart = multiple_alignment[0].annotations["start"]
				refEnd = multiple_alignment[0].annotations["start"] + refSeqLen # end in corrdinates of ref sequence
				posInRef = refStart - 1
				o = overlaps((start,end), (refStart,refEnd))
				if o > 0:
					for i in range(len(refSeq)):
						if refSeq[i] != "-":
							posInRef += 1
							#if posInRef >= start and posInRef <= end:
							#	print(targetSeq[i])
							if targetSeq[i] != "-":
								if refSeq[i] != "N" and targetSeq[i] != "N":
									# both ref and target seqs contain nucleotides
									if posInRef >= start and posInRef <= end:
										alnBasesOverlap += 1
										if refSeq[i] != targetSeq[i]:
											divergence += 1

	outName = scaffold + "_" + str(start) + "_" + str(end) + "_overlaps.txt"
	o = open(outName, 'w')	
	if alnBasesOverlap == 0:
		divergence = "NA"
	print(scaffold, str(start), str(end), alnBasesOverlap, divergence, file=o)


	o.close()

	sys.exit()


if __name__ == '__main__':
  main()
