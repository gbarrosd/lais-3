# Fase_2_lais
Projeto feito para a Fase 2 do processo de avaliação da bolsa em Python/django do LAIS

# Populando banco de dados

Quando executar o projeto pela primeira vez executar as migrations 
>$ python manage.py makemigrations 

>$ python manage.py migrate

Logo após executar o seed para popular o banco de dados com os grupos e estabelecimentos
>$ manage.py loaddata estab_data.json

>$ manage.py loaddata grupos_data.json

E finalmente execute o servidor
>$ python manage.py runserver
