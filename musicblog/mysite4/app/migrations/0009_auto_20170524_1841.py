# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-24 10:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20170524_1810'),
    ]

    operations = [
        migrations.RenameField(
            model_name='isopen',
            old_name='essay_id',
            new_name='essayid',
        ),
        migrations.RenameField(
            model_name='like',
            old_name='essay_id',
            new_name='essayid',
        ),
    ]
