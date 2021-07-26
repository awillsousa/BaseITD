import os.path      
import urllib  
import argparse
from urllib.error import HTTPError
from .scrapy import PaginaSTF

def get_url(url_busca):
        pagina = PaginaSTF(url_busca)        
        pagina.processa_divs()            
        # Se tiver proximas paginas, busca-las
        while (pagina.tem_proxima()):                
            url_busca = str(pagina.prox_pagina)
            anterior = pagina
            try:
                pagina = PaginaSTF(url_busca)               
                pagina.processa_divs()            
                
            except HTTPError as e:
                #content = e.read()
                pagina = anterior
    

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-a", "--url", required=True, help="URL de consulta de acordãos")
    args = vars(ap.parse_args())
    
    if args.acao == "importa":
        get_url(args.url)
    else:
        print("Ação desconhecida! ")


if __name__ == "__main__":
    main()


