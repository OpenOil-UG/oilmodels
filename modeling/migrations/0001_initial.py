# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('url_homepage', models.URLField(blank=True, null=True)),
                ('url_example', models.URLField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=200, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('contents', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InformationType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('filing_type', models.CharField(blank=True, max_length=200, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('patterns', models.TextField(blank=True, null=True)),
                ('examples', models.TextField(blank=True, null=True)),
                ('negative_examples', models.TextField(blank=True, null=True)),
                ('regulations', models.TextField(blank=True, null=True)),
                ('DataSource', models.ForeignKey(to='modeling.DataSource', related_name='information_types')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
