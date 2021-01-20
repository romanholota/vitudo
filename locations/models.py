from django.db import models
from django.forms import ModelForm, ModelChoiceField, Select, TextInput, Textarea, FileInput, NumberInput
from django.utils.translation import gettext_lazy as _
from accounts.models import Account
from vitudo.forms import BaseModelForm
from products.models import Product

from . managers import EmployeeManager, LocationManager, AddressManager, CustomerManager

# Create your models here.
class Employee(models.Model):
	name = models.CharField(max_length=100)
	function = models.CharField(max_length=100, null=True, blank=True)
	phone = models.CharField(max_length=100, null=True, blank=True)
	email = models.EmailField(null=True, blank=True)
	account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)

	objects = EmployeeManager()


	def __str__(self):
		return self.name

class Customer(models.Model):
	name = models.CharField(max_length=100)
	phone = models.CharField(max_length=100, null=True, blank=True)
	comment = models.CharField(max_length=1000, null=True, blank=True)
	account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)

	objects = CustomerManager()

	def __str__(self):
		return self.name

class Address(models.Model):
	name = models.CharField(max_length=100)
	address = models.CharField(max_length=100, null=True)
	city = models.CharField(max_length=100, null=True)
	employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
	comment = models.CharField(max_length=1000, null=True, blank=True)
	account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)

	objects = AddressManager()

	def __str__(self):
		return self.name

class Location(models.Model):
	name = models.CharField(max_length=100)
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
	is_warehouse = models.BooleanField(null=True, blank=True)
	account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)

	objects = LocationManager()

	def __str__(self):
		return self.name

	def active_items_count(self):
		return Location.objects.filter(id=self.id, item_location__is_active=True).count()


class AddressForm(BaseModelForm):
	employee = ModelChoiceField(queryset=None, widget=Select(attrs={'class': 'form-control'}), label="", empty_label=_('Choose employee'), required=False)

	class Meta:
		model = Address
		fields = ['name', 'address', 'city', 'employee', 'comment']
		labels = {
			'name': _('Name'),
			'address': _('Address'),
			'city': _('City'),
			'employee': _('Employee'),
			'comment': _('Comment'),
		}
		widgets = {
			'name': TextInput(attrs={'class': 'form-control', 'placeholder': _('Name')}),
			'address': TextInput(attrs={'class': 'form-control', 'placeholder': _('Address')}),
			'city': TextInput(attrs={'class': 'form-control', 'placeholder': _('City')}),
			'comment': Textarea(attrs={'class':'form-control', 'placeholder': _('Comment')})
		}

	def __init__(self, *args, **kwargs):
		account = kwargs.pop('account')
		super(AddressForm, self).__init__(*args, **kwargs)
		self.fields['employee'].queryset = Employee.objects.filter(account=account).order_by('name')


class EmployeeForm(BaseModelForm):
	class Meta:
		model = Employee
		fields = ['name', 'function', 'phone', 'email']
		labels = {
			"name": _('Employee'),
			"function": _('Role'),
			"phone": _('Phone'),
			"email": _('E-mail'),  
		}
		widgets = {
			'name': TextInput(attrs={'class': 'form-control', 'placeholder': _('Employee')}),
			'function': TextInput(attrs={'class': 'form-control', 'placeholder': _('Role')}),
			'phone': TextInput(attrs={'class': 'form-control', 'placeholder': _('Phone')}),
			'email': TextInput(attrs={'class': 'form-control', 'placeholder': _('E-mail')}),
		}

class LocationForm(BaseModelForm):
	address = ModelChoiceField(queryset=None, widget=Select(attrs={'class': 'form-control'}), label=_('Address'), empty_label=_('Select address'), required=False)
	customer = ModelChoiceField(queryset=None, widget=Select(attrs={'class': 'form-control'}), label=_('Customer'), empty_label=_('Select customer'), required=False)


	class Meta:
		model = Location
		fields = ['name', 'address', 'customer']
		labels = {
			"name": _('Name'),
			"address": _('Address'),
			"customer": _('Customer'),
		}
		widgets = {
			'name': TextInput(attrs={'class': 'form-control', 'placeholder': _('Name')}),
		}

	def __init__(self, *args, **kwargs):
		account = kwargs.pop('account')
		super(LocationForm, self).__init__(*args, **kwargs)
		self.fields['address'].queryset = Address.objects.filter(account=account).order_by('name')
		self.fields['customer'].queryset = Customer.objects.filter(account=account).order_by('name')

class CustomerForm(BaseModelForm):
	class Meta:
		model = Customer
		fields = ['name', 'phone', 'comment']
		labels = {
			"name": _('Customer'),
			"phone": _('Phone'),
			"comment": _('Comment'),
		}
		widgets = {
			'name': TextInput(attrs={'class': 'form-control', 'placeholder': _('Name')}),
			'phone': TextInput(attrs={'class': 'form-control', 'placeholder': _('Contact')}),
			'comment': Textarea(attrs={'class':'form-control', 'placeholder': _('Comment')})
		}