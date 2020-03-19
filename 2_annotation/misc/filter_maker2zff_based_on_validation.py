#python filter_maker2zff_based_on_validation.py validate.list
import sys
from Bio import SeqIO

x=open(sys.argv[1]).readlines()
x=[l.strip() for l in x]
w=SeqIO.index('genome.dna','fasta')

y=open('genome.ann').readlines()
z=open('genome_filtered.ann','a')

cur_scaf=''
output=[]
for l in y:
	if l.startswith('>'):
		if len(output)>0:
			#write to file
			z.write(cur_scaf)
			z.write('\n'.join(output)+'\n')
			d=SeqIO.write(w[l.strip()[1:]],open('genome_filtered.dna','a'),'fasta')
		#initiate values
		cur_scaf=l
		output=[]
	else:
		model=l.split()[3]
		if model in x:
			output.append(l.strip())

z.close()