from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import Account
from vitudo.forms import BaseModelForm
from django.forms import ModelForm, ModelChoiceField, Select, TextInput, Textarea, FileInput, NumberInput

from . managers import *

# Create your models here.
class Brand(models.Model):
	name = models.CharField(max_length=100)
	account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)

	objects = BrandManager()

	def __str__(self):
		return self.name

class Category(models.Model):
	name = models.CharField(max_length=100)
	account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True) 

	objects = CategoryManager()

	def __str__(self):
		return self.name

class ProductDetails(models.Model):
	image = models.ImageField(upload_to='images/', null=True, blank=True)
	desc = models.CharField(max_length=1000, null=True, blank=True)
	price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)

class Product(models.Model):
	brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	model = models.CharField(max_length=100, null=True)
	full_name = models.CharField(max_length=200, null=True)
	alternative_name = models.CharField(max_length=200, null=True, blank=True)
	details = models.ForeignKey(ProductDetails, on_delete=models.SET_NULL, null=True)
	account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)

	objects = ProductManager()

	def __str__(self):
		return self.full_name

	def active_items_count(self):
		return Product.objects.filter(id=self.id, item__is_active=True).count()

class ProductForm(BaseModelForm):
	brand = ModelChoiceField(queryset=None, widget=Select(attrs={'class': 'form-control'}), label=_('Brand'), empty_label=_('Select brand'))
	category = ModelChoiceField(queryset=None, widget=Select(attrs={'class': 'form-control'}), label=_('Category'), empty_label=_('Select category'))

	class Meta:
		model = Product
		fields = ['brand', 'category', 'model', 'alternative_name']
		labels = {
			'brand': _('Brand'),
			'category': _('Category'),
			'model': _('Model'),
			'alternative_name': _('Alternative Name'),
    	}
		widgets = {
			'model': TextInput(attrs={'class': 'form-control', 'placeholder': _('Model')}),
			'alternative_name': TextInput(attrs={'class': 'form-control', 'placeholder': _('Alternative Name')})
    	}

	def __init__(self, *args, **kwargs):
		account = kwargs.pop('account')
		super(ProductForm, self).__init__(*args, **kwargs)
		self.fields['brand'].queryset = Brand.objects.filter(account=account).order_by('name')
		self.fields['category'].queryset = Category.objects.filter(account=account).order_by('name')


class ProductDetailsForm(BaseModelForm):

	class Meta:
		model = ProductDetails
		fields = ['desc', 'image', 'price']
		labels = {
			'desc': _('Description'),
			'image': _('Image'),
			'price': _('Price'),
    	}
		widgets = {
			'desc': Textarea(attrs={'class':'form-control', 'placeholder': _('Description')}),
			'image': FileInput(attrs={'class': 'file-input'}),
			'price': NumberInput(attrs={'class': 'form-control', 'placeholder': _('Price for 24 hours')}),
    	}
	def __init__(self, *args, **kwargs):
		super(ProductDetailsForm, self).__init__(*args, **kwargs)
		self.fields['image'].required = False

class BrandForm(BaseModelForm):
	class Meta:
		model = Brand
		fields = ['name']
		labels = {
			'name': _('Name'),
		}
		widgets = {
			'name': TextInput(attrs={'class': 'form-control', 'placeholder': _('Name')}),
		}

class CategoryForm(BaseModelForm):
	class Meta:
		model = Category
		fields = ['name']
		labels = {
			'name': _('Name'),
		}
		widgets = {
			'name': TextInput(attrs={'class': 'form-control', 'placeholder': _('Name')}),
		}
