from django.db import models
from django.contrib.auth.models import User
from vitudo.forms import BaseModelForm
from django.forms import ModelForm, ModelChoiceField, Select, TextInput, Textarea, FileInput, NumberInput

from . managers import *

# Create your models here.
class Brand(models.Model):
	name = models.CharField(max_length=100)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

	objects = BrandManager()

	def __str__(self):
		return self.name

class Category(models.Model):
	name = models.CharField(max_length=100)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) 

	objects = CategoryManager()

	def __str__(self):
		return self.name

class ProductDetails(models.Model):
	image = models.ImageField(upload_to='images/', null=True, blank=True)
	desc = models.CharField(max_length=1000, null=True, blank=True)
	price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

class Product(models.Model):
	brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	model = models.CharField(max_length=100, null=True)
	full_name = models.CharField(max_length=200, null=True)
	alternative_name = models.CharField(max_length=200, null=True, blank=True)
	details = models.ForeignKey(ProductDetails, on_delete=models.SET_NULL, null=True)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

	objects = ProductManager()

	def __str__(self):
		return self.full_name

	def active_items_count(self):
		return Product.objects.filter(id=self.id, item__is_active=True).count()

class ProductForm(BaseModelForm):
	brand = ModelChoiceField(queryset=None, widget=Select(attrs={'class': 'form-control'}), label="Brand", empty_label='Select brand')
	category = ModelChoiceField(queryset=None, widget=Select(attrs={'class': 'form-control'}), label="Category", empty_label='Select category')

	class Meta:
		model = Product
		fields = ['brand', 'category', 'model', 'alternative_name']
		labels = {
			"brand": "Brand",
			"category": "Category",
			"model": "Model",
			'alternative_name': 'Alternative Name',
    	}
		widgets = {
			'model': TextInput(attrs={'class': 'form-control', 'placeholder': 'Model'}),
			'alternative_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Hovorový názov'})
    	}

	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user')
		super(ProductForm, self).__init__(*args, **kwargs)
		self.fields['brand'].queryset = Brand.objects.filter(user=user).order_by('name')
		self.fields['category'].queryset = Category.objects.filter(user=user).order_by('name')


class ProductDetailsForm(BaseModelForm):

	class Meta:
		model = ProductDetails
		fields = ['desc', 'image', 'price']
		labels = {
			"desc": "Description",
			"image": "Image",
			"price": "Price",
    	}
		help_texts = {
			'desc': 'Stručný popis produktu a jeho hlavných vlastností.',
    		'price': 'Cena za 24 hodín v EUR.',
    	}
		widgets = {
			'desc': Textarea(attrs={'class':'form-control', 'placeholder':'Description'}),
			'image': FileInput(attrs={'class': 'file-input'}),
			'price': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price for 24 hours'}),
    	}
	def __init__(self, *args, **kwargs):
		super(ProductDetailsForm, self).__init__(*args, **kwargs)
		self.fields['image'].required = False

class BrandForm(BaseModelForm):
	class Meta:
		model = Brand
		fields = ['name']
		labels = {
			"name": "Name",
		}
		widgets = {
			'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Názov'}),
		}

class CategoryForm(BaseModelForm):
	class Meta:
		model = Category
		fields = ['name']
		labels = {
			"name": "Name",
		}
		widgets = {
			'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Názov'}),
		}
