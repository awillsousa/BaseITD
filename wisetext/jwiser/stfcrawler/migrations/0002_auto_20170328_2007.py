# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-28 20:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stfcrawler', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acordao',
            name='URL_dj_dj3',
            field=models.URLField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='acordao',
            name='inteiro_teor',
            field=models.URLField(blank=True, max_length=100),
        ),
    ]
