# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yammies', '0012_auto_20150821_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='mod',
            name='changelog',
            field=models.TextField(blank=True),
        ),
    ]
