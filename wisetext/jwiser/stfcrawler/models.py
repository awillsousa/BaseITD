from django.db import models


# Uma página HTML do site alvo
class Acordao(models.Model):
    id_processo = models.CharField(max_length=30, primary_key=True)
    URL = models.URLField(max_length=500)
    URL_inteiro_teor = models.URLField(max_length=500)
    URL_dj_dj3 = models.URLField(max_length=500, blank=True)
    HTML_texto_basico = models.TextField()
    texto_basico = models.TextField(blank=True)
    pdf_inteiro_teor = models.URLField(max_length=100, blank=True)
    txt_inteiro_teor = models.URLField(max_length=100, blank=True)
    texto_inteiro_teor = models.TextField(blank=True)
    classe = models.CharField(max_length=100, blank=True)
    codigoClasse = models.CharField(max_length=30, blank=True)
    origem = models.CharField(max_length=10, blank=True)
    recurso = models.CharField(max_length=10, blank=True)
    tipoJulgamento = models.CharField(max_length=10, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True, )
    alterado_em = models.DateTimeField(auto_now=True)
