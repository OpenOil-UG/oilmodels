# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Concession',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('country', django_countries.fields.CountryField(max_length=2, null=True, blank=True)),
                ('type', models.CharField(max_length=30, choices=[('onshore', 'Onshore'), ('offshore', 'Offshore')], null=True, blank=True)),
                ('status', models.CharField(max_length=30, choices=[('licensed', 'Licensed'), ('unlicensed', 'Not Licensed')], null=True, blank=True)),
                ('source_document', models.CharField(max_length=300, null=True, blank=True)),
                ('further_info', models.TextField(blank=True, null=True)),
                ('licensees', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
