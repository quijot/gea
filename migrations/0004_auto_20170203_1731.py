# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gea', '0003_expediente_planoff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expediente',
            name='planoff',
        ),
        migrations.AlterField(
            model_name='expediente',
            name='plano',
            field=filebrowser.fields.FileBrowseField(verbose_name='Plano', max_length=200, blank=True, null=True),
        ),
    ]
