import sys

x=open(sys.argv[1]).readlines()
y=open(sys.argv[1]+'.top','a')
cur_rec=''

for l in x:
	if l.split()[0]!=cur_rec:
		i=1
		cur_rec=l.split()[0]
		y.write(l)
	else:
		if i<int(sys.argv[2]):
			y.write(l)
			i=i+1


y.close()

