Sapria genome assembly
===============

1. We assembled genomes with Supernova
2. We further scaffolded the Supernova assembly based on the linked-reads from 10X library and nanopore reads using the `ARKS-LINKS.sh`

Description of subdirectories
------------

- kmer: contains the scripts and results from jellyfish to estimate the genome size of Sapria
		
	`jellyfish.sh`: contains the scripts to run jellyfish to count kmers based on Illumina reads
	
	`*.histo`: kmer count result from jellyfish
	
	`genome_size_est.R`: R scrip used to estimate the genome size of Sapria and the size of its single-copy regions. This protocol followed the pipeline described on the [bioinformatics website from the University of Connecticut](https://bioinformatics.uconn.edu/genome-size-estimation-tutorial/).
		
