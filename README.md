# gea


Gestión de Expedientes de Agrimensores.

__gea__ es una aplicación web basada en [Django](https://www.djangoproject.com/) para gestionar expedientes de agrimensores. Hasta ahora sólo fue usada en la provincia de _Santa Fe, Argentina_.


## Requisitos previos

- GNU/Linux
- Python
- Django 1.6
- PostgreSQL
- [Grappelli](http://grappelliproject.com/) 2.5.1 (opcional)
  - [grappelli-nested-inlines](https://github.com/quijot/grappelli-nested-inlines) (opcional para ver formularios anidados, requiere Grappelli)

### Python

Python 2.7 preferentemente.

### Django

Para instalar [Django](https://www.djangoproject.com/):

```bash
$ pip install Django==1.6
```

### PostgreSQL

```bash
apt-get install postgresql postgresql-contrib postgresql-client python-psycopg2 postgresql-plpython-9.1
```

### Grappelli

Para instalar [Grappelli](http://grappelliproject.com/):

```bash
$ pip install django-grappelli==2.5.1
```

### grappelli-nested-inlines

Si instalaste Grappelli, podés aprovechar grappelli-nested-inlines para ver algunos formularios anidados. Para instalar [grappelli-nested-inlines](https://github.com/quijot/grappelli-nested-inlines):

```bash
$ pip install -e git+git://github.com/quijot/grappelli-nested-inlines.git#egg=grappelli-nested-inlines
```

## Instalación

### Crear proyecto Django y base de datos PostgreSQL

```bash
$ django-admin.py startproject estudio
$ cd estudio
$ # si no tenés un superuser de postgresql
$ createuser pgsuperuser
$ # responder "yes" cuando pregunte si queremos que sea superuser
$ createdb gea
```

### Descargar o clonar __gea__

[Descargar](https://github.com/quijot/gea/archive/master.zip) y descomprimir dentro de _estudio_ 

```bash
$ # dentro de "estudio"
$ wget https://github.com/quijot/gea/archive/master.zip
$ unzip master.zip
$ mv gea-master gea
```

o clonar (requiere git -> ```$ apt-get install git```):

```bash
$ # dentro de "estudio"
$ git clone https://github.com/quijot/gea.git
```

### Editar ```settings.py``` del proyecto Django:

```bash
$ vim estudio/settings.py
```

- Agregar __gea__ a las ```INSTALLED_APPS```:

```python
INSTALLED_APPS = (
#   'grappelli_nested', # Si instalaste grappelli-nested-inlines
#   'grappelli',        # Si instalaste Grappelli
    'django.contrib.admin',
    'django.contrib.auth',
    ...
    'gea',
)
```

- Agregar la configuración de la base de datos:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'gea',
        'USER': 'pgsuperuser',
        'PASSWORD': '<your-pg-password>',
    }
}
```

### Sincronizar la base de datos

```bash
$ # dentro de "estudio"
$ python manage.py syncdb
```

Además de sincronizar la base de datos, también se estará instalando el sistema de autenticación de Django, _Django's auth system_, con lo cual, pedirá usuario y contraseña, por ejemplo: _admin_ y _Af7Dr2ujW_.

#### Opcional: Volcar datos de la provincia de Santa Fe

Ejecutar el script que completa datos referidos a Circunscripciones, Departamentos, Distritos, Subdistritos y Zonas más algunos datos de ejemplo y crea funciones y triggers para calcular automáticamente el dígito verificador de las Partidas de Impuesto Inmobiliario:

```bash
$ # dentro de "estudio"
$ chmod +x gea/backup/db/basics-db.sh
$ ./gea/backup/db/basics-db.sh
```

### Archivos estáticos (css, img, js)

Por último, algo muy importante: los archivos de estilo, imágenes y scripts que usará nuestra nueva aplicación.

```bash
$ # dentro de "estudio"
$ python manage.py collectstatic
```

¡LISTO... Ahora podemos probar cómo quedó nuestra django-app!

```bash
$ # dentro de "estudio"
$ python manage.py runserver
```

e ingresamos a [http://127.0.0.1:8000/](http://127.0.0.1:8000/)...

## LICENCIA

[BSD](https://raw.github.com/quijot/gea/master/LICENSE)

