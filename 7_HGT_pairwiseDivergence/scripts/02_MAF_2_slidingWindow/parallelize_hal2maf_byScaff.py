#!/usr/bin/python -tt

import re
import sys
import os
#get parent directory of where script is located, as this contains shared functions
sys.path.append( os.path.abspath(__file__ + "/../../") )
import functions as shFn

def main():

	reference = sys.argv[1] 
	target = sys.argv[2] 
	scaffWithAlignedSeq_file = sys.argv[3] #"Sap_v_Mani_aln"
	minAlignedPos = 10
	scriptDir = os.path.abspath(__file__ + "/../" ) + "/"

	# the following file contains a list of Sapria scaffolds and how many positions aligned to target genome
	# only submit jobs for these scaffolds, which are far fewer than total number of scaffs

	#queue = "shared"
	queue = "holy-info"
	time = 300
	mem = 20000
	nCores = 1
	outDir = "./"

	#HALfile = "../../data/sapriaFinal.hal"
	HALfile = "/n/holylfs/LABS/informatics/bjarnold/Consults/DavisLab/HGT_pipeline/PHYLOGENY/USING_FINAL_ASSEMBLY/sapriaFinal.hal"

	# get scaffolds with aligned sequence
	scaffsWithAlignedSeq = []
	f = open(scaffWithAlignedSeq_file, 'r')
	for line in f:
		line = line.split()
		if int(line[1]) >= minAlignedPos:
			scaffsWithAlignedSeq.append(line[0])
	f.close()

	count = 0
	for scaffold in scaffsWithAlignedSeq:
		count += 1
		if count == 1:
			command = "module load hal/20160415-fasrc01\n"
			command = command + "hal2maf --noDupes --refGenome " + reference + " --refSequence " + scaffold + " "
			command = command + "--targetGenomes " + target + " "
			command = command + HALfile + " " + scaffold + ".maf\n"
			command = command + "python3 " + scriptDir + "maf_2_alignedPos.py " + scaffold + ".maf " + reference + " " + target + "\n"
		
			print(scaffold)
			#print(command)
			shFn.create_job_script(scaffold, outDir, queue, nCores, time, mem, command)	

if __name__ == '__main__':
  main()
