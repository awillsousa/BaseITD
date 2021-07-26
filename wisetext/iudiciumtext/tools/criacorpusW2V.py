# -*- coding: utf-8 -*-
from ITDDBclasses import Database
import logging
import argparse
import utilsNLP as util

'''
Criacao de um base de treino para a geracao de word embeddings baseados nos
textos da base ITD. Para treinamento do 
'''

DIR_BASE = '/home/willian/basesML/ITD/'
database = 'SandboxDB'
colecao = 'DocumentosAcordaos'

logging.basicConfig(level=logging.DEBUG)


def escreveArq(arquivo, textos):
    try:
        with open(arquivo, 'a+', encoding='utf8') as farq:
            farq.write('\n'.join(textos))
                
    except IOError as erro:
        logging.error("Erro ao tentar abrir o arquivo {}".format({arquivo}))
    
def limpatexto(texto):        
    txtlimpo = util.clean_text(texto)

    # Tokeniza e remove sentencas pequenas e malformadas    
    final= []
    for sent in util.sent_tokenizer.tokenize(txtlimpo):
        if sent.count(' ') >= 3 and sent[-1] in ['.', '!', '?', ';']:
            if sent[0:2] == '- ':
                sent = sent[2:]
            elif sent[0] == ' ' or sent[0] == '-':
                sent = sent[1:]
            
            final.append(util.clean_setence(sent))
    
    return " ".join(final)

def criacorpustreino(foutput):
    baseAcordaos = Database(diretorio=DIR_BASE, nomedb=database, colecao=colecao)
    
    acordaos = [docacordao for docacordao in baseAcordaos.colecao.find({"$and":[{"relatorio": {"$ne": None}}, 
                                                                                             {'votos': {'$not': {'$size': 0}}}, 
                                                                                             {'partes': {'$not': {'$size': 0}}}] }, 
                                                                                    {"numero": 1, "ementa": 1, "acordao": 1, 
                                                                                     "partes": 1,"relatorio": 1, "votos": 1})]
    txts = None
    vocab = set([])
    tokens = 0    
    for acordao in acordaos:
        txts = []
        logging.info("Processando acordao {0}".format(acordao['numero']))
        
        if acordao['ementa']:
            txts.append(limpatexto(acordao['ementa']['texto']))
        
        if acordao['acordao']:
            txts.append(limpatexto(acordao['acordao']['texto']))
        
        if acordao['relatorio']:
            txts.append(limpatexto(acordao['relatorio']['texto']))
        
        if acordao['votos']:
            for voto in acordao['votos']:
                txts.append(limpatexto(voto['texto']))
        
        escreveArq(foutput, txts)
    
        # Contabiliza a quantidade de tokens
        # e adiciona palavras no vocabulario        
        for t in txts:
            tokens += t.count(' ') + 1
            for w in t.split():
                vocab.add(w)
        
    # Grava o vocabulario e as informaçoes dos textos
    # processados            
    with open("ITD_W2V.vocab", 'w+', encoding='utf8') as farq:
        l_vocab = list(vocab)
        l_vocab.sort()
        farq.write('\n'.join(l_vocab))

    with open("ITD_W2V.info", 'w+', encoding='utf8') as farq:
        farq.write('Total de tokens: {}\n'.format(tokens))
        farq.write('Tamanho do Vocabulario: {}\n'.format(len(vocab)))
        
    print('Total de tokens: ', tokens)
    print('Tamanho do Vocabulario: ', len(vocab))

if __name__ == '__main__':    
    logging.info("Iniciada a aplicaçao")
    parser = argparse.ArgumentParser(
        description='''Script para limpeza de arquivos da base ITD para treinamento 
                    de modelo word embbedings.''')

    parser.add_argument('--output',
                        type=str,
                        default='ITD_W2V.train',
                        help='Arquivo de saida')

    args = parser.parse_args()
    foutput = args.output

    criacorpustreino(foutput)
    logging.info("Encerrada a aplicaçao")
    



    



