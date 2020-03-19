from Bio.Blast import NCBIWWW
help(NCBIWWW.qblast)
from Bio import SeqIO
record = SeqIO.parse("abyss/unaligned-3.fa", format="fasta")
y=[]
j=0
for i in record:
    if len(i)>300:
        y.append(i.seq)
        result_handle = NCBIWWW.qblast("blastn", "nt", i.seq)
        j=j+1
        with open(`j`+"_blast.xml", "w") as out_handle:
            out_handle.write(result_handle.read())
        result_handle.close()
    
#all >300bp scaffolds add up to 109.3 kb while the total length of all assembly is 114Mb


#####################################
#convert to a tabular output
from Bio import SearchIO
import fnmatch
import os
#from Bio.Blast import NCBIXML


#E_VALUE_THRESH =1e-5


#result_handle = open("my_blast.xml")
#blast_records = NCBIXML.read(result_handle)
#blast_records = list(blast_records)


#for multiple blast results
#blast_records = NCBIXML.parse(result_handle)


#best_hit=blast_records[0]
#for alignment in blast_record.alignments:
#    for hsp in alignment.hsps:
#         if hsp.expect < E_VALUE_THRESH:
#            print("sequence:", alignment.title)
#            print("length:", alignment.length)
#            print("e value:", hsp.expect)


blast_hit_sum=[]
filename=[]


for fn in os.listdir('.'):
    if fnmatch.fnmatch(fn,'*_blast.xml'):filename.append(fn)


for fn in filename:
    blast_qresult = SearchIO.read(fn, "blast-xml")
    blast_hit = blast_qresult[0][0]
    #if blast_hit.evalue<E_VALUE_THRESH:
    blast_hit_sum.append(fn.split('.')[0] + '\t' + blast_hit.hit_description + '\t'+ str(blast_hit.evalue)+'\t' + str(blast_hit.aln_span))


with open('unmapped_nt_blast.sum','w') as output:
    output.write('\n'.join(blast_hit_sum))


output.close()