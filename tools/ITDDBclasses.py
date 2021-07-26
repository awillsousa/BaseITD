import os
import json
import logging
from pymongo import MongoClient
from ITDclasses import DocumentoAcordao as DocAcordao

DIR_BASE = '/home/willian//basesML/ITD/'
logging.basicConfig(level=logging.INFO)


class Database():
    def __init__(self, diretorio, nomedb=None, colecao=None, servidor='localhost', porta=27017):
        self.diretorio = diretorio
        self.cliente = self.conecta(servidor, porta)
        self.database = self.getDatabase(nomedb)
        self.colecao = self.getColecao(colecao)


    def conecta(self, servidor, porta):
        try:
            return MongoClient(servidor, porta)
        except Exception as erro:
            logging.error(str(erro))
            return None


    def getDatabase(self, nomedb):
        if self.cliente:
            return self.cliente[nomedb]
        else:
            logging.error("Cliente da base de dados indisponivel!")

    def getColecao(self, colecao):
        if self.database:
            if colecao not in self.database.collection_names():
                self.database.create_collection(colecao)

            return self.database[colecao]
        else:
            logging.error("Base de dados indisponivel!")

    def importaAcordaos(self, sobrescreve=False, listaInserir=None):
        '''
        Importa os acordaos de um determinado diretorio
        :param sobrescreve: Indica se deve sobrescrever documentos existentes
        :return:
        '''
        if not listaInserir:
            dirs_acordaos = os.listdir(self.diretorio)
        else: 
            dirs_acordaos = listaInserir
            
        inseridos = 0
        problemas = 0
        for dir_acordao in dirs_acordaos:
            try:
                acordao = DocAcordao(self.diretorio, str(dir_acordao))
                if not (acordao.ementa is None and \
                   acordao.acordao is None and\
                   acordao.relatorio is None):
                    acordao_id = self.insereAcordao(acordao, sobrescreve)

                if acordao_id:
                    logging.info("Inserido o acordao {0} como objeto {1}".format(acordao.numero, acordao_id))
                    inseridos += 1
                else:
                    logging.error("Problemas ao tentar inserir o acordao {0}".format(acordao.numero))
                    problemas += 1
            except Exception as erro:
                logging.error("Problemas no processamento do acordao {0}".format(dir_acordao))
                problemas += 1
                logging.error(str(erro))

        return {'inseridos': inseridos, 'erros': problemas}

    def getAcordao(self, numero):
        '''
        Retorna um documento acordao de acordo com o seu numero passado
        :param numero: Numero do acordao na base
        :return: Objeto acordao recuperado da base de dados
        '''
        return self.colecao.find_one({'numero': numero})

    def getAcordaos(self, dicquery):
        '''
        Retorna uma lista de acordaos recuperados de acordo com um criterio de busca
        :param dicquery: Dicionario contendo a query a ser executada no banco de dados
        :return: Lista de acordaos
        '''
        return [docacordao for docacordao in self.colecao.find(dicquery)]


    def insereAcordao(self, docacordao, sobrescreve=False):
        '''
        Insere um acordao na base de dados
        :param docacordao: Objeto do tipo DocumentoAcordao
        :param sobrescreve: Indica se deve sobrescrever documentos existentes
        :return: Id do documento inserido ou None caso nao tenha sucesso
        '''

        if sobrescreve:
            try:
                self.colecao.delete_one({"numero": docacordao.numero})
            except Exception as erro:
                logging.error(erro)
                return None

        # Insere o novo acordao
        json_acordao = json.loads(docacordao.toJSON())

        return self.colecao.insert_one(json_acordao).inserted_id

    def updateAcordao(self, dicbusca, dicupdates):
        '''
        Atualiza um conjunto de documentos
        :param dicbusca: Dicionario contendo criterios de busca
        :param dicuupdates: Dicionario contendo campos para atualizacao
        :return: Resultado da inserçao
        '''
        # Busca os documentos de acordo com o criterio de busca
        r_update = self.colecao.update(dicbusca,dicupdates,{'multi': 'true'})

        return r_update

    def criaColecao(self, colecao):
        if self.database:
            try:
                r_create = self.database.create_collection(colecao)
                logging.info(str(r_create))
            except Exception as erro:
                logging.error("Erro ao tentar criar a colecao {}".format(colecao))
                logging.error(str(erro))
        else:
            logging.error("Base de dados indisponivel!")

    def insereVoto(self, docvoto, sobrescreve=False):
        '''
        Insere um voto na base de dados
        :param docvoto: Objeto do tipo Voto
        :param sobrescreve: Indica se deve sobrescrever documentos existentes
        :return: Id do documento inserido ou None caso nao tenha sucesso
        '''
        # Insere o novo acordao
        json_voto = json.loads(docvoto.toJSON())

        return self.colecao.insert_one(json_voto).inserted_id
    
    def insereRelatorio(self, docrelatorio, sobrescreve=False):
        '''
        Insere um relatorio na base de dados
        :param docrelatorio: Objeto do tipo Relatorio
        :param sobrescreve: Indica se deve sobrescrever documentos existentes
        :return: Id do documento inserido ou None caso nao tenha sucesso
        '''
        # Insere o novo acordao
        json_relatorio = json.loads(docrelatorio.toJSON())

        return self.colecao.insert_one(json_relatorio).inserted_id
