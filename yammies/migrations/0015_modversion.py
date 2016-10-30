# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import yammies.models


class Migration(migrations.Migration):

    dependencies = [
        ('yammies', '0014_auto_20150920_0201'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('archive', models.FileField(storage=yammies.models.OverwriteStorage(), null=True, upload_to=b'mods', blank=True)),
                ('releasetype', models.IntegerField(default=0, choices=[(0, b'Release'), (1, b'Beta'), (2, b'Testing'), (3, b'Experimental'), (1, b'Alpha')])),
                ('updated', models.DateTimeField(auto_now=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('changelog', models.TextField(blank=True)),
                ('version', models.CharField(max_length=30)),
                ('filesize', models.IntegerField(default=0)),
                ('filehash', models.CharField(max_length=90, null=True, blank=True)),
                ('torrent_file', models.FileField(storage=yammies.models.OverwriteStorage(), null=True, upload_to=b'torrents', blank=True)),
                ('torrent_magnet', models.TextField(blank=True)),
                ('mod', models.ForeignKey(to='yammies.Mod')),
            ],
        ),
    ]
