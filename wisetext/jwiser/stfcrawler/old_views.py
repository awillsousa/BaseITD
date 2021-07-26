from django.shortcuts import render
from django.template import loader
from django.http import Http404, HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic.base import TemplateView
from django.contrib import messages

from .models import Acordao
from .forms import AddAcordaoForm
from .scrapy import PaginaSTF


class ListaAcordaosView(TemplateView):
    template_name = 'stfcrawler/lista.html'

    def get_context_data(self, **kwargs):
        context = super(ListaAcordaosView, self).get_context_data(**kwargs)
        acordaos = Acordao.objects.all()
        paginator = Paginator(acordaos, 10)
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
    paginator = Paginator(acordaos, 10)
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
    except Acordao.DoesNotExist:
        raise Http404("Erro!")
    
    return render(request, 'stfcrawler/detail.html', {'acordao': acordao})
        
def acordao_add(request):
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = AddAcordaoForm(request.POST)
		# check whether it's valid:
		if form.is_valid():									
			paginas = []
			url_busca = str(request.POST.get("URL", ""))
			pagina = PaginaSTF(url_busca)
			paginas.append(pagina)						
			
			# Se tiver proximas paginas, busca-las
			while (pagina.tem_proxima()):				
				url_busca = str(pagina.prox_pagina)
				pagina = PaginaSTF(url_busca)
				paginas.append(pagina)											
				
		acordaos = []
		for pagina in paginas:			
			pagina.processa_divs()			
			for acordao in pagina.acordaos:
				if not(Acordao.objects.filter(id_processo=acordao["id"])):
					ac = Acordao()
					ac.id_processo = acordao["id"]
					ac.URL = acordao["link_acomp"]
					ac.URL_inteiro_teor = acordao["link_pdf"]
					ac.URL_dj_dj3 = acordao["link_dj"]
					ac.HTML = acordao["html"]
					ac.texto = acordao["texto"]
					ac.inteiro_teor = acordao['pdf']
					ac.save()
				
				
				
		# redirect to a new URL:
		#return exibe(request, v)
		return index(request)

	# if a GET (or any other method) we'll create a blank form
	else:        
		form = AddAcordaoForm()
		
	return render(request, 'stfcrawler/acordao_add.html', {'form': form})
	
	
def exibe(request, lista):    
    return render(request, 'stfcrawler/exibe.html', {'lista': lista})