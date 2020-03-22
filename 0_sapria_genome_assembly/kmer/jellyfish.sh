#load module
module load jellyfish/2.2.5-fasrc01
#run jellyfish to count kmers, here kmer size of 27 is used
jellyfish count -t 16 -C -m 27 -s 16G -g generators -G 9 -o 27mer_out --min-qual-char=?
jellyfish histo -o 27mer_out.histo 27mer_out