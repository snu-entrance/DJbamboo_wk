def dic_to_str(dic):
	result = ''
	for key, value in dic.items():
		result += key + ' : ' + value + '\n'
	return result