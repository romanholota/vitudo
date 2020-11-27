from django.contrib import admin

from . models import Location, Customer, Address, Employee

# Register your models here.
admin.site.register(Location)
admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(Employee)