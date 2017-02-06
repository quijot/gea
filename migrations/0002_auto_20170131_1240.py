# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gea', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='expediente',
            name='plano',
            field=models.FileField(blank=True, null=True, default=None, upload_to='planos'),
        ),
        migrations.AddField(
            model_name='expedientepartida',
            name='informe_catastral',
            field=models.FileField(blank=True, null=True, default=None, upload_to='set'),
        ),
    ]
