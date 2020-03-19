gff3_merge -d Sapria_longintron.rnd1_master_datastore_index.log
maker2zff -x 0.5 -l 50 Sapria_longintron.rnd1.all.gff

fathom genome.ann genome.dna -gene-stats > gene-stats.log 2>&1
fathom genome.ann genome.dna -validate > validate.log 2>&1
#filter genome.ann and genome.dna based on validate.log

# collect the training sequences and annotations, plus 1000 surrounding bp for training
fathom -categorize 1000 genome.ann genome.dna > categorize.log 2>&1
#uni.* only contains regions pass validation
fathom -export 1000 -plus uni.ann uni.dna 
mkdir params
cd params
forge ../export.ann ../export.dna > ../forge.log 2>&1

../SNAP-master/hmm-assembler.pl Sapria_V1.softmasked.fa params/ > snap1.hmm
