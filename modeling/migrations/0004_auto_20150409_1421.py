# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_pg.models.fields.datetime_
import django_pg.models.fields.json
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('hulk', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('modeling', '0003_auto_20150408_1347'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('status', models.CharField(max_length=12, choices=[('completed', 'completed'), ('in progress', 'in progress'), ('available', 'available'), ('on hold', 'on hold')])),
                ('date_completed', django_pg.models.fields.datetime_.DateTimeField(null=True, blank=True)),
                ('data', django_pg.models.fields.json.JSONField(null=True, default=None, blank=True)),
                ('source', models.ForeignKey(to='hulk.Document')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TaskGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('data', django_pg.models.fields.json.JSONField(null=True, default=None, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='task',
            name='task_group',
            field=models.ForeignKey(to='modeling.TaskGroup'),
        ),
        migrations.AddField(
            model_name='task',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
