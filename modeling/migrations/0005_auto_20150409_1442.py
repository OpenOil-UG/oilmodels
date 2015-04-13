# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modeling', '0004_auto_20150409_1421'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReserveLevel',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('category', models.CharField(choices=[('Unknown', 'Unknown'), ('1P', '1P'), ('2P', '2P'), ('3P', '3P'), ('1C', '1C'), ('2C', '2C'), ('3C', '3C')], default='Unknown', max_length=20)),
                ('unit', models.CharField(choices=[('mbbls', 'Million barels'), ('mmcf', 'Million cubic feet'), ('mboe', 'Million barels oil equivalent')], default='mbbls', max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='reserve',
            name='p1',
        ),
        migrations.RemoveField(
            model_name='reserve',
            name='p2',
        ),
        migrations.RemoveField(
            model_name='reserve',
            name='p3',
        ),
        migrations.AddField(
            model_name='reservelevel',
            name='reserve',
            field=models.ForeignKey(to='modeling.Reserve', related_name='reserve_levels'),
        ),
    ]
