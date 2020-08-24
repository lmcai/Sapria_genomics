#!/bin/bash
#SBATCH -J overlap
#SBATCH -o out
#SBATCH -e err
#SBATCH -p test
#SBATCH -n 1
#SBATCH -t 300
#SBATCH --mem=10000

SCRIPT_DIR=../../bin/03
python3 ${SCRIPT_DIR}/find_outlier_windows_byScaff.py

