#!/usr/bin/env python

""" 
"""

import sys
import re
import os
from Bio import AlignIO
from collections import defaultdict

#get parent directory of where script is located, as this contains shared functions
sys.path.append( os.path.abspath(__file__ + "/../../") )
import functions as shFn

def getPairWiseDivergenceWindows(pwDiv, winSize, pwDiv_tresh, maxWinSizeByPosition):

	pwDivOutliers = defaultdict(list)
	outlierCount = 0
	for line in pwDiv:
		line = line.strip()
		line = line.split()
		scaff = line[0]
		start = int(line[1])
		end = int(line[2])
		alnBases = int(line[3])
		div = int(line[4])/int(line[3])
		if alnBases == winSize and div <= pwDiv_tresh and (end-start) <= maxWinSizeByPosition:
			outlierCount += 1
			pwDivOutliers[scaff].append( (start, end, div, outlierCount) )	

	return(pwDivOutliers, outlierCount)

def main():

	# pwDiv_file was an analysis previously done between a reference (e.g. Sapria) and a target (e.g. Tetrastigma)
	# Target2 below is the other pairwise alignment you want to query, assuming the reference is the same!
	pwDiv_file = "../02_MAF_2_slidingWindow/concatenatedFiles/Sapria_Tetrastigma2.txt"
	#HALfile = "../../data/sapriaFinal.hal"
	HALfile = "/n/holylfs/LABS/informatics/bjarnold/Consults/DavisLab/HGT_pipeline/PHYLOGENY/USING_FINAL_ASSEMBLY/sapriaFinal.hal"
	scriptDir = os.path.abspath(__file__ + "/../" ) + "/"
	
	Reference = "Sapria"
	Target = "Manihot"
	# scaffold, start, end, # aligned bases, # differences
	pwDiv_tresh = 0.245
	winSize = 100
	maxWinSizeByPosition = 10000

	outDir = "./"
	queue = "holy-info,shared"
	nCores = 1
	time = 200
	mem = 3000

	pwDiv = open(pwDiv_file, 'r')

	pwDivOutliers, outlierCount = getPairWiseDivergenceWindows(pwDiv, winSize, pwDiv_tresh, maxWinSizeByPosition)
	# pwDivOutliers[scaff] = [ (start, end, div, outlierCount) ]
	print("Number of scaffs with outliers: ", len(pwDivOutliers))
	print("Number of outliers: ", outlierCount)

	# for each scaffold with an outlier, print out the MAF file
	#os.system("module load hal/20160415-fasrc01") # for HAL tools, need to call outside, before running python script?
	x = 0
	for scaffold in pwDivOutliers:
		x += 1
		if x == 1:
			command = "module load hal/20160415-fasrc01\n" 
			command = command + "hal2maf --noDupes --refGenome " + Reference + " --refSequence " + scaffold + " "
			command = command + "--targetGenomes " + Target + " "
			command = command + HALfile + " " + scaffold + ".maf\n" 
			for win in pwDivOutliers[scaffold]:
				start = str(win[0])
				end = str(win[1])
				div = win[2]
				command = command + "python3 " + scriptDir + "calculate_divergence.py " + scaffold + ".maf " + Reference + " " + Target + " " + start + " " + end
				command = command + "\n"
			shFn.create_job_script(scaffold, outDir, queue, nCores, time, mem, command)

	sys.exit()


if __name__ == '__main__':
  main()
