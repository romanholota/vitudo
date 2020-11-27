from django.db import models
from django.forms import ModelForm, ModelChoiceField, Select, TextInput, Textarea, FileInput, NumberInput
from django.contrib.auth.models import User
from products.models import Product

from . managers import EmployeeManager, LocationManager, AddressManager, CustomerManager

# Create your models here.
class Employee(models.Model):
	name = models.CharField(max_length=100)
	function = models.CharField(max_length=100, null=True, blank=True)
	phone = models.CharField(max_length=100, null=True, blank=True)
	email = models.EmailField(null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

	objects = EmployeeManager()


	def __str__(self):
		return self.name

class Customer(models.Model):
	name = models.CharField(max_length=100)
	phone = models.CharField(max_length=100, null=True, blank=True)
	comment = models.CharField(max_length=1000, null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

	objects = CustomerManager()

	def __str__(self):
		return self.name

class Address(models.Model):
	name = models.CharField(max_length=100)
	address = models.CharField(max_length=100, null=True)
	city = models.CharField(max_length=100, null=True)
	employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
	comment = models.CharField(max_length=1000, null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

	objects = AddressManager()

	def __str__(self):
		return self.name

class Location(models.Model):
	name = models.CharField(max_length=100)
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
	is_warehouse = models.BooleanField(null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

	objects = LocationManager()

	def __str__(self):
		return self.name
