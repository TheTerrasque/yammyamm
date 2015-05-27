# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yammies', '0008_auto_20150528_0105'),
    ]

    operations = [
        migrations.AddField(
            model_name='jsonservice',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='mod',
            name='archive',
            field=models.FileField(null=True, upload_to=b'mods', blank=True),
        ),
    ]
