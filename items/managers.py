from django.db import models
from django.db.models.query import QuerySet
from django.db.models import Q, Count, Sum
from django.apps import apps
from datetime import datetime

class ItemQuerySet(QuerySet):
	def this_account(self, account):
		return self.filter(account=account)	

	def untransfered(self):
		#vypise vsetky dostupne polozky
		return self.filter(is_transfered=False)

	def active(self):
		return self.filter(is_active=True)

	def at_location(self, location):
		return self.filter(location=location)

	def at_order(self, order):
		return self.filter(order=order)

	def this_product(self, product):
		return self.filter(product=product)

	def stock_count(self, **kwargs):
		return self.filter(**kwargs).count()

	def is_available(self, is_available):
		return self.filter(is_available=is_available)

	def search(self, search):
		return self.filter(Q(product__full_name__icontains=search) | Q(item_code=search))

class ItemManager(models.Manager):
	def create_item(self, *args, **kwargs):
		item = self.create(*args, **kwargs)
		return item

	def transfer(self, item, basket):
		if item.is_transfered and item in basket.items.all() and item.is_active: # ak je v kosiku a "transfered" tak to zrusi
			item.is_transfered = False
			basket.items.remove(item)
		elif not item.is_transfered and item.is_active:
			basket.items.add(item)
			item.is_transfered = True
		basket.save()
		item.save()
		return item

	def get_query_set(self):
		return ItemQuerySet(self.model)  

	def __getattr__(self, attr, *args):
		if attr.startswith("_"):
			raise AttributeError
		return getattr(self.get_query_set(), attr, *args)

class ItemImageManager(models.Manager):
	def create_item_image(self, **kwargs):
		item_image = self.create(image=kwargs['image'], user=kwargs['user'])
		item_image.save()
		item = kwargs['item']
		item.images.add(item_image)
		item.save()
