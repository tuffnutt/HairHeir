from django.contrib import admin
from .models import Client, Freelancer, Payment, Skill, Rate, Job
# Register your models here.

admin.site.register(Client)
admin.site.register(Freelancer)
admin.site.register(Payment)
admin.site.register(Skill)
admin.site.register(Rate)
admin.site.register(Job)
