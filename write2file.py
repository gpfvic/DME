def write2file(data,filename):
	with open(filename,'a') as f:
		for i in xrange(len(data)):
			line = map(str,data[i])
			line = '\t'.join(line)
			f.write(line+'\n')
