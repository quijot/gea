# gea

Gestión de Expedientes de Agrimensores.

__gea__ es una aplicación web basada en [Django](https://www.djangoproject.com/) para gestionar expedientes de agrimensores. Hasta ahora sólo fue usada en la provincia de _Santa Fe, Argentina_.

## Requisitos previos

- GNU/Linux
- Python 2.7.6 (No funciona directamente con Python 3, hay que cambiar por lo menos ```__unicode__``` por ```__str__``` en models.py.)
- [Django](https://pypi.python.org/pypi/Django/) 1.9.6
- [psycopg2](https://pypi.python.org/pypi/psycopg2/) 2.6.1 (opcional si utiliza PostgreSQL)
- [Grappelli](http://grappelliproject.com/) 2.8.1 (opcional)
- [django-nested-admin](https://pypi.python.org/pypi/django-nested-admin/) 3.0.2 (para formularios anidados)

## Instalación

```bash
$ pip install gea
```

Se instalan también los ```requirements``` como Django, Grappelli y nested-admin. Si además quiere utilizar PostgreSQL para la Base de Datos, deberá instalar manualmente psycopg2.

```bash
$ pip install psycopg2
```

## Puesta en marcha

### Crear proyecto Django

```bash
$ django-admin startproject estudio
```

### Editar ```settings.py``` del proyecto Django:

```bash
$ # dentro de "estudio"
$ vim estudio/settings.py
```

- Agregar __```gea```__, ```grappelli``` (opcional)  y ```nested_admin``` a las ```INSTALLED_APPS```:

```python
INSTALLED_APPS = (
    'grappelli', # opcional
    ...
    'gea.apps.GeaConfig',
    'nested_admin',
)
```

- Se pueden acomodar el Idioma y la TimeZone

```python
LANGUAGE_CODE = 'es-AR'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
```

#### Para utilizar PostgreSQL (opcional)

- Opcionalmente, configurar la Base de Datos para utilizar PostgreSQL, de otro modo, Django usa SQLite3 por defecto. Editar ```settings.py```.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'gea',
        'USER': '<postgresql-user>',
        'PASSWORD': '<postgresql-password>', # be creative
        'HOST': 'localhost',
    }
}
```

con esta opción se debe crear la BD, con el comando ```createdb``` de PostgreSQL

```bash
$ createdb gea
```

### Editar ```urls.py``` del proyecto Django:

```bash
$ # dentro de "estudio"
$ vim estudio/urls.py
```

- Importar las vistas de ```gea``` y agregar las urls de las aplicaciones que instalamos:

```python
from django.conf.urls import include, url
from django.contrib import admin

from gea.views import Home

urlpatterns = [
    ...
    url(r'^grappelli/', include('grappelli.urls')), # opcional
    url(r'^gea/', include('gea.urls')),
    url(r'^$', Home.as_view(), name='home'),
    url(r'^nested_admin/', include('nested_admin.urls')),
]
```

### Base de datos y Superusuario

```bash
$ # dentro de "estudio"
$ python manage.py makemigrations gea
$ python manage.py migrate
$ python manage.py createsuperuser
```

```makemigrations``` y ```migrate``` ponen a punto la base de datos, ```createsuperuser``` instala el sistema de autenticación de Django, _Django's auth system_, con lo cual, pedirá usuario, mail y contraseña, por ejemplo: _admin_ y _Af7Dr2ujW_. Con estos datos ingresaremos después a la interfaz de administración.

## Archivos estáticos (css, img, js)

Por último, algo muy importante: los archivos de estilo, imágenes y scripts que usará nuestra nueva aplicación.

Editar ```settings.py``` agregando la siguiente linea:

```python
STATIC_ROOT = './static/'
```

Y ejecutar:
```bash
$ # dentro de "estudio"
$ python manage.py collectstatic
```

¡**LISTO**... Ahora podemos probar cómo quedó nuestra django-app!

```bash
$ # dentro de "estudio"
$ python manage.py runserver
```

e ingresamos a [http://127.0.0.1:8000/](http://127.0.0.1:8000/)... con los datos del superusuario que creamos antes.

### Opcional sólo con PostgreSQL: Volcar datos de la provincia de Santa Fe

Ejecutar el script que completa datos referidos a Circunscripciones, Departamentos, Distritos, Subdistritos y Zonas más algunos datos de ejemplo y crea funciones y triggers para calcular automáticamente el dígito verificador de las Partidas de Impuesto Inmobiliario:

```bash
$ # dentro de "estudio"
$ chmod +x gea/backup/db/basics-db.sh
$ ./gea/backup/db/basics-db.sh
```

## LICENCIA

[BSD](https://raw.github.com/quijot/gea/master/LICENSE)
