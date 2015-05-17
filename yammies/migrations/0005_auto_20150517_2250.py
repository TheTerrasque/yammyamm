# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def crate_service(apps, schema_editor):
    JsonService = apps.get_model("yammies", "JsonService")
    JsonService.objects.create(jsonpath="models.json", name="Default Service", active=False)

class Migration(migrations.Migration):

    dependencies = [
        ('yammies', '0004_auto_20150517_2248'),
    ]

    operations = [
        migrations.RunPython(crate_service),
    ]
