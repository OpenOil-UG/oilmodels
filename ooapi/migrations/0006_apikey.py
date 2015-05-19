# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ooapi.models


class Migration(migrations.Migration):

    dependencies = [
        ('ooapi', '0005_concession_details'),
    ]

    operations = [
        migrations.CreateModel(
            name='APIKey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(default=ooapi.models.new_key, unique=True, max_length=25)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]
