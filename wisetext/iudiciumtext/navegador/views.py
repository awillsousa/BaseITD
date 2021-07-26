from django.shortcuts import render
from django.template import loader
from django.http import Http404, HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

import os.path
from .models import Acordao

# Logging
import logging

logger = logging.getLogger(__name__)

# Lista os acordaos na base
def acordao_list(request):
    acordaos = Acordao.objects.all()
    acordaos.order_by('id_processo')
    paginator = Paginator(acordaos, 50)
    page = request.GET.get('page')
    try:
        show_acordaos = paginator.page(page)
    except PageNotAnInteger:
        show_acordaos = paginator.page(1)
    except EmptyPage:
        show_acordaos = paginator.page(paginator.num_pages)

    template = loader.get_template('navegador/lista.html')
    context = {
        'lista_acordaos': show_acordaos,
    }
    return HttpResponse(template.render(context, request))

# Exibe os detalhes de um acordao
def acordao_detail(request, id_acordao):
    try:
        acordao = Acordao.objects.get(pk=id_acordao)
        existePDF = os.path.isfile(acordao.pdf_inteiro_teor)
        existeTXT = os.path.isfile(acordao.txt_inteiro_teor)
        #existeHTML = os.path.isfile(acordao.html_inteiro_teor)

    except Acordao.DoesNotExist:
        raise Http404("Erro!")

    return render(request, 'navegador/detail.html', {'acordao': acordao, 'existePDF': existePDF, 'existeTXT':existeTXT})


# Grava um acordao na base
'''
def acordao_save(acordao):
    if not (Acordaos.objects.filter(id_processo=acordao["id"])):
        try:
            ac = Acordaos()
            ac.id_processo = acordao["id"]
            ac.URL = acordao["link_acomp"]
            ac.URL_inteiro_teor = acordao["link_pdf"]
            ac.URL_dj_dj3 = acordao["link_dj"]
            ac.HTML_texto_basico = acordao["html"]
            ac.texto_basico = acordao["texto"]
            ac.pdf_inteiro_teor = acordao['pdf']
            ac.classe = dadosURL['classe']
            ac.codigoClasse = dadosURL['codigoClasse']
            ac.recurso = dadosURL['recurso']
            ac.origem = dadosURL['origem']
            ac.tipoJulgamento = dadosURL['tipoJulgamento']
            ac.save()

            logger.info("Acordao {0} salvo com sucesso.".format(acordao["id"]))
        except:
            logger.error("Erro ao salvar dados do acordao {0}.".format(acordao["id"]))


    # CODIGO PARA SALVAR ACORDAO ALTERADO
'''


def exibe(request, lista):
    return render(request, 'navegador/exibe.html', {'lista': lista})
