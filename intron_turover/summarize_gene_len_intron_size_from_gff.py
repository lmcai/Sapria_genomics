#python extract_intron_stat_from_gff.py links18.scaffolds.fa.rnd3_rerun.GAAS.gff test.csv


from gff3 import Gff3
import sys
#usage: python [input gff file] [output csv file]
gff = Gff3(sys.argv[1])
output=sys.argv[2]

intron_num={}
exon_length={}
mrna_len={}
intron_len={}
single_intron_len=[]
CDS_length={}

for l in gff.lines:
	if l['type']=='mRNA':
	#if l['type']=='mRNA' and float(l['attributes']['_AED']) <0.5:
		rna_nam=l['attributes']['Name']
		mrna_len[rna_nam]=l['end']-l['start']
		exons=[]
		CDS_len=0
		for rec in l['children']:
			exons.append((rec['start'],rec['end']))
			if rec['type']=='CDS':CDS_len=CDS_len+rec['end']-rec['start']+1
		CDS_length[rna_nam]=CDS_len
		exons_merged = []
		for begin,end in sorted(exons):
			if exons_merged and exons_merged[-1][1] >= begin - 1:
				exons_merged[-1] = (exons_merged[-1][0], end)
   			else:
   				exons_merged.append((begin, end))
   		intron_num[rna_nam]=len(exons_merged)-1
   		exon_length[rna_nam]=0
   		for begin,end in exons_merged:
   			exon_length[rna_nam]=exon_length[rna_nam]+end-begin+1
   		introns=[]
   		for i in range(1,len(sorted(exons_merged))):
   			#print(exons_merged[i][0],exons_merged[i-1][0])
   			introns.append(exons_merged[i][0]-exons_merged[i-1][1]-1)
   		intron_len[rna_nam]=sum(introns)
   		single_intron_len=single_intron_len+introns


with open(output,'a') as f:
	f.write('gene,mRNA_length,intron_number,intron_length,exon_length,CDS_length\n')
	for g in mrna_len.keys():
		f.write(g+','+str(mrna_len[g])+','+str(intron_num[g])+','+str(intron_len[g])+','+str(exon_length[g])+','+str(CDS_length[g])+'\n')
	f.close()

with open(sys.argv[1].split('.')[0]+'.intron.distr','w') as f:
	f.write('\n'.join([str(i) for i in single_intron_len]))
	f.close()
