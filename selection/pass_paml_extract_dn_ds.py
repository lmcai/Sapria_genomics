import os,sys,fnmatch
import time
from ete3 import Tree

#get all codeml output file names in the dir
codemlfiles=list()
for file in os.listdir('.'):
	 if fnmatch.fnmatch(file, '*.codeml'):codemlfiles.append(file)

out=open('codeml.sum','a')
out.write('\t'.join(['orthogroupID','specie','geneID','dN','dS'])+'\n')
for file in codemlfiles:
	try:
		x=open(file).readlines()
		dntree=Tree(x[-7])
		dstree=Tree(x[-9])
		for leaf in dstree: 
			ds=leaf.dist
			dntip=dntree&leaf.name
			dn=dntip.dist
			out.write('\t'.join([file,leaf.name.split('_')[0],leaf.name,`dn`,`ds`])+'\n')
	except:
		print file
		pass
		

out.close()