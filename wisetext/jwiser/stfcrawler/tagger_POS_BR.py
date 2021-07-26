# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 12:49:15 2017

@author: antoniosousa
"""

import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk import word_tokenize, pos_tag, ne_chunk
import pickle
import os
from fnmatch import fnmatch

def lista_arquivos(raiz, padrao="*"):
    lista = []   
    
    for caminho, subdirs, arquivos in os.walk(raiz):
        for arq in arquivos:
            if fnmatch(arq, padrao):
                lista.append(os.path.join(caminho, arq))
    return (lista)


def ie_preprocess(document):
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]

    return(sentences)

###########################################################################################################


taggerBR = pickle.load(open("tagger.pkl", 'rb'))
stopwords = nltk.corpus.stopwords.words('portuguese')
stemmer = SnowballStemmer("portuguese")
stok = nltk.data.load('tokenizers/punkt/portuguese.pickle')


# Carrega os arquivos de texto
#raiz = "Y:\\juriswiser\\stfcrawler\\pdfs\\txts\\"
raiz = "Z:\\stfcrawler\\pdfs\\TREINO\\"
arquivos = lista_arquivos(raiz,"*.txt")

tr_textos = []
ts_textos = []
i=0

perc = int(len(arquivos)/7)
ts_files = arquivos[:perc]
tr_files = arquivos[perc:]

for arq in tr_files:
    with open(arq, encoding='utf8') as f:
        lines = f.readlines()
    tr_textos.append(''.join(lines))
    i+=1

for arq in ts_files:
    with open(arq, encoding='utf8') as f:
        lines = f.readlines()
    ts_textos.append(''.join(lines))
    i+=1

print(ne_chunk(taggerBR.tag(word_tokenize(ts_textos[0]))))

'''
t1 = nltk.UnigramTagger(tr_tk_txt, backoff=taggerBR)
t2 = nltk.BigramTagger(tr_tk_txt, backoff=t1)    
t2.evaluate(ts_tk_txt)
'''

#dtset_floresta = list(nltk.corpus.floresta.tagged_sents())
#dtset_mcmorpho = [[w[0] for w in sent] for sent in nltk.corpus.mac_morpho.tagged_paras()]

