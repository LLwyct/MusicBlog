# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-24 10:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_like'),
    ]

    operations = [
        migrations.CreateModel(
            name='isopen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=128)),
                ('essay_id', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='essay',
            name='lable',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AddField(
            model_name='essay',
            name='open',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='essay',
            name='popular',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
    ]
