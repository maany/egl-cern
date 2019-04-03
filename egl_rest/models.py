from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
# Create your models here.
class Site(models.Model):
    name = models.CharField()
    tier = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    country_code = models.CharField()
    country = models.CharField()
    supported_vos
    pass

class Pledge(models.Model):
    pass

class Federation(models.Model):
    pass
