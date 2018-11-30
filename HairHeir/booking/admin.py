from django.contrib import admin
from .models import Client, Freelancer, Payment, Skill, Rate, Job, Province, District, City, Type, Schedule
# Register your models here.

admin.site.register(Client)
admin.site.register(Freelancer)
admin.site.register(Payment)
admin.site.register(Skill)
admin.site.register(Rate)
admin.site.register(Job)
admin.site.register(Province)
admin.site.register(District)
admin.site.register(City)
admin.site.register(Type)
admin.site.register(Schedule)
