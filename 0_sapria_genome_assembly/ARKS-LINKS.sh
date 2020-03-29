###########################
#Use ARKS-LINKS pipeline to scaffold assembly based on linked reads information from 10X library
###########################

#use longranger to barcode Illumina reads from 10X library
module load longranger/2.2.2-fasrc01
longranger basic --id=2_longranger_basic_barcoded_fq --fastqs=1_10Xfastq_raw/ --localcores 48

#use ARKS to further scaffold based on linked reads from 10X library
perl ~/programs/arks/bin/calcBarcodeMultiplicities.pl 2_longranger_basic_barcoded_fq/outs/barcoded.fof >barcoded_multiplicities.csv

#note I change the default -m 50-10000 to 50-200000, increased index multiplicity
#multiple -m -k -e combination
arks -p full -v -f 0_supernova_allpath_assembly/supernova.assemblyV1.fas -a 2_longranger_basic_barcoded_fq/outs/barcoded_multiplicities.csv -c 5 -t 32 -j 0.55 -o 0 -m 50-200000 -k 26 -r 0.05 -e 15000 -z 500 -d 0 -b 0_supernova_allpath_assembly/supernova.assemblyV1_c5_m50-200000_k26_r0.05_e15000_z500 2_longranger_basic_barcoded_fq/outs/barcoded.fastq.gz
arks -p full -v -f 0_supernova_allpath_assembly/supernova.assemblyV1.fas -a 2_longranger_basic_barcoded_fq/outs/barcoded_multiplicities.csv -c 5 -t 32 -j 0.55 -o 0 -m 50-100000 -k 30 -r 0.05 -e 30000 -z 500 -d 0 -b 0_supernova_allpath_assembly/supernova.assemblyV1_c5_m50-100000_k30_r0.05_e30000_z500 2_longranger_basic_barcoded_fq/outs/barcoded.fastq.gz

python ~/programs/arks/Examples/makeTSVfile.py supernova.assemblyV1_c5_m50-100000_k30_r0.05_e30000_z500_original.gv supernova.assemblyV1_c5_m50-100000_k30_r0.05_e30000_z500.tigpair_checkpoint.tsv supernova.assemblyV1.fas 
python ~/programs/arks/Examples/makeTSVfile.py supernova.assemblyV1_c5_m50-200000_k26_r0.05_e15000_z500_original.gv supernova.assemblyV1_c5_m50-200000_k26_r0.05_e15000_z500.tigpair_checkpoint.tsv supernova.assemblyV1.fas
python ~/programs/arks/Examples/makeTSVfile.py supernova.assemblyV1_c5_m50-200000_k26_r0.05_e50000_z500_original.gv supernova.assemblyV1_c5_m50-200000_k26_r0.05_e50000_z500.tigpair_checkpoint.tsv supernova.assemblyV1.fas


#LINKS make scaffolds based on ARKS output
LINKS -f supernova.assemblyV1.fas -s empty.fof -b supernova.assemblyV1_c5_m50-100000_k30_r0.05_e30000_z500 -l 5 -a 0.3 -z 500
LINKS -f supernova.assemblyV1.fas -s empty.fof -b supernova.assemblyV1_c5_m50-200000_k26_r0.05_e15000_z500 -l 5 -a 0.3 -z 500

###########################
#Then we add in low-coverage nanopore and use LINKS iteratively scaffold assembly until no improvement
###########################
#filter nanopore reads to include only reads >10kb due to memory issue

#run LINKS with filtered nanopore reads
#LINKS parameters:
#-f and -s : sequences must be on a SINGLE line with no linebreaks
#The most important parameters for decreasing RAM usage are -t and -d.
#-d     distance between k-mer pairs (ie. target distances to re-scaffold on. default -d 4000, optional)
#-t    step of sliding window when extracting k-mer pairs from long reads (default -t 2, optional)

#sh ./runIterativeLINKS.sh 24 2 5 0.3
#kmer size= 24; l=5; a= 0.3
#I iteratively run LINKS with increasing distance between k-mer pairs (-d 500 to -d 100000) to allow for linking scaffolds with longer gaps

~/programs/links_v1.8.6/LINKS -f supernova.assemblyV1.arks.fa -s empty.fof -b k$1_l$3_links1 -d 500 -t 50 -k $1 -l $3 -a $4 -z 500
~/programs/links_v1.8.6/LINKS -f ./k$1_l$3_links1.scaffolds.fa -s empty.fof -b links2 -r k$1_l$3_links1.bloom -d 750 -t 50 -k $1 -l $3 -a $4 -z 500
~/programs/links_v1.8.6/LINKS -f ./links2.scaffolds.fa -s empty.fof -b links4 -r k$1_l$3_links1.bloom -d 3000 -t 50 -k $1 -l $3 -a $4 -z 500
~/programs/links_v1.8.6/LINKS -f ./links4.scaffolds.fa -s empty.fof -b links5 -r k$1_l$3_links1.bloom -d 5000 -t 50  -k $1 -l $3 -a $4 -z 500
~/programs/links_v1.8.6/LINKS -f ./links5.scaffolds.fa -s empty.fof -b links6 -r k$1_l$3_links1.bloom -d 7000 -t 20 -k $1 -l $3 -a $4
~/programs/links_v1.8.6/LINKS -f ./links6.scaffolds.fa -s temp.fof -b links7 -r k$1_l$3_links1.bloom -d 10000 -t 20 -k 23 -l 5
~/programs/links_v1.8.6/LINKS -f ./links7.scaffolds.fa -s V0_nanofas.fof -b links8 -r links8.bloom -d 15000 -t 40 -k 24 -l 7
~/programs/links_v1.8.6/LINKS -f ./links8.scaffolds.fa -s V0_nanofas.fof -b links9 -r links8.bloom -d 20000 -t 30 -k 24 -l 7
~/programs/links_v1.8.6/LINKS -f ./links9.scaffolds.fa -s V0_nanofas.fof -b links10 -r links8.bloom -d 25000 -t 30 -k 24 -l 7
~/programs/links_v1.8.6/LINKS -f ./links10.scaffolds.fa -s V0_nanofas.fof -b links11 -r links8.bloom -d 30000 -t 30 -k 24 -l 8
~/programs/links_v1.8.6/LINKS -f ./links11.scaffolds.fa -s V0_nanofas.fof -b links12 -r links8.bloom -d 40000 -t 30 -k 24 -l 8
~/programs/links_v1.8.6/LINKS -f ./links12.scaffolds.fa -s temp.fof -b links13 -d 50000 -t 30 -k 24 -l 5
~/programs/links_v1.8.6/LINKS -f ./links13.scaffolds.fa -s temp.fof -b links14 -r links13.bloom -d 60000 -t 20 -k 24 -l 5
~/programs/links_v1.8.6/LINKS -f ./links14.scaffolds.fa -s temp.fof -b links15 -r links13.bloom -d 70000 -t 20 -k 24 -l 5
~/programs/links_v1.8.6/LINKS -f ./links15.scaffolds.fa -s temp.fof -b links16 -r links13.bloom -d 80000 -t 20 -k 24 -l 5
~/programs/links_v1.8.6/LINKS -f ./links16.scaffolds.fa -s temp.fof -b links17 -d 90000 -t 20 -k 24 -l 5
~/programs/links_v1.8.6/LINKS -f ./links17.scaffolds.fa -s temp.fof -b links18 -r links17.bloom -d 100000 -t 20 -k 24 -l 5
