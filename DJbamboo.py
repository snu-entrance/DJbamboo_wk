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


def Djbamboo(x):

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

comeondata()
print()
#Djbamboo('친구')
#print('--------')
print(Djbamboo('당분간 널 찾지 않으려고 해 그동안은 정말 찾고싶었거든 인연을 가장해 우연인 척 널 보러 갔던 날 정말 말하고 싶었는데 너한테 연락 오고 하루도 빠짐없이 생각했다고 네가 누군가를 만난다는 사실에 밥을 먹다가 울어버렸다고 그리고 내가 정말 힘들 때 안기고 싶었던 품은 그 누구도 아닌 너였다고 있잖아 너한테 연락 왔을 때 나 사실 정말 많이 흔들렸다 너한테 그렇게 여름에 상처받고 바보같이 흔들렸어 진짜 바보같지 내가 물어봤었잖아 어떻게 하면 좋겠어 그리고 나 흔들리면 안 되겠지 너한테는 너무 어려운 질문이었을까 난 확신이 듣고 싶었던 건데 너한테 돌아오는 답변은 모르겠다 뿐이였지 그리고 네 말 날 너무 아프게했어 우린 이제 답이 없잖아 한때는 정말 말 예쁘게 하는 사람이라고 생각했던 너였는데 그런 네가 말로 나를 아프게 할 줄은 정말 꿈에도 몰랐거든 그리고 나 사실 굉장히 여려 그래서 아직도 네가 상처 줬던 말 품 안에 안고 살아 그래도 있잖아 학교생활이 너무 힘들어 눈물이 쏟아지고 사람들 시선이 너무 괴로워하지 말아야 할 생각이 드는 날이면 너부터 생각나 내가 지금 걷고 있는 이 거리에서 니 이름 부르면 딱 한 번만 뒤돌아줬으면 좋겠다 내가 지금 서 있는 이 공간에서 너 이름 부르면 딱 한 번만 달려 와줬으면 좋겠다 그리고 사실 요새는 정말 안 좋은 생각이 많이 들곤 하는데 나 한 번만 안아주면 안 될까 그러면 조금이라도 살고싶을텐데 진짜 보고 싶다 아직도 널 보고 싶어 하는 내가 너무 싫지만 왜 너는 싫지않은걸까 그리고 마지막으로 생일 축하했어 현재형으로 하고 싶은 말이었는데 또 과거형이네 이제 시간이 더 흐르게 된다면 나는 너에게 있어서 이제 과거도 아닌 아무것도 아닌 존재가 되어버리겠지 나에게 있어서 너는 늘 어려운 존재인데 어려운 존재 어려운 존재야 여기서는 말할 수있을것같아 정말 터무니없는 생각이고 헛된 꿈이라는 거 잘 아는데 너가 한 번만 와줬으면 좋겠다 다시 한 번만 딱 한 번만 말해줬으면 좋겠다 달보다 네가 더 예쁘다고'))
#print('--------')
#print(Djbamboo('연대 숲 고민이 있어요. ㅠㅜㅠ 요즘 따라 연락을 하고 지내는 남자가 있어요. 원래 알던 사이이지만 방학을 한 거 나서 얼굴을 못 보게 되면서 카톡을 자주 하고 있거든요 밤에만 연락을 하게 돼요 바쁘긴 하지만 카톡을 전혀 오 가지 않고 저녁 이후부터 잠잘 때 까지만, 연락을 하고 있어요……. 카톡 내용은 뭔가…. 솔직히 남이 보면 호감이라고 느낄 것 같아요. 그렇지만 친구들 말에 의하면 저녁 6시 이후에 연락이 되는 남자는 그냥 외로워서 그런 거라나 맞는 말인 것 같아서 고민이 많네요!! 여러분도 밤에만 연락이 되는 남자는 제가 좋다기보다는 그냥 외로워서라고 생각하시나요!!?'))
#print()