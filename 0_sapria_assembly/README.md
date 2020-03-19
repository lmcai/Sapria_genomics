Genome assembly
===============

1. Prior to assembly, we preprocessed the sequencing reads using trim_fastq.sh
2. After preprocessing, we verified quality by generating FastQC reports with run_fastqc.sh
3. We assembled genomes with Supernova using supernova.sh
4. We further scaffolded the Supernova assembly based on the linked-reads from 10X library and nanopore reads using the ARKS-LINKS.sh

Subdirectories:

- kmer: contains the scripts and results from jellyfish to estimate the genome size of Sapria
- busco: contains scripts and output of running BUSCO on the assemblies



- supernova: contains scripts to generate assembly based on the 10X linked-reads library using Supernova
- ARKS-LINKS: contains scripts to run ARKS and LINKS to generate superscaffolds based on 
