# -*- coding: utf-8 -*-
from ITDDBclasses import Database
import logging
import argparse
import utilsNLP as util

'''
Criacao de um base de treino de um classificador baseados nos
textos da base ITD.
'''

DIR_BASE = '/home/willian/basesML/ITD/'
database = 'SandboxDB'
colecao = 'AcordaosRelatorios'

logging.basicConfig(level=logging.DEBUG)

MINISTROS_OK = ['MIN_GILMAR_MENDES', 'MIN_MARCO_AURELIO', 'MIN_RICARDO_LEWANDOWSKI', 
               'MIN_TEORI_ZAVASCKI', 'MIN_DIAS_TOFFOLI', 'MIN_CELSO_DE_MELLO', 
               'MIN_GILMAR_MENDES', 'MIN_EDSON_FACHIN', 'MIN_ROSA_WEBER', 'MIN_CARMEN_LUCIA', 'MIN_LUIZ_FUX',
               'MIN_ALEXANDRE_DE_MORAES', 'MIN_ROBERTO_BARROSO']


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
    baseRelatorios = Database(diretorio=DIR_BASE, nomedb=database, colecao=colecao)
    
    relatorios = [docacordao for docacordao in baseRelatorios.colecao.find({})]
    txts = []    
    total_relatorios = 0     
    label = ""
    for relatorio in relatorios:        
        if relatorio and \
           relatorio['relator'] in MINISTROS_OK and\
           relatorio['texto'] != '':            
           texto_relatorio = limpatexto(relatorio['texto'])
           label = "__label__{0}".format(relatorio['relator'])
           txts.append("{0} {1}".format(label,texto_relatorio))
           total_relatorios += 1
        
    escreveArq(foutput, txts)
            
    # Grava o vocabulario e as informa??oes dos textos
    # processados                
    with open("ITD_CLFRelatorio.info", 'w+', encoding='utf8') as farq:
        farq.write('Total de votos: {}\n'.format(total_relatorios))
        
    print('Total de votos: {}\n'.format(total_relatorios))

if __name__ == '__main__':    
    logging.info("Iniciada a aplica??ao")
    parser = argparse.ArgumentParser(
        description='''Script para limpeza de arquivos da base ITD para treinamento 
                    de modelo de classificacao.''')

    parser.add_argument('--output',
                        type=str,
                        default='ITD_CLFRelatorios.train',
                        help='Arquivo de saida')

    args = parser.parse_args()
    foutput = args.output

    criacorpustreino(foutput)
    logging.info("Encerrada a aplica??ao")
    



    



