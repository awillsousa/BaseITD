
# ITD - Iudicium Textum Dataset 

Aqui segue um guia básico de como obter uma base funcional e utilizá-la.

**Etapas Necessárias**

- Instalação do Docker
- Configuração do ambiente Python
- Execução dos scripts de carga
- Execução dos notebooks


***Instalação do Docker***

A importação dos dados em formato JSON pode ser feita em Docker ou em uma instalação local.

```bash
# cd BaseITD/tools
# docker pull mongo
# docker run -d -p 27017:27017 -p 28017:28017 -e AUTH=no  --name mongodbserver mongo
# mongoimport --db ITD --collection DocumentosAcordaos --file ../json/DocumentosAcordaos.json
# mongoimport --db ITD --collection AcordaosVotos --file ../json/AcordaosVotos.json
# mongoimport --db ITD --collection AcordaosRelatorios --file ../json/AcordaosRelatorios.json
```

***Configuração do Ambiente Python***

Utilize uma instalação do Python > 3.0. 

```bash
# pip install -r requirements.txt
```

***Execução dos Scripts***

Os scripts deve ser executados da seguinta maneira:

Para executar o download de um conjunto de acordãos:
```bash
python get_acordaos.py --url <URL CONSULTA JURISPRUDENCIA>
```

Para executar a extração da integra de um arquivo PDF e a separação das suas partes:
```bash
./extract_txt_html.sh <DIRETORIO ENTRADA> <DIRETORIO SAIDA>

# para extrair um único arquivo
java -jar pdfbox-app-2.0.15.jar ExtractText <-html> <ARQUIVO ORIGEM> <ARQUIVO DESTINO>

# para gerar o script de separação dos documentos
./separa-acordaos.sh <DIRETORIO ENTRADA> <DIRETORIO SAIDA>
Execute o script gerado
```

***Execução dos Notebooks***

Para executar os notebooks, excute o jupyter-notebook e tenha certeza de ter todas as dependências instaladas no ambiente virtual que está ativado.


