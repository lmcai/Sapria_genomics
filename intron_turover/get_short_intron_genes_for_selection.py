from gff3 import Gff3
import sys

gff = Gff3('../Sapria_longintron.rnd1.protein2genome.gff')
shortintron=open('sap.shortintron150.bed','a')
for l in gff.lines:
	#for protein2genome
	if l['type']=='protein_match':
		#if there is intron
		if len(l['children'])>1:
			scaf=l['seqid']
			protein_target_id=l['attributes']['Name']
			if protein_target_id.startswith('Potri') or protein_target_id.startswith('Mane'):
				exon_range=[]
				for rec in l['children']:
					exon_range.append([rec['start'],rec['end']])
				intron_length=[]
				for i in range(1,len(l['children'])):
					intron_start=exon_range[i-1][1]+1
					intron_end=exon_range[i][0]-1
					intron_length.append(intron_end-intron_start+1)
				if len([j for j in intron_length if j <150])==len(intron_length):
					#write this gene to shortintron
					for i in range(0,len(l['children'])):
						shortintron.write('\t'.join([scaf]+[str(j) for j in exon_range[i]]+[protein_target_id])+'\n')
				#elif len([j for j in intron_length if j >10000])>0:
				#	#write this gene to longintron
				#	for i in range(0,len(l['children'])):
				#		longintron.write('\t'.join([scaf]+[str(j) for j in exon_range[i]]+[protein_target_id])+'\n')
						
shortintron.close()
