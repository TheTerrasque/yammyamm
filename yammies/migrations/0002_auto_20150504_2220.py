# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yammies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostmirrors',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='mod',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
