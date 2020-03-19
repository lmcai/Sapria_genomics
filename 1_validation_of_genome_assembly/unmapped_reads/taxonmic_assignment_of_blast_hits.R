#in R
library(ritis)
library(taxize)
x=read.table(‘unmapped_nt_blast.sum’,header=T)
x$nt_hit_desc=as.character(x$nt_hit_desc)
for (i in 1:length(x[,1])){
    taxa=paste(strsplit(x$nt_hit_desc[i],' ')[[1]][1:2],collapse=' ')
    x$hit_taxon=taxa
    class=tax_name(query = taxa, get = "class")
    x$hit_taxon_order[i]=class$class
    family=tax_name(query = taxa, get ="family")
    x$hit_taxon_family[i]=family$family
    
}
write.csv(x,'unmapped_nt_blast.sum',row.names=F)
