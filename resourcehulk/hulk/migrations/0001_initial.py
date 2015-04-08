# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django_pg.models.fields.json
import django_pg.models.fields.datetime_
import hulk.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Commodity',
            fields=[
                ('commodity_id', models.CharField(primary_key=True, serialize=False, max_length=200, default=hulk.models.random_id)),
                ('commodity_name', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'commodity_table',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('company_id', models.CharField(primary_key=True, serialize=False, max_length=200, default=hulk.models.random_id)),
                ('open_lei_id', models.CharField(blank=True, max_length=200)),
                ('duns_number', models.CharField(blank=True, max_length=200)),
                ('company_name', models.CharField(max_length=200)),
                ('ticker_symbol', models.CharField(blank=True, max_length=200)),
                ('tax_id', models.CharField(blank=True, max_length=200)),
                ('open_corp_id', models.CharField(blank=True, max_length=200)),
                ('vat_id', models.CharField(blank=True, max_length=200)),
                ('company_url', models.CharField(blank=True, max_length=200)),
                ('cik', models.IntegerField(db_index=True, blank=True, null=True)),
                ('sic', models.IntegerField(blank=True, null=True)),
                ('jurisdiction', models.CharField(blank=True, max_length=50)),
            ],
            options={
                'db_table': 'company_table',
            },
        ),
        migrations.CreateModel(
            name='CompanyAlias',
            fields=[
                ('company_alias', models.CharField(primary_key=True, serialize=False, max_length=200, default=hulk.models.random_id)),
                ('company_id', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'company_alias_table',
            },
        ),
        migrations.CreateModel(
            name='Concession',
            fields=[
                ('concession_id', models.CharField(primary_key=True, serialize=False, max_length=200)),
                ('concession_name', models.CharField(max_length=200)),
                ('unep_geo_id', models.CharField(blank=True, max_length=200)),
                ('country', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'concession_table',
            },
        ),
        migrations.CreateModel(
            name='ConcessionAlias',
            fields=[
                ('concession_alias', models.CharField(primary_key=True, serialize=False, max_length=200)),
                ('concession_id', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'concession_alias_table',
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('contract_id', models.CharField(primary_key=True, serialize=False, max_length=200)),
                ('country', models.CharField(max_length=200)),
                ('sign_date', models.CharField(max_length=200)),
                ('title_type', models.CharField(blank=True, max_length=200)),
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
            name='DjangoMigrations',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', django_pg.models.fields.datetime_.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('doc_id', models.CharField(primary_key=True, serialize=False, max_length=200, default=hulk.models.random_id)),
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
                ('project_id', models.CharField(primary_key=True, serialize=False, max_length=200, default=hulk.models.random_id)),
                ('project_name', models.CharField(blank=True, null=True, max_length=200)),
                ('country', models.CharField(blank=True, null=True, max_length=200)),
            ],
            options={
                'db_table': 'project_table',
            },
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('label', models.CharField(primary_key=True, serialize=False, max_length=10)),
                ('metadata', django_pg.models.fields.json.JSONField(blank=True, null=True, default='{}')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SearchResult',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sequencenum', models.IntegerField()),
                ('metadata', django_pg.models.fields.json.JSONField(blank=True, null=True, default='{}')),
                ('search', models.ForeignKey(to='hulk.Search', related_name='results')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SourceInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('contributor', models.CharField(max_length=200)),
                ('license', models.CharField(max_length=200)),
                ('date', django_pg.models.fields.datetime_.DateTimeField(default=datetime.datetime.now)),
                ('info', django_pg.models.fields.json.JSONField(blank=True, null=True, default='{}')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Statement',
            fields=[
                ('statement_id', models.CharField(primary_key=True, serialize=False, max_length=200, default=hulk.models.random_id)),
                ('statement_content', models.CharField(max_length=200)),
                ('definitive', models.BooleanField(default=False)),
                ('companies', models.ManyToManyField(db_table='company_link_table', blank=True, to='hulk.Company')),
                ('concessions', models.ManyToManyField(db_table='concession_link_table', blank=True, to='hulk.Concession')),
                ('contracts', models.ManyToManyField(db_table='contract_link_table', blank=True, to='hulk.Contract')),
                ('doc', models.ForeignKey(default=None, blank=True, to='hulk.Document', null=True)),
                ('projects', models.ManyToManyField(db_table='project_link_table', blank=True, to='hulk.Project')),
                ('source', models.ForeignKey(blank=True, to='hulk.SourceInfo', null=True)),
            ],
            options={
                'db_table': 'statement_table',
            },
        ),
        migrations.AddField(
            model_name='search',
            name='source',
            field=models.ForeignKey(blank=True, to='hulk.SourceInfo', null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='source',
            field=models.ForeignKey(blank=True, to='hulk.SourceInfo', null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='source',
            field=models.ForeignKey(blank=True, to='hulk.SourceInfo', null=True),
        ),
        migrations.AddField(
            model_name='contract',
            name='doc',
            field=models.ForeignKey(blank=True, to='hulk.Document', null=True),
        ),
        migrations.AddField(
            model_name='contract',
            name='source',
            field=models.ForeignKey(blank=True, to='hulk.SourceInfo', null=True),
        ),
        migrations.AddField(
            model_name='concession',
            name='source',
            field=models.ForeignKey(blank=True, to='hulk.SourceInfo', null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='source',
            field=models.ForeignKey(blank=True, to='hulk.SourceInfo', null=True, related_name='companies'),
        ),
    ]
