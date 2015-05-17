# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yammies', '0005_auto_20150517_2250'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostmirror',
            name='service',
            field=models.ForeignKey(default=1, to='yammies.JsonService'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mod',
            name='service',
            field=models.ForeignKey(default=1, to='yammies.JsonService'),
            preserve_default=False,
        ),
    ]
