# Lista processos django executando em background
PROCESSOS=`ps -xU $(whoami) | grep -v "grep" | grep "python manage"| cut -d ' ' -f 1`

for p in $PROCESSOS; do
   echo "Processo: $p"
done
