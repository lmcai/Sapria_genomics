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
#BUSCO screen output
#INFO    C:32.9%[S:32.2%,D:0.7%],F:4.7%,M:62.4%,n:1440
#INFO    474 Complete BUSCOs (C)
#INFO    464 Complete and single-copy BUSCOs (S)
#INFO    10 Complete and duplicated BUSCOs (D)
#INFO    67 Fragmented BUSCOs (F)
#INFO    899 Missing BUSCOs (M)
#INFO    1440 Total BUSCO groups searched

cd run_sapria_rnd1_augustus/augustus_output/retraining_parameters/
rename BUSCO_sapria_rnd1_augustus_2039751926 sapria_longintron *


sed -i -- 's/BUSCO_sapria_rnd1_augustus_2039751926/sapria_longintron/g' sapria_longintron_parameters.cfg
sed -i -- 's/BUSCO_sapria_rnd1_augustus_2039751926/sapria_longintron/g' sapria_longintron_parameters.cfg.orig1


mkdir $AUGUSTUS_CONFIG_PATH/species/sapria_longintron
cp sapria_longintron*  $AUGUSTUS_CONFIG_PATH/species/sapria_longintron/