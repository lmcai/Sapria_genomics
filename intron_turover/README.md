# Intron turnover in Sapria
The gene length in Sapria exhibits extreme disparity, containing both highly streamlined genes and genes with the longest introns reported in angiosperms. To further investigate the evolutionary driving forces of this divergent selection, we used the following pipeline to characterize the length, turnover rate, and composition of introns. We also test the statistic correlation between intron length and dN/dS ratio.

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

To further investigate the turnover rate (gains and losses) of introns in Sapria, we leveraged the cross-species protein alignment from MAKER annotation to 

## dN/dS ratio calculation
Please see [selection](../selection)

## Statistic estimation of correlation significancy break point