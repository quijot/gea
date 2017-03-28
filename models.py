from django.db import models
from django_extensions.db.models import (
    TitleSlugDescriptionModel, TimeStampedModel)
# from django.urls import reverse
from django.core.urlresolvers import reverse
from filebrowser.fields import FileBrowseField


def CapitalizePhrase(string):
    phrase = ''
    for word in string.split():
        phrase = u'%s %s%s' % (phrase, word[0].upper(), word[1:].lower())
    return phrase.strip()


class CharNullField(models.CharField):  # subclass the CharField
    description = "CharField that stores NULL but returns ''"
    # this ensures to_python will be called

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return u''
        return value

    # this is the value right out of the db, or an instance
    def to_python(self, value):
        # if an instance, just return the instance
        if isinstance(value, models.CharField):
            return value
        if value is None:  # if the db has a NULL (==None in Python)
            return u''  # convert it into the Django-friendly '' string
        else:
            return value  # otherwise, return just the value

    # catches value right before sending to db
    def get_prep_value(self, value):
        # if Django tries to save '' string, send the db None (NULL)
        if value == u'':
            return None
        else:
            return value  # otherwise, just pass the value


class URLNullField(models.URLField):  # subclass the URLField
    description = "URLField that stores NULL but returns ''"
    # this ensures to_python will be called

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return u''
        return value

    # this is the value right out of the db, or an instance
    def to_python(self, value):
        # if an instance, just return the instance
        if isinstance(value, models.URLField):
            return value
        if value is None:  # if the db has a NULL (==None in Python)
            return u''  # convert it into the Django-friendly '' string
        else:
            return value  # otherwise, return just the value

    # catches value right before sending to db
    def get_prep_value(self, value):
        # if Django tries to save '' string, send the db None (NULL)
        if value == u'':
            return None
        else:
            return value  # otherwise, just pass the value


class EmailNullField(models.EmailField):  # subclass the EmailField
    description = "EmailField that stores NULL but returns ''"
    # this ensures to_python will be called

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return u''
        return value

    # this is the value right out of the db, or an instance
    def to_python(self, value):
        # if an instance, just return the instance
        if isinstance(value, models.EmailField):
            return value
        if value is None:  # if the db has a NULL (==None in Python)
            return u''  # convert it into the Django-friendly '' string
        else:
            return value  # otherwise, return just the value

    # catches value right before sending to db
    def get_prep_value(self, value):
        # if Django tries to save '' string, send the db None (NULL)
        if value == u'':
            return None
        else:
            return value  # otherwise, just pass the value


class Antecedente(models.Model):
    id = models.AutoField(primary_key=True)
    expediente = models.ForeignKey(
        'Expediente', null=True, blank=True, default=None)
    expediente_modificado = models.ForeignKey(
        'Expediente', null=True, blank=True, default=None,
        related_name='expediente_modificado')
    inscripcion_numero = models.IntegerField(
        null=True, blank=True, default=None)
    duplicado = models.BooleanField(default=False)
    obs = CharNullField("Observaciones", max_length=255, null=True, blank=True,
                        default=None)
    plano_ruta = URLNullField(
        max_length=100, null=True, blank=True, default=None)
    plano = FileBrowseField("Enlace al plano", max_length=200,
                            directory="planos/", extensions=[".pdf"],
                            blank=True, null=True)


class Catastro(models.Model):
    id = models.AutoField(primary_key=True)
    expediente_partida = models.ForeignKey('ExpedientePartida')
    zona = models.ForeignKey(
        'Zona', db_column='zona', null=True, blank=True, default=None)
    seccion = CharNullField(max_length=10, null=True, blank=True, default=None)
    poligono = CharNullField(
        max_length=10, null=True, blank=True, default=None)
    manzana = CharNullField(max_length=10, null=True, blank=True, default=None)
    parcela = CharNullField(max_length=10, null=True, blank=True, default=None)
    subparcela = CharNullField(
        max_length=10, null=True, blank=True, default=None)

    def __str__(self):
        if str(self.zona) in ('1', '2', '3'):
            return u''.join(('Z:', str(self.zona), ' - S:', self.seccion,
                             ' - M:', self.manzana, ' - P:', self.parcela))
        elif str(self.zona) in ('4', '5'):
            return u''.join(('Z:', str(self.zona), ' - Pol:', self.poligono,
                             ' - P:', self.parcela))
        else:
            return u''


class CatastroLocal(models.Model):
    id = models.AutoField(primary_key=True)
    expediente_lugar = models.ForeignKey('ExpedienteLugar')
    seccion = CharNullField(max_length=20, null=True, blank=True, default=None)
    manzana = CharNullField(max_length=20, null=True, blank=True, default=None)
    parcela = CharNullField(max_length=20, null=True, blank=True, default=None)
    subparcela = CharNullField(
        max_length=20, null=True, blank=True, default=None)
    suburbana = models.BooleanField(default=False)
    poligono = CharNullField(
        max_length=20, null=True, blank=True, default=None)

    class Meta:
        verbose_name = 'catastro local'
        verbose_name_plural = 'catastros locales'

    def __str__(self):
        return u''.join(('S:', self.seccion, ' - M:', self.manzana, ' - P:',
                         self.parcela))


class Circunscripcion(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = CharNullField(max_length=10)
    orden = CharNullField(max_length=7)

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'circunscripciones'

    def __str__(self):
        return self.nombre


class Comprobante(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = CharNullField(max_length=50)

    def __str__(self):
        return self.nombre


class Presupuesto(models.Model):
    id = models.AutoField(primary_key=True)
    expediente = models.ForeignKey('Expediente')
    monto = models.DecimalField(max_digits=8, decimal_places=2)
    fecha = models.DateField()
    porcentaje_cancelado = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name='% cancelado')
    obs = CharNullField("Observaciones", max_length=255, null=True, blank=True,
                        default=None)

    class Meta:
        ordering = ['expediente']

    def __str__(self):
        return u'%s - $%s - %s' % (self.expediente, str(self.monto),
                                   str(self.fecha))


class Pago(models.Model):
    id = models.AutoField(primary_key=True)
    presupuesto = models.ForeignKey(Presupuesto)
    comprobante = models.ForeignKey(Comprobante)
    comprobante_nro = models.IntegerField(null=True, blank=True, default=None)
    fecha = models.DateField(null=True, blank=True, default=None)
    monto = models.DecimalField(max_digits=8, decimal_places=2)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2)
    obs = CharNullField("Observaciones", max_length=255, null=True, blank=True,
                        default=None)

    def __str__(self):
        return u'%s%% - %s' % (str(self.porcentaje), str(self.fecha))


class Dp(models.Model):
    dp = models.IntegerField(primary_key=True)
    nombre = CharNullField(max_length=50, verbose_name='nombre depto')
    habitantes = models.IntegerField(null=True, blank=True)
    superficie = models.IntegerField(null=True, blank=True)
    cabecera = CharNullField(max_length=50, null=True, blank=True)
    circunscripcion = models.ForeignKey(Circunscripcion)

    def departamento(self):
        return u'%02d %s' % (self.dp, self.nombre)

    class Meta:
        verbose_name_plural = 'Departamentos'
        ordering = ['dp']

    def __str__(self):
        return u'%02d' % self.dp


class Ds(models.Model):
    id = models.AutoField(primary_key=True)
    dp = models.ForeignKey(Dp, db_column='dp')
    ds = models.IntegerField()
    nombre = CharNullField(max_length=50, verbose_name='nombre distrito')

    def distrito(self):
        return u'%02d' % self.ds

    class Meta:
        verbose_name_plural = 'distritos'
        ordering = ['dp', 'ds']

    def __str__(self):
        return u'%02d' % self.ds


class Sd(models.Model):
    id = models.AutoField(primary_key=True)
    ds = models.ForeignKey(Ds, db_column='ds')
    sd = models.IntegerField()
    nombre = CharNullField(
        max_length=50, null=True, blank=True, default=None,
        verbose_name='nombre subdistrito')

    def subdistrito(self):
        return u'%02d' % self.sd

    def dp(self):
        return self.ds.dp
    dp.short_description = 'Dp'

    def dp_nombre(self):
        return self.ds.dp.nombre
    dp_nombre.short_description = 'Dp nombre'

    def ds_nombre(self):
        return self.ds.nombre
    ds_nombre.short_description = 'Ds nombre'

    class Meta:
        verbose_name_plural = 'subdistritos'
        ordering = ['ds', 'sd']

    def __str__(self):
        return u'%s%s%02d' % (self.ds.dp, self.ds, self.sd)
    nomenclatura = property(__str__)


class Expediente(TimeStampedModel):
    id = models.IntegerField('Expediente Nº', primary_key=True)
    fecha_plano = models.DateField(null=True, blank=True, default=None)
    fecha_medicion = models.DateField(null=True, blank=True, default=None)
    inscripcion_numero = models.IntegerField('SCIT inscripción Nº',unique=True,
                                             null=True, blank=True,
                                             default=None)
    inscripcion_fecha = models.DateField('Fecha inscripción', null=True,
                                         blank=True, default=None)
    duplicado = models.BooleanField(default=False)
    orden_numero = models.IntegerField('CoPA Expendiente Nº', null=True,
                                       blank=True, default=None)
    orden_fecha = models.DateField('Fecha contrato', null=True, blank=True,
                                   default=None)
    sin_inscripcion = models.BooleanField(default=False)
    cancelado = models.BooleanField(default=False)
    cancelado_por = CharNullField(max_length=100, null=True, blank=True,
                                  default=None)
    plano_ruta = URLNullField(max_length=100, null=True, blank=True,
                              default=None)
    plano = FileBrowseField("Enlace al plano", max_length=200,
                            directory="planos/", extensions=[".pdf"],
                            blank=True, null=True)

    def get_absolute_url(self):
        return reverse('expediente', kwargs={'pk': str(self.id)})
        # return "/gea/expedientes/%i" % self.id # MAL: poco portable

    def inscripto(self):
        return (self.inscripcion_numero != 0)

    def propietarios_count(self):
        """Devuelve la cantidad de personas que figuran como propietarias."""
        return self.expedientepersona_set.filter(propietario=True).count()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return u'%d' % self.id


class ExpedienteLugar(models.Model):
    id = models.AutoField(primary_key=True)
    expediente = models.ForeignKey(Expediente)
    lugar = models.ForeignKey('Lugar')

    class Meta:
        verbose_name = 'lugar'
        verbose_name_plural = 'lugares'
        ordering = ['expediente', 'lugar']

    def __str__(self):
        return self.lugar.nombre


class ExpedienteObjeto(models.Model):
    id = models.AutoField(primary_key=True)
    expediente = models.ForeignKey(Expediente)
    objeto = models.ForeignKey('Objeto')

    class Meta:
        verbose_name = 'objeto'
        verbose_name_plural = 'objetos'
        ordering = ['expediente', 'objeto']

    def __str__(self):
        return self.objeto.nombre


class ExpedientePartida(models.Model):
    id = models.AutoField(primary_key=True)
    expediente = models.ForeignKey(Expediente)
    partida = models.ForeignKey('Partida')
    set_ruta = URLNullField(
        max_length=100, null=True, blank=True, default=None)
    informe_catastral = FileBrowseField(max_length=200, directory="set/",
                                        extensions=[".pdf"], blank=True,
                                        null=True)

    class Meta:
        verbose_name = 'partida'
        verbose_name_plural = 'partidas'
        ordering = ['expediente', 'partida']

    def __str__(self):
        return u'%s' % self.partida


class ExpedientePersona(models.Model):
    id = models.AutoField(primary_key=True)
    expediente = models.ForeignKey(Expediente)
    persona = models.ForeignKey('Persona')
    comitente = models.BooleanField(default=False)
    propietario = models.BooleanField(default=True)
    poseedor = models.BooleanField(default=False)
    sucesor = models.BooleanField(default=False)
    partes_indivisas_propias = models.IntegerField(
        null=True, blank=True, default=None)
    partes_indivisas_total = models.IntegerField(
        null=True, blank=True, default=None)
    sucesion = models.BooleanField(default=False)
    nuda_propiedad = models.BooleanField(default=False)
    usufructo = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'persona involucrada'
        verbose_name_plural = 'personas involucradas'
        ordering = [
            'persona__apellidos', 'persona__nombres']

    def __str__(self):
        return u'%d - %s %s' % (self.expediente.id,
                                self.persona.apellidos,
                                self.persona.nombres)


class ExpedienteProfesional(models.Model):
    id = models.AutoField(primary_key=True)
    expediente = models.ForeignKey(Expediente)
    profesional = models.ForeignKey('Profesional')

    class Meta:
        verbose_name = 'profesional firmante'
        verbose_name_plural = 'profesionales firmantes'
        ordering = ['profesional__apellidos', 'profesional__nombres']

    def __str__(self):
        return self.profesional.nombre_completo()


class Lugar(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = CharNullField(max_length=80)
    obs = CharNullField("Observaciones", max_length=255, null=True, blank=True,
                        default=None)

    class Meta:
        verbose_name_plural = 'lugares'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Objeto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = CharNullField(max_length=80)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Partida(models.Model):
    id = models.AutoField(primary_key=True)
    sd = models.ForeignKey(
        'Sd', db_column='sd', null=True, blank=True, default=None)
    pii = models.IntegerField()
    subpii = models.IntegerField()
    api = models.SmallIntegerField(null=True, blank=True, default=0)

    def pii_completa(self):
        return u'%s-%06d/%04d-%d' % (self.sd, self.pii, self.subpii, self.api)

    def calc_dvapi(self, sd, pii, subpii=0):
        coef = '9731'
        _coef = coef + coef + coef + coef
        strpii = '%06d%06d%04d' % (sd, pii, subpii)
        suma = 0
        for i in range(0, len(strpii)):
            m = str(int(strpii[i]) * int(_coef[i]))
            suma += int(m[len(m) - 1])
        return (10 - (suma % 10)) % 10

    def get_dvapi(self):
        return self.calc_dvapi(int(self.sd.nomenclatura), self.pii,
                               self.subpii)
    dvapi = property(get_dvapi)

    class Meta:
        unique_together = (('pii', 'subpii'))
        ordering = ['pii', 'subpii']

    def __str__(self):
        return u'%06d/%04d-%d' % (self.pii, self.subpii, self.api)

    def save(self, force_insert=False, force_update=False):
        self.subpii = self.subpii if self.subpii else 0
        self.api = self.get_dvapi()
        super(Partida, self).save(force_insert, force_update)


class PartidaDominio(models.Model):
    id = models.AutoField(primary_key=True)
    partida = models.ForeignKey(Partida)
    tomo = models.IntegerField(null=True, blank=True, default=None)
    par = models.BooleanField(default=False)
    impar = models.BooleanField(default=False)
    folio = models.IntegerField(null=True, blank=True, default=None)
    numero = models.IntegerField(null=True, blank=True, default=None)
    fecha = models.DateField(null=True, blank=True, default=None)
    fecha_inscripcion_definitiva = models.DateField(
        null=True, blank=True, default=None)

    class Meta:
        verbose_name_plural = 'partida_dominios'


class Persona(models.Model):
    id = models.AutoField(primary_key=True)
    nombres = CharNullField(max_length=100, null=True, blank=True,
                            default=None)
    apellidos = CharNullField(max_length=100)
    nombres_alternativos = CharNullField(
        max_length=100, null=True, blank=True, default=None)
    apellidos_alternativos = CharNullField(
        max_length=100, null=True, blank=True, default=None)
    domicilio = CharNullField(
        max_length=50, null=True, blank=True, default=None)
    lugar = models.ForeignKey(Lugar, null=True, blank=True, default=None)
    telefono = CharNullField(max_length=20, null=True, blank=True,
                             default=None)
    celular = CharNullField(max_length=20, null=True, blank=True, default=None)
    email = EmailNullField(
        max_length=50, unique=True, null=True, blank=True, default=None)
    cuit_cuil = CharNullField(
        max_length=14, unique=True, null=True, blank=True, default=None,
        verbose_name='CUIT/CUIL/CDI')
    TIPO_DOC = ((0, 'DNI'), (1, 'LC'), (2, 'LE'), (3, 'Otro'))
    tipo_doc = models.SmallIntegerField(
        null=True, blank=True, choices=TIPO_DOC, default=None)
    documento = models.IntegerField(
        unique=True, null=True, blank=True, default=None)

    def get_absolute_url(self):
        return reverse('persona', kwargs={'pk': str(self.id)})

    def nombre_completo(self):
        return (u'%s %s' % (self.apellidos, self.nombres)).strip()

    def show_tipo_doc(self):
        if self.tipo_doc != '' and self.tipo_doc is not None:
            return self.TIPO_DOC[self.tipo_doc][1]
    show_tipo_doc.short_description = 'Tipo doc'
    show_tipo_doc.admin_order_field = 'tipo_doc'

    class Meta:
        ordering = ['apellidos', 'nombres']

    def __str__(self):
        return self.nombre_completo()

    def save(self, force_insert=False, force_update=False):
        self.apellidos = self.apellidos.upper().strip()
        self.apellidos_alternativos = self.apellidos_alternativos.upper().strip()
        self.nombres = CapitalizePhrase(self.nombres)
        self.nombres_alternativos = CapitalizePhrase(self.nombres_alternativos)
        super(Persona, self).save(force_insert, force_update)


class Profesional(models.Model):
    id = models.AutoField(primary_key=True)
    nombres = CharNullField(max_length=50)
    apellidos = CharNullField(max_length=50)
    titulo = models.ForeignKey('Titulo', null=True, blank=True, default=None)
    icopa = CharNullField(max_length=8, null=True, blank=True, default=None)
    domicilio = CharNullField(
        max_length=50, null=True, blank=True, default=None)
    lugar = models.ForeignKey(Lugar, null=True, blank=True, default=None)
    telefono = CharNullField(
        max_length=20, null=True, blank=True, default=None)
    celular = CharNullField(max_length=20, null=True, blank=True, default=None)
    web = URLNullField(max_length=50, null=True, blank=True, default=None)
    email = EmailNullField(
        max_length=50, unique=True, null=True, blank=True, default=None)
    cuit_cuil = CharNullField(
        max_length=14, unique=True, null=True, blank=True, default=None,
        verbose_name='DNI/CUIT/CUIL/CDI')
    habilitado = models.BooleanField(default=True)
    jubilado = models.BooleanField(default=False)
    fallecido = models.BooleanField(default=False)

    def nombre_completo(self):
        return u'%s %s' % (self.apellidos, self.nombres)

    class Meta:
        verbose_name_plural = 'profesionales'
        ordering = ['apellidos', 'nombres']

    def __str__(self):
        return u'%s %s' % (self.apellidos, self.nombres)

    def save(self, force_insert=False, force_update=False):
        self.apellidos = self.apellidos.upper().strip()
        self.nombres = CapitalizePhrase(self.nombres)
        super(Profesional, self).save(force_insert, force_update)


class Titulo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = CharNullField(max_length=30)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Zona(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = CharNullField(max_length=50)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return u'%d' % self.id
