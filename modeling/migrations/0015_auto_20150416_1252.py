# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modeling', '0014_auto_20150416_1245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservelevel',
            name='reserve',
        ),
        migrations.RenameField(
            model_name='reserve',
            old_name='year',
            new_name='date',
        ),
        migrations.RemoveField(
            model_name='reserve',
            name='country',
        ),
        migrations.RemoveField(
            model_name='reserve',
            name='reporting_level',
        ),
        migrations.AddField(
            model_name='reserve',
            name='confidence',
            field=models.CharField(choices=[('Unknown', 'Unknown'), ('1P', '1P'), ('2P', '2P'), ('3P', '3P'), ('1C', '1C'), ('2C', '2C'), ('3C', '3C')], max_length=20, default='Unknown'),
        ),
        migrations.AddField(
            model_name='reserve',
            name='level',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reserve',
            name='status',
            field=models.CharField(choices=[('developed', 'Developed'), ('undeveloped', 'Undeveloped'), ('total', 'Total'), ('unspecified', 'Unspecified')], max_length=20, default='unspecified'),
        ),
        migrations.AddField(
            model_name='reserve',
            name='unit',
            field=models.CharField(choices=[('mbbls', 'Million barels'), ('mmcf', 'Million cubic feet (mmcf/mmscf)'), ('mboe', 'Million barels oil equivalent')], max_length=20, default='mbbls'),
        ),
        migrations.DeleteModel(
            name='ReserveLevel',
        ),
    ]
