#!/bin/bash
DIR=$1
LISTA=`find $1 -name *.pdf`
#for ARQUIVO in $LISTA; do
#   ARQPDF=`echo $ARQUIVO| cut -d '/' -f 2`
   
   # Lista a quantidade de imagens do arquivo PDF
   # arquivo que o pdfimagens retorna apenas duas linhas
   # nao possuem imagens
   # Os arquivos com mais de duas linhas, possuem alguma imagem
   # Os arquivos que possuem a quantidade de imagens igual ao 
   # numero de paginas, sao documentos escaneados. 
   # Aparentemente os arquivos dos acordaos do STF nao possuem
   # imagens nela, apenas texto. 
#   N_IMGS=$(pdfimages -list $ARQUIVO | wc -l | bc) 
#   echo "Imagens: $N_IMGS Arquivo: $ARQUIVO" >> lista
#   if [ $N_IMGS -eq 2 ] 
#   then
#       #echo "$ARQUIVO" >> lista-pdf-txt      # para usar com pdftotext
#       echo "$ARQUIVO PDF to TXT" 
#   else
#       #echo "$ARQUIVO" >> lista-pdf-img      # para converter img + ocr
#       echo "$ARQUIVO PDF to IMG to TXT" 
#   fi
#done

# Realiza a conversao de PDF para TEXTO
for ARQPDFTXT in $(cat lista-pdf-txt); do
    NOMEARQTXT=`echo "$ARQPDFTXT" | cut -d '/' -f 2 | cut -d '.' -f 1`
    RESULT=$(./pdf-to-text.sh $NOMEARQTXT)
done    

# Realiza a conversao de PDF para TIF e depois para TEXTO
for ARQPDFIMG in $(cat lista-pdf-img); do
    NOMEARQIMG=`echo "$ARQPDFIMG" | cut -d '/' -f 2 | cut -d '.' -f 1`
    RESULT=$(./pdf-to-img-to-text.sh $NOMEARQIMG)
done


