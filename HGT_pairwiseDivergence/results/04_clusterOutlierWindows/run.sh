#!/bin/bash
#SBATCH -J clustOutliers
#SBATCH -o out
#SBATCH -e err
#SBATCH -p holy-info
#SBATCH -n 1
#SBATCH -t 3000
#SBATCH --mem=10000


SCRIPT_DIR=../../bin/04
FILE_DIR=../../results/03_analyseOutlierWindowsBetweenAlignments/SvT_divergence_0.245
minDists=(500)
for m in ${minDists[@]};
do
python3 ${SCRIPT_DIR}/clusterOutlierWindows.py $FILE_DIR/HGTcandidates_notPresIn_ManPop $m
done





