# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_pg.models.fields.json
import hulk.models
import django_pg.models.fields.datetime_
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Commodity',
            fields=[
                ('commodity_id', models.CharField(max_length=200, serialize=False, primary_key=True, default=hulk.models.random_id)),
                ('commodity_name', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'commodity_table',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('company_id', models.CharField(max_length=200, serialize=False, primary_key=True, default=hulk.models.random_id)),
                ('open_lei_id', models.CharField(max_length=200, blank=True)),
                ('duns_number', models.CharField(max_length=200, blank=True)),
                ('company_name', models.CharField(max_length=200)),
                ('ticker_symbol', models.CharField(max_length=200, blank=True)),
                ('tax_id', models.CharField(max_length=200, blank=True)),
                ('open_corp_id', models.CharField(max_length=200, blank=True)),
                ('vat_id', models.CharField(max_length=200, blank=True)),
                ('company_url', models.CharField(max_length=200, blank=True)),
                ('cik', models.IntegerField(db_index=True, null=True, blank=True)),
                ('sic', models.IntegerField(null=True, blank=True)),
                ('jurisdiction', models.CharField(max_length=50, blank=True)),
            ],
            options={
                'db_table': 'company_table',
            },
        ),
        migrations.CreateModel(
            name='CompanyAlias',
            fields=[
                ('company_alias', models.CharField(max_length=200, serialize=False, primary_key=True, default=hulk.models.random_id)),
                ('company_id', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'company_alias_table',
            },
        ),
        migrations.CreateModel(
            name='Concession',
            fields=[
                ('concession_id', models.CharField(max_length=200, serialize=False, primary_key=True)),
                ('concession_name', models.CharField(max_length=200)),
                ('unep_geo_id', models.CharField(max_length=200, blank=True)),
                ('country', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'concession_table',
            },
        ),
        migrations.CreateModel(
            name='ConcessionAlias',
            fields=[
                ('concession_alias', models.CharField(max_length=200, serialize=False, primary_key=True)),
                ('concession_id', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'concession_alias_table',
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('contract_id', models.CharField(max_length=200, serialize=False, primary_key=True)),
                ('country', models.CharField(max_length=200)),
                ('sign_date', models.CharField(max_length=200)),
                ('title_type', models.CharField(max_length=200, blank=True)),
                ('source_url', models.CharField(max_length=200)),
                ('doc_cloud_id', models.CharField(max_length=200)),
                ('doc_cloud_url', models.CharField(max_length=200)),
                ('sign_year', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'contract_table',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('doc_id', models.CharField(max_length=200, serialize=False, primary_key=True, default=hulk.models.random_id)),
                ('host_url', models.CharField(max_length=200, default='')),
                ('source_url', models.CharField(max_length=200, default='')),
            ],
            options={
                'db_table': 'document_table',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_id', models.CharField(max_length=200, serialize=False, primary_key=True, default=hulk.models.random_id)),
                ('project_name', models.CharField(max_length=200, null=True, blank=True)),
                ('country', models.CharField(max_length=200, null=True, blank=True)),
            ],
            options={
                'db_table': 'project_table',
            },
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('label', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('metadata', django_pg.models.fields.json.JSONField(null=True, blank=True, default='{}')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SearchResult',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('sequencenum', models.IntegerField()),
                ('metadata', django_pg.models.fields.json.JSONField(null=True, blank=True, default='{}')),
                ('search', models.ForeignKey(to='hulk.Search', related_name='results')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SourceInfo',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('contributor', models.CharField(max_length=200)),
                ('license', models.CharField(max_length=200)),
                ('date', django_pg.models.fields.datetime_.DateTimeField(default=datetime.datetime.now)),
                ('info', django_pg.models.fields.json.JSONField(null=True, blank=True, default='{}')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Statement',
            fields=[
                ('statement_id', models.CharField(max_length=200, serialize=False, primary_key=True, default=hulk.models.random_id)),
                ('statement_content', models.CharField(max_length=200)),
                ('definitive', models.BooleanField(default=False)),
                ('companies', models.ManyToManyField(to='hulk.Company', blank=True, db_table='company_link_table')),
                ('concessions', models.ManyToManyField(to='hulk.Concession', blank=True, db_table='concession_link_table')),
                ('contracts', models.ManyToManyField(to='hulk.Contract', blank=True, db_table='contract_link_table')),
                ('doc', models.ForeignKey(null=True, blank=True, default=None, to='hulk.Document')),
                ('projects', models.ManyToManyField(to='hulk.Project', blank=True, db_table='project_link_table')),
                ('source', models.ForeignKey(null=True, blank=True, to='hulk.SourceInfo')),
            ],
            options={
                'db_table': 'statement_table',
            },
        ),
        migrations.AddField(
            model_name='search',
            name='source',
            field=models.ForeignKey(null=True, blank=True, to='hulk.SourceInfo'),
        ),
        migrations.AddField(
            model_name='project',
            name='source',
            field=models.ForeignKey(null=True, blank=True, to='hulk.SourceInfo'),
        ),
        migrations.AddField(
            model_name='document',
            name='source',
            field=models.ForeignKey(null=True, blank=True, to='hulk.SourceInfo'),
        ),
        migrations.AddField(
            model_name='contract',
            name='doc',
            field=models.ForeignKey(null=True, blank=True, to='hulk.Document'),
        ),
        migrations.AddField(
            model_name='contract',
            name='source',
            field=models.ForeignKey(null=True, blank=True, to='hulk.SourceInfo'),
        ),
        migrations.AddField(
            model_name='concession',
            name='source',
            field=models.ForeignKey(null=True, blank=True, to='hulk.SourceInfo'),
        ),
        migrations.AddField(
            model_name='company',
            name='source',
            field=models.ForeignKey(null=True, blank=True, to='hulk.SourceInfo', related_name='companies'),
        ),
    ]
