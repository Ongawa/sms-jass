# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Basin',
            fields=[
                ('basin_id', models.CharField(verbose_name='Nombre:', serialize=False, primary_key=True, max_length=50)),
                ('location', models.CharField(verbose_name='Ubicación:', max_length=100)),
            ],
            options={
                'verbose_name': 'Cuenca',
                'verbose_name_plural': 'Cuencas',
                'ordering': ['basin_id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FormatMessage',
            fields=[
                ('id', models.AutoField(verbose_name='Id', serialize=False, primary_key=True)),
                ('message', models.CharField(verbose_name='Mensaje:', max_length=100)),
            ],
            options={
                'verbose_name': 'Formato Mensaje',
                'verbose_name_plural': 'Formato Mensaje',
                'ordering': ['message'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Interruption',
            fields=[
                ('id', models.AutoField(verbose_name='Id', serialize=False, primary_key=True)),
                ('date', models.DateField(verbose_name='Fecha:')),
                ('time', models.TimeField(verbose_name='Hora')),
                ('reason', models.CharField(verbose_name='Causa:', max_length=100, choices=[('Mantenimiento', 'Mantenimiento'), ('Reparacion', 'Reparacion')], default='Mantenimiento')),
                ('duration', models.CharField(verbose_name='Duracioń:', max_length=10)),
            ],
            options={
                'verbose_name': 'Interrpción',
                'verbose_name_plural': 'Interrupciones',
                'ordering': ['reservoir_id', 'date', 'time'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('manager_id', models.CharField(verbose_name='DNI:', max_length=10)),
                ('name', models.CharField(verbose_name='Nombres:', max_length=100)),
                ('surname', models.CharField(verbose_name='Apellidos:', max_length=200)),
                ('address', models.CharField(verbose_name='Dirección:', max_length=100)),
                ('phone', models.CharField(verbose_name='Teléfono:', serialize=False, primary_key=True, max_length=15)),
            ],
            options={
                'verbose_name': 'Responsable',
                'verbose_name_plural': 'Responsables',
                'ordering': ['manager_id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(verbose_name='Id', serialize=False, primary_key=True)),
                ('date', models.DateField(verbose_name='Fecha:')),
                ('time', models.TimeField(verbose_name='Hora')),
                ('level_cl', models.CharField(verbose_name='Nivel Cloro:', max_length=10)),
                ('add_cl', models.CharField(verbose_name='Incremento Cloro:', max_length=10)),
                ('caudal', models.CharField(verbose_name='Caudal:', max_length=10)),
                ('user_pay', models.CharField(verbose_name='Usuarios Pagantes:', max_length=10)),
            ],
            options={
                'verbose_name': 'Medición',
                'verbose_name_plural': 'Mediciones',
                'ordering': ['reservoir_id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Outbox',
            fields=[
                ('id', models.AutoField(verbose_name='Id', serialize=False, primary_key=True)),
                ('outbox_id', models.CharField(verbose_name='Teléfono:', max_length=15)),
                ('message', models.CharField(verbose_name='Mensaje:', max_length=200)),
                ('date', models.DateField(verbose_name='Fecha:')),
                ('time', models.TimeField(verbose_name='Hora')),
            ],
            options={
                'verbose_name': 'Bandeja de Salida',
                'verbose_name_plural': 'Bandeja de Salida',
                'ordering': ['date', 'time', 'outbox_id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='Id', serialize=False, primary_key=True)),
                ('date', models.DateField(verbose_name='Fecha:')),
                ('time', models.TimeField(verbose_name='Hora')),
                ('message', models.CharField(verbose_name='Mensaje:', max_length=100)),
                ('detail', models.CharField(verbose_name='Detalle MSM:', max_length=100, choices=[('Entrada', 'Entrada'), ('Salida', 'Salida')], default='Entrada')),
                ('process', models.BooleanField(verbose_name='Procesado:', default=False)),
            ],
            options={
                'verbose_name': 'Mensaje',
                'verbose_name_plural': 'Mensajes',
                'ordering': ['reservoir_id', 'date', 'time'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Remenber',
            fields=[
                ('remenber_id', models.CharField(verbose_name='Teléfono:', serialize=False, primary_key=True, max_length=15)),
                ('sent', models.IntegerField(verbose_name='Recordatorio:')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Reservoir',
            fields=[
                ('reservoir_id', models.CharField(verbose_name='Nombre:', serialize=False, primary_key=True, max_length=50)),
                ('number_user', models.IntegerField(verbose_name='Número de Usuarios:')),
                ('position', models.CharField(verbose_name='Cordenadas:', max_length=30)),
                ('basin_id', models.ForeignKey(verbose_name='Cuenca:', to='Data.Basin')),
                ('manager_id', models.ManyToManyField(verbose_name='Responsable:', to='Data.Manager')),
            ],
            options={
                'verbose_name': 'JASS',
                'verbose_name_plural': 'JASS',
                'ordering': ['reservoir_id'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='record',
            name='reservoir_id',
            field=models.ForeignKey(verbose_name='JASS:', to='Data.Reservoir'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='measurement',
            name='reservoir_id',
            field=models.ForeignKey(verbose_name='JASS:', to='Data.Reservoir'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='interruption',
            name='reservoir_id',
            field=models.ForeignKey(verbose_name='JASS:', to='Data.Reservoir'),
            preserve_default=True,
        ),
    ]
