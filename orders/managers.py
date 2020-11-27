from django.db import models
from django.db.models.query import QuerySet
from django.db.models import Q, Count, Sum
from django.apps import apps
from datetime import datetime

class OrderQuerySet(QuerySet):
	def this_user(self, user):
		return self.filter(user=user)

	def is_done(self, is_done):
		return self.filter(is_done=is_done)

	def this_customer(self, customer):
		return self.filter(customer=customer)

	def unreturned(self):
		return self.filter(supposed_end__lt=datetime.now(), is_done=False)

	def search(self, search):
		return self.filter(Q(customer__name__icontains=search) | Q(id__icontains=search))

class OrderManager(models.Manager):
	def is_done(self, **kwargs):
		order, created = self.update_or_create(id=kwargs['id'], defaults={**kwargs})
		return order

	def create_order(self, *args, **kwargs):
		order = self.create(*args, **kwargs)
		return order

	def get_query_set(self):
		return OrderQuerySet(self.model)

	def __getattr__(self, attr, *args):
		if attr.startswith("_"):
			raise AttributeError
		return getattr(self.get_query_set(), attr, *args)

