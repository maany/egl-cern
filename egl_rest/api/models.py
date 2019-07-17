from django.db import models
from django.contrib.postgres.fields import ArrayField
import datetime


class Federation(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    accounting_name = models.CharField(max_length=100)
    supported_vos = models.ManyToManyField('VO')
    tier = models.IntegerField(default=-1)


class Pledge(models.Model):
    id = models.AutoField(primary_key=True)
    federation = models.ForeignKey(Federation, on_delete=models.PROTECT, )
    year = models.IntegerField(default=datetime.datetime.now().year)
    cpu = models.IntegerField(default=-1)
    disk = models.IntegerField(default=-1)
    tape = models.IntegerField(default=-1)
    vo = models.ForeignKey('VO', on_delete=models.PROTECT, default=None)


class SiteVO(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=70, default="Null", unique=True)
    site = models.ForeignKey('Site', on_delete=models.PROTECT)
    vo = models.ForeignKey('VO', on_delete=models.PROTECT)


class VO(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)


class Site(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=70, unique=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    tier = models.IntegerField(default=-1)
    supported_vos = models.ManyToManyField(VO)
    country = models.CharField(max_length=30)
    country_code = models.CharField(max_length=10)
    federation = models.ForeignKey(Federation, on_delete=models.PROTECT, null=True)
    active = models.BooleanField(default=False)
    sources = ArrayField(models.CharField(max_length=30), default=list)
    hepspec06 = models.IntegerField(default=-1)
    cores = models.IntegerField(default=-1)
    total_online_storage = models.IntegerField(default=-1, null=True)
    total_nearline_storage = models.IntegerField(default=-1, null=True)


class Transfer(models.Model):
    id = models.AutoField(primary_key=True)
    transferred_volume = models.FloatField()
    source = models.ForeignKey(Site, related_name='data_transfer_source', on_delete=models.PROTECT)
    destination = models.ForeignKey(Site, related_name='data_transfer_destination', on_delete=models.PROTECT)
    vo = models.ForeignKey(VO, on_delete=models.PROTECT, null=True)
    technology = models.CharField(max_length=30, null=True)
    average_file_size = models.FloatField(default=-1.0)
    average_operation_time = models.FloatField(default=-1.0)
    efficiency = models.FloatField(default=-1.0)
    count = models.IntegerField(default=-1)
    begin = models.IntegerField(default=-1)
    end = models.IntegerField(default=-1)
    total_operation_time = models.FloatField(default=-1)
