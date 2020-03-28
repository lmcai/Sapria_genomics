#get gene region bed file
grep gene ../sapria/10_maker_annotation_sapria/Sapria_longintron.rnd2_old_snap_evidence_based.GAAS.gff | awk '{print $1,$4,$5}' | sed 's/ /\t/g' | sort -k1,1 -k2,2n | bedtools merge -i - > Sapria_longintron.gene.bed

#get intergenic region bed file
subtractBed -a sap.chrom.sizes -b Sapria_longintron.gene.bed >Sapria_longintron.intergenic.bed

#get sequences of intergenic region
bedtools getfasta -fi ../sapria/10_maker_annotation_sapria/Sapria_V1.softmasked.fa -bed Sapria_longintron.intergenic.bed >Sapria_longintron.intergenic.fas

#blast proteoms of Sapria, Manihot, Populus, Vitis, uniprot against intergenic sequences
makeblastdb -in Sapria_longintron.intergenic.$ID.fas -out SAP${SLURM_ARRAY_TASK_ID} -dbtype nucl
#do not use multi threads in tblastn, core dump error
tblastn -db SAP${SLURM_ARRAY_TASK_ID} -query protein.db.fas -out sap.intergenic.blast.out.${SLURM_ARRAY_TASK_ID} -evalue 1e-5 -outfmt 6

#run Shiu Lab maker-p pipeline
python ~/programs/ShiuLab_pseudo_pkg/pseudo_wrap.py makerp_parameters