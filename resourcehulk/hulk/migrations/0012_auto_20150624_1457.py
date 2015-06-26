# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hulk', '0011_auto_20150624_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statement',
            name='companies',
            field=models.ManyToManyField(to='hulk.Company', blank=True),
        ),
        migrations.AlterField(
            model_name='statement',
            name='concessions',
            field=models.ManyToManyField(to='hulk.Concession', blank=True),
        ),
        migrations.AlterField(
            model_name='statement',
            name='contracts',
            field=models.ManyToManyField(to='hulk.Contract', blank=True),
        ),
        migrations.AlterField(
            model_name='statement',
            name='projects',
            field=models.ManyToManyField(to='hulk.Project', blank=True),
        ),
        migrations.AlterModelTable(
            name='statement',
            table=None,
        ),
    ]
