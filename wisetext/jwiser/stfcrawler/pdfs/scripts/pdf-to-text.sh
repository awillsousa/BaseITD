#!/bin/bash

# Converte em um diretorio de arquivos textos, onde cada arquivo de texto representa uma pagina
# do documento original

# Pega o arquivo PDF e converte para arquivos TIFF no diretorio de imagens
# Em seguida converte as imagens TIFF para documentos TXT
# Para cada arquivo PDF eh criado um diretorio _folder_ em cada um dos 
# diretorio (txtx, imgs)

PDFDIR=".."
TXTDIR="../txts"
mkdir -p $TXTDIR
ARQUIVO=$1

# Realiza a conversao novamente, apenas se o arquivo nao existe
if [ ! -f $TXTDIR/$ARQUIVO.txt ]; 
then
    if [ -f $PDFDIR/$ARQUIVO.pdf ]
    then
        pdftotext -eol unix $PDFDIR/$ARQUIVO.pdf $TXTDIR/$ARQUIVO.txt
    else
        echo "Arquivo $ARQUIVO.pdf ausente!"
    fi
fi

