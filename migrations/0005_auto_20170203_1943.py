# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gea', '0004_auto_20170203_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='antecedente',
            name='plano',
            field=filebrowser.fields.FileBrowseField(verbose_name='Enlace al plano', max_length=200, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='expediente',
            name='plano',
            field=filebrowser.fields.FileBrowseField(verbose_name='Enlace al plano', max_length=200, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='expedientepartida',
            name='informe_catastral',
            field=filebrowser.fields.FileBrowseField(max_length=200, blank=True, null=True),
        ),
    ]
