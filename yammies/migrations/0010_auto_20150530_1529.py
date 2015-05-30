# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import yammies.models


class Migration(migrations.Migration):

    dependencies = [
        ('yammies', '0009_auto_20150528_0119'),
    ]

    operations = [
        migrations.CreateModel(
            name='JsonServiceSuggestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
            ],
        ),
        migrations.AddField(
            model_name='jsonservice',
            name='torrent_link',
            field=models.CharField(blank=True, max_length=2, null=True, choices=[(b'T', b'Torrent file'), (b'M', b'Magnet link (infohash)')]),
        ),
        migrations.AddField(
            model_name='jsonservice',
            name='torrent_minimum_bytes',
            field=models.PositiveIntegerField(default=1048576),
        ),
        migrations.AddField(
            model_name='jsonservice',
            name='torrent_webseeds',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='mod',
            name='archive',
            field=models.FileField(storage=yammies.models.OverwriteStorage(), null=True, upload_to=b'mods', blank=True),
        ),
        migrations.AlterField(
            model_name='mod',
            name='torrent_file',
            field=models.FileField(storage=yammies.models.OverwriteStorage(), null=True, upload_to=b'torrents', blank=True),
        ),
        migrations.AddField(
            model_name='jsonservicesuggestion',
            name='service',
            field=models.ForeignKey(to='yammies.JsonService'),
        ),
    ]
