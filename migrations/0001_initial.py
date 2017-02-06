# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import gea.models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Antecedente',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('inscripcion_numero', models.IntegerField(blank=True, null=True, default=None)),
                ('duplicado', models.BooleanField(default=False)),
                ('obs', gea.models.CharNullField(max_length=255, blank=True, null=True, default=None)),
                ('plano_ruta', gea.models.URLNullField(max_length=100, blank=True, null=True, default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Catastro',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('seccion', gea.models.CharNullField(max_length=10, blank=True, null=True, default=None)),
                ('poligono', gea.models.CharNullField(max_length=10, blank=True, null=True, default=None)),
                ('manzana', gea.models.CharNullField(max_length=10, blank=True, null=True, default=None)),
                ('parcela', gea.models.CharNullField(max_length=10, blank=True, null=True, default=None)),
                ('subparcela', gea.models.CharNullField(max_length=10, blank=True, null=True, default=None)),
            ],
        ),
        migrations.CreateModel(
            name='CatastroLocal',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('seccion', gea.models.CharNullField(max_length=20, blank=True, null=True, default=None)),
                ('manzana', gea.models.CharNullField(max_length=20, blank=True, null=True, default=None)),
                ('parcela', gea.models.CharNullField(max_length=20, blank=True, null=True, default=None)),
                ('subparcela', gea.models.CharNullField(max_length=20, blank=True, null=True, default=None)),
                ('suburbana', models.BooleanField(default=False)),
                ('poligono', gea.models.CharNullField(max_length=20, blank=True, null=True, default=None)),
            ],
            options={
                'verbose_name': 'catastro local',
                'verbose_name_plural': 'catastros locales',
            },
        ),
        migrations.CreateModel(
            name='Circunscripcion',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', gea.models.CharNullField(max_length=10)),
                ('orden', gea.models.CharNullField(max_length=7)),
            ],
            options={
                'verbose_name_plural': 'circunscripciones',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Comprobante',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', gea.models.CharNullField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Dp',
            fields=[
                ('dp', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', gea.models.CharNullField(verbose_name='nombre depto', max_length=50)),
                ('habitantes', models.IntegerField(blank=True, null=True)),
                ('superficie', models.IntegerField(blank=True, null=True)),
                ('cabecera', gea.models.CharNullField(max_length=50, blank=True, null=True)),
                ('circunscripcion', models.ForeignKey(to='gea.Circunscripcion')),
            ],
            options={
                'verbose_name_plural': 'Departamentos',
                'ordering': ['dp'],
            },
        ),
        migrations.CreateModel(
            name='Ds',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ds', models.IntegerField()),
                ('nombre', gea.models.CharNullField(verbose_name='nombre distrito', max_length=50)),
                ('dp', models.ForeignKey(db_column='dp', to='gea.Dp')),
            ],
            options={
                'verbose_name_plural': 'distritos',
                'ordering': ['dp', 'ds'],
            },
        ),
        migrations.CreateModel(
            name='Expediente',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(verbose_name='created', auto_now_add=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(verbose_name='modified', auto_now=True)),
                ('id', models.IntegerField(verbose_name='Expediente Nº', primary_key=True, serialize=False)),
                ('fecha_plano', models.DateField(blank=True, null=True, default=None)),
                ('fecha_medicion', models.DateField(blank=True, null=True, default=None)),
                ('inscripcion_numero', models.IntegerField(verbose_name='SCIT inscripción Nº', unique=True, blank=True, null=True, default=None)),
                ('inscripcion_fecha', models.DateField(verbose_name='Fecha inscripción', blank=True, null=True, default=None)),
                ('duplicado', models.BooleanField(default=False)),
                ('orden_numero', models.IntegerField(verbose_name='CoPA Expendiente Nº', blank=True, null=True, default=None)),
                ('orden_fecha', models.DateField(verbose_name='Fecha contrato', blank=True, null=True, default=None)),
                ('sin_inscripcion', models.BooleanField(default=False)),
                ('cancelado', models.BooleanField(default=False)),
                ('cancelado_por', gea.models.CharNullField(max_length=100, blank=True, null=True, default=None)),
                ('plano_ruta', gea.models.URLNullField(max_length=100, blank=True, null=True, default=None)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ExpedienteLugar',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('expediente', models.ForeignKey(to='gea.Expediente')),
            ],
            options={
                'verbose_name': 'lugar',
                'verbose_name_plural': 'lugares',
                'ordering': ['expediente', 'lugar'],
            },
        ),
        migrations.CreateModel(
            name='ExpedienteObjeto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('expediente', models.ForeignKey(to='gea.Expediente')),
            ],
            options={
                'verbose_name': 'objeto',
                'verbose_name_plural': 'objetos',
                'ordering': ['expediente', 'objeto'],
            },
        ),
        migrations.CreateModel(
            name='ExpedientePartida',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('set_ruta', gea.models.URLNullField(max_length=100, blank=True, null=True, default=None)),
                ('expediente', models.ForeignKey(to='gea.Expediente')),
            ],
            options={
                'verbose_name': 'partida',
                'verbose_name_plural': 'partidas',
                'ordering': ['expediente', 'partida'],
            },
        ),
        migrations.CreateModel(
            name='ExpedientePersona',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('comitente', models.BooleanField(default=False)),
                ('propietario', models.BooleanField(default=True)),
                ('poseedor', models.BooleanField(default=False)),
                ('sucesor', models.BooleanField(default=False)),
                ('partes_indivisas_propias', models.IntegerField(blank=True, null=True, default=None)),
                ('partes_indivisas_total', models.IntegerField(blank=True, null=True, default=None)),
                ('sucesion', models.BooleanField(default=False)),
                ('nuda_propiedad', models.BooleanField(default=False)),
                ('usufructo', models.BooleanField(default=False)),
                ('expediente', models.ForeignKey(to='gea.Expediente')),
            ],
            options={
                'verbose_name': 'persona involucrada',
                'verbose_name_plural': 'personas involucradas',
                'ordering': ['persona__apellidos', 'persona__nombres'],
            },
        ),
        migrations.CreateModel(
            name='ExpedienteProfesional',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('expediente', models.ForeignKey(to='gea.Expediente')),
            ],
            options={
                'verbose_name': 'profesional firmante',
                'verbose_name_plural': 'profesionales firmantes',
                'ordering': ['profesional__apellidos', 'profesional__nombres'],
            },
        ),
        migrations.CreateModel(
            name='Lugar',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', gea.models.CharNullField(max_length=80)),
                ('obs', gea.models.CharNullField(max_length=255, blank=True, null=True, default=None)),
            ],
            options={
                'verbose_name_plural': 'lugares',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Objeto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', gea.models.CharNullField(max_length=80)),
            ],
            options={
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('comprobante_nro', models.IntegerField(blank=True, null=True, default=None)),
                ('fecha', models.DateField(blank=True, null=True, default=None)),
                ('monto', models.DecimalField(max_digits=8, decimal_places=2)),
                ('porcentaje', models.DecimalField(max_digits=5, decimal_places=2)),
                ('obs', gea.models.CharNullField(max_length=255, blank=True, null=True, default=None)),
                ('comprobante', models.ForeignKey(to='gea.Comprobante')),
            ],
        ),
        migrations.CreateModel(
            name='Partida',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('pii', models.IntegerField()),
                ('subpii', models.IntegerField()),
                ('api', models.SmallIntegerField(blank=True, null=True, default=0)),
            ],
            options={
                'ordering': ['pii', 'subpii'],
            },
        ),
        migrations.CreateModel(
            name='PartidaDominio',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tomo', models.IntegerField(blank=True, null=True, default=None)),
                ('par', models.BooleanField(default=False)),
                ('impar', models.BooleanField(default=False)),
                ('folio', models.IntegerField(blank=True, null=True, default=None)),
                ('numero', models.IntegerField(blank=True, null=True, default=None)),
                ('fecha', models.DateField(blank=True, null=True, default=None)),
                ('fecha_inscripcion_definitiva', models.DateField(blank=True, null=True, default=None)),
                ('partida', models.ForeignKey(to='gea.Partida')),
            ],
            options={
                'verbose_name_plural': 'partida_dominios',
            },
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombres', gea.models.CharNullField(max_length=100, blank=True, null=True, default=None)),
                ('apellidos', gea.models.CharNullField(max_length=100)),
                ('nombres_alternativos', gea.models.CharNullField(max_length=100, blank=True, null=True, default=None)),
                ('apellidos_alternativos', gea.models.CharNullField(max_length=100, blank=True, null=True, default=None)),
                ('domicilio', gea.models.CharNullField(max_length=50, blank=True, null=True, default=None)),
                ('telefono', gea.models.CharNullField(max_length=20, blank=True, null=True, default=None)),
                ('celular', gea.models.CharNullField(max_length=20, blank=True, null=True, default=None)),
                ('email', gea.models.EmailNullField(max_length=50, unique=True, blank=True, null=True, default=None)),
                ('cuit_cuil', gea.models.CharNullField(verbose_name='CUIT/CUIL/CDI', max_length=14, unique=True, blank=True, null=True, default=None)),
                ('tipo_doc', models.SmallIntegerField(blank=True, null=True, default=None, choices=[(0, 'DNI'), (1, 'LC'), (2, 'LE'), (3, 'Otro')])),
                ('documento', models.IntegerField(unique=True, blank=True, null=True, default=None)),
                ('lugar', models.ForeignKey(blank=True, null=True, default=None, to='gea.Lugar')),
            ],
            options={
                'ordering': ['apellidos', 'nombres'],
            },
        ),
        migrations.CreateModel(
            name='Presupuesto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('monto', models.DecimalField(max_digits=8, decimal_places=2)),
                ('fecha', models.DateField()),
                ('porcentaje_cancelado', models.DecimalField(verbose_name='% cancelado', max_digits=5, decimal_places=2)),
                ('obs', gea.models.CharNullField(max_length=255, blank=True, null=True, default=None)),
                ('expediente', models.ForeignKey(to='gea.Expediente')),
            ],
            options={
                'ordering': ['expediente'],
            },
        ),
        migrations.CreateModel(
            name='Profesional',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombres', gea.models.CharNullField(max_length=50)),
                ('apellidos', gea.models.CharNullField(max_length=50)),
                ('icopa', gea.models.CharNullField(max_length=8, blank=True, null=True, default=None)),
                ('domicilio', gea.models.CharNullField(max_length=50, blank=True, null=True, default=None)),
                ('telefono', gea.models.CharNullField(max_length=20, blank=True, null=True, default=None)),
                ('celular', gea.models.CharNullField(max_length=20, blank=True, null=True, default=None)),
                ('web', gea.models.URLNullField(max_length=50, blank=True, null=True, default=None)),
                ('email', gea.models.EmailNullField(max_length=50, unique=True, blank=True, null=True, default=None)),
                ('cuit_cuil', gea.models.CharNullField(verbose_name='DNI/CUIT/CUIL/CDI', max_length=14, unique=True, blank=True, null=True, default=None)),
                ('habilitado', models.BooleanField(default=True)),
                ('jubilado', models.BooleanField(default=False)),
                ('fallecido', models.BooleanField(default=False)),
                ('lugar', models.ForeignKey(blank=True, null=True, default=None, to='gea.Lugar')),
            ],
            options={
                'verbose_name_plural': 'profesionales',
                'ordering': ['apellidos', 'nombres'],
            },
        ),
        migrations.CreateModel(
            name='Sd',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sd', models.IntegerField()),
                ('nombre', gea.models.CharNullField(verbose_name='nombre subdistrito', max_length=50, blank=True, null=True, default=None)),
                ('ds', models.ForeignKey(db_column='ds', to='gea.Ds')),
            ],
            options={
                'verbose_name_plural': 'subdistritos',
                'ordering': ['ds', 'sd'],
            },
        ),
        migrations.CreateModel(
            name='Titulo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', gea.models.CharNullField(max_length=30)),
            ],
            options={
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Zona',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('descripcion', gea.models.CharNullField(max_length=50)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='profesional',
            name='titulo',
            field=models.ForeignKey(blank=True, null=True, default=None, to='gea.Titulo'),
        ),
        migrations.AddField(
            model_name='partida',
            name='sd',
            field=models.ForeignKey(blank=True, null=True, default=None, db_column='sd', to='gea.Sd'),
        ),
        migrations.AddField(
            model_name='pago',
            name='presupuesto',
            field=models.ForeignKey(to='gea.Presupuesto'),
        ),
        migrations.AddField(
            model_name='expedienteprofesional',
            name='profesional',
            field=models.ForeignKey(to='gea.Profesional'),
        ),
        migrations.AddField(
            model_name='expedientepersona',
            name='persona',
            field=models.ForeignKey(to='gea.Persona'),
        ),
        migrations.AddField(
            model_name='expedientepartida',
            name='partida',
            field=models.ForeignKey(to='gea.Partida'),
        ),
        migrations.AddField(
            model_name='expedienteobjeto',
            name='objeto',
            field=models.ForeignKey(to='gea.Objeto'),
        ),
        migrations.AddField(
            model_name='expedientelugar',
            name='lugar',
            field=models.ForeignKey(to='gea.Lugar'),
        ),
        migrations.AddField(
            model_name='catastrolocal',
            name='expediente_lugar',
            field=models.ForeignKey(to='gea.ExpedienteLugar'),
        ),
        migrations.AddField(
            model_name='catastro',
            name='expediente_partida',
            field=models.ForeignKey(to='gea.ExpedientePartida'),
        ),
        migrations.AddField(
            model_name='catastro',
            name='zona',
            field=models.ForeignKey(blank=True, null=True, default=None, db_column='zona', to='gea.Zona'),
        ),
        migrations.AddField(
            model_name='antecedente',
            name='expediente',
            field=models.ForeignKey(blank=True, null=True, default=None, to='gea.Expediente'),
        ),
        migrations.AddField(
            model_name='antecedente',
            name='expediente_modificado',
            field=models.ForeignKey(blank=True, null=True, default=None, related_name='expediente_modificado', to='gea.Expediente'),
        ),
        migrations.AlterUniqueTogether(
            name='partida',
            unique_together=set([('pii', 'subpii')]),
        ),
    ]
