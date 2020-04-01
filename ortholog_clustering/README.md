Ortholog clustering
===================

OrthoFinder
--------------------
We used OrthoFinder to assign ortholog groups for 38 species that are widely sampled across angiosperm phylogeny
```
#generate blast command to distribute jobs more efficiently
orthofinder.py -f [direcotory containing proteoms] -op
#run orthofinder to only assign orthologs but not generate alignments and trees
orthofinder.py -b WorkingDirectory/ -t 8 -a 8 -og
```		
The resulting ortholog group assignment was used to assess gene loss in Sapria.
