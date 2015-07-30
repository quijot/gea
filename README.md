# gea

Gestión de Expedientes de Agrimensores.

__gea__ es una aplicación web basada en [Django](https://www.djangoproject.com/) para gestionar expedientes de agrimensores. Hasta ahora sólo fue usada en la provincia de _Santa Fe, Argentina_.

## Requisitos previos

- GNU/Linux
- Python 2.7.6 (no probé otro, pero seguro funciona bien)
- [Django](https://pypi.python.org/pypi/Django/) 1.8.3
- [psycopg2](https://pypi.python.org/pypi/psycopg2/) 2.6.1
- [Grappelli](http://grappelliproject.com/) 2.7.1
- [django-nested-admin](https://pypi.python.org/pypi/django-nested-admin/) 2.1.0 (para formularios anidados)

## Instalación

```bash
$ pip install gea
```

Se instalan también los ```requirements``` como Django, Grappelli, etc.

## Puesta en marcha

### Crear proyecto Django

```bash
$ django-admin startproject estudio
```

### Editar ```settings.py``` del proyecto Django:

```bash
$ vim estudio/settings.py
```

- Agregar __```gea```__, ```grappelli``` y ```nested_admin``` a las ```INSTALLED_APPS```:

```python
INSTALLED_APPS = (
    'grappelli',
    ...
    'gea',
    'nested_admin',
)
```

- Se pueden acomodar el Idioma y la TimeZone

```python
LANGUAGE_CODE = 'es-AR'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
```

### Editar ```urls.py``` del proyecto Django:

```bash
$ vim estudio/urls.py
```

- Agregar las urls de las aplicaciones que instalamos:

```python
from gea import views

urlpatterns = [
    ...
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^gea/', include('gea.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^nested_admin/', include('nested_admin.urls')),
]
```

### Base de datos y Superusuario

```bash
$ # dentro de "estudio"
$ python manage.py migrate
$ python manage.py createsuperuser
```

```migrate``` pone a punto la base de datos, ```createsuperuser``` instala el sistema de autenticación de Django, _Django's auth system_, con lo cual, pedirá usuario y contraseña, por ejemplo: _admin_ y _Af7Dr2ujW_. Con estos datos ingresaremos después a la interfaz de administración.


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
