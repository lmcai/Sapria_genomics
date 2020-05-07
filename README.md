# Sapria_genomics
Scripts and supplemental material for the assembly and analysis of Sapria genome.

Description of the subdirectories
----------------------
The content of each subdirectory is listed as follows. For detailed description and scripts, please see the README file within each directory.

- **sapria_genome_assembly**
  
  kmer-based genome size estimation
  
  de novo assembly with Supernova using 10X library
 
  scaffolding with the ARKS-LINKS pipeline using long-read data 
- **validation_of_genome_assembly**

  mapping Illumina, nanopore, and transcripts to the assembly
  
  assembly of unmapped Illumina reads
  
  BUSCO assessment
  
  missing BUSCO simulation in the Manihot genome
  
  non-repetitive region size estimation based on read coverage
  
- **annotation**
  
  de novo repeat annotation with repeatModeler and repeatMasker
  
  gene prediction with MAKER
   
  pseudogene annotation with the Shiu Lab pipeline
- **ortholog_clustering**
  
  ortholog group assignment with OrthoFinder
  
  pseudogenes ortholog group assignment for phylogenetic inference
  
- **intron_turnover**
  
  intron length and position characterization
  
  intron turnover rate based on cross-species protein alignment
  
  correlation test of maximum intron length and dN/dS ratio

- **phylogenetic_assessment_of_HGT**
  
  alignment and gene tree reconstruction
  
  custom python script to identify HGT based on phylogeny
  
