from django.contrib import admin

# Register your models here.

from models import *

admin.site.register(User)
admin.site.register(Event)
admin.site.register(Calendar)
admin.site.register(Group)