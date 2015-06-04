# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yammies', '0010_auto_20150530_1529'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jsonservice',
            name='torrent_link',
        ),
        migrations.AddField(
            model_name='jsonservice',
            name='torrent_path',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
