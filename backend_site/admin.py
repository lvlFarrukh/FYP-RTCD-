from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(controller_user)
admin.site.register(suspect_person_detail)
admin.site.register(app_user)
admin.site.register(suspect_from_app_User)
admin.site.register(suspect_from_anonymous)
