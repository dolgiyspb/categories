# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-30 12:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories_app', '0003_auto_20171130_0704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
