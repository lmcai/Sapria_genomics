import os,sys,fnmatch
import time
from ete3 import Tree

#get all tree file names in the dir

treefiles=list()
for file in os.listdir('.'):
	 if fnmatch.fnmatch(file, '*.treefile'):treefiles.append(file)

          
def get_malp_mono_group(tree):
	for leaf in tree:
		if leaf.name.startswith(('Rca','Rtu','Rhi','Sap','pSAP','Ptr','Jat','Mes')):
			leaf.add_features(group='malp')
	#visualization
	#print tree.get_ascii(attributes=["name", "parasite"], show_internal=False)
	#get all monophyletic groups and add to a list
	mono_group_nodes=[]
	for node in tree.get_monophyletic(values=["malp"], target_attr="group"):
		#print node
		mono_group_nodes.append(node)
	#return len(mono_group_nodes)
	return mono_group_nodes

def remv_sp(tree,taxa):
	for leaf in tree:
		if leaf.name.startswith(taxa):
			leaf.add_features(remv='true')
	remv_group_nodes=[]
	for node in tree.get_monophyletic(values=["true"], target_attr="remv"):
		removed_node = node.detach()
	return tree

#loop through files and output senario string to file 
out=open('VGT.senario.tsv','w')
out.write('Gene_ID\tVGT(Y/N)\tVGT_gr_num\tVGT_gr_name\tVGT_BS\tHGT_gr_num\tHGT_gr_name\tHGT_BS\tHGT_source\n')
for file in treefiles:
	t = Tree(file,format=1)
	geneID=file.split('.')[0]
	print geneID
	#reroot tree with basal angiosperm:
	outgr=[]
	for candidate in ['Amb','Cin','Osa','Sor','Aqu','Nel','Hel','Sol','Dau']:
		outgr = outgr + [leaf.name for leaf in t if leaf.name.startswith(candidate)]
	#root with non-malp members if basal group is available
	if len(outgr)==0:
		outgr = [leaf.name for leaf in t if not leaf.name.startswith(('Rca','Rtu','Rhi','Sap','pSHI','Ptr','Jat','Mes','Vvi','Tet'))]
	try:
		t.set_outgroup( t&outgr[0] )
	except IndexError:
		print('Can\'t root tree: '+file)
		pass
	#count malp monophyletic group with sapria
	#########let's remove Rca, Rtu, Rhi for now	
	########t=remv_sp(t,('Rca','Rtu','Rhi'))
	#malp_num_w_sap=get_malp_mono_group(t)
	#malp_num_wout_sap=get_malp_mono_group(remv_sp(t,('Rca','Rtu','Rhi','Sap','pSHI')))
	malp_w_sap=get_malp_mono_group(t)
	HGT_gr=[]
	HGT_BS=[]
	HGT_source=[]
	VGT_gr=[]
	VGT_BS=[]
	descendants=[]
	free_living_descendants=[]
	parasitic_descendants=[]
	for node in malp_w_sap:
		descendants=[leaf.name for leaf in node]
		free_living_descendants=[l for l in descendants if l.startswith(('Ptr','Jat','Mes'))]
		parasitic_descendants=[l for l in descendants if l.startswith(('Rca','Rtu','Rhi','Sap','pSHI'))]
		if len(free_living_descendants)>0 and len(parasitic_descendants)>0:
			VGT_gr.append(','.join(parasitic_descendants))
			sap_node=node.get_common_ancestor(parasitic_descendants)
			try:
				VGT_BS.append(sap_node.get_ancestors()[0].name)
			except IndexError:
				pass
		elif len(free_living_descendants)==0 and len(parasitic_descendants)>0:
			HGT_gr.append(','.join(parasitic_descendants))
			#some weird behaviour of tree reading of ete3: 'root' dose not have name and node names are shifted when reroot. the original 'root' do nor have name and can be used to identify the issue. The following solution may not be corrected
			try:
				HGT_BS.append(node.get_ancestors()[0].name)
				HGT_source.append(','.join([leaf.name for leaf in node.get_sisters()[0]]))
			except IndexError:
				pass
	#if malp_num_w_sap==malp_num_wout_sap:
	#	out.write(geneID+'\t'+'Y\n')
	#else:
	#	out.write(geneID+'\t'+'N\n')
	if len(HGT_gr)==0:
		out.write('\t'.join([geneID,'Y',str(len(VGT_gr)),'//'.join(VGT_gr),'#'.join(VGT_BS),'0','','',''])+'\n')
	else:
		out.write('\t'.join([geneID,'N',str(len(VGT_gr)),'//'.join(VGT_gr),'',str(len(HGT_gr)),'//'.join(HGT_gr),'#'.join(HGT_BS),'//'.join(HGT_source)])+'\n')
out.close()


