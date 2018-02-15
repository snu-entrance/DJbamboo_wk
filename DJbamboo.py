#-*- coding: utf-8 -*- 
import re
from konlpy.tag import Twitter
import numpy as np
import pandas as pd
import os
from spellChecker import spellChecker

def comeondata():

    data_dir = os.environ['bamboo_data']

    global music_info
    music_info = pd.read_csv(data_dir+'/topic3.csv', encoding='utf-8')

    global music_vec
    music_vec = pd.read_csv(data_dir+'/lov.csv')

    global word_vec
    global word_set
    word_vectors = pd.read_csv(data_dir+'/word_vectors.csv', encoding='utf-8')

    word_set = word_vectors['X']
    word_vec = word_vectors[[col for col in word_vectors.columns if col != 'X']]

    global wordve
    wordve = word_set.values


def DJbamboo(x):

    pos_tagger = Twitter()
    
    def tokenize(doc):
        return ['/'.join(t) for t in pos_tagger.pos(str(doc), norm=True, stem=True)]

    x = spellChecker(x)
    docs = tokenize(x)

    def test(s):
        hangul = re.compile('[^ |가-힣]+') # 한글과 띄어쓰기를 제외한 모든 글자
        result = hangul.sub('', s) # 한글과 띄어쓰기를 제외한 모든 부분을 제거
        return(result)

    def np_index(np_array, x):
        return sum((np_array == x) * np.array(range(len(np_array))))

    rex = test(str(docs))
    rex = rex.split(" ")

    ind = []
    for i in range(len(rex)):
        if rex[i] in wordve:
            ix = np_index(wordve, rex[i])
            ind.append(word_vec.iloc[ix])

    ind = np.array(ind)
    ind = ind.astype(np.float64)
    
    savec = np.mean(ind, axis=0)
    
    def cosine_measure(v1, v2):
        return np.dot(v1,v2) / np.sqrt(np.dot(v2,v2))

    vector_dot_result = cosine_measure(music_vec, savec)

    # 몇 개 뽑?
    n_get = 10
    rst = {}
    for i in range(n_get):
        argmax = np.argmax(vector_dot_result)
        rst['song'+str(i+1)] = music_info.loc[argmax,'title']
        rst['name'+str(i+1)] = music_info.loc[argmax,'artist']
        #print('{0} {1:10s} {2:6s}'.format(vector_dot_result[argmax], 
        #    music_info.loc[argmax,'title'], music_info.loc[argmax,'artist']))
        vector_dot_result[argmax] = np.min(vector_dot_result)-1

    return(rst)

if __name__ == '__main__':
    comeondata()