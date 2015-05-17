# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yammies', '0003_auto_20150504_2252'),
    ]

    operations = [
        migrations.CreateModel(
            name='JsonService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jsonpath', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('verbose_json', models.BooleanField(default=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AlterField(
            model_name='mod',
            name='archive',
            field=models.FileField(null=True, upload_to=b'files', blank=True),
        ),
    ]
