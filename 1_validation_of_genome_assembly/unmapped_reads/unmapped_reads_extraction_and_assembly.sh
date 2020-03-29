################################
#mapping illumina reads to assembly
bwa mem -t32 -p -C Sapria_V1.fa ../2_longranger_basic_barcoded_fq/outs/barcoded.fastq.gz | samtools sort -@16 -t -o Sapria_V1.reads.sort.bam
		
################################
#extract unmapped reads with samtools
module load samtools/1.5-fasrc02
#get unmapped reads
samtools view -f 4 -b Sapria_V1.reads.sort.bam | samtools bam2fq >Sapria_V1.unmapped.fastq	

################################
#Reads error correction
module load TrimGalore/0.5.0-fasrc01
module load cutadapt/1.8.1-fasrc01
trim_galore -q 5 --phred33 --length 36 --stringency 5 Sapria_V1.unmapped.fastq


################################
#Assembly with Abyss
module load gcc/4.9.3-fasrc01 abyss/1.5.2-fasrc01
abyss-pe k=20 name=unaligned se=Sapria_V1.unmapped_trimmed.fq

#output summary
n       n:500   n:N50   min     N80     N50     N20     E-size  max     sum     name
4396601 59      25      500     542     629     758     672     1289    37908   unaligned-unitigs.fa

