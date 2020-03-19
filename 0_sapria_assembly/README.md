Genome assembly
===============

1. Prior to assembly, we preprocessed the sequencing reads using trim_fastq.sh
2. After preprocessing, we verified quality by generating FastQC reports with run_fastqc.sh
3. We assembled genomes with Supernova using supernova.sh
4. We further scaffolded the Supernova assembly based on the linked-reads from 10X library and nanopore reads using the ARKS-LINKS.sh

Subdirectories:

- kmer: contains the scripts and results from jellyfish to estimate the genome size of Sapria
		
		--jellyfish.sh: contains the scripts to run jellyfish to count kmers based on Illumina reads
		
		--*.histo: kmer count result from jellyfish
		
		--geno_size_est.R: R scrip used to estimate the genome size of Sapria and the size of its single-copy regions. This protocol followed the pipeline described on the bioinformatics website from the University of Connecticut (https://bioinformatics.uconn.edu/genome-size-estimation-tutorial/).
		
- busco: contains scripts and output of running BUSCO on the assemblies



- supernova: contains scripts to generate assembly based on the 10X linked-reads library using Supernova
- ARKS-LINKS: contains scripts to run ARKS and LINKS to generate superscaffolds based on 
