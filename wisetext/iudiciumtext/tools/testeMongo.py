from pymongo import MongoClient

client = MongoClient() # conecta num cliente do MongoDB rodando na sua máquina
db = client['SandboxDB'] # acessa o banco de dados
collection = db['DocumentosAcordao'] # acessa a minha coleção dentro desse banco de dados

collection.find_one()

