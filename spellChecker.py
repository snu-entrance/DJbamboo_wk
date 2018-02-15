#-*- coding: utf-8 -*-
from hanspell import spell_checker

spell_checker_limit = 500
sep_len = int(spell_checker_limit * 0.9)

def spellChecker(x):
	if len(x) <= spell_checker_limit:
		return spell_checker.check(x).checked
	lx = seperateSentence(x)

	result_x = ''

	for sen in lx:
		result_x += spell_checker.check(sen).checked

	return result_x

def seperateSentence(x):
	if len(x) <= spell_checker_limit:
		return [x]

	# 만약 sep가 발견되면, 그 값을 기준으로 두 문장으로 나누어준다.
	sep_words=['!', '?', '.', ',', ' ']
	for sep in sep_words:
		try:
			ind = x[sep_len:spell_checker_limit].index(sep)
		except:
			ind = -1
		if ind != -1:
			break

	# 만약 모든 sep를 못 발견하면, 500자 기준으로 나누고, 뒤 문장은 다시 함수에 넣고 돌린다.
	if ind == -1:
		return [x[:500]]+seperateSentence(x[500:])

	return [x[:(sep_len+ind)]]+seperateSentence(x[500:])