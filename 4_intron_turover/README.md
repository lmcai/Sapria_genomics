# Intron turnover in Sapria
The gene length in Sapria exhibits extreme disparity, containing both highly streamlined genes and genes with the longest introns reported in angiosperms. To further investigate the evolutionary driving forces of this divergent selection, we used the **evidence-based gene annotation from MAKER** to characterize the length, turnover rate, and composition of introns. We also test the statistic correlation between intron length and dN/dS ratio.

## Characterization of intron position and length
1. **Gene-wise characters**

We used a custom python script `summarize_gene_len_intron_size_from_gff.py` to summarize the gene length, intron number, intron length, and CDS length for each gene.
```
python summarize_gene_len_intron_size_from_gff.py [input_genome_annotation.gff] [output_prefix.csv]
```
This python script will output a csv file `output_prefix.csv` containing the gene length, intron number, intron length, and CDS length for each gene. 


2. **Intron-wise characters**

We used a custom python scrip `get_intron_position_from_gff.py` to summarize the positions and length of each intron. The output is a tab delimited file bed file `intron_pos.bed` containing staffold ID, start position, end position, and gene name of each intron.

```
python get_intron_position_from_gff.py [input_genome_annotationgff] [intron_pos.bed]
```
## GO enrichment of highly compact genes
We firstly extracted highly compact genes with all introns <150 bp (or without introns) in the `intron_pos.bed` file.

We then identified the best-matching orthologs from Manihot/Populus for each highly compact Sapria genes using BLAST.
```
makeblastdb -in sapria_compact_genes.fa -dbtype nucl -out sapria_compact_genes
blastn -task dc-megablast -db sapria_compact_genes -num_threads 1 -query Mes.cds.fas -outfmt 6 -evalue 1e-40 -out sapria_compact_genes2mes.blast
#get top blast result
export LC_ALL=C LC_LANG=C; sort -k1,1 -k12,12gr -k11,11g -k3,3gr sapria_compact_genes2mes.blast >sapria_compact_genes2mes.blast.srt
python filter_sorted_blast_for_top_number_hits.py sapria_compact_genes2mes.blast.srt 1
```
We then conducted GO enrichment analysis for highly compact genes using the Manihot/Populus orthologs using the [PlantRegMap web server](http://plantregmap.cbi.pku.edu.cn/go.php).

## TE activities in introns
To investigate TE activities in introns, we used `bedtools` to calculate the total sizes of introns that have been annotated as 'intron' by RepeatMaker. 
1. Maker a bed file of repeat annotation
```
#sapria.scaffolds.fa.out is the output from repeatmasker containing positions and classifications of repeats
awk -v OFS='\t' '{print $5, $6,$7,$11}' sapria.scaffolds.fa.out >sapria.scaffolds.fa.repeatmasker.bed
```
2. Use bedtools to get intronic regions intersect with the repeat annotation and calculate the total size

For introns longer than 1000 bp:

```
#filter the intron_pos.bed to get positions of intron longer than 1000 bp:sapria.intron_long1000.bed
#summarize total size using bedtools
bedtools intersect -a sapria.scaffolds.fa.repeatmasker.bed -b sapria.intron_long1000.bed | sort -k1,1 -k2,2n | bedtools merge | awk '{ sum += ($3 - $2) } END { print sum}'
89,596,714
awk '{ sum += ($3 - $2) } END { print sum}' sapria.intron_long1000.bed
121,107,309
74.0% length of these >1kb introns are identified as repeats

```

For introns shorter than 1000 bp:

```
#filter the intron_pos.bed to get positions of intron shorter than 1000 bp:sapria.intron_short1000.bed
#summarize total size using bedtools
bedtools intersect -a sapria.scaffolds.fa.repeatmasker.bed -b sapria.intron_short1000.bed | sort -k1,1 -k2,2n | bedtools merge | awk '{ sum += ($3 - $2) } END { print sum}'
814,879
awk '{ sum += ($3 - $2) } END { print sum}' sapria.intron_short1000.bed
4,070,409
20.0% length of these <1kb introns are identified as repeats
```

## Intron turnover in Sapria using cross-species protein alignment

To further investigate the turnover rate (gains and losses) of introns in Sapria, we leveraged the cross-species protein alignment from MAKER annotation to compare the intron positions in Sapria to that from Manihot and Populus.

1. The custom python script `intron_length_comparison_with_intersp_protein2genome.py` was used to extract homologous positions of Sapria introns on Manihot/Populus proteins using MAKER gff output.

```
python intron_length_comparison_with_intersp_protein2genome.py
```
This python script will output two tab delimited files:

i. `rnd1_protein2genome.sum_by_intron.tsv` contains position information of each annotated intron based on cross-species protein alignment:

```
prot_aln_ID	scaffold	start	end	type	5_end_intron_ID	protein_hit	protein_corrd	alignment_note
ALN_1	scaffold10004_11099	3524	4044	prot_match	-	Manes.08G163400.1	2..175	M153 R2 M1 R1 M21
ALN_2	scaffold10004_11099	3506	4044	prot_match	-	Potri.013G005600.1	2..181	M159 R2 M1 R1 M21
ALN_3	scaffold10004_11099	3512	4044	prot_match	-	Potri.018G013700.1	2..179	M157 R2 M1 R1 F2 M20
ALN_4	scaffold10004_11099	3506	3982	prot_match	-	Potri.015G142600.1	23..181	M159

```

ii. `rnd1_protein2genome.sum_by_gene.tsv` summarizes counts of intron gains and losses based on cross-species protein alignment:

```
prot_aln_ID	scaffold	start	end	prot_name	intron_gain	intron_loss	ancestral_intron_num	sap_intron_num	aln_quality	raw_aln_annotation
ALN_1	scaffold10004_11099	3524	4044	Manes.08G163400.1	0	5	5	0	bad	M153 R2 M1 R1 M21
ALN_2	scaffold10004_11099	3506	4044	Potri.013G005600.1	0	4	5	0	bad	M159 R2 M1 R1 M21
ALN_3	scaffold10004_11099	3512	4044	Potri.018G013700.1	0	7	7	0	bad	M157 R2 M1 R1 F2 M20
ALN_4	scaffold10004_11099	3506	3982	Potri.015G142600.1	0	1	1	0	good	M159
```

2. Multiple proteins can be aligned to a single gene region in Sapria. To take a conservative measure of intron turnover in Sapria, we only chose the protein alignment that invoke the least number of gene structure change. We applied the following filtering criteria:

i. For each gene predicted by MAKER annotation, the mapped regions of the Manihot/Populus protein exceed 80% of the total protein length. 

ii. For each maker gene, the protein alignment with least number of intron gains and losses is chosen. 

```
python extract_high_confidence_protein2genome_one_per_gene.py
```

This outputs a file named `Sapria_longintron.rnd1_rerun.maker.best_protein2genome.80prot_len.tsv`:
```
Gene_ID	Aln_ID	scaffold	start	end	protein_name	intron_gain	intron_loss	intron_num_in_ref_sp	intron_num_in_sapria	note
maker-scaffold65_2763911-exonerate_est2genome-gene-0.13-mRNA-1	ALN_144233	scaffold65_2763911	2028383	2104681	Potri.018G074500.1	0	1	23	22	bad	M63 F2_R2 M41_M29 F2_R2 M29_M53 F1_R1 M26_M7 I1 M40 F1_R1 M101_M94_M105 F2_R2 M54 F1_R1 M35_M53 F1_R1 M27 I1 M13 F1_R1 M31_M111_M97_M28_M2 I1 M41 F2_R2 M76 F2_R2 M58_M85_M90
maker-scaffold65_2763911-exonerate_est2genome-gene-0.13-mRNA-1	ALN_144237	scaffold65_2763911	2028383	2104681	Manes.16G064000.1	0	1	23	22	bad	M63 F2_R2 M41_M29 F2_R2 M29_M53 F1_R1 M26_M7 I1 M40 F1_R1 M101_M13 D1 M80_M105 F2_R2 M54 F1_R1 M35_M53 F1_R1 M25 I1 M15 F1_R1 M31_M111_M97_M28_M2 I1 M41 F2_R2 M76 F2_R2 M58_M85_M90

```

Summerize the percentage of Sapria genes that experience intron loss:
```
awk '{if ($9>0) print $1}' Sapria_longintron.rnd1_rerun.maker.best_protein2genome.80prot_len.tsv | sort -u | wc -l
2538
awk '{print $1}' Sapria_longintron.rnd1_rerun.maker.best_protein2genome.80prot_len.tsv | sort -u | wc -l
8910
```
A total of 8910 genes have valid protein alignment (>80% aligned protein length). 2538/8920=28.5% genes experience intron loss. 40% of them do not have introns. 

## Correlation of maximum intron length and dN/dS ratio
1. Calculation of dN/dS ratio for each gene

Please see [selection](../selection)

2. Statistic test of correlation between the maximum inton length and dN/dS ratio

We used Pearson's correlation test to identify any significant correlation between the maximum inton length and dN/dS ratio. 

The initial result suggested significant correlation for the entire dataset (p-value 9.9e-12), but insignificant correlation when only considering genes with intron length less than 1000 bp (p-value 0.73). To statistically infer the break point where such correlation become significant, we iteratively infer the p-value of pearson’s correlation using thresholds ranging from 10 to 10,000 bp. The R script is available in `intron_length_selection_pressure.R`.


