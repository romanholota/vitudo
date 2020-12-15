from django.db import models
from items.models import Item
from locations.models import Location, Employee
from orders.models import Order
from accounts.models import Account
from django import forms

from . managers import TransferManager

# Create your models here.
class Basket(models.Model):
	items = models.ManyToManyField(Item)
	account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)

class Transfer(models.Model):
	item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
	origin_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='origin')
	target_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='target')
	date = models.DateTimeField(null=True, blank=True)
	employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
	comment = models.CharField(max_length=1000, null=True, blank=True)
	account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)

	objects = TransferManager()
