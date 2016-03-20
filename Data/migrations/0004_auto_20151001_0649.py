# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Data', '0003_auto_20150929_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='message',
            field=models.CharField(max_length=200, verbose_name=b'Mensaje:'),
        ),
    ]
