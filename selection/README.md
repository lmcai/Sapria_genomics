# Selection analysis with PAML

We used PAML to calculate the dN/dS ratio for the each branch in the following tree under a free ratio model


                     /-Rafflesia_cantleyi (Rafflesiaceae)
                  /-|
               /-|   \-Rafflesia_tuan-mudae (Rafflesiaceae)
              |  |
            /-|   \-Rhizanthes_zippelii (Rafflesiaceae)
           |  |
         /-|   \-Sapria_himalayana (Rafflesiaceae)
        |  |
        |  |   /-Manihot (Malpighiales)
      /-|   \-|
     |  |      \-Jatropha (Malpighiales)
   /-|  |
  |  |   \-Populus (Malpighiales)
--|  |
  |   \-Arabidopsis (Malvales)
  |
   \-Glycine (Fabales)

##PAML input preparation

- **Get one representative sequence per lineage**

For each gene tree, we subsample monophyletic lineages containing the above species to conduct the PAML analysis. We only choose one representative sequences from each species. Tree subsampling script `prune_paralogs_RT.py` from Ya Yang's [phylogenomic_dataset_construction](https://bitbucket.org/yangya/phylogenomic_dataset_construction/src/master/) package was used to achieve this.
```
python yangya-phylogenomic_dataset_construction-489685700c2a/prune_paralogs_RT.py [input tree dir] .treefile [output dir] 3 species.list 
```
- **Sequence extraction**
Then we used custom python script `get_VGT_Raff_for_paml.py` to further filtered these subsampled trees to require them to contain Sapria, at least one Malpighiales species, and at least one outgroup species (Arabidopsis and Glycine). We also used this script to extract DNA and protein seuqences.

- **Alignment**

We used MAFFT-einsi to align protein sequences and then transfer the protein alignment to codon alignment using pal2nal.

##PAML
