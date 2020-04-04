Phylogenetic assessment of HGT
=================================
We inferred phylogeny tree for each orthogroup to assess horizontal gene transfer.

Adding pseudogenes to orthogroup
--------------------
We first filtered pseudogenes by length (> 150 bp) and collinearity to protein sequences (no structural change) for better phylogeny inference results. Sequences meet the criteria were extracted using `pseudogene_sequence_output.py`.

Pseudogenes were compared with each orthogroup using BLAST. Representative sequences from each orthogroup was extracted using `sap_ortho_filter.py`. Sequences exhibit significant similarity (evalue<1e-40) were then added to each orthogroup for downstream analysis.
```
makeblastdb -in orthogroup_ref.fas -dbtype nucl -out orthogroup_ref
blastn -task dc-megablast -db orthogroup_ref -num_threads 16 -query sap_longintron.pseudogene.fas -outfmt 6 -perc_identity 40 -evalue 1e-40 -out orthogroup.pseudogene.blast.out
#get the best orthogroup assignmentn for each pseudogene
export LC_ALL=C LC_LANG=C; sort -k1,1 -k12,12gr -k11,11g -k3,3gr orthogroup.pseudogene.blast.out >orthogroup.pseudogene.blast.srt
python filter_sorted_blast_for_top_number_hits.py orthogroup.pseudogene.blast.srt 1
```

Filter orthogroup for phylogenetic reconstruction
--------------------
We used the custom python script `sap_ortho_filter.py` to filter for orthogroups suitable for phylogenetic assessment of HGT based on following criteria:

1. Contain at least one gene or pseudogene from Rafflesiaceae
2. Contain at least 10 species and at least one non-Rafflesiaceae Malpighiales species for hypothesis testing
3. Contain less than 1000 orthologs from all species

Alignment and phylogeny inference
--------------------
Protein sequences were aligned with mafft using the E-INS-i algorithm, which can align several conserved motifs embedded in long unalignable regions. We then use pal2nal to align DNA sequences based on protein alignments. We also added pseudogene sequences to the alignment subsequently using 'mafft --add'. The alignments were then trimmed with trimal to remove sites containing >85% gaps.

We infer Maximum Likelihood (ML) phylogeny of each orthogroup with IQTREE. We applied 3000 [ultrafast](http://www.iqtree.org/doc/Tutorial) bootstrap replicates and 2000 [SH-aLRT](http://www.iqtree.org/doc/Tutorial) bootstrap replicates.

The script used for alignment and tree inference is provided in `mafft_palnal_trimal_fasttree_iqtree.sh`.

Pass gene tree to identify HGT candidates
--------------------
We used a custom python script `VGT_HGT_classification_for_prerooted_tree.py` to identify candidate of horizontally transfered genes. This python script will pass all tree files within a folder and output `VGT.senario.tsv` which contains, for each gene per line, vertically transmitted Sapria genes and horizontally transmitted genes and there donor lineages.
 