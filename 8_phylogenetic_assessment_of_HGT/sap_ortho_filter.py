import random
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

x=open('Orthogroups.csv').readlines()
y=open('Orthogroups.GeneCount.csv').readlines()
ath_seq=SeqIO.index('../../15_orthofinder_seq/Proteome/Ath.cds.fas','fasta')
vvi_seq=SeqIO.index('../../15_orthofinder_seq/Proteome/Vvi.cds.fas','fasta')
mes_seq=SeqIO.index('../../15_orthofinder_seq/Proteome/Mes.cds.fas','fasta')
ptr_seq=SeqIO.index('../../15_orthofinder_seq/Proteome/Ptr.cds.fas','fasta')
gly_seq=SeqIO.index('../../15_orthofinder_seq/Proteome/Gly.cds.fas','fasta')
sol_seq=SeqIO.index('../../15_orthofinder_seq/Proteome/Sol.cds.fas','fasta')

#filter orthogroup to contain at least 10 species at least one non-Rafflesiaceae Malpighiales
orthoseq_out=open('orthogroup_ref.fas','a')
e=open('Orthogroups.10sp.onemalp.list','a')
for i in range(1,len(y)):
	gene_num=y[i].split('\t')
	sp_missing=gene_num[1:-1].count('0')
	malp_num=sum(j!='0' for j in [gene_num[11],gene_num[12],gene_num[18]])
	#at least 10 species and one non-Rafflesiaceae Malpiales
	if sp_missing<29 and malp_num>0:
	#at least 10 species and one non-Rafflesiaceae Malpiales + at least one rafflesiaceae gene/pseudogene
	#if sp_missing<29 and malp_num>0 and (sum(j!='0' for j in [gene_num[31],gene_num[32],gene_num[33],gene_num[38]])>0 or y[i].split('\t')[0] in x):
		#output orthogroup to file
		e.write(y[i])
		#pick representative sequences from ath,vvi,mes,ptr,gly,sol to write to blast database
		ath=x[i].split('\t')[3].split(', ')
		vvi=x[i].split('\t')[22].split(', ')
		mes=x[i].split('\t')[12].split(', ')
		ptr=x[i].split('\t')[18].split(', ')
		gly=x[i].split('\t')[7].split(', ')
		sol=x[i].split('\t')[20].split(', ')
		try:
			d=SeqIO.write(SeqRecord(ath_seq[random.choice(ath)].seq,id=y[i].split()[0]+'_ath'),orthoseq_out,'fasta')
		except:
			pass
		try:
			d=SeqIO.write(SeqRecord(vvi_seq[random.choice(vvi)].seq,id=y[i].split()[0]+'_vvi'),orthoseq_out,'fasta')
		except:
			pass
		try:
			d=SeqIO.write(SeqRecord(mes_seq[random.choice(mes)].seq,id=y[i].split()[0]+'_mes'),orthoseq_out,'fasta')
		except:
			pass
		try:
			d=SeqIO.write(SeqRecord(ptr_seq[random.choice(ptr)].seq,id=y[i].split()[0]+'_ptr'),orthoseq_out,'fasta')
		except:
			pass
		try:
			d=SeqIO.write(SeqRecord(gly_seq[random.choice(gly)].seq,id=y[i].split()[0]+'_gly'),orthoseq_out,'fasta')
		except:
			pass
		try:
			d=SeqIO.write(SeqRecord(sol_seq[random.choice(sol)].seq,id=y[i].split()[0]+'_sol'),orthoseq_out,'fasta')
		except:
			pass

e.close()
orthoseq_out.close()


