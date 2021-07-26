from pymongo import MongoClient
import json
import os
import argparse
from ITDclasses import DocumentoAcordao as DocAcordao
from ITDDBclasses import Database

DIR_BASE = '../ITD/'
database = 'ITD'
colecao = 'DocumentosAcordaos'


def reProcPartes(listaParteReproc):
    baseAcordaos = Database(diretorio=DIR_BASE, nomedb=database, colecao=colecao)

    resultado = baseAcordaos.importaAcordaos(sobrescreve=True, listaInserir=listaParteReproc)
    print(str(resultado))
    
    
def reimportaAcordaos(lista):
    baseAcordaos = Database(diretorio=DIR_BASE, nomedb=database, colecao=colecao)

    resultado = baseAcordaos.importaAcordaos(sobrescreve=True, listaInserir=lista)
    print(str(resultado))
    

def importaBaseCompleta():
    baseAcordaos = Database(diretorio=DIR_BASE, nomedb=database, colecao=colecao)

    resultado = baseAcordaos.importaAcordaos()
    print(str(resultado))


def importaLoteAcordaos():    
    dirs_acordaos = os.listdir(DIR_BASE)
    jsons_acordaos = []

    for dir_acordao in dirs_acordaos:
        #print(dir_acordao)
        try:
            acordao = DocAcordao(DIR_BASE, str(dir_acordao))
            json_acordao = json.loads(acordao.toJSON())

            acordao_id = colecao.insert_one(json_acordao).inserted_id
            print("Inserido o acordao {0}".format(acordao_id))
        except Exception as erro:
            print("Problemas no processamento do acordao {0}".format(dir_acordao))
            print(str(erro))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-a", "--acao", required=True, help="Acao a ser executada")
    args = vars(ap.parse_args())
    
    if args.acao == "importa":
        importaBaseCompleta()
    else:
        print("Ação desconhecida! ")


if __name__ == "__main__":
    main()


