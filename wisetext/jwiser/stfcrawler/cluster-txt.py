# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 10:27:07 2017

@author: antoniosousa
"""

import os
from fnmatch import fnmatch
from numpy import loadtxt
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.cluster.hierarchy import ward, dendrogram
from sklearn.manifold import MDS
from nltk.stem.snowball import SnowballStemmer
import matplotlib.pyplot as plt
import matplotlib as mpl
import pickle
import nltk
import numpy as np
import pandas as pd
import re
import os
import codecs
from sklearn import feature_extraction
import mpld3


def lista_arquivos(raiz, padrao="*"):
    lista = []   
    
    for caminho, subdirs, arquivos in os.walk(raiz):
        for arq in arquivos:
            if fnmatch(arq, padrao):
                lista.append(os.path.join(caminho, arq))
    return (lista)    

# here I define a tokenizer and stemmer which returns the set of stems in the text that it is passed
def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems

def tokenize_only(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens

def strip_proppers_POS(text):
    tagged = pos_tag(text.split()) #use NLTK's part of speech tagger
    non_propernouns = [word for word,pos in tagged if pos != 'NNP' and pos != 'NNPS']
    return non_propernouns


###########################################################################################################


stopwords = nltk.corpus.stopwords.words('portuguese')
stemmer = SnowballStemmer("portuguese")

# Carrega os arquivos de texto
#raiz = "Y:\\juriswiser\\stfcrawler\\pdfs\\txts\\"
raiz = "Y:\\juriswiser\\stfcrawler\\pdfs\\BONS_CONVS\\"
arquivos = lista_arquivos(raiz,"*.txt")

textos = []
i=0
#arquivos = arquivos[:10]
for arq in arquivos:
    with open(arq, encoding='utf8') as f:
        lines = f.readlines()
    textos.append(''.join(lines))
    i+=1
    
totalvocab_stemmed = []
totalvocab_tokenized = []
for texto in textos:
    allwords_stemmed = tokenize_and_stem(texto)
    totalvocab_stemmed.extend(allwords_stemmed)
    
    allwords_tokenized = tokenize_only(texto)
    totalvocab_tokenized.extend(allwords_tokenized)    

vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index = [x for x in range(len(totalvocab_tokenized))])
tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                                 min_df=0.2, stop_words=stopwords,
                                 use_idf=True, tokenizer=tokenize_only, ngram_range=(1,3))

tfidf_matrix = tfidf_vectorizer.fit_transform(textos)
terms = tfidf_vectorizer.get_feature_names()
dist = 1 - cosine_similarity(tfidf_matrix)

num_clusters = 3
km = KMeans(n_clusters=num_clusters)
km.fit(tfidf_matrix)
clusters = km.labels_.tolist()

lista_arquivos = { 'arquivo': arquivos, 'texto': textos, 'cluster': clusters }
frame = pd.DataFrame(lista_arquivos, index = [clusters] , columns = ['arquivo', 'texto', 'cluster'])
#frame = pd.DataFrame(lista_arquivos, index = [x for x in range(len(arquivos))]  , columns = ['arquivo', 'texto', 'cluster'])
print("Contagem por cluster: \n {0}".format(str(frame['cluster'].value_counts())))

grouped = frame['arquivo'].groupby(frame['cluster'])
print(str(grouped))

# Lista os principais termos de cada cluster
print("Termos Top20 por cluster: \n")
order_centroids = km.cluster_centers_.argsort()[:, ::-1]
for i in range(num_clusters):
    print("Cluster %d words:" % i, end='')
    for ind in [w for w in order_centroids[i, :20] if w not in stopwords]:
        print(" {0}".format(vocab_frame['words'][ind]), end=',')
    print("\n\n")    
    print("Cluster %d arquivos:" % i, end='')
    for arquivo in frame.ix[i]['arquivo'].values.tolist():
        print(' %s,' % arquivo, end='')
    print("\n\n")
    
    
# Exporta tabelas para HTML
arquivos_html = "<html>"
arquivos_html += "<h3>Cluster 0</h3>"
arquivos_html += frame[['arquivo']].loc[frame['cluster'] == 0].to_html(index=False)
arquivos_html += "<h3>Cluster 1</h3>"
arquivos_html += frame[['arquivo']].loc[frame['cluster'] == 1].to_html(index=False)
arquivos_html += "<h3>Cluster 2</h3>"
arquivos_html += frame[['arquivo']].loc[frame['cluster'] == 2].to_html(index=False)
arquivos_html += "</html>"

# Visualizacao dos clusters
MDS()

# two components as we're plotting points in a two-dimensional plane
# "precomputed" because we provide a distance matrix
# we will also specify `random_state` so the plot is reproducible.
mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
pos = mds.fit_transform(dist)  # shape (n_components, n_samples)
xs, ys = pos[:, 0], pos[:, 1]

'''
tagger = pickle.load(open("tagger.pkl", "wb"))
portuguese_sent_tokenizer = nltk.data.load("tokenizers/punkt/portuguese.pickle")
sentences = portuguese_sent_tokenizer.tokenize(textos)
tags = [tagger.tag(nltk.word_tokenize(sentence)) for sentence in sentences]
'''

#set up colors per clusters using a dict
cluster_colors = {0: '#1b9e77', 1: '#d95f02', 2: '#7570b3', 3: '#e7298a', 4: '#66a61e'}

#set up cluster names using a dict
cluster_names = {0: 'Documentos Tipo 1', 
                 1: 'Documentos Tipo 2',
                 2: 'Documentos Tipo 3'}
                 #3: 'Documentos Tipo 4',
                 #4: 'Documentos Tipo 5'
                 #}

#%matplotlib inline

#create data frame that has the result of the MDS plus the cluster numbers and titles
df = pd.DataFrame(dict(x=xs, y=ys, label=clusters, title=arquivos)) 

#group by cluster
groups = df.groupby('label')

# set up plot
fig, ax = plt.subplots(figsize=(17, 9)) # set size
ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling

#iterate through groups to layer the plot
#note that I use the cluster_name and cluster_color dicts with the 'name' lookup to return the appropriate color/label
for name, group in groups:
    ax.plot(group.x, group.y, marker='o', linestyle='', ms=12, label=cluster_names[name], color=cluster_colors[name], mec='none')
    ax.set_aspect('auto')
    ax.tick_params(\
        axis= 'x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelbottom='off')
    ax.tick_params(\
        axis= 'y',         # changes apply to the y-axis
        which='both',      # both major and minor ticks are affected
        left='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelleft='off')
    
ax.legend(numpoints=1)  #show legend with only 1 point

#add label in x,y position with the label as the film title
#for i in range(len(df)):
#    ax.text(df.ix[i]['x'], df.ix[i]['y'], str(df.ix[i]['title']).split('\\')[-1], size=8)  
    
    
plt.show() #show the plot
plt.close()

#uncomment the below to save the plot if need be
#plt.savefig('clusters_small_noaxes.png', dpi=200)

linkage_matrix = ward(dist) #define the linkage_matrix using ward clustering pre-computed distances

fig, ax = plt.subplots(figsize=(15, 20)) # set size
ax = dendrogram(linkage_matrix, orientation="right", labels=[arq.split('\\')[-1] for arq in arquivos]);

plt.tick_params(\
    axis= 'x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off')

plt.tight_layout() #show plot with tight layout
plt.show() #show the plot

#uncomment below to save figure
#plt.savefig('ward_clusters.png', dpi=200) #save figure as ward_clusters

plt.close()






