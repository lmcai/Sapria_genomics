#python intron_length_comparison_with_intersp_protein2genome.py Sapria_longintron.rnd1.protein2genome.gff rnd1_rerun_protein2genome.intron_pos.tsv

from gff3 import Gff3
import sys,re

#gff = Gff3(sys.argv[1])
#output=open(sys.argv[2],'a')
gff = Gff3('Sapria_longintron.rnd1.protein2genome.gff')
output=open('rnd1_protein2genome.sum_by_intron.tsv','a')

output.write('\t'.join(['prot_aln_ID','scaffold','start','end','type','5_end_intron_ID','protein_hit','protein_corrd','alignment_note'])+'\n')
ID=0
for l in gff.lines:
	#for protein2genome
	if l['type']=='protein_match':
		protein_target_id=l['attributes']['Name']
		if protein_target_id.startswith('Potri') or protein_target_id.startswith('Mane'):
			ID=ID+1
			#if no intron
			if len(l['children'])==1:
				scaf=l['seqid']
				strand=l['strand']
				rec=l['children'][0]
				output.write('\t'.join(['ALN_'+`ID`,scaf,str(rec['start']),str(rec['end']),'prot_match','-',protein_target_id,'..'.join([str(rec['attributes']['Target']['start']),str(rec['attributes']['Target']['end'])]),rec['attributes']['Gap']])+'\n')
			#if there is intron
			else:
				scaf=l['seqid']
				strand=l['strand']
				exon_range=[]
				protein_range=[]
				for rec in l['children']:
					#write match part first
					output.write('\t'.join(['ALN_'+`ID`,scaf,str(rec['start']),str(rec['end']),'prot_match','-',protein_target_id,'..'.join([str(rec['attributes']['Target']['start']),str(rec['attributes']['Target']['end'])]),rec['attributes']['Gap']])+'\n')
					exon_range.append([rec['start'],rec['end']])
					protein_range.append([rec['attributes']['Target']['start'],rec['attributes']['Target']['end']])
				if strand=='+':
					#the first intron on 5' end
					intron_id=1
					for i in range(1,len(l['children'])):
						intron_start=exon_range[i-1][1]+1
						intron_end=exon_range[i][0]-1
						protein_boundary=[protein_range[i-1][1],protein_range[i][0]]
						protein_boundary.sort()
						protein_boundary=[str(j) for j in protein_boundary]
						output.write('\t'.join(['ALN_'+`ID`,scaf,str(intron_start),str(intron_end),'intron',str(intron_id),protein_target_id,'..'.join(protein_boundary),''])+'\n')
						intron_id=intron_id+1
				else:
					#the last intron on 5' end
					intron_id=1
					for i in range(1,len(l['children'])):
						intron_start=exon_range[i][1]+1
						intron_end=exon_range[i-1][0]-1
						protein_boundary=[protein_range[i-1][1],protein_range[i][0]]
						protein_boundary.sort()
						protein_boundary=[str(j) for j in protein_boundary]
						output.write('\t'.join(['ALN_'+`ID`,scaf,str(intron_start),str(intron_end),'intron',str(intron_id),protein_target_id,'..'.join(protein_boundary),''])+'\n')
						intron_id=intron_id+1

output.close()

###########################################################
#Summarize intron turn over by gene
#create intron position dictionaries for Manihot and Populus
mes=open('intron_turn_over_manihot_populus/manihot.intron.pos.tsv').readlines()
ptr=open('intron_turn_over_manihot_populus/populus.intron.pos.tsv').readlines()

intron_pos={}
for l in mes:
	try:
		intron_pos[l.split()[0]].append(int(l.split()[1].split('..')[0]))
	except ValueError:intron_pos[l.split()[0]]=[]
	except KeyError:
		try:intron_pos[l.split()[0]]=[int(l.split()[1].split('..')[0])]
		except ValueError:intron_pos[l.split()[0]]=[]


	
for l in ptr:
	try:
		intron_pos[l.split()[0]].append(int(l.split()[1].split('..')[0]))
	except ValueError:intron_pos[l.split()[0]]=[]
	except KeyError:
		try:intron_pos[l.split()[0]]=[int(l.split()[1].split('..')[0])]
		except ValueError:intron_pos[l.split()[0]]=[]

x=open('rnd1_protein2genome.sum_by_intron.tsv').readlines()
output=open('rnd1_protein2genome.sum_by_gene.tsv','a')
output.write('\t'.join(['prot_aln_ID','scaffold','start','end','prot_name','intron_gain','intron_loss','ancestral_intron_num','sap_intron_num','aln_quality','raw_aln_annotation'])+'\n')
def number_fall_in_ranges(range,candidate,buffer_number):
	hit=0
	for i in candidate:
		for j in range:
			if i >int(j[0])+buffer_number and i < int(j[1])-buffer_number:hit=hit+1
	return hit

def number_new_intron(ancestor_intron_pos,new_introns,buffer_number):
	new=0
	for i in new_introns:
		intron_hit=[]
		for j in ancestor_intron_pos:
			if j-buffer_number<int(i[0]) and j+buffer_number>int(i[1]):
				intron_hit.append(j)
		if len(intron_hit)==0:new=new+1
	return new

cur_aln=''
recs_prot=[]
for l in x[1:]:
	aln=l.split()[0]
	#if a new alignment
	if aln!=cur_aln:
		#output align results from previous alignment
		if len(recs_prot):
			#examine protein alignment quality
			aln_quality='good'
			for i in aln_note:
				#contain insertion/deletion/frameshift etc.
				if len([j for j in i.split() if j.startswith(('R','I','D','F'))])>0:
					if len(i.split())==2:
						#if these mismatches are close to the ends of exons
						aln_quality='potential_problematic'
					else:
						#if these mismatches are close to the ends of exons
						if len([j for j in i.split()[1:-1] if j.startswith(('R','I','D','F'))])==0:aln_quality='potential_problematic'
						#mismatches are in the middle of exons
						else:
							aln_quality='bad'
							break
			#count number of protein intron fall within this aligned range
			if len(intron_pos[prot_name])==0:
				intron_loss=0
				intron_gain=len(recs_intron)
			else:
				intron_loss=number_fall_in_ranges(recs_prot,intron_pos[prot_name],5)
				intron_gain=0
				if len(recs_intron):
					#examine intron position: if it is newly gained or remain ancestor position
					intron_gain=number_new_intron(intron_pos[prot_name],recs_intron,5)
			#output to file
			#print('\t'.join([cur_aln,scaf,`min(rec_coord)`,`max(rec_coord)`,prot_name,`intron_gain`,`intron_loss`,`len(intron_pos[prot_name])`,`len(recs_intron)`])+'\n')
			output.write('\t'.join([cur_aln,scaf,`min(rec_coord)`,`max(rec_coord)`,prot_name,`intron_gain`,`intron_loss`,`len(intron_pos[prot_name])`,`len(recs_intron)`,aln_quality,'_'.join(aln_note)])+'\n')
		#initiate value
		cur_aln=aln
		scaf=l.split()[1]
		rec_coord=[]
		recs_intron=[]
		recs_prot=[]
		prot_name=l.split()[6]
		aln_note=[]
	#same alignment
	rec_coord=rec_coord+[int(jj) for jj in l.split()[2:4]]
	if l.split()[4]=='prot_match':
		recs_prot.append(l.split('\t')[7].split('..'))
		aln_note.append(l.split('\t')[-1].strip())
	else:recs_intron.append(l.split('\t')[7].split('..'))

output.close()