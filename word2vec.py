import pandas as pd
from konlpy.tag import Twitter
from gensim.models.word2vec import Word2Vec
from random import shuffle

def make_wv(data,tag=True,using_tag = ['Noun','Verb','Adjective'],size=100,window=5,min_count=100):
    data = shuffle(data)

    pos_tagger = Twitter()
    def tokenize(doc):
        return ['/'.join(t) for t in pos_tagger.pos(str(doc), norm=True, stem=True)]
    
    if tag is True:
        data_tag = [tokenize(x) for x in data]
    else:
        data_tag = x
    
    def tag_filter(x):
        out = []
        for t in x:
            if t.split('/')[1] in using_tag:
                out.append(t)
        return out
    
    data_filter = [tag_filter(x) for x in data_tag]
    model = Word2Vec(data_filter, size=size, window=window, min_count=min_count, iter=10)
    wv_df =pd.DataFrame(model.wv[model.wv.vocab])
    
    return pd.concat([pd.Series(list(model.wv.vocab.keys())),wv_df],axis=1)