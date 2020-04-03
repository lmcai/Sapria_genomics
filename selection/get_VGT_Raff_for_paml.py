import os,sys,fnmatch
import time
from ete3 import Tree
import random
from Bio import SeqIO

#get all tree file names in the dir
treefiles=list()
for file in os.listdir('.'):
	 if fnmatch.fnmatch(file, '*.ortho1.tre'):treefiles.append(file)


aa_dict=SeqIO.index('../paml.faa','fasta')
na_dict=SeqIO.index('../paml.cds.fas','fasta')
def get_closest_mono_group(tree,ingroup,sp):
	target_sp=[leaf.name for leaf in tree if leaf.name.startswith(sp)]
	try:
		cur_dist=10
		for tip in target_sp:
			if tree.get_distance(ingroup,tip)<cur_dist:
				closest_tip=tip
		return closest_tip
	except UnboundLocalError:
		return None


for file in treefiles:
	t = Tree(file,format=1)
	geneID=file.split('.')[0]
	tips2preserve=[leaf.name for leaf in t]
	sap=[i for i in tips2preserve if i.startswith('Sap')]
	malp=[i for i in tips2preserve if i.startswith(('Mes','Ptr','Jat'))]
	if len(sap)==0 or len(malp)==0:
		#screen print trees without sapria or malpighiales
		print(file+' not enough ingroup, skipping...')
		continue
	else:
		#add ath and gly as outgroup
		print(file + ' processing...')
		t_full=Tree('../tem_tree_dir/'+geneID+'.treefile',format=1)
		ath=get_closest_mono_group(t_full,sap[0],'Ath')
		gly=get_closest_mono_group(t_full,sap[0],'Gly')
		#remove pseudogene, add outgroup Ath and Gly
		tips2preserve=tips2preserve+[i for i in [ath,gly] if i]
		tips2preserve=[i for i in tips2preserve if not i.startswith('pSHI')]
		#tips2remove=[]
		#tips2remove=[leaf.name for leaf in t_full if not leaf.name in tips2preserve]
		#pSAP=[i for i in tips2preserve if i.startswith('pSHI')]
		#tips2remove=tips2remove+pSAP
		t_full.prune(tips2preserve)
		#output tree to file	
		t_full.write(format=1, outfile=file+'.paml.raff.tre')
		#write aa and na to file
		for tip in [leaf.name for leaf in t_full]:
			d=SeqIO.write(aa_dict[tip],open(file+'.paml.raff.faa','a'),'fasta')
			d=SeqIO.write(na_dict[tip],open(file+'.paml.raff.fna','a'),'fasta')
		#remove Rafflesia and Rhizanthes
		tips2preserve=[i for i in tips2preserve if not i.startswith(('Rca','Rtu','Rhi'))]
		t_full.prune(tips2preserve)
		#output tree to file
		t_full.write(format=1, outfile=file+'.paml.sap.tre')
		#write aa and na to file
		for tip in [leaf.name for leaf in t_full]:
			d=SeqIO.write(aa_dict[tip],open(file+'.paml.sap.faa','a'),'fasta')
			d=SeqIO.write(na_dict[tip],open(file+'.paml.sap.fna','a'),'fasta')

