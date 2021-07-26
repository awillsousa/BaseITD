#!/bin/bash

DIR_PDFS="/home/willian/juriswiser/stfcrawler/pdfs/txts/"
CONVS="CONVS"
for D in $(ls -d $DIR_PDFS*/); do
    ARQ=$(echo "$D" | sed 's/\/$/\.txt/g' | sed 's/txts/CONV/g' ) 
    
    cat $D*.txt >> $ARQ;
    #echo "cat $D*.txt >> $ARQ";
done

