#Filter out scaffolds <10kb and the resulting assembly is Sapria_V1.softmasked_10kb.fa
#1. Build database
~/programs/RepeatModeler-open-1.0.11/BuildDatabase -name Sapria_10k -engine ncbi Sapria_V1.softmasked_10kb.fa
#2. run repeatmodelr
module load RepeatMasker/4.0.5-fasrc05
~/programs/RepeatModeler-open-1.0.11/RepeatModeler -engine ncbi -pa 32 -database Sapria_10k 2>&1 | tee repeatmodeler.log

#Program Time: 34:03:08 (hh:mm:ss) Elapsed Time
#Working directory:  /scratch/lmcai/94_repeat_anno/repeatmodeler/RM_22203.TueJun41951552019
#may be deleted unless there were problems with the run.

#The results have been saved to:
#  Sapria_10k-families.fa  - Consensus sequences for each family identified.
#  Sapria_10k-families.stk - Seed alignments for each family identified.

