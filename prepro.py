ftest = open('orange_small_test.data')
ftrain = open('orange_small_train.data')

ftest = [line.replace('\r\n','') for line in ftest]
small_test_data = [line.split('\t')  for line in ftest][1:]
ftrain = [line.replace('\r\n','') for line in ftrain]
small_train_data = [line.split('\t')  for line in ftrain][1:]


float_index_test = []
float_index_train = []
string_index_test = []
string_index_train = []

#convert string to float
for i in xrange(len(small_test_data)):
	test_count = 0
	train_count = 0
	for j in xrange(230):
		try:
			small_test_data[i][j] = float(small_test_data[i][j])
			test_count += 1
			float_index_test.append(j)
		except:
			if (small_test_data[i][j]) != '':
				test_count += 1
				string_index_test.append(j)
	
	
		try:
			small_train_data[i][j] = float(small_train_data[i][j])
			train_count +=1
			float_index_train.append(j)
		except:
			if (small_train_data[i][j]) != '':
				train_count += 1
				string_index_train.append(j)
	small_test_data[i].append(test_count)
	small_train_data[i].append(train_count)

float_index_test = list(set(float_index_test))[:-2]    # num: 174
#remove value 201, 206 as they contain both numbers and strings
float_index_train = list(set(float_index_train))[:-2]
string_index_test = list(set(string_index_test))   #num: 38
string_index_train = list(set(string_index_train))

#check whether a line has both string and float
'''
k=216
for i in xrange(50000):
	try:
		x = float(small_test_data_rotate[k][i])
		print i
	except:
		None
'''


#rotate 50000*231 data to 231*50000 //add one new feature -> 231
small_test_data_rotate=[]
small_train_data_rotate=[]

for i in xrange(231):
	small_test_data_rotate.append( [small_test_data[j][i] for j in xrange(50000)])
	small_train_data_rotate.append( [small_train_data[j][i] for j in xrange(50000)])
	
	
	

#missing value process , only for float attributes

for i in float_index_test:
	atts = filter(lambda x: x!='', small_test_data_rotate[i])
	meanValue = sum(atts) / len(atts)
	small_test_data_rotate[i] =  [x if x!='' else meanValue for x in small_test_data_rotate[i]] 

for i in float_index_train:
	atts = filter(lambda x: x!='', small_train_data_rotate[i])
	meanValue = sum(atts) / len(atts)
	small_train_data_rotate = [x if x!='' else meanValue for x in small_train_data_rotate[i]] 
	
	

#process for string attributes, 
string_10_bin_test = {}
string_10_bin_train = {}
atts_count = {}
duplicate = set()

import operator
#find 10 most frequent values
for i in string_index_test:
	duplicate.clear()
	for x in small_test_data_rotate[i] :
		if x not in duplicate:
			atts_count[x] =  small_test_data_rotate[i].count(x)
			duplicate.add(x)
	sorted_atts_count = sorted(atts_count.iteritems(), key=operator.itemgetter(1))
	string_10_bin_test[i] =  [ x[0]  for x in sorted_atts_count[-11:-1] ]

	duplicate.clear()
	for x in small_train_data_rotate[i] :
		if x not in duplicate:
			atts_count[x] =  small_train_data_rotate[i].count(x)
			duplicate.add(x)
	sorted_atts_count = sorted(atts_count.iteritems(), key=operator.itemgetter(1))
	string_10_bin_train[i] =  [ x[0]  for x in sorted_atts_count[-11:-1] ] 
	
	print i
	
	


#binning using the 10 most frequent values
new_test_data = small_test_data_rotate
new_train_data = small_train_data_rotate

for i in string_index_test:
	test_bin_index = dict( [ (string_10_bin_test[i][j],j) for j in xrange(len(string_10_bin_test[i])) ] )
	new_test_data[i] =  [ test_bin_index[x] if x in string_10_bin_test[i] else 0 for x in small_test_data_rotate[i] ] 

	train_bin_index = dict( [ (string_10_bin_train[i][j],j) for j in xrange(len(string_10_bin_train[i])) ] )
	new_train_data[i] = [ train_bin_index[x] if x in string_10_bin_train[i] else 0 for x in small_train_data_rotate[i] ] 
	print i
	
	
	

	
#normalisation both float and string(int)
for i in xrange(230):
	print i
	minValue = min(new_test_data[i])
	maxValue = max(new_test_data[i])
	diff = maxValue - minValue
	new_test_data[i] = map( lambda x: (x-minValue)/diff, new_test_data[i])
	
	minValue = min(new_train_data[i])
	maxValue = max(new_train_data[i])
	diff = maxValue - minValue
	new_train_data[i] = map( lambda x: (x-minValue)/diff, new_train_data[i])
	


	
	
	


	
	


			
		

'''
>>> for i in string_index_test:
...     print i,string_10_bin_test[i]
... 
190 ['6dX3', 'r__I', 'smXZ']
191 ['0vimfo8zhV', '9hRmfo875g', 'wRXmfo875g', 'CxSr4RXktW', '75lr4RXktW', 'qFpmfo8zhV', '8I1r4RXXnK', 'zKnr4RXktW', 'DHeq9ayfAo', 'r__I']
192 ['qFpmfo8zhV', 'rEUOq2QD1qfkRr6qpua', 'eSGpMwS8zSGgq_trOpckZ5', 'LrdZy8QqgUfkVShG', 'e6CkoqApVR', 'g62hiBSaKg', 'r__I', 'AERks4l', '2Knk1KF', 'smXZ']
193 ['rEUOq2QD1qfkRr6qpua', 'LrdZy8QqgUfkVShG', 'e6CkoqApVR', 'g62hiBSaKg', 'r__I', 'AERks4l', '2Knk1KF', 'SEuy', 'smXZ', 'RO12']
194 ['CiJDdr4TQ0rGERIS', 'g62hiBSaKg', 'LfvqpCtLOY', 'r__I', 'AERks4l', '2Knk1KF', 'SEuy', 'smXZ', 'RO12', '']
195 ['g62hiBSaKg', 'LfvqpCtLOY', 'r__I', 'AERks4l', '2Knk1KF', 'SEuy', 'smXZ', 'RO12', '', 'taul']
196 ['JLbT', '487l', 'TyGl', 'lK27', '0Xwj', '2Knk1KF', 'SEuy', 'smXZ', 'RO12', 'taul']
197 ['487l', 'TyGl', 'fhk21Ss', 'lK27', '0Xwj', '2Knk1KF', 'SEuy', 'smXZ', 'RO12', 'taul']
198 ['487l', 'TyGl', 'fhk21Ss', 'lK27', '0Xwj', '2Knk1KF', 'SEuy', 'smXZ', 'RO12', 'taul']
199 ['TyGl', 'fhk21Ss', 'lK27', '0Xwj', '2Knk1KF', 'SEuy', 'smXZ', '', 'RO12', 'taul']
200 ['TyGl', 'fhk21Ss', 'lK27', '0Xwj', '2Knk1KF', 'SEuy', 'smXZ', 'RO12', '', 'taul']
201 ['TyGl', 'fhk21Ss', 'lK27', '0Xwj', '2Knk1KF', 'SEuy', 'smXZ', 'RO12', '', 'taul']
202 ['TyGl', 'fhk21Ss', 'lK27', '0Xwj', '2Knk1KF', 'SEuy', 'smXZ', 'RO12', '9_Y1', 'taul']
203 ['TyGl', 'fhk21Ss', 'lK27', '0Xwj', '2Knk1KF', 'SEuy', 'smXZ', 'RO12', '9_Y1', 'taul']
204 ['0Xwj', 'sJzTlal', '2Knk1KF', '09_Q', 'SEuy', 'smXZ', 'VpdQ', 'RO12', '9_Y1', 'taul']
205 ['zm5i', '2Knk1KF', '09_Q', 'SEuy', 'smXZ', 'IYzP', 'VpdQ', 'RO12', '9_Y1', 'taul']
206 ['2Knk1KF', '09_Q', 'SEuy', 'smXZ', 'IYzP', 'VpdQ', 'me75fM6ugJ', 'RO12', '9_Y1', 'taul']
207 ['09_Q', 'SEuy', 'smXZ', 'IYzP', 'VpdQ', 'me75fM6ugJ', 'RO12', '9_Y1', 'kIsH', 'taul']
209 ['SEuy', 'smXZ', 'IYzP', 'VpdQ', 'me75fM6ugJ', 'RO12', '9_Y1', 'kIsH', 'uKAI', 'taul']
210 ['smXZ', 'IYzP', 'VpdQ', 'me75fM6ugJ', 'RO12', 'L84s', '9_Y1', 'kIsH', 'uKAI', 'taul']
211 ['IYzP', 'NhsEn4L', 'VpdQ', 'me75fM6ugJ', 'RO12', 'L84s', '9_Y1', 'kIsH', 'uKAI', 'taul']
212 ['NhsEn4L', 'VpdQ', 'me75fM6ugJ', 'RO12', 'L84s', '9_Y1', 'kIsH', 'uKAI', 'taul', '']
213 ['', 'NhsEn4L', 'VpdQ', 'me75fM6ugJ', 'RO12', 'L84s', '9_Y1', 'kIsH', 'uKAI', 'taul']
214 ['NhsEn4L', 'VpdQ', 'me75fM6ugJ', 'RO12', 'L84s', '9_Y1', 'kIsH', 'uKAI', 'taul', '']
215 ['NhsEn4L', 'VpdQ', 'me75fM6ugJ', 'RO12', 'L84s', '9_Y1', 'kIsH', 'uKAI', 'taul', '']
216 ['IYzP', 'NhsEn4L', 'VpdQ', 'me75fM6ugJ', 'RO12', 'L84s', '9_Y1', 'kIsH', 'uKAI', 'taul']
217 ['cJvF', 'NhsEn4L', 'VpdQ', 'me75fM6ugJ', 'RO12', 'L84s', '9_Y1', 'kIsH', 'uKAI', 'taul']
218 ['NhsEn4L', 'VpdQ', 'me75fM6ugJ', 'RO12', 'FzaX', 'L84s', '9_Y1', 'kIsH', 'uKAI', 'taul']
219 ['NhsEn4L', 'VpdQ', 'me75fM6ugJ', 'RO12', 'L84s', 'FzaX', '9_Y1', 'kIsH', 'uKAI', 'taul']
220 ['VpdQ', 'me75fM6ugJ', 'RO12', 'oslk', 'L84s', 'FzaX', '9_Y1', 'kIsH', 'uKAI', 'taul']
221 ['VpdQ', 'me75fM6ugJ', 'RO12', 'oslk', 'L84s', 'FzaX', '9_Y1', 'kIsH', 'uKAI', 'taul']
222 ['me75fM6ugJ', 'RO12', 'LM8l689qOp', 'oslk', 'L84s', 'FzaX', '9_Y1', 'kIsH', 'uKAI', 'taul']
223 ['RO12', 'LM8l689qOp', 'oslk', 'L84s', 'FzaX', '9_Y1', 'kIsH', 'uKAI', 'taul', '']
224 ['me75fM6ugJ', 'RO12', 'LM8l689qOp', 'oslk', 'L84s', 'FzaX', '9_Y1', 'kIsH', 'uKAI', 'taul']
225 ['me75fM6ugJ', 'RO12', 'LM8l689qOp', 'oslk', 'L84s', 'FzaX', '9_Y1', 'kIsH', 'uKAI', 'taul']
226 ['RAYp', 'RO12', 'LM8l689qOp', 'oslk', 'L84s', 'FzaX', '9_Y1', 'kIsH', 'uKAI', 'taul']
227 ['RAYp', 'RO12', 'LM8l689qOp', 'oslk', 'L84s', 'FzaX', '9_Y1', 'kIsH', 'uKAI', 'taul']
228 ['RAYp', 'RO12', 'LM8l689qOp', 'oslk', 'L84s', 'FzaX', '9_Y1', 'kIsH', 'uKAI', 'taul']
'''
'''
>>> for i in string_index_train:
...     print i,string_10_bin_train[i]
... 
190 ['6dX3', 'r__I', 'smXZ']
191 ['CxSr4RXktW', '2jirEyXktW', '1GdOj1KXzC', '75lr4RXktW', '8I1r4RXXnK', 'HYTrjIK12c', 'zKnr4RXktW', 'DHeq9ayfAo', 'qFpmfo8zhV', 'r__I']
192 ['qFpmfo8zhV', 'eSGpMwS8zSGgq_trOpckZ5', 'rEUOq2QD1qfkRr6qpua', 'LrdZy8QqgUfkVShG', 'e6CkoqApVR', 'g62hiBSaKg', 'r__I', 'AERks4l', '2Knk1KF', 'smXZ']
193 ['rEUOq2QD1qfkRr6qpua', 'LrdZy8QqgUfkVShG', 'e6CkoqApVR', 'g62hiBSaKg', 'r__I', 'AERks4l', '2Knk1KF', 'SEuy', 'smXZ', 'RO12']
194 ['CiJDdr4TQ0rGERIS', 'g62hiBSaKg', 'LfvqpCtLOY', 'r__I', 'AERks4l', '2Knk1KF', 'SEuy', 'smXZ', 'RO12', '']
195 ['g62hiBSaKg', 'LfvqpCtLOY', 'r__I', 'AERks4l', '2Knk1KF', 'SEuy', 'smXZ', 'RO12', '', 'taul']
196 ['JLbT', '487l', 'TyGl', 'lK27', '0Xwj', '2Knk1KF', 'SEuy', 'smXZ', 'RO12', 'taul']
197 ['487l', 'TyGl', 'fhk21Ss', 'lK27', '0Xwj', '2Knk1KF', 'SEuy', 'smXZ', 'RO12', 'taul']
198 ['487l', 'TyGl', 'fhk21Ss', 'lK27', '0Xwj', '2Knk1KF', 'SEuy', 'smXZ', 'RO12', 'taul']
199 ['TyGl', 'fhk21Ss', 'lK27', '0Xwj', '2Knk1KF', 'SEuy', 'smXZ', '', 'RO12', 'taul']
200 ['TyGl', 'fhk21Ss', 'lK27', '0Xwj', '2Knk1KF', 'SEuy', 'smXZ', 'RO12', '', 'taul']
201 ['487l', 'TyGl', 'fhk21Ss', 'lK27', '0Xwj', '2Knk1KF', 'SEuy', 'smXZ', 'RO12', 'taul']
202 ['TyGl', 'fhk21Ss', 'lK27', '0Xwj', '2Knk1KF', 'SEuy', 'smXZ', 'RO12', '9_Y1', 'taul']
203 ['TyGl', 'fhk21Ss', 'lK27', '0Xwj', '2Knk1KF', 'SEuy', 'smXZ', 'RO12', '9_Y1', 'taul']
204 ['sJzTlal', '0Xwj', '2Knk1KF', '09_Q', 'SEuy', 'smXZ', 'VpdQ', 'RO12', '9_Y1', 'taul']
205 ['zm5i', '2Knk1KF', '09_Q', 'SEuy', 'smXZ', 'IYzP', 'VpdQ', 'RO12', '9_Y1', 'taul']
206 ['2Knk1KF', '09_Q', 'SEuy', 'smXZ', 'IYzP', 'VpdQ', 'me75fM6ugJ', 'RO12', '9_Y1', 'taul']
207 ['09_Q', 'SEuy', 'smXZ', 'IYzP', 'VpdQ', 'me75fM6ugJ', 'RO12', '9_Y1', 'kIsH', 'taul']
209 ['SEuy', 'smXZ', 'IYzP', 'VpdQ', 'me75fM6ugJ', 'RO12', '9_Y1', 'kIsH', 'uKAI', 'taul']
210 ['smXZ', 'IYzP', 'VpdQ', 'me75fM6ugJ', 'RO12', 'L84s', '9_Y1', 'kIsH', 'uKAI', 'taul']
211 ['IYzP', 'NhsEn4L', 'VpdQ', 'me75fM6ugJ', 'RO12', 'L84s', '9_Y1', 'kIsH', 'uKAI', 'taul']
212 ['NhsEn4L', 'VpdQ', 'me75fM6ugJ', 'RO12', 'L84s', '9_Y1', 'kIsH', 'uKAI', 'taul', '']
213 ['', 'NhsEn4L', 'VpdQ', 'me75fM6ugJ', 'RO12', 'L84s', '9_Y1', 'kIsH', 'uKAI', 'taul']
214 ['NhsEn4L', 'VpdQ', 'me75fM6ugJ', 'RO12', 'L84s', '9_Y1', 'kIsH', 'uKAI', 'taul', '']
215 ['NhsEn4L', 'VpdQ', 'me75fM6ugJ', 'RO12', 'L84s', '9_Y1', 'kIsH', 'uKAI', 'taul', '']
216 ['IYzP', 'NhsEn4L', 'VpdQ', 'me75fM6ugJ', 'RO12', 'L84s', '9_Y1', 'kIsH', 'uKAI', 'taul']
217 ['cJvF', 'NhsEn4L', 'VpdQ', 'me75fM6ugJ', 'RO12', 'L84s', '9_Y1', 'kIsH', 'uKAI', 'taul']
218 ['NhsEn4L', 'VpdQ', 'me75fM6ugJ', 'RO12', 'L84s', 'FzaX', '9_Y1', 'kIsH', 'uKAI', 'taul']
219 ['NhsEn4L', 'VpdQ', 'me75fM6ugJ', 'RO12', 'L84s', 'FzaX', '9_Y1', 'kIsH', 'uKAI', 'taul']
220 ['VpdQ', 'me75fM6ugJ', 'RO12', 'oslk', 'L84s', 'FzaX', '9_Y1', 'kIsH', 'uKAI', 'taul']
221 ['VpdQ', 'me75fM6ugJ', 'RO12', 'oslk', 'L84s', 'FzaX', '9_Y1', 'kIsH', 'uKAI', 'taul']
222 ['me75fM6ugJ', 'RO12', 'LM8l689qOp', 'oslk', 'L84s', 'FzaX', '9_Y1', 'kIsH', 'uKAI', 'taul']
223 ['RO12', 'LM8l689qOp', 'oslk', 'L84s', 'FzaX', '9_Y1', 'kIsH', 'uKAI', 'taul', '']
224 ['me75fM6ugJ', 'RO12', 'LM8l689qOp', 'oslk', 'L84s', 'FzaX', '9_Y1', 'kIsH', 'uKAI', 'taul']
225 ['me75fM6ugJ', 'RO12', 'LM8l689qOp', 'oslk', 'L84s', 'FzaX', '9_Y1', 'kIsH', 'uKAI', 'taul']
226 ['RAYp', 'RO12', 'LM8l689qOp', 'oslk', 'L84s', 'FzaX', '9_Y1', 'kIsH', 'uKAI', 'taul']
227 ['RAYp', 'RO12', 'LM8l689qOp', 'oslk', 'L84s', 'FzaX', '9_Y1', 'kIsH', 'uKAI', 'taul']
228 ['RAYp', 'RO12', 'LM8l689qOp', 'oslk', 'L84s', 'FzaX', '9_Y1', 'kIsH', 'uKAI', 'taul']
'''















