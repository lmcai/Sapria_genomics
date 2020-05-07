x=read.table('sap.shortintron1k.omega')
y=read.table('sap.longintron10k.omega')
x=x[!is.na(x$V3),]
x=x[x$V4<4,]
x=x[x$V4<4 & x$V3/x$V4<1,]
y=y[!is.na(y$V3),]
y=y[y$V4<4 & y$V3/y$V4<1,]
plot(density(x$V3/x$V4,na.rm = T),main='',xlab='dN/dS')
lines(density(y$V3/y$V4,na.rm = T))
t.test(x$V3/x$V4,y$V3/y$V4,alternative='less')

	Welch Two Sample t-test

data:  x$V3/x$V4 and y$V3/y$V4
t = -2.5844, df = 1453, p-value = 0.004925
alternative hypothesis: true difference in means is less than 0
95 percent confidence interval:
         -Inf -0.003219344
sample estimates:
mean of x mean of y 
0.1555595 0.1644247 


z=read.table('sap.longintron1k.omega',stringsAsFactors = F)
z=z[!is.na(z$V3),]
z=z[z$V4<4 & z$V3/z$V4<1,]
t.test(x$V3/x$V4,z$V3/z$V4,alternative='less')

	Welch Two Sample t-test

data:  x$V3/x$V4 and z$V3/z$V4
t = -0.70889, df = 2706.5, p-value = 0.2392
alternative hypothesis: true difference in means is less than 0
95 percent confidence interval:
       -Inf 0.00277715
sample estimates:
mean of x mean of y 
0.1555595 0.1576616 