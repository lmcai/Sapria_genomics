Genome annotation
===============
Prior to gene model prediction, species-specific repeat library was generated using RepeatModeler. Then repetitive elements was annotated by Repeatmakser in the assembly and transfered to MAKER.

Gene model prediction of Sapria was generated by MAKER based on multiple sources of information including RNAseq, proteoms of closely-related species, and the uniprot-swissprot database. SNAP and AUGUSTUS were used for ab initio gene prediction.

Repeat annotation
------------
In order to improve the performance of species-specific repeat identification, we only include scaffolds longer than 10kb in the RepeatModeler analysis (see Repeatmodeler documentation).

Species-specific repeat library generation: repeatmodeler.sh

Repeat annotation and result summarization: repeatmasker.sh

Evidence-based MAKER annotation run1
------------
The initial MAKER run was based on EST data from four Rafflesiaceae species including Sapria, proteoms from close relatives (Manihot, Populus and Vitis), and uniprot-swissprot database. We especially set the maximum intron size to be 100 kb (split_hit=100000) in MAKER to accomodate the long intron in Sapria. 

MAKER control file: maker_opt.ctl1

ab initio training and MAKER annotation run2
------------
SNAP training script: snap.sh

AUGUSTUS training script: augustus.sh

MAKER control file: maker_opt.ctl2

ab initio retraining and MAKER annotation run3
------------
SNAP was retrained based on the output from run2 following the same method described in snap.sh. We then reran MAKER based on the retrained SNAP model.

MAKER control file: maker_opt.ctl3

Pseudogene annotation with the Shiu Lab pipeline
------------
Detailed documentation of the pipeline can be found on GitHub (https://github.com/ShiuLab/PseudogenePipeline)

Intergenic sequences are extracted using bedtools. Then proteoms from Sapria, Manihot, Populus, and Vitis were aligned to the intergenic sequences using tblastn. Then the python script from Shiu Lab was used to create pseudogene annotation. 

Scripts are provided in makerp.sh
