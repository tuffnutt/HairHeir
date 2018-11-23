from django.db import models


# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=250)
    address = models.CharField(max_length=350)
    business_reg_no = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    owner_name = models.CharField(max_length=250)
    owner_id_no = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Skill(models.Model):
    category = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Freelancer(models.Model):
    name = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=50)
    id_no = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    rate = models.FloatField()
    skill = models.ManyToManyField(Skill)

    def __str__(self):
        return self.name


class Job(models.Model):
    saloon_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    freelancer_id = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    duration = models.IntegerField
    status = models.BooleanField

    def __str__(self):
        return self.id


class Payment(models.Model):
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE)
    status = models.BooleanField
    price = models.FloatField

    def __str__(self):
        return self.job_id


class Rate(models.Model):
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE)
    rate = models.IntegerField


class Schedule(models.Model):
    freelancer_id = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    saloon_id = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    date = models.DateField
    status = models.BooleanField







