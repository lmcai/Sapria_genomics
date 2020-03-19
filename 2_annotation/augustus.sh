#load modules
module load bedtools2/2.26.0-fasrc01

#extract mRNA and 1000bp on 3’ and 5’ side from run1
awk -v OFS="\t" '{ if ($3 == "mRNA") print $1, $4, $5 }' ../snap_rnd1/Sapria_longintron.rnd1.all.gff | \
  awk -v OFS="\t" '{ if ($2 < 1000) print $1, "0", $3+1000; else print $1, $2-1000, $3+1000 }' | \
  bedtools getfasta -fi ../Sapria_V1.softmasked.fa -bed - -fo sapria.maker.round1.transcripts1000.fasta


#augustus in BUSCO
#set up env variables
module load centos6
module load BUSCO/3.0.2-fasrc01
export AUGUSTUS_CONFIG_PATH=/n/home08/lmcai/programs/Augustus/config/

#run BUSCO 
python ~/programs/busco/scripts/run_BUSCO.py -i sapria.maker.round1.transcripts1000.fasta \
 -o sapria_rnd1_augustus -l /n/holyscratch01/davis_lab/lmcai/embryophyta_odb9 -m genome -c 20 --long \
 -sp arabidopsis -z --augustus_parameters='--progress=true'
#~24h
INFO    Results:
INFO    C:25.5%[S:24.7%,D:0.8%],F:8.2%,M:66.3%,n:1440
INFO    367 Complete BUSCOs (C)
INFO    355 Complete and single-copy BUSCOs (S)
INFO    12 Complete and duplicated BUSCOs (D)
INFO    118 Fragmented BUSCOs (F)
INFO    955 Missing BUSCOs (M)
INFO    1440 Total BUSCO groups searched


cd run_sapria_rnd1_augustus/augustus_output/retraining_parameters/
rename BUSCO_sapria_rnd1_augustus_3756819707 sapria_constrictor *


#sed -i 's/BUSCO_Bcon_rnd2_maker_2277442865/Boa_constrictor/g' Boa_constrictor_parameters.cfg
sed -i -- 's/BUSCO_sapria_rnd1_augustus_3756819707/sapria_constrictor/g' sapria_constrictor_parameters.cfg
sed -i -- 's/BUSCO_sapria_rnd1_augustus_3756819707/sapria_constrictor/g' sapria_constrictor_parameters.cfg.orig1


mkdir $AUGUSTUS_CONFIG_PATH/species/sapria_constrictor
cp sapria_constrictor*  $AUGUSTUS_CONFIG_PATH/species/sapria_constrictor/