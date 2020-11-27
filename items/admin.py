from django.contrib import admin

from . models import Item, ItemDetails, ItemImage

# Register your models here.
admin.site.register(Item)
admin.site.register(ItemDetails)
admin.site.register(ItemImage)