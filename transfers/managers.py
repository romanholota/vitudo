from django.db import models
from django.db.models.query import QuerySet
from django.db.models import Q, Count, Sum
from django.apps import apps
from datetime import datetime

class TransferQuerySet(QuerySet):
	def this_account(self, account):
		return self.filter(account=account)

	def this_location(self, location):
		return self.filter(Q(target_location=location) | Q(origin_location=location))

	def this_order(self, order):
		return self.filter(order=order)

	def this_item(self, item):
		return self.filter(item=item)

	def search(self, search):
		return self.filter(Q(origin_location__name__icontains=search) | Q(target_location__name__icontains=search) | Q(item__product__full_name__icontains=search))

	def is_order(self, is_order):
		if is_order == 'True':
			return self.filter(order__isnull=False)
		elif is_order == 'False':
			return self.filter(order__isnull=True)
		else:
			return self

class TransferManager(models.Manager):
	def create_transfer(self, **kwargs):
		item = kwargs['item']
		transfer = self.create(item=item, origin_location=kwargs['origin'], target_location=kwargs['target'], date=kwargs['date'], account=kwargs['account'])
		transfer.save()
		item.is_available = kwargs['item_available']
		item.is_transfered = kwargs['item_transfered']
		item.location = kwargs['target']
		item.save()
		return transfer

	def get_query_set(self):
		return TransferQuerySet(self.model)

	def __getattr__(self, attr, *args):
		if attr.startswith("_"):
			raise AttributeError
		return getattr(self.get_query_set(), attr, *args)
