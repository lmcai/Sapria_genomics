#!/bin/bash
#SBATCH -J halSnps
#SBATCH -o out
#SBATCH -e err
#SBATCH -p holy-info
#SBATCH -n 1
#SBATCH -t 3000
#SBATCH --mem=10000

SCRIPT_DIR=../../bin/02
SCAFFOLDS_DIR=../01_scaffoldsWithAlignedBases/02_scaffolds
# give this script the name of the reference genome, target genome, and the file that shows which scaffolds actually contain aligned bases, in order
# to restrict analyses to scaffolds with data.
python3 ${SCRIPT_DIR}/parallelize_hal2maf_byScaff.py \
Sapria \
Populus \
${SCAFFOLDS_DIR}/Sapria_Populus

