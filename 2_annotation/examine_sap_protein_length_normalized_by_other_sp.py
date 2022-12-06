#path
#/n/holyscratch01/davis_lab/lmcai/sapria/15_orthofinder_seq


from Bio import SeqIO
import os,fnmatch,re
a={}
for fn in os.listdir('../../15_orthofinder_seq/Proteome/'):
        if fnmatch.fnmatch(fn,'*.faa'):
            recs=SeqIO.parse('../../15_orthofinder_seq/Proteome/'+fn,'fasta')
            for rec in recs:
                a[rec.id]=len(rec.seq)

from scipy import stats
from numpy import max,mean,std

x=open('Orthogroups.csv').readlines()

b={}
c={}
d={}
e={}
f={}
g={}
h={}
z={}

for l in x[1:]:
    if l.split('\t')[38].strip()!='' or l.split('\t')[32]!='' or l.split('\t')[33]!='' or l.split('\t')[31]!='':
        b[l.split('\t')[0]]=''
        c[l.split('\t')[0]]=''
        d[l.split('\t')[0]]=''
        e[l.split('\t')[0]]=''
        f[l.split('\t')[0]]=''
        g[l.split('\t')[0]]=''
        h[l.split('\t')[0]]=''
        z[l.split('\t')[0]]=''
        o=[]
        for i in l.split('\t')[1:32]+l.split('\t')[34:38]:
            for j in i.split(', '):
                try:o.append(a[j])
                except KeyError:pass
        if l.split('\t')[38].strip()!='':
            s=[]
            for i in l.split('\t')[38].strip().split(', '):
                s.append(a[i])
            b[l.split('\t')[0]]=max(s)/stats.trim_mean(o, 0.1)
            c[l.split('\t')[0]]=max(s)
            d[l.split('\t')[0]]=mean(s)/stats.trim_mean(o, 0.1)
            #normalize by z-score
            if std(o)>0:z[l.split('\t')[0]]=(max(s)-mean(o))/std(o)
            #get number of adjacent genes in the orthogroup (position <2)
            pos=[]
            for i in l.split('\t')[38].strip().split(', '):
                m=re.search(r'SHI(\d*)-R*',i)
                pos.append(int(m.group(1)))
            if len(pos)>1:
                pos_inv=[]
                pos.sort()
                for i in range(1,len(pos)):
                    pos_inv.append(pos[i]-pos[i-1])
                h[l.split('\t')[0]]=pos_inv.count(1)+pos_inv.count(2)
            else:
                h[l.split('\t')[0]]=0
                
            
        if l.split('\t')[31]!='':
            rca=[]
            for i in l.split('\t')[31].split(', '):
                rca.append(a[i])
            
            e[l.split('\t')[0]]=mean(rca)/stats.trim_mean(o, 0.1)
        if l.split('\t')[32]!='':
            rhi=[]
            for i in l.split('\t')[32].split(', '):
                rhi.append(a[i])
            f[l.split('\t')[0]]=mean(rhi)/stats.trim_mean(o, 0.1)
        if l.split('\t')[33]!='':
            rtu=[]
            for i in l.split('\t')[33].split(', '):
                rtu.append(a[i])
            g[l.split('\t')[0]]=mean(rtu)/stats.trim_mean(o, 0.1)

        
out=open('rafflesiaceae_aa_len.dist','a')
out.write('\t'.join(['ID','longest_sapria(%)','mean_sapria(%)','longest_sapria(nt)','mean_rca(%)','mean_rhi(%)','mean_rtu(%)','number_adjacent_sap_gene','longest_sapria_zscore'])+'\n')
for key in b:
    out.write(key+'\t'+str(b[key])+'\t'+str(d[key])+'\t'+str(c[key])+'\t'+str(e[key])+'\t'+str(f[key])+'\t'+str(g[key])+'\t'+str(h[key])+'\t'+str(z[key])+'\n')

out.close()


#plot in R
x=read.csv('~/Downloads/rafflesiaceae_aa_len.dist',sep='\t')
hist(x$longest_sapria...,xlim=c(0,2),breaks=300,main = 'ratio of Sapria protein length to other orthologs',xlab = 'rafflesia/(ortholog ave.)')