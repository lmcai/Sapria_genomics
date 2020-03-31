Validation of the Sapria genome assembly
===============
We used a variety of methods to assess the completeness of the Sapria genome assembly.

##1.	Reads mapping

- We align Illumina reads to the assembly with bwa

		bwa mem -t32 -p -C Sapria_V1.fa barcoded.fastq.gz | samtools sort -@16 -t -o Sapria_V1.reads.sort.bam
		samtools view -f 4 -b Sapria_V1.reads.sort.bam | samtools bam2fq >Sapria_V1.unmapped.fastq	
		12,729,388 out of 1,299,944,392 (0.9%) reads are not mapped

- We align nanopore reads to the assembly with minimap2

		minimap2 -ax map-ont -t 16 Sapria_V1.fa Sapria_nanopore.fastq >Sapria_V1.nanopore.sam
		162,737 out of 5,501,706 (2.9%) reads are not mapped

- We align transcripts to the assembly with GMAP
		
		gmap_build -d Sapria_GMAP_db Sapria_V1.fa
		gmap -D . -d Sapria_GMAP_db Sapria.transcripts.fasta -S >GMAP.sum
		147 out of 16,366 (0.9%) transcripts are not mapped
		
##2.	Assembly of unmapped Illumina reads

Unmapped reads were extracted, trimmed, and assembled into unitigs. All unitigs longer than 300bp and were compared to the NCBI non-redundant nucleotide database using BLAST to identify the closest known matching sequence. 

##3.	BUSCO assessment

The completeness of the Sapria assembly was mapped against 1,440 conserved plant BUSCO.v3 and 303 conserved eukaryotic [BUSCO.v3](https://busco.ezlab.org/).

We also assessed functional biases in missing plant BUSCOs. Orthologs from Arabidopsis for each BUSCO was determined by BLAST and subsequently used for GO analysis on [PlantRegMap](http://plantregmap.cbi.pku.edu.cn/go.php).

##4.	Simulate missing data in Manihot genome and assess functional bias in missing BUSCOs

We simulated 64% missing data in the Manihot reference genome by randomly subsample its contig. 64% is the maximum estimated proportion of missing data in the Sapria assembly based on the flow cytometry genome size estimation (1.28 Gb assembly / 3.5 Gb genome).

We subsequently ran BUSCO on the simulated assembly and the result indicated same level of missing BUSCO (55%). We conducted the same GO analysis for these missing BUSCOs described above to examine any functional category enrichment.

##5.	Estimation of non-repetitive regions of the assembly based on read base coverage

We summarized the base coverage for each site in the assembly to determine the size of non-repetitive regions. This result was compared to the estimated non-repetitive region size in the genome based on [kmer distribution](../0_sapria_genome_assembly/kmer).
```
module load bedtools2/2.26.0-fasrc01
bedtools genomecov -bga -ibam Sapria_V1.reads.sort.bam>Sapria_V1.10XIllumina.cov.bed
#then read the bed file in python and generate a hostogram file for base coverage distribution
#Based on the site coverage histogram, peak coverage is 60.2 X (See Fig. S#). Assuming regions within (0,120) are non-repetitive regions, 904 Mb out of 1.119Gb are non-repetitive in the current assembly	
```
Description of subdirectories
------------
- unmapped_reads: contains scripts used to assemble unmapped Illumina reads and automatically BLAST against the NCBI non-redundant nucleotide database
- busco: contains scripts to run BUSCO on the assembly and detailed output from BUSCO containing and its Arabidopsis ortholog
- manihot_simulation: full BUSCO output on the simulated Manihot assembly and GO enrichment results