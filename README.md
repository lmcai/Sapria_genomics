# Sapria_genomics
Scripts and supplemental material for the assembly and analysis of Sapria genome.

**Disclaimer**: Although we welcome re-use of these materials, except where noted the code we are sharing here is specific to this project and to the Harvard compute cluster. Filenames and paths are often hard-coded in scripts, and software versions/dependencies are often managed via calls to the Harvard Cannon cluster Lmod system.

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

- **selection**

  dN/dS ratio calculation using PAML

- **tetrastigma_genome_assembly**

  nanopore de novo assembly with minimap-miniasm
  
  nanopore de novo assembly with CANU
  
  assembly merging using Quickmerge
  
- **HGT_pairwiseDivergence (Contributor: [Dr. Brian Arnold](https://github.com/brian-arnold))**

  Genome alignment of 10 plant species using Cactus
  
  Sliding window-based analysis of pairwise divergence to detect HGT
  
  Grouping nearby HGT genomic windows into longer blocks
  

- **phylogenetic_assessment_of_HGT**
  
  alignment and gene tree reconstruction
  
  custom python script to identify HGT based on phylogeny
  
