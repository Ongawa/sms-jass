# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Data', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='reservoir_id',
            field=models.CharField(max_length=100, verbose_name='Jass:'),
        ),
    ]
