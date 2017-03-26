# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-25 16:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Band',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('origin', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='owned_record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_date', models.DateField(default=django.utils.timezone.now)),
                ('disc_type', models.CharField(choices=[('vinyl', 'Vinyl Disc'), ('cd', 'CD')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('release_year', models.DateField()),
                ('band_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Band')),
                ('genre_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Genre')),
                ('label_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Label')),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('number', models.IntegerField(default=0)),
                ('length', models.TimeField()),
                ('record_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Record')),
            ],
        ),
        migrations.AddField(
            model_name='owned_record',
            name='record',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Record'),
        ),
    ]