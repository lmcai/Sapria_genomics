#filter reads by length, minimum 10kb
awk 'BEGIN {FS = "\t" ; OFS = "\n"} {header = $0 ; getline seq ; getline qheader ; getline qseq ; if (length(seq) >= 10000) {print header, seq, qheader, qseq}}' < Tetrastigma_nanopore.fastq > Tetrastigma_10k_nanopore.fastq &

#all-by-all reads mapping
module load minimap2/2.9-fasrc01
minimap2 -t 32 -k15 -Xw5 -m500 -g10000 -r2000 --max-chain-skip 25 ../../00_nanopore_raw_fastq/Tetrastigma_10k_nanopore.fastq ../../00_nanopore_raw_fastq/Tetrastigma_10k_nanopore.fastq | gzip -1 >tetra.ovlp.paf.gz
#[M::main] Real time: 60348.198 sec; CPU: 1815553.207 sec

#assembly with miniasm
module load miniasm/0.2-fasrc01
miniasm -f ../../00_nanopore_raw_fastq/Tetrastigma_10k_nanopore.fastq tetra.ovlp.paf.gz > tetra.nanopore.m500.gfa
#[M::main] Real time: 5315.122 sec; CPU: 5308.325 sec

awk '$1 ~/S/ {print ">"$2"\n"$3}' tetra.nanopore.m500.gfa > tetra.m500.miniasm.fasta

#map Illumina reads to the draft assembly for polishing
module load bwa/0.7.15-fasrc02
module load samtools/1.5-fasrc02
bwa index tetra.m500.miniasm.fasta
bwa mem -t16 tetra.m500.miniasm.fasta tetra.illumina.fq.gz | samtools sort -@16 -m 16G -o tetra.m500.miniasm.illumina.sort.bam
#[main] Real time: 330386.582 sec; CPU: 3489880.158 sec

#run BUSCO to QC results
#module load centos6
#module load BUSCO/3.0.2-fasrc01
#python ~/programs/busco/scripts/run_BUSCO.py -c 8 -z -i ../tetra.miniasm.fasta -o tetra.miniasm.busco -l /n/scratchlfs/davis_lab/lmcai/embryophyta_odb9 -m geno
#BUSCO
#INFO    43 Complete BUSCOs (C)
#INFO    42 Complete and single-copy BUSCOs (S)
#INFO    1 Complete and duplicated BUSCOs (D)
#INFO    11 Fragmented BUSCOs (F)
#INFO    1386 Missing BUSCOs (M)
#INFO    1440 Total BUSCO groups searched
#INFO    BUSCO analysis done. Total running time: 62093.823899 seconds

#polish with pilon, round 1
source activate pilon
module load samtools/1.5-fasrc02
samtools index  tetra.miniasm.illumina.sort.bam
#because the bam file was generated from a concatenated fq file, the pairing is lost. should be treated as unpaired bam.
pilon -Xmx1000G --genome tetra.miniasm.m500.fasta --unpaired tetra.miniasm.illumina.sort.bam --diploid --output tetra.miniasm.pilon --threads 2
#5-6days

#run BUSCO for QC
#python ~/programs/busco/scripts/run_BUSCO.py -c 8 -z -i tetra.miniasm.pilon1.fasta -o tetra.miniasm.pilon1.busco -l /n/scratchlfs/davis_lab/lmcai/embryophyta_odb9 -m geno
# BUSCO was run in mode: genome
#     C:77.3%[S:74.2%,D:3.1%],F:5.2%,M:17.5%,n:1440

#polish with pilon, round 2
bwa index tetra.miniasm.pilon1.fasta 
#[main] Real time: 4875.169 sec; CPU: 4868.853 sec
bwa mem -t16 tetra.miniasm.pilon1.fasta tetra.illumina.fq.gz | samtools sort -@16 -m 16G -o tetra.pilon1.illumina.sort.bam
#[main] Real time: 159140.170 sec; CPU: 2530825.955 sec
samtools index tetra.pilon1.illumina.sort.bam
pilon -Xmx1000G --genome tetra.miniasm.pilon1.fasta --unpaired tetra.pilon1.illumina.sort.bam --diploid --output tetra.miniasm.pilon2 --threads 2

#run BUSCO for QC
#python ~/programs/busco/scripts/run_BUSCO.py -c 8 -z -i tetra.miniasm.pilon2.fasta -o tetra.miniasm.pilon2.busco -l /n/scratchlfs/davis_lab/lmcai/embryophyta_odb9 -m geno
#        C:85.1%[S:80.6%,D:4.5%],F:3.3%,M:11.6%,n:1440

#polish with pilon, round 3
bwa index tetra.miniasm.pilon2.fasta 
bwa mem -t16 tetra.miniasm.pilon2.fasta tetra.illumina.fq.gz | samtools sort -@16 -m 16G -o tetra.pilon2.illumina.sort.bam
samtools index tetra.pilon2.illumina.sort.bam
pilon -Xmx1000G --genome tetra.miniasm.pilon2.fasta --unpaired tetra.pilon2.illumina.sort.bam --diploid --output tetra.miniasm.pilon3 --threads 2
#not much improvement in BUSCO, stop polishing
#       C:86.1%[S:81.4%,D:4.7%],F:3.6%,M:10.3%,n:1440
