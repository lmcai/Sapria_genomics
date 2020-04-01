printf -v ID "OG%07d" ${SLURM_ARRAY_TASK_ID}
echo $ID
cd /n/holyscratch01/davis_lab/lmcai/sapria/15_orthofinder_seq/aa_aln

module load mafft/7.407-fasrc01
#if there are less than 800 gene copies, use the accurate linsi; otherwise use mafft
gene_num=$((grep '>' $ID.aa.fas| wc -l) 2>&1)
if [ "$gene_num" -lt 500 ]
then
mafft-einsi $ID.aa.fas > $ID.aa.fas.aln
else
mafft $ID.aa.fas > $ID.aa.fas.aln
fi
echo 'aa alignment done...'

cd /n/holyscratch01/davis_lab/lmcai/sapria/15_orthofinder_seq/na_aln
#if there's pseudogene, add pseudogene sequences
FILE=../pseudogene_ortho_assignment/$ID.pseudo.fas
if test -f "$FILE"
then
../pal2nal.pl ../aa_aln/$ID.aa.fas.aln $ID.na.fas -output fasta >$ID.na.fas.nopseudo.aln
mafft --adjustdirection --add $FILE --keeplength $ID.na.fas.nopseudo.aln | sed 's/_R_//g' >$ID.na.fas.aln
else
../pal2nal.pl ../aa_aln/$ID.aa.fas.aln $ID.na.fas -output fasta >$ID.na.fas.aln
fi

ALIGN=$ID.na.fas.aln
if test ! -f "$ALIGN"
then
echo 'pal2nal failed, so I will align DNA directly: ' $ID
cat $ID.na.fas $FILE | mafft-einsi - > $ID.na.fas.aln
#in case pal2nal failed..
fi
echo 'na alignment done...'

#mildly trim the alignment
trimal -in $ID.na.fas.aln -out $ID.na.fas.aln.trimmed.fas -gt 0.15

#fastree
FastTree -nt -gtr < $ID.na.fas.aln.trimmed.fas >$ID.fast.tre

echo 'fasttree done...'

module load gcc/7.1.0-fasrc01 openmpi/3.1.3-fasrc01 iqtree/1.6.10-fasrc02

OUT=$((python ../get_outgroup.py $ID.na.fas.aln) 2>&1)
#model selection currentlt cannot run on multiple mpi
mpirun -np 1 iqtree-mpi -s $ID.na.fas.aln.trimmed.fas -o $OUT -pre $ID -nt AUTO -bb 3000 -bnni -alrt 2000 -nm 3000 -redo

rm $ID.bionj
rm $ID.ckp.gz
rm $ID.uniqueseq.phy
rm $ID.mldist

rm $ID.contree
rm $ID.log
rm $ID.model.gz
rm $ID.splits.nex
rm $ID.ufboot
