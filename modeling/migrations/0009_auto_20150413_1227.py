# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modeling', '0008_auto_20150413_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserve',
            name='interest',
            field=models.FloatField(default=100, verbose_name='Interest of the company in this project'),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='year',
            field=models.IntegerField(help_text='year statement applies to, if specified, otherwise publication year of the source document', blank=True, null=True),
        ),
    ]
