from django.db import models
from django.db.models.query import QuerySet
from django.db.models import Q, Count, Sum
from django.apps import apps
from datetime import datetime

class AddressQuerySet(QuerySet):
	def search(self, search):
		return self.filter(Q(name__icontains=search) | Q(city__icontains=search))

	def this_account(self, account):
		return self.filter(account=account)

	def this_city(self, city):
		return self.filter(city=city)

	def this_employee(self, employee):
		return self.filter(employee=employee)

class LocationQuerySet(QuerySet):
	def this_account(self, account):
		return self.filter(account=account)

	def search(self, search):
		return self.filter(name__icontains=search)

	def has_items(self, has_items):
		if has_items=='True':
			return self.annotate(item_count=Count('item_location')).filter(item_count__gt=0)
		elif has_items == 'False':
			return self.annotate(item_count=Count('item_location')).filter(item_count=0)
		else:
			return self

	def is_warehouse(self, is_warehouse):
		return self.filter(is_warehouse=is_warehouse)

class CustomerQuerySet(QuerySet):
	def this_account(self, account):
		return self.filter(account=account)

	def has_orders(self, has_orders):
		if has_orders == 'True':
			return self.annotate(order_count=Count('order')).filter(order_count__gt=0)
		elif has_orders == 'False':
			return self.annotate(order_count=Count('order')).filter(order_count=0)
		else:
			return self

	def search(self, search):
		return self.filter(Q(name__icontains=search) | Q(phone__icontains=search))

class LocationManager(models.Manager):
	def create_location(self, *args, **kwargs):
		location = self.create(*args, **kwargs)
		return location

	def get_query_set(self):
		return LocationQuerySet(self.model)

	def __getattr__(self, attr, *args):
		if attr.startswith("_"):
			raise AttributeError
		return getattr(self.get_query_set(), attr, *args)

class AddressManager(models.Manager):
	def create_address(self, *args, **kwargs):
		address = self.create(*args, **kwargs)
		location_model = apps.get_model('locations', 'Location')
		new_location = location_model.objects.create(name=address.name, address=address, account=kwargs['account'])
		return address

	def get_query_set(self):
		return AddressQuerySet(self.model)

	def __getattr__(self, attr, *args):
		if attr.startswith("_"):
			raise AttributeError
		return getattr(self.get_query_set(), attr, *args)

class CustomerManager(models.Manager):
	def create_customer(self, *args, **kwargs):
		customer = self.create(*args, **kwargs)
		location_model = apps.get_model('locations', 'Location')
		new_location = location_model.objects.create(name=customer.name, customer=customer, account=kwargs['account'])
		return customer

	def get_query_set(self):
		return CustomerQuerySet(self.model)  

	def __getattr__(self, attr, *args):
		if attr.startswith("_"):
			raise AttributeError
		return getattr(self.get_query_set(), attr, *args)

class EmployeeManager(models.Manager):
	def create_employee(self, *args, **kwargs):
		employee = self.create(*args, **kwargs)
		location_model = apps.get_model('locations', 'Location')
		new_location = location_model.objects.create(name=employee.name, account=kwargs['account'])
		return employee

	def get_query_set(self):
		return EmployeeQuerySet(self.model)

	def __getattr__(self, attr, *args):
		if attr.startswith("_"):
			raise AttributeError
		return getattr(self.get_query_set(), attr, *args)

class EmployeeQuerySet(QuerySet):
	def this_account(self, account):
		return self.filter(account=account)

	def has_addresses(self, has_addresses):
		if has_addresses == 'True':
			return self.annotate(address_count=Count('address')).filter(address_count__gt=0)
		elif has_addresses == 'False':
			return self.annotate(address_count=Count('address')).filter(address_count=0)
		else:
			return self

	def search(self, search):
		return self.filter(name__icontains=search)
