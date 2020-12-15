from django.db import models
from django.forms import ModelForm, ModelChoiceField, Select, TextInput, Textarea, FileInput, NumberInput
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

class AddressForm(BaseModelForm):
	employee = ModelChoiceField(queryset=None, widget=Select(attrs={'class': 'form-control'}), label="", empty_label='Vyber zamestnanca', required=False)

	class Meta:
		model = Address
		fields = ['name', 'address', 'city', 'employee', 'comment']
		labels = {
			'name': '',
			'address': '',
			'city': '',
			'employee': '',
			'comment': '',
		}
		widgets = {
			'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Názov'}),
			'address': TextInput(attrs={'class': 'form-control', 'placeholder': 'Adresa'}),
			'city': TextInput(attrs={'class': 'form-control', 'placeholder': 'Mesto'}),
			'comment': Textarea(attrs={'class':'form-control', 'placeholder':'Poznámka'})
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
			"name": "Name",
			"function": "Function",
			"phone": "Phone",
			"email": "E-mail",  
		}
		widgets = {
			'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Meno'}),
			'function': TextInput(attrs={'class': 'form-control', 'placeholder': 'Funkcia'}),
			'phone': TextInput(attrs={'class': 'form-control', 'placeholder': 'Kontakt'}),
			'email': TextInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
		}

class LocationForm(BaseModelForm):
	address = ModelChoiceField(queryset=None, widget=Select(attrs={'class': 'form-control'}), label="", empty_label='Select address', required=False)
	customer = ModelChoiceField(queryset=None, widget=Select(attrs={'class': 'form-control'}), label="", empty_label='Select customer', required=False)


	class Meta:
		model = Location
		fields = ['name', 'address', 'customer']
		labels = {
			"name": "",
			"address": "",
			"customer": "",
		}
		widgets = {
			'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Názov'}),
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
			"name": "",
			"phone": "",
			"comment": "",
		}
		widgets = {
			'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Meno'}),
			'phone': TextInput(attrs={'class': 'form-control', 'placeholder': 'Kontakt'}),
			'comment': Textarea(attrs={'class':'form-control', 'placeholder':'Poznámka'})
		}