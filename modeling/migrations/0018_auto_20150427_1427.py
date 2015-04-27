# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modeling', '0017_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='production',
            name='unit',
            field=models.CharField(max_length=20, choices=[('bbls', 'Barrels'), ('mbbls', 'Million barrels'), ('mmcf', 'Million cubic feet (mmcf/mmscf)'), ('mboe', 'Million barels oil equivalent'), ('tdf', 'Thousand Cubic Feet (mcf/mscf)')], default='mbbls'),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='unit',
            field=models.CharField(max_length=20, choices=[('bbls', 'Barrels'), ('mbbls', 'Million barrels'), ('mmcf', 'Million cubic feet (mmcf/mmscf)'), ('mboe', 'Million barels oil equivalent'), ('tdf', 'Thousand Cubic Feet (mcf/mscf)')], default='mbbls'),
        ),
    ]
