# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('yammies', '0011_auto_20150604_1649'),
    ]

    operations = [
        migrations.AddField(
            model_name='jsonservice',
            name='owner',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mod',
            name='created_by',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='jsonservice',
            name='json_name',
            field=models.SlugField(help_text=b'Base name for json file', unique=True),
        ),
        migrations.AlterField(
            model_name='jsonservice',
            name='torrent_announce',
            field=models.CharField(default=b'udp://open.demonii.com:1337', max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='jsonservice',
            name='torrent_enable',
            field=models.BooleanField(default=False, help_text=b'Enable torrent gereration for mods connected to this service'),
        ),
        migrations.AlterField(
            model_name='jsonservice',
            name='torrent_minimum_bytes',
            field=models.PositiveIntegerField(default=5242880, help_text=b'Minimum size to generate a torrent for the mod'),
        ),
        migrations.AlterField(
            model_name='jsonservice',
            name='torrent_webseeds',
            field=models.BooleanField(default=False, help_text=b'Add http link to the file in torrent. Largely unsupported, and requires at least one Host Mirror entry'),
        ),
        migrations.AlterField(
            model_name='jsonservice',
            name='verbose_json',
            field=models.BooleanField(default=True, help_text=b'Make the generated JSON file more readable. Turn off to save space'),
        ),
    ]
