import re
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

y=open('sap.intergenic.blast.out_parsed_G100000.PE_I100000.PS1').readlines()
x=open('sap.intergenic.blast.out_parsed_G100000.PE_I100000.PS1.pairs.sw.out.disable_count').readlines()
#sapria assembly
a=SeqIO.index('Sapria_longintron.intergenic.fas','fasta')
seq_out=open('sap_longintron.pseudogene.fas','a')
map_out=open('sap_longintron.pseudogene.name.map','a')

j=1
for l in y:
	prot_hit=l.split('\t')[3]
	prot_coord=re.findall(r'\d+, \d+', prot_hit)
	direction=[int(i.split(', ')[0])-int(i.split(', ')[1]) for i in prot_coord]
	if len([i for i in direction if i >0])==len(direction):order='descending'
	elif len([i for i in direction if i <0])==len(direction):order='growing'
	else:order='bad'
	prot_range=re.findall(r'\d+', prot_hit)
	prot_range=[int(i) for i in prot_range]
	prot_len=max(prot_range)-min(prot_range)+1
	#protein length needs to be >50 nt and protein direction is consistent within the hit
	if prot_len>49 and order!='bad':
		validated='Y'
		#if there is a gap in protein alignment, make sure overlapping protein bases are less than 10 nt
		if len(prot_coord)>1:
			for i in range(1,len(prot_coord)):
				if order=='descending' and int(prot_coord[i].split(', ')[0])-int(prot_coord[i-1].split(', ')[1])>10:
					validated='N'
				elif order=='growing' and int(prot_coord[i-1].split(', ')[1])-int(prot_coord[i].split(', ')[0])>10:
					validated='N'
		#if the protein ordering is fine
		if validated=='Y':
			#output annotated pseudogene sequence to file and create a name map
			scaf=l.split('\t')[0]
			coord_sap=re.findall(r'\d+, \d+', l.split('\t')[2])
			coord_sap=[[int(i.split(', ')[0]),int(i.split(', ')[1])] for i in coord_sap]
			coord_sap.sort()
			#merge ranges
			coord_sap_merged = []
			for begin,end in coord_sap:
				if coord_sap_merged and coord_sap_merged[-1][1] >= begin - 1:
					coord_sap_merged[-1] = (coord_sap_merged[-1][0], end)
				else:
					coord_sap_merged.append((begin, end))
			sap_cds_seq=''
        	for i in coord_sap_merged:
        		s=int(i[0])-1
        		e=int(i[1])
        		sap_cds_seq= sap_cds_seq + a[scaf].seq[s:e]
        	
        	#add stop codon information to ID
        	sap_range=re.findall(r'\d+', l.split('\t')[2])
        	disable_count_string=[ll for ll in x if l.split('\t')[1]+' '+scaf+'|'+sap_range[0]+'-'+sap_range[1] in ll]
        	try:
        		ID='pSHI'+'{num:06d}'.format(num=j)+'_'+scaf.split(':')[0]+'_'+'_'.join(disable_count_string[0].split()[-4:])
        	except IndexError:
        		ID='pSHI'+'{num:06d}'.format(num=j)+'_'+scaf.split(':')[0]
        	sap_rec=SeqRecord(sap_cds_seq,id=ID,description=ID)
        	d=SeqIO.write(sap_rec,seq_out,'fasta')
        	map_out.write(l.strip()+'\t'+ID+'\n')
        	j=j+1

seq_out.close()
map_out.close()