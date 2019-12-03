# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gea', '0006_auto_20170206_1730'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='antecedente',
            name='plano',
        ),
        migrations.RemoveField(
            model_name='expediente',
            name='plano',
        ),
        migrations.RemoveField(
            model_name='expedientepartida',
            name='informe_catastral',
        ),
    ]
