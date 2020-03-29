Validation of the Sapria genome assembly
===============
We used a variety of methods to assess the completeness of the Sapria genome assembly.

1.	Reads mapping

2.	Assembly of unmapped Illumina reads

Unmapped reads were extracted, trimmed, and assembled into unitigs. All unitigs longer than 300bp and were compared to the NCBI non-redundant nucleotide database using BLAST to identify the closest known matching sequence. 

3.	BUSCO assessment

The completeness of the Sapria assembly was mapped against 1,440 conserved plant BUSCO.v3 and 303 conserved eukaryotic BUSCO.v3 (https://busco.ezlab.org/).

We also assessed functional biases in missing plant BUSCOs. Orthologs from Arabidopsis for each BUSCO was determined by BLAST and subsequently used for GO analysis on PlantRegMap (http://plantregmap.cbi.pku.edu.cn/go.php).

4.	Simulation

5.	Estimation of non-repetitive regions of the assembly based on read base coverage

We summarized the base coverage for each site to determine the size of non-repetitive regions in the assembly. This result was compared to the estimated non-repetitive region size in the genome based on kmer distribution (see ../0_sapria_genome_assembly/kmer).	

Description of subdirectories
------------
- unmapped_reads:
- busco: contains scripts and output of running BUSCO on the assembly
- 