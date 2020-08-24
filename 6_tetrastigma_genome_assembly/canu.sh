module load canu/1.8-fasrc01
#low coverage (20X) need to adjust correctedErrorRate
#if not set useGrid=false, automatically submit hundreds of jobs. These jobs may fail because canu do not set the right memory limit. I suggest running it through local machine to get the commands and customize your batch job submission file 
canu -p tetrastigma genomeSize=1.7g useGrid=false correctedErrorRate=0.16 corMaxEvidenceErate=0.15 minReadLength=10000 -nanopore-raw ../../00_nanopore_raw_fastq/Tetrastigma_10k_nanopore.fastq -d .

#or if you have corrected nanopore reads
canu -p tetrastigma genomeSize=1.7g useGrid=false maxMemory=128g maxThreads=16 -nanopore-corrected ../minimap_miniasm_racon/tetra_10k.corr.fas -d .