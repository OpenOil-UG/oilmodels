# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ooapi', '0002_auto_20150429_0952'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConcessionSearchResult',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('source', models.CharField(choices=[('bing', 'Bing')], max_length=20)),
                ('date_scraped', models.DateField(default=datetime.datetime.now)),
                ('reviewed', models.BooleanField(default=False)),
                ('blacklisted', models.BooleanField(default=False)),
                ('url', models.URLField()),
                ('title', models.CharField(max_length=200)),
                ('priority', models.IntegerField(default=0)),
                ('description', models.TextField(blank=True, null=True)),
                ('concession', models.ForeignKey(to='ooapi.Concession')),
            ],
        ),
    ]
