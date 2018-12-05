from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class Province(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class District(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class City(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class User(AbstractUser):
    is_client = models.BooleanField(default=False)
    is_freelancer = models.BooleanField(default=False)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=250, null=True)
    bank = models.CharField(max_length=150, null=True)
    band_account_no = models.CharField(max_length=50, null=True)


class Gallery(models.Model):
    image = models.FileField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    business_reg_no = models.CharField(max_length=100, null=True)
    owner_name = models.CharField(max_length=250, null=True)
    owner_id_no = models.CharField(max_length=20, null=True)
    profile_picture = models.FileField(null=True, default='profile.png')

    def __str__(self):
        return self.user.username


class Skill(models.Model):
    category = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

TIPOLOGIA_CHOICES = [
    ("male", "Male"),
    ("female", "Female"),
]

class Freelancer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    id_no = models.CharField(max_length=20, null=True)
    type = models.ManyToManyField(Type, related_name='types', null=True, blank=True)
    rate = models.FloatField(default=0.0)
    price = models.FloatField(default=0.0)
    skill = models.ManyToManyField(Skill)
    gender = models.CharField(max_length=20, choices=TIPOLOGIA_CHOICES, null=Type)
    profile_picture = models.FileField(null=True)

    def __str__(self):
        return self.user.username


class Job(models.Model):
    saloon_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    freelancer_id = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    duration = models.IntegerField(default=0)
    status = models.BooleanField(default=False)


class Payment(models.Model):
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    price = models.FloatField(default=0.0)


class Rate(models.Model):
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)


class Schedule(models.Model):
    freelancer_id = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    saloon_id = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    date = models.DateField(null=True)
    status = models.BooleanField(default=False)







