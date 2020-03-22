#################################
#Genome size estimation based on kmer distribution
#All kmer distribution plots generated here are presented in Figure S##
#################################

##################################
#kmer size=27

dataframe27=read.table('sapria_27mer_out.histo',sep='\t')
#plot(dataframe27$V2,type = 's',ylim=c(0,1e8),xlim=c(0,100),xlab = "27-mer frequency",ylab = "distinct 27-mers",main = "27-mer spectra for: 10X Illumina 3 lanes",cex.main=0.8)
#points(dataframe27[2:100,],pch=20,cex=0.5)

#peak = 28
sum(as.numeric(dataframe27[11:10000,1]*dataframe27[11:10000,2]))/28
#genome size estimation: 2.127278511 Gb

sum(as.numeric(dataframe27[11:55,1]*dataframe27[11:55,2]))/sum(as.numeric(dataframe27[11:10000,1]*dataframe27[11:10000,2]))
#%non-repetitive 0.3241422

##################################
#kmer size=20

dataframe20 <- read.table("20mer_out.histo")
#plot(dataframe20$V2,type = 's',ylim=c(0,1e8),xlim=c(0,80),xlab = "20-mer frequency",ylab = "distinct 20-mers",main = "20-mer spectra for: 10X Illumina 3 lanes",cex.main=0.8)

sum(as.numeric(dataframe20[14:10000,1]*dataframe20[14:10000,2]))/32
#genome size estimation:  1.697552480 G

sum(as.numeric(dataframe20[14:55,1]*dataframe20[14:55,2]))/sum(as.numeric(dataframe20[14:10000,1]*dataframe20[14:10000,2]))
#%non-repetitive 0.276699

##################################
#kmer size=35

dataframe19 <- read.table("35mer_out.histo")
#plot(dataframe19$V2,type = 's',ylim=c(0,1e8),xlim=c(0,50),xlab = "35-mer frequency",ylab = "distinct 35-mers",main = "35-mer spectra for: 10X Illumina 3 lanes",cex.main=0.8)

sum(as.numeric(dataframe19[9:10000,1]*dataframe19[9:10000,2]))/22
#genome size estimation: 2.544764498 G

sum(as.numeric(dataframe19[9:50,1]*dataframe19[9:50,2]))/sum(as.numeric(dataframe19[9:10000,1]*dataframe19[9:10000,2]))
#%non-repetitive 0.3694134
