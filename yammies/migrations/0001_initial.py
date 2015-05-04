# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HostMirrors',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Mod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, db_index=True)),
                ('version', models.CharField(max_length=30)),
                ('archive', models.FileField(upload_to=b'files')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(blank=True)),
                ('filesize', models.IntegerField(default=0)),
                ('filehash', models.CharField(max_length=90, null=True, blank=True)),
                ('homepage', models.CharField(max_length=200, null=True, blank=True)),
                ('author', models.CharField(max_length=60, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ModCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='ModDependency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dependency', models.CharField(max_length=30, db_index=True)),
                ('relation', models.IntegerField(default=0, choices=[(0, b'Requires'), (1, b'Provides'), (2, b'Conflicts'), (3, b'Recommends')])),
                ('mod', models.ForeignKey(to='yammies.Mod')),
            ],
        ),
        migrations.AddField(
            model_name='mod',
            name='category',
            field=models.ForeignKey(to='yammies.ModCategory'),
        ),
    ]
