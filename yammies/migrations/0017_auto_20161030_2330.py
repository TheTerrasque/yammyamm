# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yammies', '0016_auto_20161030_2311'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mod',
            name='archive',
        ),
        migrations.RemoveField(
            model_name='mod',
            name='changelog',
        ),
        migrations.RemoveField(
            model_name='mod',
            name='filehash',
        ),
        migrations.RemoveField(
            model_name='mod',
            name='filesize',
        ),
        migrations.RemoveField(
            model_name='mod',
            name='torrent_file',
        ),
        migrations.RemoveField(
            model_name='mod',
            name='torrent_magnet',
        ),
        migrations.RemoveField(
            model_name='mod',
            name='version',
        ),
    ]
