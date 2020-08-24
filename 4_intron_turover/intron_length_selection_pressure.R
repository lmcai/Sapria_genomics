#in R
setwd('Dropbox/Sapria/longintron_annotation/')
x=read.table('rnd1_rerun.intron.rnd2_old_snap_evidence_based.omega.tsv',header = T)
x=x[x$omega<0.6,]

cor.test(x$max_intron_length, x$omega, method='pearson')

	Pearson's product-moment correlation

data:  x$max_intron_length and x$omega
t = 6.8334, df = 3221, p-value = 9.875e-12
alternative hypothesis: true correlation is not equal to 0
95 percent confidence interval:
 0.08536737 0.15343396
sample estimates:
      cor 
0.1195411 

pearson_significance <- function(cutoff, df) {
    a=df[df$max_intron_length<cutoff,]
    b=df[df$max_intron_length>cutoff,]
    a_p=cor.test(a$max_intron_length, a$omega, method="pearson")$p.value
    b_p=cor.test(b$max_intron_length, b$omega, method="pearson")$p.value
    return(c(a_p,b_p))
}
c=c(0,0,0)
for (i in seq(10,10000,10)){
c=rbind(c,c(i,pearson_significance(i,x)))
}
##
#find break point 
plot(0,1, xlim=c(0,10000),ylim=c(0,1),pch=20,cex=0.4,xlab = 'max intron length break point (bp)',ylab='p-value',main = 'Pearson\'s correlation test p-value for introns <breaks point')
lines(c[,1],c[,2],pch=20,cex=0.4)
lines(c[,1],c[,3],pch=20,cex=0.4,col='red')

##scatter plot of maax intron length and omega
#break_pt=2000
break_pt=4960

data1=x[x$max_intron_length>break_pt & x$max_intron_length<40000 & x$omega<0.4,]
data2=x[x$max_intron_length<break_pt & x$omega<0.4,]

#model1<-lm(omega ~ max_intron_length, data = data1)
library(ggplot2)
ggplot(data1, aes(x=max_intron_length, y=omega))+
    geom_point(size=0.4)+
    geom_smooth(data=data1,method=lm, se=TRUE)+
    theme_classic()+
    geom_point(data=data2,size=0.4, color='gray')+
    #geom_smooth(data=data2,method=lm, se=TRUE)+
    geom_vline(xintercept=break_pt, linetype='dashed', color='darkblue')
    
