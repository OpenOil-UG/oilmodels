# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_pg.models.fields.json


class Migration(migrations.Migration):

    dependencies = [
        ('hulk', '0009_auto_20150611_0717'),
        ('modeling', '0023_auto_20150618_1023'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraInformation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=100, null=True, blank=True)),
                ('extra_data', django_pg.models.fields.json.JSONField(default=None, null=True, blank=True)),
                ('company', models.ForeignKey(blank=True, to='hulk.Company', null=True)),
                ('project', models.ForeignKey(blank=True, to='hulk.Project', null=True)),
                ('source', models.ForeignKey(blank=True, to='hulk.Document', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
