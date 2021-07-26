#!/bin/bash

# Converte em um diretorio de arquivos textos, onde cada arquivo de texto representa uma pagina
# do documento original

# Pega o arquivo PDF e converte para arquivos TIFF no diretorio de imagens
# Em seguida converte as imagens TIFF para documentos TXT
# Para cada arquivo PDF eh criado um diretorio _folder_ em cada um dos 
# diretorio (txtx, imgs)

PDFDIR=".."
TXTDIR="../txts"
IMGDIR="../imgs"
mkdir -p $TXTDIR
mkdir -p $IMGDIR

# Cria o diretorio para o aruqivo PDF
ARQUIVO=`echo $1 | sed 's/.pdf//' | sed 's/.*\///'`
mkdir -p $TXTDIR/$ARQUIVO
mkdir -p $IMGDIR/$ARQUIVO

#Print the name of the dude we're working on.
echo $ARQUIVO
echo "\n\n"

# Primeiro converte o PDF para arquivos TIF. 
if [ ! -f $IMGDIR/$ARQUIVO/scan_1.tif ]; # Aplica o ghostscript apenas se nao existe nenhuma pagina convertida
then
    if [ -f $PDFDIR/$ARQUIVO.pdf ]
    then
        gs -dNOPAUSE -dBATCH -sDEVICE=tiffg4 -sOutputFile=$IMGDIR/$ARQUIVO/scan_%d.tif $PDFDIR/$ARQUIVO.pdf
    else
        gs -dNOPAUSE -dBATCH -sDEVICE=tiffg4 -sOutputFile=$IMGDIR/$ARQUIVO/scan_%d.tif $ARQUIVO.pdf
    fi
fi


# Aplica OCR nas paginas. Uma de cada vez
i=1
while [ $i -ge 0 ]
do
    if [ -e $IMGDIR/$ARQUIVO/scan_$i.tif ]
    then
        if [ ! -e $TXTDIR/$ARQUIVO/$i.txt ] #now doesn't overwrite
        then
            tesseract -l por $IMGDIR/$ARQUIVO/scan_$i.tif $TXTDIR/$ARQUIVO/$i
        #add the text to the result.txt file
        fi
        i=$(( $i + 1 ))
    else #Break if the tif file doesn't exist.
        i=-100
    fi
done
