from django import forms

class AcordaoForm(forms.Form):
    link_acompanhamento = forms.CharField(label='Link Acompanhamento')
    link_inteiroteor = forms.CharField(label='Link Inteiro Teor')
    arquivo_pdf = forms.CharField(label='Arquivo PDF')

    html_div = forms.CharField(label='HTML Acord&atilde;o',
        widget=forms.Textarea(),
    )
    texto_div = forms.CharField(label='Texto Acord&atilde;o',
        widget=forms.Textarea(),
    )

    