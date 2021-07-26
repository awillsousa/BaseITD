# Executa a aplicaçao django em background

# Limpa o arquivo anterior
rm nohup.out

# Executa aplicacao
nohup python manage.py runserver 0:8000 &


