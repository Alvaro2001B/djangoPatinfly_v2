# Introducció

## Veure migracions pendents

````shell
 .\patinfly_venv\Scripts\python.exe .\manage.py showmigrations
````

## Migrar canvis de la BBDD

````shell
.\patinfly_venv\Scripts\python.exe .\manage.py makemigrations
.\patinfly_venv\Scripts\python.exe .\manage.py migrate
````

## Crear un usuario

````shell
 .\patinfly_venv\Scripts\python.exe .\manage.py createsuperuser
````

## Añadir app

````shell
.\patinfly_venv\Scripts\python.exe .\manage.py startapp nombre
````