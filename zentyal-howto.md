# Hacerlo funcionar en [Zentyal](http://www.zentyal.org/)

## Requisitos previos

- Apache 2.4.7 (no probé otro, pero seguro funciona bien)
- mod_wsgi
- PostgreSQL 9.3.9

### mod_wgsi:

```bash
$ sudo apt-get install libapache2-mod-wsgi
```

### PostgreSQL

```bash
sudo apt-get install postgresql postgresql-contrib postgresql-client postgresql-plpython-9.3

#### Crear base de datos PostgreSQL

Vas a necesitar un superuser de postgresql. [En este post](http://stackoverflow.com/questions/1471571/how-to-configure-postgresql-for-the-first-time) explica bastante bien cómo hacerlo.

```bash
$ # si no tenés un superuser de postgresql, crealo ahora
$ createdb gea
```
#### Editar ```settings.py``` del proyecto Django:

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

## Crear un Host Virtual en Zentyal

Office -> Servidor Web -> Hosts virtuales -> Añadir nuevo

Supongamos que elegimos el nombre __gea.net__.

## Configurar wsgi

Crear un archivo que se incluirá en la configuración del VirtualHost.

```bash
$ sudo vim /etc/apache2/sites-available/user-ebox-gea.net/extra.conf
```

Pegar dentro las siguientes directivas, reemplazando _<path-to-estudio>_ con lo que corresponda. El objetivo poder usar ```wsgi``` como daemon.

```bash
# static files
Alias /static/ /<path-to-estudio>/static/
<Directory /<path-to-estudio>/static>
Require all granted
</Directory>

# wsgi as daemon
WSGIDaemonProcess gea.net python-path=/<path-to-estudio>
WSGIProcessGroup gea.net

# wsgi script alias and location
WSGIScriptAlias / /<path-to-estudio>/estudio/wsgi.py
<Directory /<path-to-estudio>/estudio>
<Files wsgi.py>
Require all granted
</Files>
</Directory>
```

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

## Usar __gea__ en Zentyal

¡Listo! Ya podemos entrar a [http://gea.net](http://gea.net/admin) y usar __```gea```__ desde todas las terminales en Zentyal!

Cada vez que hagamos un cambio en la aplicación, deberemos hacer reload del servidor web:

```bash
$ sudo service apache2 reload
```
