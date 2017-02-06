# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gea', '0002_auto_20170131_1240'),
    ]

    operations = [
        migrations.AddField(
            model_name='expediente',
            name='planoff',
            field=filebrowser.fields.FileBrowseField(verbose_name='PDF', max_length=200, blank=True, null=True),
        ),
    ]
