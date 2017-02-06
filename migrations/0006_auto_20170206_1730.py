# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import gea.models


class Migration(migrations.Migration):

    dependencies = [
        ('gea', '0005_auto_20170203_1943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='antecedente',
            name='obs',
            field=gea.models.CharNullField(verbose_name='Observaciones', max_length=255, blank=True, null=True, default=None),
        ),
        migrations.AlterField(
            model_name='lugar',
            name='obs',
            field=gea.models.CharNullField(verbose_name='Observaciones', max_length=255, blank=True, null=True, default=None),
        ),
        migrations.AlterField(
            model_name='pago',
            name='obs',
            field=gea.models.CharNullField(verbose_name='Observaciones', max_length=255, blank=True, null=True, default=None),
        ),
        migrations.AlterField(
            model_name='presupuesto',
            name='obs',
            field=gea.models.CharNullField(verbose_name='Observaciones', max_length=255, blank=True, null=True, default=None),
        ),
    ]
