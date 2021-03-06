module load centos6
module load BUSCO/3.0.2-fasrc01
#compare sapria assembly to plant BUSCO
python ~/programs/busco/scripts/run_BUSCO.py -i Sapria_V1.softmasked.fa -o sapria.plant -l /n/scratchlfs/davis_lab/lmcai/embryophyta_odb9 -m genome -c 8

#compare sapria assembly to eukaryote BUSCO
python ~/programs/busco/scripts/run_BUSCO.py -i Sapria_V1.softmasked.fa -o sapria.eukaryote -l /n/scratchlfs/davis_lab/lmcai/eukaryota_odb10 -m genome -c 8
