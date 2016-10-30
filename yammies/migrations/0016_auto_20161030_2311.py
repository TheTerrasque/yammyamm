# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def create_modversion(apps, schema_editor):
    Mod = apps.get_model("yammies", "Mod")
    ModVersion = apps.get_model("yammies", "ModVersion")
    for mod in Mod.objects.all():
        mv = ModVersion()
        mv.mod = mod
        mv.archive = mod.archive
        mv.version = mod.version
        mv.changelog = mod.changelog
        mv.filesize = mod.filesize
        mv.filehas = mod.filehash
        mv.torrent_file = mod.torrent_file
        mv.torrent_magnet = mod.torrent_magnet
        mv.save()
    

class Migration(migrations.Migration):

    dependencies = [
        ('yammies', '0015_modversion'),
    ]

    operations = [
        migrations.RunPython(create_modversion),
    ]
