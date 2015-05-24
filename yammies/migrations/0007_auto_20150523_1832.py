# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yammies', '0006_auto_20150517_2257'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mod',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='jsonservice',
            name='torrent_announce',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='jsonservice',
            name='torrent_enable',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='mod',
            name='torrent_file',
            field=models.FileField(null=True, upload_to=b'torrents', blank=True),
        ),
        migrations.AddField(
            model_name='mod',
            name='torrent_magnet',
            field=models.TextField(blank=True),
        ),
    ]
