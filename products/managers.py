from django.db import models
from django.db.models.query import QuerySet
from django.db.models import Q, Count, Sum
from django.apps import apps
from datetime import datetime

class ProductQuerySet(QuerySet):
	def search(self, search):
		return self.filter(Q(full_name__icontains=search) | Q(category__name__icontains=search))

	def this_account(self, account):
		return self.filter(account=account)

	def this_brand(self, brand):
		return self.filter(brand=brand)

	def this_category(self, category):
		return self.filter(category=category)

class BrandQuerySet(QuerySet):
	def this_account(self, account):
		return self.filter(account=account)

	def has_products(self, has_products):
		if has_products == 'True':
			return self.annotate(product_count=Count('product')).filter(product_count__gt=0)
		elif has_products == 'False':
			return self.annotate(product_count=Count('product')).filter(product_count=0)
		else:
			return self

	def search(self, search):
		return self.filter(name__icontains=search)

class CategoryQuerySet(QuerySet):
	def this_account(self, account):
		return self.filter(account=account)

	def has_products(self, has_products):
		if has_products == 'True':
			return self.annotate(product_count=Count('product')).filter(product_count__gt=0)
		elif has_products == 'False':
			return self.annotate(product_count=Count('product')).filter(product_count=0)
		else:
			return self

	def search(self, search):
		return self.filter(name=search)
		
class CategoryManager(models.Manager):
	def get_query_set(self):
		return CategoryQuerySet(self.model)

	def create_category(self, *args, **kwargs):
		category = self.create(*args, **kwargs)
		return category

	def __getattr__(self, attr, *args):
		if attr.startswith("_"):
			raise AttributeError
		return getattr(self.get_query_set(), attr, *args)

class BrandManager(models.Manager):
	def get_query_set(self):
		return BrandQuerySet(self.model)

	def create_brand(self, *args, **kwargs):
		brand = self.create(*args, **kwargs)
		return brand

	def __getattr__(self, attr, *args):
		if attr.startswith("_"):
			raise AttributeError
		return getattr(self.get_query_set(), attr, *args)

class ProductManager(models.Manager):
	def update_or_create_product(self, **kwargs):
		product, created = self.update_or_create(id=kwargs['id'], defaults={**kwargs})
		return product

	def get_query_set(self):
		return ProductQuerySet(self.model)

	def __getattr__(self, attr, *args):
		if attr.startswith("_"):
			raise AttributeError
		return getattr(self.get_query_set(), attr, *args)

