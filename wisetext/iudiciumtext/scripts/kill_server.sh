# Lista processos django executando em background
PROCESSOS=`ps -xU $(whoami) | grep -v "grep" | grep "python manage"| cut -d ' ' -f 1`

for p in $PROCESSOS; do
    echo "Encerrando processo: $p"
    R=`kill $p`
    if [ $? -eq 0 ]; then
       echo "Processo encerrado com sucesso."
    else
       echo "Falha ao encerrar processo..."
    fi   
done
