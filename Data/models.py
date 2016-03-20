# coding=utf-8
from django.db import models

class Basin(models.Model):
    """docsrting for Basin"""
    basin_id = models.CharField("Nombre:", max_length=50, primary_key=True)
    location = models.CharField("Ubicación:", max_length=100)

    class Meta:
        ordering = ["basin_id"]
        verbose_name_plural = "Cuencas"
        verbose_name = "Cuenca"

    def __str__(self):
        return self.basin_id

class Manager(models.Model):
    """docsrting for Manager"""
    manager_id = models.CharField("DNI:", max_length=10)
    name = models.CharField("Nombres:", max_length=100)
    surname = models.CharField("Apellidos:", max_length=200)
    address = models.CharField("Dirección:", max_length=100)
    phone = models.CharField("Teléfono:", max_length=15, primary_key=True)

    class Meta:
        ordering = ["manager_id"]
        verbose_name_plural = "Responsables"
        verbose_name = "Responsable"

    def __str__(self):
        return self.phone + " " + self.name + " " + self.surname

class Reservoir(models.Model):
    """docsrting for Reservoir"""
    reservoir_id = models.CharField("Nombre:", max_length=50, primary_key=True)
    basin_id = models.ForeignKey(Basin, verbose_name="Cuenca:")
    number_user = models.IntegerField("Número de Usuarios:")
    position = models.CharField("Cordenadas:", max_length=30)
    manager_id = models.ManyToManyField(Manager, verbose_name="Responsable:")

    class Meta:
        ordering = ["reservoir_id"]
        verbose_name_plural = "JASS"
        verbose_name = "JASS"

    def __str__(self):
        return self.reservoir_id

class Measurement(models.Model):
    """docsrting for Measurement"""
    id = models.AutoField("Id", primary_key=True)
    reservoir_id = models.ForeignKey(Reservoir, verbose_name="JASS:")
    date = models.DateField("Fecha:", auto_now=False)
    time = models.TimeField("Hora", auto_now=False)
    level_cl = models.CharField("Nivel Cloro:", max_length=10)
    add_cl = models.CharField("Incremento Cloro:", max_length=10)
    caudal = models.CharField("Caudal:", max_length=10)
    user_pay = models.CharField("Usuarios Pagantes:",max_length=10)

    class Meta:
        ordering = ["reservoir_id"]
        verbose_name_plural = "Mediciones"
        verbose_name = "Medición"

    def __str__(self):
        return str(self.reservoir_id)

class Interruption(models.Model):
    """docsrting for Interruption"""
    Mantenimiento = 'Mantenimiento'
    Reparacion = 'Reparacion'
    reason_choice = (
        (Mantenimiento, 'Mantenimiento'),
        (Reparacion, 'Reparacion'),
    )

    id = models.AutoField("Id", primary_key=True)
    reservoir_id = models.ForeignKey(Reservoir, verbose_name="JASS:")
    date = models.DateField("Fecha:", auto_now=False)
    time = models.TimeField("Hora", auto_now=False)
    reason = models.CharField("Causa:",
                              choices=reason_choice,default=Mantenimiento,max_length=100)
    duration = models.CharField("Duracioń:", max_length=10)

    class Meta:
        ordering = ["reservoir_id","date","time"]
        verbose_name_plural = "Interrupciones"
        verbose_name = "Interrpción"

    def __str__(self):
        return str(self.reservoir_id)

class Record(models.Model):
    """docsrting for Record"""
    Entrada = 'Entrada'
    Salida = 'Salida'
    message_choice = (
        (Entrada, 'Entrada'),
        (Salida, 'Salida'),
    )

    id = models.AutoField("Id", primary_key=True)
    reservoir_id = models.CharField("Jass:",max_length=100)
    date = models.DateField("Fecha:", auto_now=False)
    time = models.TimeField("Hora", auto_now=False)
    message = models.CharField("Mensaje:", max_length=200)
    detail = models.CharField("Detalle MSM:",
                              choices=message_choice,default=Entrada,max_length=100)
    process = models.BooleanField(verbose_name="Procesado:",default=False)

    class Meta:
        ordering = ["reservoir_id","date","time"]
        verbose_name_plural = "Mensajes"
        verbose_name = "Mensaje"

    def __str__(self):
        return str(self.reservoir_id)

class Outbox (models.Model):
    """docsrting for outbox"""
    id = models.AutoField("Id", primary_key=True)
    outbox_id = models.CharField("Teléfono:", max_length=15)
    message = models.CharField("Mensaje:", max_length=200)
    date = models.DateField("Fecha:", auto_now=False)
    time = models.TimeField("Hora", auto_now=False)

    class Meta:
        ordering = ["date","time","outbox_id"]
        verbose_name_plural = "Bandeja de Salida"
        verbose_name = "Bandeja de Salida"

    def __str__(self):
        return str(self.outbox_id)


class Remenber (models.Model):
    """docsrting for Remenber"""
    remenber_id = models.CharField("Teléfono:",primary_key=True, max_length=15)
    sent = models.IntegerField("Recordatorio:")

    def __str__(self):
        return str(self.remenber_id)

class FormatMessage (models.Model):
    """docsrting for FormatMessage"""
    id = models.AutoField("Id", primary_key=True)
    message = models.CharField("Mensaje:", max_length=100)

    class Meta:
        ordering = ["message"]
        verbose_name_plural = "Formato Mensaje"
        verbose_name = "Formato Mensaje"

    def __str__(self):
        return str(self.message)

