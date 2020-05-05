from django.db import models
from django.urls import reverse
from django_extensions.db.models import TimeStampedModel


def CapitalizePhrase(string):
    phrase = ""
    for word in string.split():
        phrase = f"{phrase} {word[0].upper()}{word[1:].lower()}"
    return phrase.strip()


class Antecedente(models.Model):
    expediente = models.ForeignKey("Expediente", on_delete=models.CASCADE)
    expediente_modificado = models.ForeignKey(
        "Expediente", related_name="expediente_modificado", on_delete=models.CASCADE
    )
    inscripcion_numero = models.IntegerField()
    duplicado = models.BooleanField(default=False)
    observacion = models.CharField(max_length=255)
    plano_ruta = models.URLField(max_length=100)
    # plano = FileBrowseField(
    #     "Enlace al plano", max_length=200, directory="planos/", extensions=[".pdf"],
    # )


class Catastro(models.Model):
    expediente_partida = models.ForeignKey(
        "ExpedientePartida", on_delete=models.CASCADE
    )
    zona = models.ForeignKey("Zona", on_delete=models.CASCADE)
    seccion = models.CharField(max_length=10)
    poligono = models.CharField(max_length=10)
    manzana = models.CharField(max_length=10)
    parcela = models.CharField(max_length=10)
    subparcela = models.CharField(max_length=10)

    def __str__(self):
        if self.zona in (1, 2, 3):
            return f"Z:{self.zona} - S:{self.seccion} - M:{self.manzana} - P:{self.parcela}"
        elif self.zona in (4, 5):
            return f"Z:{self.zona} - Pol:{self.poligono} - P:{self.parcela}"
        else:
            return ""


class CatastroLocal(models.Model):
    expediente_lugar = models.ForeignKey("ExpedienteLugar", on_delete=models.CASCADE)
    seccion = models.CharField(max_length=20, blank=True)
    manzana = models.CharField(max_length=20, blank=True)
    parcela = models.CharField(max_length=20, blank=True)
    subparcela = models.CharField(max_length=20, blank=True)
    suburbana = models.BooleanField(default=False)
    poligono = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = "catastro local"
        verbose_name_plural = "catastros locales"

    def __str__(self):
        return f"S:{self.seccion} - M:{self.manzana} - P:{self.parcela}"


class Circunscripcion(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=10)
    orden = models.CharField(max_length=7)

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "circunscripciones"

    def __str__(self):
        return self.nombre


class Comprobante(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Presupuesto(models.Model):
    expediente = models.ForeignKey("Expediente", on_delete=models.PROTECT)
    monto = models.DecimalField(max_digits=8, decimal_places=2)
    fecha = models.DateField()
    porcentaje_cancelado = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="% cancelado"
    )
    observacion = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["expediente"]

    def __str__(self):
        return f"{self.expediente} - ${self.monto:.2f} - {self.fecha}"


class Pago(models.Model):
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.PROTECT)
    comprobante = models.ForeignKey(Comprobante, on_delete=models.PROTECT)
    comprobante_nro = models.IntegerField()
    fecha = models.DateField()
    monto = models.DecimalField(max_digits=8, decimal_places=2)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2)
    observacion = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.porcentaje}% - {self.fecha}"


class Dp(models.Model):
    dp = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50, verbose_name="nombre depto")
    habitantes = models.IntegerField(blank=True)
    superficie = models.IntegerField(blank=True)
    cabecera = models.CharField(max_length=50, blank=True)
    circunscripcion = models.ForeignKey(Circunscripcion, on_delete=models.PROTECT)

    def departamento(self):
        return f"{self.dp:02d} {self.nombre}"

    class Meta:
        verbose_name_plural = "Departamentos"
        ordering = ["dp"]

    def __str__(self):
        return f"{self.dp:02d}"


class Ds(models.Model):
    id = models.AutoField(primary_key=True)
    # dp = models.ForeignKey(Dp, db_column="dp", on_delete=models.PROTECT)
    dp = models.ForeignKey(Dp, on_delete=models.PROTECT)
    ds = models.IntegerField()
    nombre = models.CharField(max_length=50, verbose_name="nombre distrito")

    @property
    def distrito(self):
        return f"{self.ds:02d}"

    class Meta:
        verbose_name_plural = "distritos"
        ordering = ["dp", "ds"]

    def __str__(self):
        return f"{self.ds:02d}"


class Sd(models.Model):
    id = models.AutoField(primary_key=True)
    ds = models.ForeignKey(Ds, db_column="ds", on_delete=models.PROTECT)
    sd = models.IntegerField()
    nombre = models.CharField(
        max_length=50, blank=True, verbose_name="nombre subdistrito",
    )

    @property
    def subdistrito(self):
        return f"{self.sd:02d}"

    @property
    def dp(self):
        return self.ds.dp

    @property
    def dp_nombre(self):
        return self.ds.dp.nombre

    @property
    def ds_nombre(self):
        return self.ds.nombre

    class Meta:
        verbose_name_plural = "subdistritos"
        ordering = ["ds", "sd"]

    def __str__(self):
        return f"{self.ds.dp}{self.ds}{self.sd:02d}"

    nomenclatura = property(__str__)


class Lugar(models.Model):
    nombre = models.CharField(max_length=80)
    observacion = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = "lugares"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Objeto(models.Model):
    nombre = models.CharField(max_length=80)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Titulo(models.Model):
    nombre = models.CharField(max_length=30)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Profesional(models.Model):
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    titulo = models.ForeignKey(
        Titulo, null=True, default=None, on_delete=models.SET_NULL
    )
    icopa = models.CharField("ICoPA", max_length=8, blank=True)
    domicilio = models.CharField(max_length=50, blank=True)
    lugar = models.ForeignKey(Lugar, null=True, default=None, on_delete=models.SET_NULL)
    telefono = models.CharField(max_length=20, blank=True)
    celular = models.CharField(max_length=20, blank=True)
    web = models.URLField(max_length=50, blank=True)
    email = models.EmailField(max_length=50, blank=True)
    cuit_cuil = models.CharField(
        max_length=14, blank=True, verbose_name="CUIT/CUIL/CDI",
    )
    habilitado = models.BooleanField(default=True)
    jubilado = models.BooleanField(default=False)
    fallecido = models.BooleanField(default=False)

    @property
    def nombre_completo(self):
        return f"{self.apellidos} {self.nombres}"

    class Meta:
        verbose_name_plural = "profesionales"
        ordering = ["apellidos", "nombres"]

    def __str__(self):
        return self.nombre_completo

    def save(self, *args, **kwargs):
        self.apellidos = self.apellidos.upper().strip()
        self.nombres = CapitalizePhrase(self.nombres)
        super().save(*args, **kwargs)


class Expediente(TimeStampedModel):
    id = models.IntegerField("Expediente Nº", primary_key=True)
    fecha_plano = models.DateField(blank=True, null=True)
    fecha_medicion = models.DateField(blank=True, null=True)
    inscripcion_numero = models.IntegerField(
        "SCIT inscripción Nº", unique=True, blank=True, null=True
    )
    inscripcion_fecha = models.DateField("Fecha inscripción", blank=True, null=True)
    duplicado = models.BooleanField(default=False)
    orden_numero = models.IntegerField("CoPA Expendiente Nº", blank=True, null=True)
    orden_fecha = models.DateField("Fecha contrato", blank=True, null=True)
    sin_inscripcion = models.BooleanField(default=False)
    cancelado = models.BooleanField(default=False)
    cancelado_por = models.CharField(max_length=100, blank=True)
    plano_ruta = models.URLField(max_length=100, blank=True)
    # plano = FileBrowseField(
    #     "Enlace al plano",
    #     max_length=200,
    #     directory="planos/",
    #     extensions=[".pdf"],
    # )
    objetos = models.ManyToManyField(Objeto)
    profesionales_firmantes = models.ManyToManyField(Profesional)

    def get_absolute_url(self):
        return reverse("expediente", kwargs={"pk": str(self.id)})

    def inscripto(self):
        return self.inscripcion_numero != 0

    def propietarios_count(self):
        """Devuelve la cantidad de personas que figuran como propietarias."""
        return self.expedientepersona_set.filter(propietario=True).count()

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.id}"


class ExpedienteLugar(models.Model):
    expediente = models.ForeignKey(Expediente, on_delete=models.CASCADE)
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "lugar"
        verbose_name_plural = "lugares"
        ordering = ["expediente", "lugar"]

    def __str__(self):
        return self.lugar.nombre


class ExpedientePartida(models.Model):
    expediente = models.ForeignKey(Expediente, on_delete=models.CASCADE)
    partida = models.ForeignKey("Partida", on_delete=models.CASCADE)
    set_ruta = models.URLField(max_length=100, blank=True)
    # informe_catastral = FileBrowseField(
    #     max_length=200,
    #     directory="set/",
    #     extensions=[".pdf"],
    # )

    class Meta:
        verbose_name = "partida"
        verbose_name_plural = "partidas"
        ordering = ["expediente", "partida"]

    def __str__(self):
        return f"{self.partida}"


class ExpedientePersona(models.Model):
    expediente = models.ForeignKey(Expediente, on_delete=models.CASCADE)
    persona = models.ForeignKey("Persona", on_delete=models.CASCADE)
    comitente = models.BooleanField(default=False)
    propietario = models.BooleanField(default=True)
    poseedor = models.BooleanField(default=False)
    sucesor = models.BooleanField(default=False)
    partes_indivisas_propias = models.IntegerField(blank=True)
    partes_indivisas_total = models.IntegerField(blank=True)
    sucesion = models.BooleanField(default=False)
    nuda_propiedad = models.BooleanField(default=False)
    usufructo = models.BooleanField(default=False)

    class Meta:
        verbose_name = "persona involucrada"
        verbose_name_plural = "personas involucradas"
        ordering = ["persona__apellidos", "persona__nombres"]

    def __str__(self):
        return f"{self.expediente.id} - {self.persona.apellidos} {self.persona.nombres}"


class Partida(models.Model):
    sd = models.ForeignKey(
        "Sd", db_column="sd", null=True, default=None, on_delete=models.SET_NULL
    )
    pii = models.IntegerField()
    subpii = models.IntegerField()
    api = models.SmallIntegerField()

    @property
    def partida(self):
        return f"{self.pii:06d}/{self.subpii:04d}-{self.api}"

    @property
    def partida_completa(self):
        return f"{self.sd}-{self.partida}"

    def calc_dvapi(self, sd, pii, subpii=0):
        coef = "9731"
        _coef = coef + coef + coef + coef
        strpii = "%06d%06d%04d" % (sd, pii, subpii)
        suma = 0
        for i in range(0, len(strpii)):
            m = str(int(strpii[i]) * int(_coef[i]))
            suma += int(m[len(m) - 1])
        return (10 - (suma % 10)) % 10

    def get_dvapi(self):
        return self.calc_dvapi(int(self.sd.nomenclatura), self.pii, self.subpii)

    dvapi = property(get_dvapi)

    class Meta:
        unique_together = ("pii", "subpii")
        ordering = ["pii", "subpii"]

    def __str__(self):
        return self.partida

    def save(self, *args, **kwargs):
        self.subpii = self.subpii if self.subpii else 0
        self.api = self.get_dvapi()
        super().save(*args, **kwargs)


class PartidaDominio(models.Model):
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE)
    tomo = models.IntegerField(blank=True)
    par = models.BooleanField(default=False)
    impar = models.BooleanField(default=False)
    folio = models.IntegerField(blank=True)
    numero = models.IntegerField(blank=True)
    fecha = models.DateField(blank=True)
    fecha_inscripcion_definitiva = models.DateField(blank=True)

    class Meta:
        verbose_name_plural = "partida_dominios"


class Persona(models.Model):
    nombres = models.CharField(max_length=100, blank=True)
    apellidos = models.CharField(max_length=100)
    nombres_alternativos = models.CharField(max_length=100, blank=True)
    apellidos_alternativos = models.CharField(max_length=100, blank=True)
    domicilio = models.CharField(max_length=50, blank=True)
    lugar = models.ForeignKey(Lugar, null=True, default=None, on_delete=models.SET_NULL)
    telefono = models.CharField(max_length=20, blank=True)
    celular = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=50, blank=True)
    cuit_cuil = models.CharField(
        max_length=14,
        unique=True,
        blank=True,
        null=True,
        default=None,
        verbose_name="CUIT/CUIL/CDI",
    )
    TIPO_DOC = ((0, "DNI"), (1, "LC"), (2, "LE"), (3, "Otro"))
    tipo_doc = models.SmallIntegerField(blank=True, choices=TIPO_DOC)
    documento = models.IntegerField(unique=True, blank=True, default=None)

    def get_absolute_url(self):
        return reverse("persona", kwargs={"pk": str(self.id)})

    @property
    def nombre_completo(self):
        return f"{self.apellidos} {self.nombres}"

    def show_tipo_doc(self):
        if self.tipo_doc != "" and self.tipo_doc is not None:
            return self.TIPO_DOC[self.tipo_doc][1]

    show_tipo_doc.short_description = "Tipo doc"
    show_tipo_doc.admin_order_field = "tipo_doc"

    class Meta:
        ordering = ["apellidos", "nombres"]

    def __str__(self):
        return self.nombre_completo

    def save(self, *args, **kwargs):
        self.apellidos = self.apellidos.upper().strip()
        self.apellidos_alternativos = self.apellidos_alternativos.upper().strip()
        self.nombres = CapitalizePhrase(self.nombres)
        self.nombres_alternativos = CapitalizePhrase(self.nombres_alternativos)
        super().save(*args, **kwargs)


class Zona(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=50)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.id}"
