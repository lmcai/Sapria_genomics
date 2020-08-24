#!/usr/bin/python -tt

import re
import sys
import os
from collections import defaultdict

def main():

	fn = sys.argv[1]
	# IT IS ASSUMED THAT THIS FILE IS SORTED BY POSITION WITHIN SCAFFOLDS!
	minDist = int(sys.argv[2])

	# these quantify the number of outlier windows in each category
	# singletons refer to outlier windows that were not clustered (or physically nearby) other windows
	# runs refer to outlier windows that were clustered together based on their end points being within "minDist" distance (in bp)
	outliers_total = 0
	outliers_runs = 0
	outliers_singletons = 0

	midPts = defaultdict(list)
	endPts = defaultdict(list)
	f = open(fn, 'r')
	for line in f:
		line = line.strip()
		line = line.split()
		scaff = line[0]
		start = int(line[1])
		end = int(line[2])
		pos = start + (end-start)/2

		outliers_total += 1
		midPts[scaff].append(pos)
		endPts[scaff].append((start, end))
		
	# COLLECT DISTANCES BETWEEN ADJACENT WINDOWS
	Results = []
	orphanOutliers = 0
	for scaff in midPts:
		if len(midPts[scaff]) > 1:
			for i in range(len(midPts[scaff]) - 1):
				x = midPts[scaff][i+1]-midPts[scaff][i]
				Results.append(x)
		else:
			orphanOutliers += 1
	print("orphan outliers: ", orphanOutliers)

	outName = fn.split("/")[-1].replace(".txt", "")
	outName = outName + "_DistBtWindows.txt"
	o = open(outName, 'w')
	for x in Results:
		print(x, file=o)
	o.close()

	
	# INFER HGT LENGTHS BY RUNS OF LOW DIVERGENCE
	Runs = defaultdict(list) # keeps track of indices for EACH run, a list of lists per scaff
	Runs_all = defaultdict(list) # keeps track of all indices involved in runs, just one list per scaff
	Singletons = defaultdict(list)
	for scaff in endPts:
		# each element in Runs list represents an element that is close to it's next neighbor
		# to get Sapria coords, use the start of the 0th element, end of the last+1 element
		# e.g. x = currRun[0], y=currRun[-1]+1
		# start = endPts[scaff][x][0], end = endPts[scaff][y][1]
		length = len(endPts[scaff])
		if length > 1:
			currRun = [] # this list aggregates nearby outlier windows, and gets cleared below when the next outlier window is too distant
			for i in range(length - 1): # subtract 1 because always looking at next element
				dist = endPts[scaff][i+1][0] - endPts[scaff][i][1]
				if dist < 0:
					print("distance b/t outliers less than zero, file format issue!!")
				if dist <= minDist:
					currRun.append(i)
					Runs_all[scaff].append(i)
					if i == (length-2): # i.e. last iteration
						# if 2nd to last window, add to current run here if last window also nearby 
						# if 2nd to last and last window aren't part of same run, this gets processed below
						currRun.append((i+1))
						Runs_all[scaff].append((i+1))
						Runs[scaff].append(currRun)
						outliers_runs += len(currRun)
				if dist > minDist:
					if len(currRun) > 0:
						# curr element is last of run
						currRun.append(i)
						Runs_all[scaff].append(i)
						Runs[scaff].append(currRun)
						outliers_runs += len(currRun)
					currRun = []

	outName = fn.split("/")[-1].replace(".txt", "")
	outName = outName + "_RunTractLens_" + str(minDist) + ".txt"
	o = open(outName, 'w')
	print("scaff start end length NumWin", file=o)
	for scaff in Runs:
		for currRun in Runs[scaff]:
			if len(currRun) >= 1:
				x = currRun[0]
				y = currRun[-1]
				start = endPts[scaff][x][0]
				end = endPts[scaff][y][1]
				print(scaff, start, end, (end-start), len(currRun), file=o) 
	o.close()

	outName = fn.split("/")[-1].replace(".txt", "")
	outName = outName + "_Singletons_" + str(minDist) + ".txt"
	o = open(outName, 'w')
	print("scaff start end length", file=o)
	for scaff in endPts:
		for i in range(len(endPts[scaff])):
			if i not in Runs_all[scaff]:
				outliers_singletons += 1
				start = endPts[scaff][i][0]
				end = endPts[scaff][i][1]
				print(scaff, start, end, (end-start), file=o) 
	
	o.close()
	print("outliers_total: ", outliers_total)
	print("outliers_runs: ", outliers_runs)
	print("outliers_singletons: ", outliers_singletons)
	sys.exit()

if __name__ == '__main__':
  main()
