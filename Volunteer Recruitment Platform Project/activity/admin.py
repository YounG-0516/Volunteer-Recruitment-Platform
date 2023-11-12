from django.contrib import admin
from .models import Activity, Location, ActivityType, Ingroup

admin.site.register(Activity)
admin.site.register(ActivityType)
admin.site.register(Ingroup)
admin.site.register(Location)

# Register your models here.
