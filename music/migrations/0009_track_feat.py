# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-05 17:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0008_auto_20170403_1926'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='feat',
            field=models.ManyToManyField(to='music.Band'),
        ),
    ]
