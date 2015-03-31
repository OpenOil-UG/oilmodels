# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modeling', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('iso2', models.CharField(primary_key=True, serialize=False, max_length=2)),
                ('name', models.CharField(max_length=75)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Reserve',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('p1', models.FloatField(null=True, blank=True)),
                ('p2', models.FloatField(null=True, blank=True)),
                ('p3', models.FloatField(null=True, blank=True)),
                ('year', models.IntegerField(null=True, blank=True)),
                ('field_name', models.CharField(blank=True, null=True, max_length=200)),
                ('project_name', models.CharField(blank=True, null=True, max_length=200)),
                ('company_name', models.CharField(blank=True, null=True, max_length=200)),
                ('reporting_level', models.CharField(choices=[('field', 'Field'), ('project', 'Project'), ('company-country', 'Company (in one country)'), ('company', 'Company (global)'), ('country', 'Country (all companies')], max_length=100)),
                ('country', models.ForeignKey(null=True, blank=True, to='modeling.Country')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
