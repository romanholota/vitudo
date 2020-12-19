from django.db import models
from orders.models import Order
from accounts.models import Account

from . managers import PaymentManager

# Create your models here.
class Payment(models.Model):
	amount = models.DecimalField(max_digits=5, decimal_places=2)
	comment = models.CharField(max_length=100, null=True, blank=True)
	date = models.DateTimeField(null=True, blank=True)
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	deleted = models.BooleanField(default=False)
	account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)

	objects = PaymentManager()
