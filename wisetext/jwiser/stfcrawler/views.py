from django.shortcuts import render
from django.template import loader
from django.http import Http404, HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic.base import TemplateView
from django.contrib import messages

import os.path      
import urllib  
from urllib.error import HTTPError

from .models import Acordao
from .forms import AddAcordaoForm
from .scrapy import PaginaSTF

# Logging
import logging
logger = logging.getLogger(__name__)

# CONSTANTES
LIMITE_TENTATIVAS = 5

class ListaAcordaosView(TemplateView):
    template_name = 'stfcrawler/lista.html'

    def get_context_data(self, **kwargs):
        context = super(ListaAcordaosView, self).get_context_data(**kwargs)

        acordaos = sorted(Acordao.objects.all(), key=lambda n: (int(n.id_processo)))
        paginator = Paginator(acordaos, 50)
        page = self.request.GET.get('page')
        try:
            show_acordaos = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            show_acordaos = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            show_acordaos = paginator.page(paginator.num_pages)
        context['lista_acordaos'] = show_acordaos
        return context

class HomePageView(TemplateView):
    template_name = 'stfcrawler/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        messages.info(self.request, 'hello http://example.com')
        return context


def index(request):   
    acordaos = Acordao.objects.all()   
    acordaos.order_by('id_processo')  
    paginator = Paginator(acordaos, 50)
    page = request.GET.get('page')
    try:
        show_acordaos = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        show_acordaos = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        show_acordaos = paginator.page(paginator.num_pages)
    
    template = loader.get_template('stfcrawler/lista.html')
    context = {
        'lista_acordaos': show_acordaos,
    }
    return HttpResponse(template.render(context, request))
    
def detail(request, id_acordao):
    try:
        acordao = Acordao.objects.get(pk=id_acordao)
        existePDF = os.path.isfile(acordao.pdf_inteiro_teor)
        
        if not existePDF:
            g = urllib.request.urlopen(acordao.URL_inteiro_teor)
            arquivoPDF = "stfcrawler/pdfs/"+str(id_acordao)+".pdf"
            with open(arquivoPDF, 'b+w') as f:
                f.write(g.read())

        existePDF = os.path.isfile(acordao.pdf_inteiro_teor)
    except Acordao.DoesNotExist:
        raise Http404("Erro!")
    
    return render(request, 'stfcrawler/detail.html', {'acordao': acordao, 'existePDF':existePDF})

# Os acordaos sao adicionados por meio de uma URL de busca da jurisprudencia do STF
# Eh feita a recuperacao da página HTML da busca do site do STF e a partir dos dados
# obtidos, cada um dos acordaos é inserido na base e o arquivo PDF do seu inteiro teor
# eh baixado e armazenado localmente.
def acordao_add(request):
    # Se for uma requisicao POST, processa os dados do formulario
    if request.method == 'POST':
        # Cria um formulario e popula com os dados do request
        form = AddAcordaoForm(request.POST)
        # Checa o formulario primeiro
        if form.is_valid():                                    
            paginas = []
            url_busca = str(request.POST.get("URL", ""))
            pagina = PaginaSTF(url_busca)

            # Processa a primeira pagina
            pagina.processa_divs()            
            for acordao in pagina.acordaos:
                grava_Acordao(acordao)

            # Se tiver proximas paginas, busca-la-eias
            tentativas = 0
            while (pagina.tem_proxima()):                
                url_busca = str(pagina.prox_pagina)
                anterior = pagina
                try:
                    pagina = PaginaSTF(url_busca)
                    pagina.processa_divs()            
                    for acordao in pagina.acordaos:
                        grava_Acordao(acordao)
                except HTTPError as e:
                    if tentativas <= LIMITE_TENTATIVAS:
                        # Tenta de novo
                        pagina = anterior
                    else:
                        logger.error("Erro ao recuperar dados da pagina {0}. \
                                     Encerrando apos {1} tentativas.".format(url_busca, LIMITE_TENTATIVAS))

        return index(request)

    # se for GET (ou qualquer outro tipo) cria um form em branco
    else:        
        form = AddAcordaoForm()
        
    return render(request, 'stfcrawler/acordao_add.html', {'form': form})

# Grava um acordao na base
def grava_Acordao(acordao):
    if not (Acordao.objects.filter(id_processo=acordao["id"])):
        try:
            ac = Acordao()
            ac.id_processo = acordao["id"]
            ac.URL = acordao["link_acomp"]
            ac.URL_inteiro_teor = acordao["link_pdf"]
            ac.URL_dj_dj3 = acordao["link_dj"]
            ac.HTML_texto_basico = acordao["html"]
            ac.texto_basico = acordao["texto"]
            ac.pdf_inteiro_teor = acordao['pdf']
            dadosURL = dados_da_URL(acordao["link_acomp"])
            ac.classe = dadosURL['classe']
            ac.codigoClasse = dadosURL['codigoClasse']
            ac.recurso = dadosURL['recurso']
            ac.origem = dadosURL['origem']
            ac.tipoJulgamento = dadosURL['tipoJulgamento']
            ac.save()

            logger.info("Acordao {0} salvo com sucesso.".format(acordao["id"]))
        except:
            logger.error("Erro ao salvar dados do acordao {0}.".format(acordao["id"]))


def exibe(request, lista):    
    return render(request, 'stfcrawler/exibe.html', {'lista': lista})

# Extrai campos da URL do processo
def dados_da_URL(s):
    try:
        if not(s is None):
            campos_vals = s.split("&")[1:] # pega somente os campos extras da url
            valores = [p.split("=") for p in campos_vals]

            return ({l[0]:l[1] for l in valores})
    except:
        logger.error('Erro na extracao de dados da URL!')
        return None
