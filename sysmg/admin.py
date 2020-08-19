from django.contrib import admin

# Register your models here.
from sysmg.models import Machinfo, User, Operationlog

admin.site.register(Machinfo)
admin.site.register(User)
admin.site.register(Operationlog)