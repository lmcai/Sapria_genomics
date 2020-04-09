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

Identify HGT candidates in gene trees
--------------------
We used a custom python script `VGT_HGT_classification_for_prerooted_tree.py` to identify candidate of horizontally transfered genes. This python script will pass all tree files within a folder and output `VGT.senario.tsv` which contains, for each gene per line, vertically transmitted Sapria genes and horizontally transmitted genes and there donor lineages.

Expand taxon sampling within Vitaceae to investigate former host association
--------------------
A total of 191 gene trees are classified as candidates for Vitatceae-associated HGT. We used BLAST to search for orthologous copies of these genes in the published transcriptomes from 18 Vitaceae species (15 species from [Wen et al. 2013](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0074394); 3 species from [oneKP](https://github.com/ropensci/onekp)).

1. Five representative sequences were randomly chosen from each orthogroup to build BLAST database. This result in the fasta file `HGT_orthogroup_ref.fas`.
2. We used cd-hit to remove redundant sequences with >99% similarity for each transcriptome
```
cd-hit-est -i [inpit] -o [output] -c 0.99 -M 0
```
3. Using BLASTn to find additional orthologous Vitaceae genes with an e value threshold of 1e-40
```
makeblastdb -in HGT_orthogroup_ref.fas -dbtype nucl -out HGT_orthogroup_ref
blastn -task dc-megablast -db HGT_orthogroup_ref -num_threads 16 -query Vitaceae.add.cdhit.fas -outfmt 6 -evalue 1e-40 -out HGT_orthogroup_ref.blast
```
4. Infer alignment and phylogeny for each orthogroup as described above.

Validation of HGT candidates
--------------------
The following criteria were applied to all Vitaceae-associated HGT candidates to identify a confident set of HGTs:
1. Nest within Vitaceae with ultrafast bootstrap support > 80 and SH-aLRT bootstrap support > 80 
2. Branch length <
3. Unambiguous DNA sequence > 150 bp
4. Manual check tree topology to ensure gene tree generally match species tree and the HGT pattern is not driven by paralogous copies

Characterize current and former Vitaceae host
--------------------
