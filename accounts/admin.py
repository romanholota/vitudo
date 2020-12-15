from django.contrib import admin

# Register your models here.
from . models import UserDetails, Account

admin.site.register(UserDetails)
admin.site.register(Account)