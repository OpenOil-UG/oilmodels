# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_pg.models.fields.json


class Migration(migrations.Migration):

    dependencies = [
        ('modeling', '0018_auto_20150427_1427'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnreviewedData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('metadata', django_pg.models.fields.json.JSONField(default=None, null=True, blank=True)),
                ('data', django_pg.models.fields.json.JSONField(default=None, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='production',
            name='commodity',
            field=models.CharField(max_length=100, choices=[(b'gas', b'Gas'), (b'oil', b'Oil, grade unspecified'), (b'oil_heavy', b'Oil, heavy'), (b'oil_light', b'Oil, light and medium')]),
        ),
        migrations.AlterField(
            model_name='production',
            name='unit',
            field=models.CharField(default=b'mbbls', max_length=20, choices=[(b'bbls', b'Barrels'), (b'mbbls', b'Million barrels'), (b'mmcf', b'Million cubic feet (mmcf/mmscf)'), (b'mboe', b'Million barels oil equivalent'), (b'tdf', b'Thousand Cubic Feet (mcf/mscf)'), (b'm3', b'Cubic Metres')]),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='commodity',
            field=models.CharField(max_length=100, choices=[(b'gas', b'Gas'), (b'oil', b'Oil, grade unspecified'), (b'oil_heavy', b'Oil, heavy'), (b'oil_light', b'Oil, light and medium')]),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='unit',
            field=models.CharField(default=b'mbbls', max_length=20, choices=[(b'bbls', b'Barrels'), (b'mbbls', b'Million barrels'), (b'mmcf', b'Million cubic feet (mmcf/mmscf)'), (b'mboe', b'Million barels oil equivalent'), (b'tdf', b'Thousand Cubic Feet (mcf/mscf)'), (b'm3', b'Cubic Metres')]),
        ),
    ]
