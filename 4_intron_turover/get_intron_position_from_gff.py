#python get_intron_position_from_mes_gff.py [input gff] [output tsv name]

from gff3 import Gff3
import sys

gff = Gff3(sys.argv[1])
output=open(sys.argv[2],'a')

for l in gff.lines:
	if l['type']=='mRNA':
		rna_nam=l['attributes']['Name']
		if len(l['children'])==1:
		#if no intron
			output.write('\t'.join([rna_nam,'NA','NA','NA'])+'\n')
		else:
		#if there's intron
			cur_cds_3_end=0
			#coding region
			CDSs=[i for i in l['children'] if i['type']=='CDS']
			for i in range(0,len(CDSs)-1):
				cur_cds_3_end=cur_cds_3_end+CDSs[i]['end']-CDSs[i]['start']+1
				pos_str=str(int(round(float(cur_cds_3_end)/3)))+'..'+str(int(round(float(cur_cds_3_end)/3))+1)
				intron_num=CDSs[i]['attributes']['ID'].split('.')[-1]
				if CDSs[i+1]['start']>CDSs[i]['end']:
					intron_len=CDSs[i+1]['start']-CDSs[i]['end']-1
				else:
					intron_len=CDSs[i]['start']-CDSs[i+1]['end']-1
				#print('\t'.join([rna_nam,pos_str,str(intron_num),str(intron_len)]))
				output.write('\t'.join([rna_nam,pos_str,str(intron_num),str(intron_len)])+'\n')
				

output.close()
