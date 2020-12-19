from django.db import models
from django.db.models.query import QuerySet
from django.db.models import Q, Count, Sum
from django.apps import apps
from datetime import datetime

class PaymentQuerySet(QuerySet):
	def this_account(self, account):
		return self.filter(account=account)

	def this_order(self, order):
		return self.filter(order=order)

class PaymentManager(models.Manager):
	def create_payment(self, *args, **kwargs):
		payment = self.create(*args, **kwargs)

	def get_query_set(self):
		return PaymentQuerySet(self.model)

	def __getattr__(self, attr, *args):
		if attr.startswith("_"):
			raise AttributeError
		return getattr(self.get_query_set(), attr, *args)
