from django.db import models
from locations.models import Customer
from django import forms
from django.contrib.auth.models import User

from . managers import OrderManager, OrderItemManager

# Create your models here.
class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order_no = models.CharField(max_length=10, blank=True, null=True)
	price = models.DecimalField(max_digits=5, decimal_places=2)
	supposed_price = models.DecimalField(max_digits=5, decimal_places=2, null=True)
	start = models.DateTimeField(null=True, blank=True)
	supposed_end = models.DateTimeField(null=True, blank=True)
	real_end = models.DateTimeField(null=True, blank=True)
	is_done = models.BooleanField(default=False)
	item_count = models.IntegerField(null=True, blank=True)
	comment = models.CharField(max_length=1000, null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

	objects = OrderManager()

	def pin_order(self, **kwargs):
		item = kwargs['item']
		transfer = kwargs['transfer']

		# priradi order ak item ziadnu nema, inak odstrani lebo sa jedna o vratku
		if not item.order:
			item.order = self
		else:
			item.order = None
		
		# prevod ma vzdy priradeny order, ak sa jedna o prevod na zakaznika
		transfer.order = self	
		
		item.save()
		transfer.save()
		return self

class OrderItem(models.Model):
	item = models.ForeignKey('items.Item', on_delete=models.CASCADE)
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	price = models.DecimalField(max_digits=5, decimal_places=2)

	objects = OrderItemManager()
