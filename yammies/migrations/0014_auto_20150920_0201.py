# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('yammies', '0013_mod_changelog'),
    ]

    operations = [
        migrations.AddField(
            model_name='jsonservice',
            name='editors',
            field=models.ManyToManyField(related_name='edit_services', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='jsonservice',
            name='open_for_all',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='jsonservice',
            name='owner',
            field=models.ForeignKey(related_name='owned_services', to=settings.AUTH_USER_MODEL),
        ),
    ]
