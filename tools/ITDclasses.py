
'''
Executa o pre-processamento sobre os arquivos da base IudiciumTextDataset (ITD)
'''

import os
import re
import json
import logging
from bs4 import BeautifulSoup


logging.basicConfig(level=logging.INFO)

# Indicador HTML de quebra de pagina
INDICADOR_DIV_PG = "page-break-before:always; page-break-after:always"


def compilaRegexExcluir():
    expr_busca_p = [r"^Documento assinado digitalmente conforme MP.*$",
                    r"^documento pode ser acessado (pelo|no) endere.*$",
                    # r"^documento pode ser acessado no endere.*$",
                    r"^http://www.stf.jus.br/portal/autenticacao/autenticarDocumento.asp.*sob o código.*e senha.*$",
                    r"^Inteiro Teor do Acórdão \- Página \d{1,5} de \d{1,5}[ ]*$",
                    r"^Supremo Tribunal Federal.*Inteiro Teor do Acórdão \- Página.*de.*$",
                    r"^Supremo Tribunal Federal[\s\n]{0,}$",
                    r"^[\s]{0,}Brasília, \d{1,2} de (janeiro|fevereiro|março|abril|maio|julho|agosto|setembro|outubro|novembro|dezembro) de \d{4}.$",
                    # r"[\s]{0,}Brasília, \d{1,2} de (janeiro|fevereiro|março|abril|maio|julho|agosto|setembro|outubro|novembro|dezembro) de \d{4}.$",
                    r"^Ministr.* Relator[\s\n]{0,}$",
                    "^[0-9]{0,5}[ \n]+$"]

    padroesexcluir = [re.compile(p) for p in expr_busca_p]

    return padroesexcluir

def compilaPartesOK():
    return ['RELATOR', 'RELATORA', 'PACTE.(S)', 'IMPTE.(S)', 'COATOR(A/S)(ES)', 'RECTE.(S)', 'ADV.(A/S)', 'RECDO.(A/S)', 'PROC.(A/S)(ES)',
                'AGTE.(S)', 'AGDO.(A/S)', 'INVEST.(A/S)', 'REVISOR', 'RÉU(É)(S)', 'REVISORA', 'EMBTE.', 'ADVDA.', 'EMBDOS.', 'ADVDOS.',
                'SUSDO.(A/S)','REQDO.(A/S)','SUSTE.(S)', 'ADVDAS.', 'RECLTE.(S)', 'RECLDO.(A/S)', 'EMBDO.', 'AGTES.', 'AGDO.', 'AGTE.', 
                'EMBTES.', 'LIT.ATIV.(A/S)', 'APTE.(S)', 'APDO.(A/S)', 'BENEF.(A/S)', 'LITISC.(S)', 'ADV.DAT.(A/S)', 'INDIC.(A/S)', 
                'DNTE.(S)', 'DNDO.(A/S)', 'ADV.LIT.(A/S)', 'CURADOR(A/S)(ES)', 'IMPDO.(A/S)', 'INTDO.(A/S)', 'EMBTE.(S)',
                'REQTE.(S)', 'AUTOR(A/S)(ES)','EMBDO.(A/S)', 'AM.CURIAE.', 'LIT.PAS.(A/S)', 'EXTDO.(A/S)', 'REU(É)(S)',
                'ASSIST.(S)', 'ADV.', 'AGDOS.', 'RÉ', 'REGISTRADO', 'DP', 'QTE.(S)', 'EXTDO.', 'AGDA.', 'REDATOR DO ACORDAO', 
                'REDATORA DO ACORDAO', 'REDATOR', 'REDATORA']


class DocumentoAcordao():
    padroesexcluir = compilaRegexExcluir()
    PARTES_OK = compilaPartesOK()
    def __init__(self, caminho, numero, formato='html'):
            self.numero = numero
            self.caminho = caminho
            self.formato = formato
            self.arquivopdf = os.path.join(caminho, numero, "{0}.pdf".format(numero))
            self.arquivotxt = os.path.join(caminho, numero, "txt/{0}.txt".format(numero))
            self.arquivohtml = os.path.join(caminho, numero, "html/{0}.html".format(numero))
            self.integratxt = self.carregaIntegra(self.arquivotxt, tipo='txt')
            self.integrahtml = self.carregaIntegra(self.arquivohtml, tipo='html')
            self.arquivossecoes = self.buscaArqsSecoes(os.path.join(caminho, numero, formato))
            self.partes = []
            self.ementa = None
            self.acordao = None
            self.preProcessaAcordaoEmenta(self.parseHtml(self.arquivossecoes['EMENTA_ACORDAO']))
            self.relatorio = None
            self.preProcessaRelatorio(self.parseHtml(self.arquivossecoes['RELATORIO']))
            self.extratoata = None
            self.preProcessaAta(self.parseHtml(self.arquivossecoes['ATA']))
            self.votos = []
            self.preProcessaVotos(self.arquivossecoes['VOTOS'])

    def carregaIntegra(self, arquivo, tipo='html'):
        logging.debug("Carregando integra {0}...".format(tipo))
        if not os.path.isfile(arquivo):
            print("Arquivo de integra passado invalido!")

        if tipo == 'html':
            html = self.parseHtml(arquivo)
            return html.prettify()
        elif tipo == 'txt':
            return self.parseTxt(arquivo)
        else:
            return None

    def parseTxt(self, arquivo):
        txt = ""
        try:
            with open(arquivo) as ftxt:
                txt = ftxt.readlines()
        except IOError as erro:
            logging.error("Erro ao tentar o arquivo {0}".format(arquivo))
            logging.error(str(erro))
        except Exception as erro:
            logging.error("Erro inesperado: {}".format(os.sys.exc_info()[0]))
            logging.error(str(erro))

        return txt

    def parseHtml(self, arquivo):
        '''
        Recebe o caminho de um arquivo html e devolve um objeto BeautifulSoup com o arquivo parseado
        :return: Objeto BeautifulSoup
        '''
        txthtml = ""
        try:
            paginahtml = open(arquivo)
            txthtml = BeautifulSoup(paginahtml, 'lxml')
            paginahtml.close()
        except IOError as erro:
            logging.error("Erro ao tentar o arquivo {0}".format(arquivo))
            logging.error(str(erro))
        except Exception as erro:
            logging.error("Erro inesperado: {}".format(os.sys.exc_info()[0]))
            logging.error(str(erro))

        return txthtml

    def buscaRelator(self):
        for parte in self.partes:
            if 'RELATOR' in parte.tipo or \
               'RELATORA' in parte.tipo:
                return parte.nome
            else:
                return ''

    def buscaArqsSecoes(self, DIRETORIO_ACORDAO, TIPO='.html'):
        logging.debug("Recuperando seçoes ...")
        arquivos = {'VOTOS': {}, 'EMENTA_ACORDAO': None, 'RELATORIO': None, 'ATA': None, 'OUTROS': []}
        for r, d, f in os.walk(DIRETORIO_ACORDAO):
            for file in f:
                if TIPO in file:
                    if '_Voto_' in file:
                        arquivos['VOTOS'][file.replace('.html', '')] = os.path.join(r, file)
                    elif '_Ementa_e_Acordao_' in file:
                        arquivos['EMENTA_ACORDAO'] = os.path.join(r, file)
                    elif '_Relatorio_' in file:
                        arquivos['RELATORIO'] = os.path.join(r, file)
                    elif '_Extrato_de_Ata_' in file:
                        arquivos['ATA'] = os.path.join(r, file)
                    else:
                        arquivos['OUTROS'].append(os.path.join(r, file))

        return arquivos

    def preProcessaAcordaoEmenta(self, texto_html):
        logging.debug("Pre-processando ementa e acordao ...")
        if texto_html == "":
           return None 

        # cada div corresponde a uma página
        divs = []
        divs.extend(texto_html.find_all("div", style=INDICADOR_DIV_PG))

        secao_ementa = []   # Paragrafos que compoem a ementa
        secao_partes = []   # Paragrafos que compoem a secao de partes
        secao_acordao = []  # Paragrafos que compoem a secao do texto do acordao

        # Itera as divs e seus paragrafos para separar as partes, ementa e texto do acordao
        flag_pag1 = True
        parte_atual = "PARTES"
        for div in divs:
            for i, parag in enumerate(div.find_all("p")):
                # print("Tag <p> sendo processada: {0}".format(parag.text))
                if i == 0 or i == 1:
                    parag.decompose()
                elif i == 2 and flag_pag1:
                    flag_pag1 = False
                    parag.decompose()
                elif any([r.match(parag.text.replace('\n', ' ')) for r in self.padroesexcluir]) or \
                     any([r.match(parag.text) for r in self.padroesexcluir]):
                    parag.decompose()
                else:
                    if "A C Ó R D Ã O" in parag.text or "ACÓRDÃO" in parag.text:
                        if not any(pOK in parag.text for pOK in self.PARTES_OK):
                            # Nesta parte, depois será bom verificar se sempre acontece do indicador do acórdão
                            # "A C Ó R D Ã O" vir dentro da tag <p> anterior
                            parag.string = parag.text.replace("A C Ó R D Ã O", '')
                            parag.string = parag.text.replace("ACÓRDÃO", '')
                            parte_atual = "ACORDAO"
                            secao_ementa.append(parag)
                        elif parte_atual == "PARTES":
                            secao_partes.append(parag)
                            
                    elif "EMENTA" in parag.text.replace(' ','').upper():    
                        '''    
                        elif ("EMENTA:" in parag.text) or \
                             ("Ementa:" in parag.text) or \
                             ("EMENTA" in parag.text) or \
                             ("E  M  E  N  T  A:" in parag.text) or \
                             ("EMENTA" in parag.text.replace(' ', '')):
                        '''
                        parte_atual = "EMENTA"
                        # parag.string = parag.text.replace('\n', ' ')
                        secao_ementa.append(parag)
                    
                    else:
                        if parag:  # Vai saber se não tem None na jogada
                            if parte_atual == "PARTES":                                
                                    secao_partes.append(parag)                                
                            elif parte_atual == "EMENTA":
                                # parag.string = parag.text.replace('\n', ' ')
                                secao_ementa.append(parag)
                            elif parte_atual == "ACORDAO":
                                # parag.string = parag.text.replace('\n', ' ')
                                secao_acordao.append(parag)

        secao_ementa = ' '.join([s.text.replace('\n', ' ') for s in secao_ementa])
        secao_acordao = ' '.join([s.text.replace('\n', ' ') for s in secao_acordao])

        self.acordao = Acordao(secao_acordao)
        self.ementa = Ementa(secao_ementa)

        self.preProcessaPartes(secao_partes)

    def preProcessaPartes(self, partes_html):
        PADROES_SIGLA_EXCLUIR = ['PROCURADOR-GERAL', 'ADVOGADO-GERAL', 'PÚBLICO-GERAL']

        partes_display = "".join([p.text for p in partes_html])
        linhas_parte = partes_display.split('\n')
        linhas_excluir = []
        linha_marcada = 0
        residual = ""
        tem_residual = False
        iter_partes = linhas_parte[:]
        for i, linha in enumerate(iter_partes):
            if ":" not in linha:            
                if any(pOK in linha for pOK in self.PARTES_OK) or tem_residual:
                    tem_residual = True
                    residual += linha
                    residual += " "                
                else:                                       
                    linhas_parte[linha_marcada] += linha
                    
                linhas_excluir.append(i)    
            else:            
                linha_marcada = i
                
                if tem_residual:                
                    linhas_parte[linha_marcada] = residual + linha 
                    tem_residual = False
                    residual = ""

        del iter_partes
        for l in linhas_excluir[::-1]:
            del linhas_parte[l]

        partes = {}
        for linha in linhas_parte:
            l = linha.split(':')
            partes[l[0].replace(' ', '')] = l[1]

        for tipo, nome in partes.items():
            nome_base = ''
            sigla = ''
            if '-' in nome and not any(f in nome for f in PADROES_SIGLA_EXCLUIR):
                l_nome_base = nome.split('-')
                nome_base = '-'.join(l_nome_base[:-1])
                sigla = l_nome_base[-1].replace(' ', '')
            elif 'E OUTRO(A/S)' in nome:
                nome_base = nome
                nome_base.replace('E OUTRO(A/S)', '')
            else:
                nome_base = nome

            tipo_base = tipo.replace(' ', '')

            self.partes.append(Parte(tipo=tipo_base.lstrip(' ').rstrip(' '),
                                     nome=nome_base.lstrip(' ').rstrip(' '),
                                     sigla=sigla.lstrip(' ').rstrip(' ')))

    def preProcessaRelatorio(self, texto_html):
        logging.debug("Pre-processando relatorio ...")
        if texto_html == "":
           return None

        # cada div corresponde a uma página
        divs = texto_html.find_all("div", style=INDICADOR_DIV_PG)

        # Itera as divs e seus paragrafos para extrair apenas o texto do relatório
        flag_pag1 = True
        parte_atual = "PARTES"
        secao_relatorio = []
        for div in divs:
            for i, parag in enumerate(div.find_all("p")):
                if i == 0 or i == 1:
                    parag.decompose()
                elif i == 2 and flag_pag1:
                    flag_pag1 = False
                    parag.decompose()

                if "R E L A T Ó R I O" in parag.text or "RELATÓRIO" in parag.text:
                    parte_atual = "RELATORIO"
                elif any([r.match(parag.text.replace('\n', ' ')) for r in self.padroesexcluir]):
                    parag.decompose()
                elif parte_atual == "RELATORIO":
                    if parag:
                        secao_relatorio.append(parag)

        self.relatorio = Relatorio(texto=' '.join([s.text.replace('\n', ' ') for s in secao_relatorio]),
                                   relator=self.buscaRelator())

    def preProcessaVotos(self, arquivos_votos):
        logging.debug("Pre-processando votos ...")
        if len(arquivos_votos.keys()) == 0:
           return None
 
        for voto, arq_voto in arquivos_votos.items():
            # cada div corresponde a uma página
            try:
                texto_voto = self.parseHtml(arq_voto)
            except IOError as e:
                logging.error("Erro ao tentar abrir o arquivo {0}".format(arq_voto))

            divs = texto_voto.find_all("div", style=INDICADOR_DIV_PG)
            secao_voto = []
            # Itera as divs e seus paragrafos para extrair apenas o texto do relatório
            flag_pag1 = True
            for div in divs:
                for i, parag in enumerate(div.find_all("p")):
                    if i == 0 or i == 1:
                        parag.decompose()
                    elif i == 2 and flag_pag1:
                        flag_pag1 = False
                        parag.decompose()

                    if "V O T O" in parag.text:
                        parte_atual = "VOTO"
                    elif any([r.match(parag.text.replace('\n', ' ')) for r in self.padroesexcluir]):
                        parag.decompose()
                    else:  # parte_atual == "VOTO"
                        if parag:
                            secao_voto.append(parag)
            min_votante = re.sub(r"^.*_Voto_","",voto)
            min_votante = re.sub(r"_pg_.*$", "", min_votante)
            self.votos.append(Voto(texto=' '.join([s.text.replace('\n', ' ') for s in secao_voto]),
                                   votante=min_votante))

    def preProcessaAta(self, texto_html):
        logging.debug("Pre-processando extrato da ata ...")
        if texto_html == "":
           return None
        # cada div corresponde a uma página
        divs = texto_html.find_all("div", style=INDICADOR_DIV_PG)

        # Itera as divs e seus paragrafos para extrair apenas o texto do relatório
        flag_pag1 = True
        parte_atual = "VOTO"
        secao_ata = []
        for div in divs:
            for i, parag in enumerate(div.find_all("p")):
                if i == 0:
                    parag.decompose()

                if "EXTRATO DE ATA" in parag.text:
                    parte_atual = "ATA"
                elif any([r.match(parag.text.replace('\n', ' ')) for r in self.padroesexcluir]):
                    parag.decompose()
                elif parte_atual == "ATA":
                    if parag:
                        secao_ata.append(parag)

        self.extratoata = ExtratoAta(texto=' '.join([s.text.replace('\n', ' ') for s in secao_ata]))
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class SecaoAcordao(object):
    def __init__(self, texto):
        self.texto = texto

    def tokeniza(self):
        pass
    '''
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
    '''


class Parte(SecaoAcordao):
    def __init__(self, tipo, nome, sigla=''):
        self.tipo = tipo
        self.nome = nome
        self.sigla = sigla

class Ementa(SecaoAcordao):
    def __init__(self, texto):
        self.texto = texto

class Acordao(SecaoAcordao):
    def __init__(self, texto):
        self.texto = texto

class Relatorio(SecaoAcordao):
    def __init__(self, texto, relator=None):
        self.relator = relator
        self.texto = texto
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

class ExtratoAta(SecaoAcordao):
    def __init__(self, texto):
        self.texto = texto

class Voto():
    def __init__(self, texto, votante=None):
        self.votante = votante
        self.texto = texto
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

