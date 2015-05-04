# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yammies', '0002_auto_20150504_2220'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HostMirrors',
            new_name='HostMirror',
        ),
    ]
