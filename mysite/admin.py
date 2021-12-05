from django.contrib import admin

from . import models
# Register your models here.
admin.site.register(models.groupModel)
admin.site.register(models.requestModel)
admin.site.register(models.activityModel)
admin.site.register(models.userActivityModel)