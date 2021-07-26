# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 16:32:58 2017

@author: antoniosousa
"""

import nltk 
import pickle
from random import shuffle


def extract_entity_names(t):
    entity_names = []

    if hasattr(t, 'label') and t.label:
        if t.label() == 'NE':
            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))

    return entity_names

def untag(tagged_sentence):
    return [w for w, t in tagged_sentence]

def train_tagger():
    dataset1 = list(nltk.corpus.floresta.tagged_sents())
    dataset2 = [[w[0] for w in sent] for sent in nltk.corpus.mac_morpho.tagged_paras()]
    
    traindata = [[(w, t) for (w, t) in sent] for sent in dataset1]
    traindata2 = traindata + [[(w, t) for (w, t) in sent] for sent in dataset2]
    
    shuffle(traindata)
    shuffle(traindata2)
    
    regex_patterns = [
        (r"^[nN][ao]s?$", "ADP"),
        (r"^[dD][ao]s?$", "ADP"),
        (r"^[pP]el[ao]s?$", "ADP"),
        (r"^[nN]est[ae]s?$", "ADP"),
        (r"^[nN]um$", "ADP"),
        (r"^[nN]ess[ae]s?$", "ADP"),
        (r"^[nN]aquel[ae]s?$", "ADP"),
        (r"^\xe0$", "ADP"),
    ]
    
    tagger = nltk.BigramTagger(
                traindata, backoff=nltk.RegexpTagger(
                    regex_patterns, backoff=nltk.UnigramTagger(
                        traindata2, backoff=nltk.AffixTagger(
                            traindata2, backoff=nltk.DefaultTagger('NOUN')
                        )
                    )
                )
            )
    templates = nltk.brill.fntbl37()
    tagger = nltk.BrillTaggerTrainer(tagger, templates)
    tagger = tagger.train(traindata, max_rules=100)
    
    return (tagger)

'''
Carga dos arquivos textos (raw)
'''
raiz = "Z:\\stfcrawler\\pdfs\\TREINO\\"
with open(raiz+"741829.txt", 'r', encoding='UTF-8') as f:
    sample = f.read()


'''
Limpeza dos arquivos textos
'''
# Remove stopwords
stopwords = nltk.corpus.stopwords.words('portuguese')


'''
Segmentacao, tokenizacao, POS Tag
'''
stok = nltk.data.load('tokenizers/punkt/portuguese.pickle')

#sentences = nltk.sent_tokenize(sample)
sentences = stok.tokenize(sample)
tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]

taggerBR = train_tagger()
#tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
tagged_sentences = [taggerBR.tag(sentence) for sentence in tokenized_sentences]
#print(tagged_sentences)
chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)

#for tree in chunked_sentences:
#    print(str(tree))

entity_names = []
for tree in chunked_sentences:
    entity_names.extend(extract_entity_names(tree))

# Print unique entity names
entidades = [n for n in list(set(entity_names)) if len(n.split()) > 1]



for e in entidades: 
    print(e)