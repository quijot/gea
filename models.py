# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class CharNullField(models.CharField): #subclass the CharField
    description = "CharField that stores NULL but returns ''"
    __metaclass__ = models.SubfieldBase # this ensures to_python will be called
    def to_python(self, value):  #this is the value right out of the db, or an instance
       if isinstance(value, models.CharField): #if an instance, just return the instance
              return value 
       if value==None:   #if the db has a NULL (==None in Python)
              return ""  #convert it into the Django-friendly '' string
       else:
              return value #otherwise, return just the value
    def get_prep_value(self, value):  #catches value right before sending to db
       if value=="":     #if Django tries to save '' string, send the db None (NULL)
            return None
       else:
            return value #otherwise, just pass the value

class URLNullField(models.URLField): #subclass the URLField
    description = "URLField that stores NULL but returns ''"
    __metaclass__ = models.SubfieldBase # this ensures to_python will be called
    def to_python(self, value):  #this is the value right out of the db, or an instance
       if isinstance(value, models.URLField): #if an instance, just return the instance
              return value 
       if value==None:   #if the db has a NULL (==None in Python)
              return ""  #convert it into the Django-friendly '' string
       else:
              return value #otherwise, return just the value
    def get_prep_value(self, value):  #catches value right before sending to db
       if value=="":     #if Django tries to save '' string, send the db None (NULL)
            return None
       else:
            return value #otherwise, just pass the value

class EmailNullField(models.EmailField): #subclass the EmailField
    description = "EmailField that stores NULL but returns ''"
    __metaclass__ = models.SubfieldBase # this ensures to_python will be called
    def to_python(self, value):  #this is the value right out of the db, or an instance
        if isinstance(value, models.EmailField): #if an instance, just return the instance
            return value 
        if value==None:   #if the db has a NULL (==None in Python)
            return ""  #convert it into the Django-friendly '' string
        else:
            return value #otherwise, return just the value
    def get_prep_value(self, value):  #catches value right before sending to db
        if value=="":     #if Django tries to save '' string, send the db None (NULL)
            return None
        else:
            return value #otherwise, just pass the value
            
class Antecedente(models.Model):
    id = models.AutoField(primary_key=True)
    expediente = models.ForeignKey('Expediente', null=True, blank=True, default=None)
    expediente_modificado = models.ForeignKey('Expediente', null=True, blank=True, default=None, related_name='expediente_modificado')
    inscripcion_numero = models.IntegerField(null=True, blank=True, default=None)
    duplicado = models.BooleanField(default=False)
    obs = CharNullField(max_length=255, null=True, blank=True, default=None)
    plano_ruta = URLNullField(max_length=100, null=True, blank=True, default=None)
    class Meta:
        db_table = 'antecedente'

class Catastro(models.Model):
    id = models.AutoField(primary_key=True)
    expediente_partida = models.ForeignKey('ExpedientePartida')
    zona = models.ForeignKey('Zona', db_column='zona', null=True, blank=True, default=None)
    seccion = CharNullField(max_length=10, null=True, blank=True, default=None)
    poligono = CharNullField(max_length=10, null=True, blank=True, default=None)
    manzana = CharNullField(max_length=10, null=True, blank=True, default=None)
    parcela = CharNullField(max_length=10, null=True, blank=True, default=None)
    subparcela = CharNullField(max_length=10, null=True, blank=True, default=None)
    class Meta:
        db_table = 'catastro'

class CatastroLocal(models.Model):
    id = models.AutoField(primary_key=True)
    expediente_lugar = models.ForeignKey('ExpedienteLugar')
    seccion = CharNullField(max_length=20, null=True, blank=True, default=None)
    manzana = CharNullField(max_length=20, null=True, blank=True, default=None)
    parcela = CharNullField(max_length=20, null=True, blank=True, default=None)
    subparcela = CharNullField(max_length=20, null=True, blank=True, default=None)
    suburbana = models.BooleanField(default=False)
    poligono = CharNullField(max_length=20, null=True, blank=True, default=None)
    class Meta:
        db_table = 'catastro_local'
        verbose_name_plural = 'catastros_locales'
    def __unicode__(self):
        return '%s-%s-%s' % (self.seccion, self.manzana, self.parcela)

class Circunscripcion(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = CharNullField(max_length=10)
    orden = CharNullField(max_length=7)
    class Meta:
        db_table = 'circunscripcion'
        ordering = ['id']
        verbose_name_plural = 'circunscripciones'
    def __unicode__(self):
        return self.nombre

class Dp(models.Model):
    dp = models.IntegerField(primary_key=True)
    nombre = CharNullField(max_length=50, verbose_name='nombre depto')
    habitantes = models.IntegerField(null=True, blank=True)
    superficie = models.IntegerField(null=True, blank=True)
    cabecera = CharNullField(max_length=50, null=True, blank=True)
    circunscripcion = models.ForeignKey(Circunscripcion)
    def departamento(self):
        return '%02d %s' % (self.dp, self.nombre)
    class Meta:
        db_table = 'dp'
        verbose_name_plural = 'Departamentos'
        ordering = ['dp']
    def __unicode__(self):
        return '%02d' % self.dp

class Ds(models.Model):
    id = models.AutoField(primary_key=True)
    dp = models.ForeignKey(Dp, db_column='dp')
    ds = models.IntegerField()
    nombre = CharNullField(max_length=50, verbose_name='nombre distrito')
    def distrito(self):
        return '%02d %s' % (self.ds, self.nombre)
    class Meta:
        db_table = 'ds'
        verbose_name_plural = 'distritos'
        ordering = ['dp', 'ds']
    def __unicode__(self):
        return '%02d' % self.ds

class Expediente(models.Model):
    MENSURAS = ((1, 1),(2, 2),(3, 3),(4, 4))
    id = models.IntegerField(primary_key=True)
    fecha_plano = models.DateField(null=True, blank=True, default=None)
    mensuras = models.SmallIntegerField(null=True, blank=True, choices=MENSURAS, default=1, verbose_name='cantidad de mensuras')
    inscripcion_numero = models.IntegerField(unique=True, null=True, blank=True, default=None)
    inscripcion_fecha = models.DateField(null=True, blank=True, default=None)
    duplicado = models.BooleanField(default=False)
    orden_numero = models.IntegerField(null=True, blank=True, default=None)
    orden_fecha = models.DateField(null=True, blank=True, default=None)
    sin_inscripcion = models.BooleanField(default=False)
    cancelado = models.BooleanField(default=False)
    cancelado_por = CharNullField(max_length=100, null=True, blank=True, default=None)
    plano_ruta = URLNullField(max_length=100, null=True, blank=True, default=None)
    def inscripto(self):
        return (inscripcion_numero != 0)
    class Meta:
        db_table = 'expediente'
        ordering = ['-id']
    def __unicode__(self):
        return str(self.id)

class ExpedienteLugar(models.Model):
    id = models.AutoField(primary_key=True)
    expediente = models.ForeignKey(Expediente)
    lugar = models.ForeignKey('Lugar')
    class Meta:
        db_table = 'expediente_lugar'
        verbose_name_plural = 'expedientes_lugares'
        ordering = ['expediente']
    def __unicode__(self):
        return str(self.expediente)

class ExpedienteObjeto(models.Model):
    MENSURAS = ((1, 1),(2, 2),(3, 3),(4, 4))
    id = models.AutoField(primary_key=True)
    expediente = models.ForeignKey(Expediente)
    mensura = models.SmallIntegerField(null=True, blank=True, choices=MENSURAS, default=1)
    objeto = models.ForeignKey('Objeto')
    class Meta:
        db_table = 'expediente_objeto'
        verbose_name_plural = 'expedientes_objetos'

class ExpedientePartida(models.Model):
    id = models.AutoField(primary_key=True)
    expediente = models.ForeignKey(Expediente)
    partida = models.ForeignKey('Partida')
    class Meta:
        db_table = 'expediente_partida'
        verbose_name_plural = 'expedientes_partidas'
        ordering = ['expediente']
    def __unicode__(self):
        return '%s - %s' % (str(self.expediente), self.partida)

class ExpedientePersona(models.Model):
    ITEMS = ((1, 'a'),(2, 'b'),(3, 'c'),(4, 'd'),(5, 'e'),(6, 'f'),(7, 'g'),(8, 'h'))
    MENSURAS = ((1, 1),(2, 2),(3, 3),(4, 4))
    id = models.AutoField(primary_key=True)
    expediente = models.ForeignKey(Expediente)
    mensura = models.SmallIntegerField(null=True, blank=True, choices=MENSURAS, default=1)
    item = models.SmallIntegerField(null=True, blank=True, choices=ITEMS, default=None)
    persona = models.ForeignKey('Persona')
    comitente = models.BooleanField(default=False)
    propietario = models.BooleanField(default=True)
    poseedor = models.BooleanField(default=False)
    partes_indivisas_propias = models.IntegerField(null=True, blank=True, default=None)
    partes_indivisas_total = models.IntegerField(null=True, blank=True, default=None)
    sucesion = models.BooleanField(default=False)
    nuda_propiedad = models.BooleanField(default=False)
    usufructo = models.BooleanField(default=False)
    class Meta:
        db_table = 'expediente_persona'
        verbose_name_plural = 'expedientes_personas'
        ordering = ['mensura', 'item', 'persona__apellidos', 'persona__nombres']

class ExpedienteProfesional(models.Model):
    id = models.AutoField(primary_key=True)
    expediente = models.ForeignKey(Expediente)
    profesional = models.ForeignKey('Profesional')
    class Meta:
        db_table = 'expediente_profesional'
        verbose_name_plural = 'expedientes_profesionales'

class Lugar(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = CharNullField(max_length=80)
    obs = CharNullField(max_length=255, null=True, blank=True, default=None)
    class Meta:
        db_table = 'lugar'
        verbose_name_plural = 'lugares'
        ordering = ['nombre']
    def __unicode__(self):
        return self.nombre

class Objeto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = CharNullField(max_length=80)
    class Meta:
        db_table = 'objeto'
        ordering = ['nombre']
    def __unicode__(self):
        return self.nombre

class Partida(models.Model):
    id = models.AutoField(primary_key=True)
    sd = models.ForeignKey('Sd', db_column='sd', null=True, blank=True, default=None)
    pii = models.IntegerField()
    subpii = models.IntegerField()
    api = models.SmallIntegerField(null=True, blank=True, default=0)
    def pii_completa(self):
        return '%s-%06d/%04d-%d' % (self.sd, self.pii, self.subpii, self.api)
    class Meta:
        db_table = 'partida'
        unique_together = (('pii', 'subpii'))
        ordering = ['pii', 'subpii']
    def __unicode__(self):
        return '%06d/%04d-%d' % (self.pii, self.subpii, self.api)

class PartidaDominio(models.Model):
    id = models.AutoField(primary_key=True)
    partida = models.ForeignKey(Partida)
    tomo = models.IntegerField(null=True, blank=True, default=None)
    par = models.BooleanField(default=False)
    impar = models.BooleanField(default=False)
    folio = models.IntegerField(null=True, blank=True, default=None)
    numero = models.IntegerField(null=True, blank=True, default=None)
    fecha = models.DateField(null=True, blank=True, default=None)
    fecha_inscripcion_definitiva = models.DateField(null=True, blank=True, default=None)
    class Meta:
        db_table = 'partida_dominio'
        verbose_name_plural = 'partida_dominios'

class Persona(models.Model):
    id = models.AutoField(primary_key=True)
    nombres = CharNullField(max_length=100, null=True, blank=True, default=None)
    apellidos = CharNullField(max_length=100)
    nombres_alternativos = CharNullField(max_length=100, null=True, blank=True, default=None)
    apellidos_alternativos = CharNullField(max_length=100, null=True, blank=True, default=None)
    domicilio = CharNullField(max_length=50, null=True, blank=True, default=None)
    lugar = models.ForeignKey(Lugar, null=True, blank=True, default=None)
    telefono = CharNullField(max_length=20, null=True, blank=True, default=None)
    celular = CharNullField(max_length=20, null=True, blank=True, default=None)
    email = EmailNullField(max_length=50, unique=True, null=True, blank=True, default=None)
    cuit_cuil = CharNullField(max_length=14, unique=True, null=True, blank=True, default=None, verbose_name='DNI/CUIT/CUIL/CDI')
    def nombre_completo(self):
        return '%s %s' % (self.apellidos, self.nombres)
    class Meta:
        db_table = 'persona'
        ordering = ['apellidos', 'nombres']
    def __unicode__(self):
        return '%s %s' % (self.apellidos, self.nombres)

class Profesional(models.Model):
    id = models.AutoField(primary_key=True)
    nombres = CharNullField(max_length=50)
    apellidos = CharNullField(max_length=50)
    titulo = models.ForeignKey('Titulo', null=True, blank=True, default=None)
    icopa = CharNullField(max_length=8, null=True, blank=True, default=None)
    domicilio = CharNullField(max_length=50, null=True, blank=True, default=None)
    lugar = models.ForeignKey(Lugar, null=True, blank=True, default=None)
    telefono = CharNullField(max_length=20, null=True, blank=True, default=None)
    celular = CharNullField(max_length=20, null=True, blank=True, default=None)
    web = URLNullField(max_length=50, null=True, blank=True, default=None)
    email = EmailNullField(max_length=50, unique=True, null=True, blank=True, default=None)
    cuit_cuil = CharNullField(max_length=14, unique=True, null=True, blank=True, default=None, verbose_name='DNI/CUIT/CUIL/CDI')
    habilitado = models.BooleanField(default=True)
    jubilado = models.BooleanField(default=False)
    fallecido = models.BooleanField(default=False)
    def nombre_completo(self):
        return '%s %s' % (self.apellidos, self.nombres)
    class Meta:
        db_table = 'profesional'
        verbose_name_plural = 'profesionales'
        ordering = ['apellidos', 'nombres']
    def __unicode__(self):
        return '%s %s' % (self.apellidos, self.nombres)

class Sd(models.Model):
    id = models.AutoField(primary_key=True)
    ds = models.ForeignKey(Ds, db_column='ds')
    sd = models.IntegerField()
    nombre = CharNullField(max_length=50, null = True, blank=True, default = None, verbose_name='nombre subdistrito')
    class Meta:
        db_table = 'sd'
        verbose_name_plural = 'subdistritos'
        ordering = ['ds', 'sd']
    def __unicode__(self):
        return '%s%s%02d' % (self.ds.dp, self.ds, self.sd)

class Titulo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = CharNullField(max_length=30)
    class Meta:
        db_table = 'titulo'
        ordering = ['nombre']
    def __unicode__(self):
        return self.nombre

class Zona(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = CharNullField(max_length=50)
    class Meta:
        db_table = 'zona'
        ordering = ['id']
    def __unicode__(self):
        return str(self.id)

