#!/bin/bash
#SBATCH -J HALtools
#SBATCH -o out.analyzeWig
#SBATCH -e err.analyzeWig
#SBATCH -p holy-info 
#SBATCH -n 1
#SBATCH -t 3000
#SBATCH --mem=10000


# make sure these wig files are not compressed!
wigs=(`ls ../01_wigFiles/Sapria_*.wig`)

for i in ${wigs[@]}
do
	echo $i
	python3 ../../../bin/02/analyzeWig_byScaff.py $i
done

