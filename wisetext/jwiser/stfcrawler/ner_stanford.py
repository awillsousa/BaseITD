# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 16:32:58 2017

@author: antoniosousa
"""

import os
import nltk 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
from random import shuffle
from nltk import pos_tag
from nltk.parse import stanford
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from nltk.chunk import conlltags2tree
from nltk.tree import Tree
from nltk.tokenize import PunktSentenceTokenizer

from nltk.corpus.reader.conll import ConllCorpusReader



style.use('fivethirtyeight')
# Remove stopwords
stopwords = nltk.corpus.stopwords.words('portuguese')
# Tokenizador
stok = nltk.data.load('tokenizers/punkt/portuguese.pickle')


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

def pos_text(txt_file):    
    try:
        custom_sent_tokenizer = stok(open(txt_file, mode='r', encoding='UTF-8').read())
        tokenized = custom_sent_tokenizer.tokenize(txt_file)
        for i in tokenized[:5]:
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
            print(tagged)

    except Exception as e:
        print(str(e))

def chunk_text(txt_file):
    try:
        #custom_sent_tokenizer = stok(open(txt_file, mode='r', encoding='UTF-8').read())
        texto = open_file(txt_file)
        custom_sent_tokenizer = PunktSentenceTokenizer(texto)
        tokenized = custom_sent_tokenizer.tokenize(texto)
        for i in tokenized:
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
            chunkGram = r"""Chunk: {<RB.?>*<VB.?>*<NNP>+<NN>?}"""
            chunkParser = nltk.RegexpParser(chunkGram)
            chunked = chunkParser.parse(tagged)
            chunked.draw()     

    except Exception as e:
        print(str(e))



def open_file(txt_file):
   raiz = "Z:\\stfcrawler\\pdfs\\TREINO\\"
   with open(raiz+"741829.txt", 'r', encoding='UTF-8') as f:
        raw_text = f.read() 	    
   return raw_text

'''
Carga dos arquivos textos (raw)
'''
def tok_text(txt_file):
   '''
   raiz = "Z:\\stfcrawler\\pdfs\\TREINO\\"
   with open(raiz+"741829.txt", 'r', encoding='UTF-8') as f:
        raw_text = f.read() 	 
   '''   
   return (word_tokenize(open_file(txt_file)))

# Stanford NER tagger    
def stanford_tagger(token_text):
	st = StanfordNERTagger('/opt/ftminer/stanford/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz',
							'/opt/ftminer/stanford/stanford-ner/stanford-ner.jar',
							encoding='utf-8')   
	ne_tagged = st.tag(token_text)
	return(ne_tagged)
 
# NLTK POS and NER taggers   
def nltk_tagger(token_text):
	tagged_words = nltk.pos_tag(token_text)
	ne_tagged = nltk.ne_chunk(tagged_words)
	return(ne_tagged)

# Tag tokens with standard NLP BIO tags
def bio_tagger(ne_tagged):
		bio_tagged = []
		prev_tag = "O"
		for token, tag in ne_tagged:
			if tag == "O": #O
				bio_tagged.append((token, tag))
				prev_tag = tag
				continue
			if tag != "O" and prev_tag == "O": # Begin NE
				bio_tagged.append((token, "B-"+tag))
				prev_tag = tag
			elif prev_tag != "O" and prev_tag == tag: # Inside NE
				bio_tagged.append((token, "I-"+tag))
				prev_tag = tag
			elif prev_tag != "O" and prev_tag != tag: # Adjacent NE
				bio_tagged.append((token, "B-"+tag))
				prev_tag = tag
		return bio_tagged

# Create tree       
def stanford_tree(bio_tagged):
	tokens, ne_tags = zip(*bio_tagged)
	pos_tags = [pos for token, pos in pos_tag(tokens)]

	conlltags = [(token, pos, ne) for token, pos, ne in zip(tokens, pos_tags, ne_tags)]
	ne_tree = conlltags2tree(conlltags)
	return ne_tree

# Parse named entities from tree
def structure_ne(ne_tree):
	ne = []
	for subtree in ne_tree:
		if type(subtree) == Tree: # If subtree is a noun chunk, i.e. NE != "O"
			ne_label = subtree.label()
			ne_string = " ".join([token for token, pos in subtree.leaves()])
			ne.append((ne_string, ne_label))
	return ne

def read_conll():
    root = "W:\\Maltparser-PT-BR\\pt-br-corrected\\"
    conllcorpus = ConllCorpusReader(root, ".conll", ('words', 'pos', 'tree'))
    
    return(conllcorpus.words('pt-br-universal-test.conll'))


def stanford_main(txt_file):
    #txt_file = "Z:\\stfcrawler\\pdfs\\TREINO\\741829.txt"
    print(structure_ne(stanford_tree(bio_tagger(stanford_tagger(tok_text(txt_file))))))

def nltk_main(txt_file):
    #txt_file = "Z:\\stfcrawler\\pdfs\\TREINO\\741829.txt"
    
    return(structure_ne(nltk_tagger(tok_text(txt_file))))

if __name__ == '__main__':
    txt_file = "Z:\\stfcrawler\\pdfs\\TREINO\\741829.txt"
	 #stanford_main()
    #pos_tok = nltk_main(txt_file)   
    #pessoas = list(set([p for p,l in pos_tok if l in 'PERSON' and len(p.split()) > 1]))
    #t = pos_text(txt_file)
    #chunk_text(txt_file)
    
    root = "W:\\Maltparser-PT-BR\\pt-br-corrected\\"
    #conllcorpus = ConllCorpusReader(root, ".conll", ('words', 'pos', 'tree'))    
    conllcorpus = ConllCorpusReader(root, ".conll", ('words', 'pos', 'tree'))    
    p = conllcorpus.words('pt-br-universal-test.conll')    
    raw_text = conllcorpus.raw('pt-br-universal-test.conll')
    tag_words = str(conllcorpus.tagged_words('pt-br-universal-test.conll'))    
    t = conllcorpus.parsed_sents('pt-br-universal-test.conll')