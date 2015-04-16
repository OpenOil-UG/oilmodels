# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modeling', '0009_auto_20150413_1227'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservelevel',
            name='status',
            field=models.CharField(choices=[('developed', 'Developed'), ('undeveloped', 'Undeveloped'), ('total', 'Total'), ('unspecified', 'Unspecified')], max_length=20, default='unspecified'),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='interest',
            field=models.FloatField(verbose_name='Interest of the company in this project (%)', default=100),
        ),
    ]
