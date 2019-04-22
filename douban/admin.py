from django.contrib import admin

# Register your models here.
from douban import models
admin.site.register(models.movie)
admin.site.register(models.user)