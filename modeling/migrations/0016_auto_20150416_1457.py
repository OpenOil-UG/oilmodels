# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hulk', '0006_project_parent'),
        ('modeling', '0015_auto_20150416_1252'),
    ]

    operations = [
        migrations.AddField(
            model_name='production',
            name='source',
            field=models.ForeignKey(to='hulk.Document', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='production',
            name='unit',
            field=models.CharField(default='mbbls', max_length=20, choices=[('mbbls', 'Million barels'), ('mmcf', 'Million cubic feet (mmcf/mmscf)'), ('mboe', 'Million barels oil equivalent'), ('tdf', 'Thousand Cubic Feet (mcf/mscf)')]),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='unit',
            field=models.CharField(default='mbbls', max_length=20, choices=[('mbbls', 'Million barels'), ('mmcf', 'Million cubic feet (mmcf/mmscf)'), ('mboe', 'Million barels oil equivalent'), ('tdf', 'Thousand Cubic Feet (mcf/mscf)')]),
        ),
    ]
