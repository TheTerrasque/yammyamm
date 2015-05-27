# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import yammies.models


class Migration(migrations.Migration):

    dependencies = [
        ('yammies', '0007_auto_20150523_1832'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jsonservice',
            name='jsonpath',
        ),
        migrations.AddField(
            model_name='jsonservice',
            name='json_file',
            field=models.FileField(storage=yammies.models.OverwriteStorage(), null=True, upload_to=b'service', blank=True),
        ),
        migrations.AddField(
            model_name='jsonservice',
            name='json_name',
            field=models.SlugField(default='default', unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mod',
            name='long_description',
            field=models.TextField(blank=True),
        ),
    ]
