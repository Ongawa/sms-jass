# coding=utf-8
from django.contrib import admin
from Data.models import *

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('manager_id','name','surname','address','phone')
    list_filter = ('manager_id','name','surname','address','phone')
    search_fields = ['manager_id','name','surname','address','phone']

@admin.register(Basin)
class BasinAdmin(admin.ModelAdmin):
    """docstring for BasinAdmin"""
    list_display = ('basin_id','location')
    list_filter = ('basin_id','location')
    search_fields = ['basin_id','location']

@admin.register(Reservoir)
class ReservoirAdmin(admin.ModelAdmin):
    """docstring for ReservoirAdmin"""
    list_display = ('reservoir_id','basin_id','number_user','position')
    list_filter = ('reservoir_id','basin_id','number_user','position','manager_id')
    search_fields = ['reservoir_id','basin_id__basin_id','number_user','position','manager_id__manager_id']
    filter_horizontal = ('manager_id',)

@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    """docstring for MeasurementAdmin"""
    list_display = ('reservoir_id','date','level_cl','add_cl','caudal','user_pay')
    list_filter = ('reservoir_id','date','level_cl','add_cl','caudal','user_pay')
    search_fields = ['reservoir_id__reservoir_id','date','level_cl','add_cl','caudal','user_pay']

@admin.register(Interruption)
class InterruptionAdmin(admin.ModelAdmin):
    """docstring for InterrpciónAdmin"""
    list_display = ('reservoir_id','date','reason','duration')
    list_filter = ('reservoir_id','date','reason','duration')
    search_fields = ['reservoir_id__reservoir_id','date','reason','duration']

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    """docstring for RecordAdmin"""
    list_display = ('reservoir_id','date','message','detail','process')
    list_filter = ('reservoir_id','date','message','detail','process')
    search_fields = ['reservoir_id__reservoir_id','date','message','detail','process']

@admin.register(Outbox)
class OutboxAdmin(admin.ModelAdmin):
    """docstring for OutboxAdmin"""
    list_display = ('outbox_id','message','date','time')
    list_filter = ('outbox_id','message','date','time')
    search_fields = ['outbox_id','message','date','time']

@admin.register(FormatMessage)
class FormatMessageAdmin(admin.ModelAdmin):
    """docstring for Format_MessageAdmin"""
    list_display = ('message',)
    list_filter = ('message',)
    search_fields = ['message']

