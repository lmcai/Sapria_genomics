#!/bin/bash
#SBATCH -J HALtools
#SBATCH -o out
#SBATCH -e err
#SBATCH -p holy-info
#SBATCH -n 1
#SBATCH -t 3000
#SBATCH --mem=40000

# FILES ARE NAMED SUCH THAT THE FIRST SPECIES IS THE REFERENCE, THE SECOND SPECIES IS THE TARGET

HALFILE=/n/holylfs/LABS/informatics/bjarnold/Consults/DavisLab/HGT_pipeline/PHYLOGENY/USING_FINAL_ASSEMBLY/sapriaFinal.hal

module load hal/20160415-fasrc01

halAlignmentDepth \
--inMemory \
--noAncestors \
--targetGenomes Populus \
--outWiggle Sapria_Populus.wig \
--step 1 \
$HALFILE \
Sapria

halAlignmentDepth \
--inMemory \
--noAncestors \
--targetGenomes Manihot \
--outWiggle Sapria_Manihot.wig \
--step 1 \
$HALFILE \
Sapria

halAlignmentDepth \
--inMemory \
--noAncestors \
--targetGenomes Tetrastigma2 \
--outWiggle Sapria_Tetrastigma2.wig \
--step 1 \
$HALFILE \
Sapria
