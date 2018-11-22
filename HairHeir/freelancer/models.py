from django.db import models


# Create your models here.
class Saloon(models.Model):
    name = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    business_reg_no = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    owner_name = models.CharField(max_length=250)
    owner_id_no = models.CharField(max_length=250)


class Stylist(models.Model):
    name = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    id_no = models.CharField(max_length=250)
    type = models.CharField(max_length=250)
    rate = models.FloatField()


class Job(models.Model):
    saloon_id = models.ForeignKey(Saloon, on_delete=models.CASCADE)
    stylist_id = models.ForeignKey(Stylist, on_delete=models.CASCADE)
    duration = models.CharField(max_length=250)
    status = models.BooleanField


class Payment (models.Model) :
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE)
    status = models.BooleanField
    price = models.FloatField


class Rate (models.Model) :
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE)
    rate = models.IntegerField



