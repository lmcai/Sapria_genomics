# Intron turnover in Sapria
The intron length in Sapria exhibits extreme disparity, containing both highly streamlined genes and genes with the longest introns reported in angiosperms. To further investigate the evolutionary driving forces of this divergent selection, we used the following pipeline to characterize the length, turnover rate, and composition of introns. We also test the statistic correlation between intron length and dN/dS ratio.

## Characterization of intron position and length
We used a custom python script `summarize_gene_len_intron_size_from_gff.py` to summarize the gene length, intron number, intron length, and CDS length for each gene. 
```
python summarize_gene_len_intron_size_from_gff.py [input_genome_annotation.gff] [output_prefix.csv]
```
This python script will output two files:

1. a csv file `output_prefix.csv` containing the gene length, intron number, intron length, and CDS length for each gene. 
2. a csv file `output_prefix.distr` containing all intron lengths for plotting purpose.

## Intron turnover in Sapria using cross-species protein alignment

## GO enrichment of highly compact genes
We firstly extracted genes with all introns <150 bp (or without introns) using the python script `get_short_intron_genes_for_selection.py`.

## Intron composition

## dN/dS ratio calculation

## Statistic estimation of correlation significancy break point