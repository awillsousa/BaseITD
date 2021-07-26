from urllib import request
import requests
from bs4 import BeautifulSoup
import re

#url = "http://www.stf.jus.br/portal/jurisprudencia/listarJurisprudencia.asp?s1=%28JUSTICA+ADJ2+TRABALHO+E+COMPET%24+E+ACIDENTE+ADJ2+TRABALHO%29&base=baseAcordaos&url=http://tinyurl.com/l2448cn"

class PaginaHTML:    
    def __init__(self, url):
        self.url = url
        self.URLbase = ""        
        paginahtml = request.urlopen(url).read().decode("iso-8859-1")
        #paginahtml = request.urlopen(url).read().decode("utf-8")
        self.souphtml = BeautifulSoup(paginahtml, 'lxml')            
        self.links = self.souphtml.find_all('a')
        
    def get_html(self):
        if self.souphtml:
            return(self.souphtml.text)
        else:
            raise("Conteudo HTML vazio!")
    
    def lista_links(self):
        lista = []
        for l in self.links:
            lista.append('{0}'.format(l[0]))
        
        return (lista)
            
class PaginaSTF(PaginaHTML):    
    def __init__(self, url):
        PaginaHTML.__init__(self,url)
        self.URLbase = "http://www.stf.jus.br/portal"
        
        prox = self.souphtml.find_all("a", text=re.compile("Pr\wximo "), limit=1)            
        if len(prox) == 1:
            self.prox_pagina = self.URLbase +"/jurisprudencia/"+ str(prox[0].attrs['href'])
        else:
            self.prox_pagina = ""
        
        # recupera as divs com descrição dos acordãos    
        self.divsAcordaos = self.souphtml.find_all("div", {"class": "abasAcompanhamento"})
        self.acordaos = []
    
    def add_urlbase(self, url):
        return (self.URLbase + url)
        
    # processa todas as divs de acordao, extraindo os dados e armazenando num lista
    # de models do tipo Acordao
    def processa_divs(self):
        for div in self.divsAcordaos:
            self.acordaos.append(self.get_dados_acordao(div))
            
    def get_dados_acordao(self, div):        
        acordao = {}                
            
        # Recupera o link do documento pdf
        for link in div.find_all('a', text=re.compile("Inteiro Teor")):            
            self.add_urlbase(link.get('href')[2:])
            acordao['link_pdf'] = url
        
        # Recupera o link de acompanhamento
        for link in div.find_all('a', text=re.compile("Acompanhamento Processual")):            
            url = self.add_urlbase(link.get('href')[2:])
            acordao['link_acomp'] = url

        # Recupera o link DJ/DJe
        for link in div.find_all('a', text=re.compile("DJ/DJe")):            
            self.add_urlbase(link.get('href')[2:])
            acordao['link_dj'] = url

        # Recupera o id do processo        
        id_proc = re.compile(".*verProcessoAndamento.asp\?numero=(.*)\&classe.*").match(acordao['link_acomp']).groups()[0]
        acordao['id'] = id_proc
         # HTML e texto puro
        acordao['html'] = str(div)
        acordao['texto'] = div.text
        acordao['pdf'] = self.grava_pdf(acordao['id'], acordao['link_pdf'])             
        return (acordao)
    
    def grava_pdf(self, id, link):
        arquivoPDF = "./stfcrawler/pdfs/"+id+".pdf"
        #arquivoPDF = id+".pdf"
        response = requests.get(link)

        # Store the data
        with open(arquivoPDF, 'w') as outfile:
            outfile.write(response.content)
        '''
        # download do arquivo
        response = request.urlopen(link)
        content_type = response.info().get('Content-Type')
        u = response

        # gravação do arquivo
        f = open(arquivoPDF, 'wb')
        meta = u.info()

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

        file_size_dl += len(buffer)
        f.write(buffer)
        f.close()
        '''
        return (arquivoPDF)
        
    def tem_proxima(self):
        if self.prox_pagina:
            return (True)
        
        return (False)
        
    def get_divs_acordaos(self):
        divsAcordaos = self.souphtml.find_all("div", {"class": "abasAcompanhamento"})
        return (divsAcordaos)