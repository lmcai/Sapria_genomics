#############
#use site coverage to calculate genomesize repeat abundance
#
import re
x=open('links18.scaffolds.fa.repeatmasker.TRF.merged_ann.cleaned.modifiedname.bed').readlines()
y=open('links18.10XIllumina.cov.tsv','r')

genome_sum=0
tmp_lines = y.readlines(1024)
repeat_abundance={}
#initiate key-value pairs so that do not need to do it repetitively for each line
dd=[l.split()[3] for l in x]
dd=set(dd)
for d in dd:repeat_abundance[d]=0

i=0
while tmp_lines:
	cur_scaffold=tmp_lines[0].split()[0].split(',')[0]
	current_range=[int(j) for j in x[i].split()[1:3]]
	current_repeat_name=x[i].split()[3]
	for l in tmp_lines:
		#add up genome count
		genome_sum=genome_sum+int(l.split()[2])
		site_scaf=l.split()[0].split(',')[0]
		#in current repeat range
		if site_scaf==cur_scaffold and int(l.split()[1])>=current_range[0] and int(l.split()[1])<=current_range[1]:repeat_abundance[current_repeat_name]=repeat_abundance[current_repeat_name]+int(l.split()[2])
		elif site_scaf==cur_scaffold and int(l.split()[1])>current_range[1]:
			#should not exceed the range of total repeat annotation
			i=min(i+1,1283098)
			cur_scaffold=x[i].split()[0]
			current_range=[int(j) for j in x[i].split()[1:3]]
			current_repeat_name=x[i].split()[3]
			if site_scaf==cur_scaffold and int(l.split()[1])>=current_range[0] and int(l.split()[1])<=current_range[1]:repeat_abundance[current_repeat_name]=repeat_abundance[current_repeat_name]+int(l.split()[2])
		elif int(re.findall(r"[\d']+",site_scaf)[0])>int(re.findall(r"[\d']+",cur_scaffold)[0]):
			i=min(i+1,1283098)
			cur_scaffold=x[i].split()[0]
			current_range=[int(j) for j in x[i].split()[1:3]]
			current_repeat_name=x[i].split()[3]
			if site_scaf==cur_scaffold and int(l.split()[1])>=current_range[0] and int(l.split()[1])<=current_range[1]:repeat_abundance[current_repeat_name]=repeat_abundance[current_repeat_name]+int(l.split()[2])	
    tmp_lines = y.readlines(1024)
    









 
x=open('a').readlines()
y=open('b').readlines()
repeat_abundance={}
genome_sum=0
repeat_abundance['aa']=0
repeat_abundance['bb']=0
repeat_abundance['cc']=0
cur_scaffold='s1'
i=0
current_range=[int(j) for j in x[i].split()[1:3]]
current_repeat_name=x[i].split()[3]
for l in y:
	genome_sum=genome_sum+int(l.split()[2])
	site_scaf=l.split()[0].split(',')[0]
	if site_scaf==cur_scaffold and int(l.split()[1])>=current_range[0] and int(l.split()[1])<=current_range[1]:
		repeat_abundance[current_repeat_name]=repeat_abundance[current_repeat_name]+int(l.split()[2])
	elif site_scaf==cur_scaffold and int(l.split()[1])>current_range[1]:
		i=min(i+1,1283098)
		cur_scaffold=x[i].split()[0]
		current_range=[int(j) for j in x[i].split()[1:3]]
		current_repeat_name=x[i].split()[3]
		if site_scaf==cur_scaffold and int(l.split()[1])>=current_range[0] and int(l.split()[1])<=current_range[1]:repeat_abundance[current_repeat_name]=repeat_abundance[current_repeat_name]+int(l.split()[2])
	elif int(re.findall(r"[\d']+",site_scaf)[0])>int(re.findall(r"[\d']+",cur_scaffold)[0]):
		i=min(i+1,1283098)
		cur_scaffold=x[i].split()[0]
		current_range=[int(j) for j in x[i].split()[1:3]]
		current_repeat_name=x[i].split()[3]
		if site_scaf==cur_scaffold and int(l.split()[1])>=current_range[0] and int(l.split()[1])<=current_range[1]:repeat_abundance[current_repeat_name]=repeat_abundance[current_repeat_name]+int(l.split()[2])
