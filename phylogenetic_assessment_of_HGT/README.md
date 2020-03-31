Phylogenetic assessment of HGT
=================================
We inferred phylogeny tree for each orthogroup to assess horizontal gene transfer.

Adding pseudogenes to orthogroup
--------------------
We first filtered pseudogenes by length (> 150 bp) and collinearity to protein sequences (no small-scale structural change allowed) for better phylogeny inference results. Sequences meet the criteria were extracted using `pseudogene_sequence_output.py`.

Pseudogenes were compared with each orthogroup using BLAST. Sequences exhibit significant similarity (evalue<1e-30) were then added to each orthogroup for downstream analysis.


Filter orthogroup for phylogenetic reconstruction
--------------------
Following criteria were used to select orthogroups suitable for phylogenetic assessment of HGT:

1. 

Alignment
--------------------

Maximum Likelihood phylogeny
--------------------
