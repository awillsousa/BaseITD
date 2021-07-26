# Extrai o texto de um arquivo pdf e grava dois arquivos. O primeiro contendo o texto puro e o segundo contendo o 
# seu conteudo em HMTL

DIR_ORIGEM=$1
DIR_DESTINO=$2

for ARQ in $(find $DIR_ORIGEM -name "*.pdf" -type f); do
    BASE_NOME=`basename $ARQ | cut -d "." -f 1`
    TXT_DESTINO="$DIR_DESTINO/txt/$BASE_NOME.txt"
    HTML_DESTINO="$DIR_DESTINO/html/$BASE_NOME.html"

    # Extrai o texto
    if [ ! -f $TXT_DESTINO ]; then
       echo "Gerando arquivo txt [$TXT_DESTINO]..."  
       java -jar pdfbox-app-2.0.15.jar ExtractText $ARQ $TXT_DESTINO
    else
       echo "Arquivo txt já existe!"  
    fi

    # Extrai o html
    if [ ! -f $HTML_DESTINO ]; then
       echo "Gerando arquivo html [$HTML_DESTINO]..."  
       java -jar pdfbox-app-2.0.15.jar ExtractText -html $ARQ $HTML_DESTINO
    else
       echo "Arquivo html já existe!"  
    fi

done
