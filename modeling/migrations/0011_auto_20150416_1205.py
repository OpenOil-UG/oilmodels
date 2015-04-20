# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hulk', '0004_auto_20150416_1205'),
        ('modeling', '0010_auto_20150413_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='Production',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('date', models.DateField(blank=True, null=True)),
                ('commodity', models.CharField(max_length=100, choices=[('gas', 'Gas'), ('oil', 'Oil, grade unspecified'), ('oil', 'Oil, heavy'), ('oil', 'Oil, light and medium')])),
                ('actual_predicted', models.CharField(max_length=10, choices=[('actual', 'Actual'), ('predicted', 'Predicted')])),
                ('confidence', models.CharField(max_length=10)),
                ('level', models.FloatField()),
                ('unit', models.CharField(max_length=20, choices=[('mbbls', 'Million barels'), ('mmcf', 'Million cubic feet (mmcf/mmscf)'), ('mboe', 'Million barels oil equivalent')], default='mbbls')),
                ('per', models.CharField(max_length=20, choices=[('day', 'day'), ('month', 'month'), ('year', 'year')], default='year')),
                ('company', models.ForeignKey(to='hulk.Company', null=True, blank=True)),
                ('project', models.ForeignKey(to='hulk.Project', null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RenameField(
            model_name='reservelevel',
            old_name='category',
            new_name='confidence',
        ),
        migrations.AlterField(
            model_name='reservelevel',
            name='unit',
            field=models.CharField(max_length=20, choices=[('mbbls', 'Million barels'), ('mmcf', 'Million cubic feet (mmcf/mmscf)'), ('mboe', 'Million barels oil equivalent')], default='mbbls'),
        ),
    ]
