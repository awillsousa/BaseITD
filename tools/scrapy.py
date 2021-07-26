from urllib import request
from urllib.error import HTTPError
import requests
from bs4 import BeautifulSoup
import re
import os.path

#url = "http://www.stf.jus.br/portal/jurisprudencia/listarJurisprudencia.asp?s1=%28JUSTICA+ADJ2+TRABALHO+E+COMPET%24+E+ACIDENTE+ADJ2+TRABALHO%29&base=baseAcordaos&url=http://tinyurl.com/l2448cn"

class PaginaHTML:    
    def __init__(self, url):
        self.url = url
        self.URLbase = ""  
        paginahtml = None
        
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
            acordao['link_pdf'] = self.add_urlbase(link.get('href')[2:])
        
        # Recupera o link de acompanhamento
        for link in div.find_all('a', text=re.compile("Acompanhamento Processual")):            
            acordao['link_acomp'] = self.add_urlbase(link.get('href')[2:])

        # Recupera o link DJ/DJe
        acordao['link_dj'] = ""
        for link in div.find_all('a', text=re.compile("DJ/DJe")):                        
            acordao['link_dj'] = self.add_urlbase(link.get('href')[2:])
            

        # Recupera o id do processo        
        id_proc = re.compile(".*verProcessoAndamento.asp\?numero=(.*)\&classe.*").match(acordao['link_acomp']).groups()[0]
        acordao['id'] = id_proc
         # HTML e texto puro
        acordao['html'] = str(div)
        acordao['texto'] = div.text
        acordao['pdf'] = self.grava_pdf(acordao['id'], acordao['link_pdf'])             
        return (acordao)
    
    def grava_pdf(self, id, link):
        arquivoPDF = "../ITD/"+id+".pdf"        
        
        if not os.path.isfile(arquivoPDF):
            g = request.urlopen(link)
            with open(arquivoPDF, 'b+w') as f:
                f.write(g.read())
                
        return (arquivoPDF)
        
    def tem_proxima(self):
        if self.prox_pagina:
            return (True)
        
        return (False)
        
    def get_divs_acordaos(self):
        divsAcordaos = self.souphtml.find_all("div", {"class": "abasAcompanhamento"})
        return (divsAcordaos)