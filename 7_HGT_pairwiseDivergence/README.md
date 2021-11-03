These python scripts were used to carry out a window-based analysis of divergence between pairs of taxa in a HAL file. This analysis was carried out
using a series of steps corresponding to the numerically labelled directories within the 'scripts' directory, and these scripts were used to generate
the output within the results directory.

A quirk of this pipeline involves the use of python scripts to parallelize tasks by submitting 1 job (via SLURM) per scaffold. We found this 
dramatically sped up analyses, but also various functions of the HAL utilities performed extremely slow when the species chosen as the reference was
a draft assembly that contained may scaffolds (e.g. Sapria contained > 100k scaffolds).

Thus, in order to submit as few jobs as possible, we first identified scaffolds that contained at least some aligned bases between a pair of species,
which amounted to around ~2k jobs/scaffolds.


The pipeline is broken up into the following components, which correspond to distinct directory names in the results folder:

###
# 01_scaffoldsWithAlignedBases
###
Here we first find which scaffolds for a particular alignment pair actually contain aligned bases. This analysis is split into two parts that first
uses the halAlignmentDepth program to calculate alignment depth and outputs a WIG file. This WIG file is then read by a python script 
(analyzeWig_byScaff.py) to compute how many aligned bases there are for each scaffold. Subsequent analyses are then parallelized by scaffold, but 
only for those scaffolds that actually contained aligned bases.

Within the 01_wigFiles subdirectory, files are in WIG format, and within the 02_scaffolds subdirectory, files are named according to the two species
in the pair and contain 2 columns: scaffold name and number of aligned bases for that scaffold.

###
# 02_MAF_2_slidingWindow
###
In this directory we use the hal2maf program to print a MAF file per scaffold and then feed this file to a python script (maf_2_alignedPos.py) that
does a sliding window analysis, computing the number of aligned bases per window (which should be 100 unless the analysis has reached the end of a
scaffold) as well as the number of aligned bases that differ between the species pair. Since this analysis is carried out by scaffold, all files must 
be concatenated once all jobs have finished. The results for this analysis may be found in the "concatenatedFiles" subdirectory and these files are
named according to the two species used in the pair. Within each file are four columns that contain the scaffold name, start and end coordinate 
(according to the Sapria genome) of the window, the number of aligned bases, and the number of pairwise differences.


###
# 03_analyseOutlierWindowsBetweenAlignments
###
Here we take windows of interest from the previous analysis (02_MAF_2_slidingWindow) and investigate these regions in other pairwise alignments (i.e.
between the parasite Sapria and its two closer relatives: Manihot and Populus). We again use the hal2maf program to output a MAF file for each
scaffold that contains windows below a specified divergence (i.e. 0.245). A python script then reads these MAF files and finds these regions, 
specified in coordinates of the Sapria genome, in these other pairwise alignments.

###
# 04_clusterOutlierWindows
###
This analysis takes outlier windows that are below 0.245 divergence between Sapria and Tetrastigma (and also have no aligned bases between Sapria and
either of its two close relatives, Manihot and Populus) and studies if any of them are within 500bp of one another. If any outlier windows are nearby,
they are combined into a single window with a start and end position that correspond to the start and end positions of the combined windows (i.e. the
start of the leftmost outlier window and the end of the rightmost outlier window)


