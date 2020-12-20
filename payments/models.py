from django.db import models
from django.forms import NumberInput, TextInput
from orders.models import Order
from accounts.models import Account
from vitudo.forms import BaseModelForm
from django.utils.translation import gettext_lazy as _

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

class PaymentForm(BaseModelForm):
	class Meta:
		model = Payment
		fields = ['amount', 'comment']
		labels = {
			"amount": _('Price'),
			"comment": _('Comment'),
		}
		widgets = {
			'amount': NumberInput(attrs={'class': 'form-control', 'placeholder': _('Price')}),
			'comment': TextInput(attrs={'class': 'form-control', 'placeholder': _('Comment')}),		
		}