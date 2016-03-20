# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Data', '0002_auto_20150626_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basin',
            name='location',
            field=models.CharField(max_length=100, verbose_name=b'Ubicaci\xc3\xb3n:'),
        ),
        migrations.AlterField(
            model_name='interruption',
            name='duration',
            field=models.CharField(max_length=10, verbose_name=b'Duracio\xc5\x84:'),
        ),
        migrations.AlterField(
            model_name='manager',
            name='address',
            field=models.CharField(max_length=100, verbose_name=b'Direcci\xc3\xb3n:'),
        ),
        migrations.AlterField(
            model_name='manager',
            name='phone',
            field=models.CharField(max_length=15, serialize=False, verbose_name=b'Tel\xc3\xa9fono:', primary_key=True),
        ),
        migrations.AlterField(
            model_name='outbox',
            name='outbox_id',
            field=models.CharField(max_length=15, verbose_name=b'Tel\xc3\xa9fono:'),
        ),
        migrations.AlterField(
            model_name='remenber',
            name='remenber_id',
            field=models.CharField(max_length=15, serialize=False, verbose_name=b'Tel\xc3\xa9fono:', primary_key=True),
        ),
        migrations.AlterField(
            model_name='reservoir',
            name='number_user',
            field=models.IntegerField(verbose_name=b'N\xc3\xbamero de Usuarios:'),
        ),
    ]
