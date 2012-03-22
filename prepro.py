

f = open('orange_small_train.data')
f = [line.replace('\r\n','') for line in f]
data = [line.split('\t')  for line in f][1:]  #remove the title (the line 1)
num_features = len(data[1])
num_lines = len(data)

float_index = []
string_index = []

#convert string to float
for i in xrange(num_lines):
	float_count = 0
	for j in xrange(num_features):
		try:
			data[i][j] = float(data[i][j])
			float_count +=1
			float_index.append(j)
		except:
			if (data[i][j]) != '':
				float_count += 1
				string_index.append(j)
	data[i].append(float_count)
	
num_features = num_features + 1  #add a extra feture to num_features -> 231

float_index = list(set(float_index))[:-2]    # num: 174
#remove value 201, 206 as they contain both numbers and strings
string_index = list(set(string_index))   #num: 38


#rotate 50000*231 data to 231*50000 //add one new feature -> 231
data_rotate=[]
for i in xrange(231):
	data_rotate.append( [data[j][i] for j in xrange(50000)])
	
	
#missing value process , only for float attributes
for i in float_index:
	atts = filter(lambda x: x!='', data_rotate[i])
	meanValue = sum(atts) / len(atts)
	data_rotate[i] = [x if x!='' else meanValue for x in data_rotate[i]] 
	

#process for string attributes, 
string_10_bin = {}
atts_count = {}
duplicate = set()
import operator
#find 10 most frequent values
for i in string_index:
	duplicate.clear()
	for x in data_rotate[i] :
		if x not in duplicate:
			atts_count[x] =  data_rotate[i].count(x)
			duplicate.add(x)
	sorted_atts_count = sorted(atts_count.iteritems(), key=operator.itemgetter(1))
	string_10_bin[i] =  [x[0] for x in sorted_atts_count[-11:-1] ]  #fetch 10 most frequent values, including ''
	print i
	
	
#binning using the 10 most frequent values
new_data = data_rotate
for i in string_index:
	bin_index = dict( [ (string_10_bin[i][j],j) for j in xrange(len(string_10_bin[i])) ] )
	new_data[i] = [ bin_index[x] if x in string_10_bin[i] else 0 for x in data_rotate[i] ] 
	print i
	
	
	


	
	





