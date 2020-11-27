from django.db import models
from django.forms import ModelForm, ModelChoiceField, Select, TextInput, Textarea, FileInput, NumberInput
from django.contrib.auth.models import User
from products.models import Product
from locations.models import Location
from vitudo.forms import BaseModelForm

from . managers import ItemManager, ItemImageManager

# Create your models here.
class ItemDetails(models.Model):
	desc = models.CharField(max_length=1000, null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

class ItemImage(models.Model):
	image = models.ImageField(upload_to='images/', null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

	objects = ItemImageManager()

class Item(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
	warehouse = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='warehouse')
	location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='item_location')
	item_code = models.CharField(max_length=50, null=True, blank=True)
	is_transfered = models.BooleanField()
	is_available = models.BooleanField()
	is_active = models.BooleanField(default=True)
	details = models.ForeignKey(ItemDetails, on_delete=models.SET_NULL, null=True)
	images = models.ManyToManyField(ItemImage, blank=True)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

	objects = ItemManager()

	def __str__(self):
		return self.product.model

class ItemForm(BaseModelForm):
	product = ModelChoiceField(queryset=None, widget=Select(attrs={'class': 'form-control'}), label="Product", empty_label='Choose product')
	warehouse = ModelChoiceField(queryset=None, widget=Select(attrs={'class': 'form-control'}), label="Warehouse", empty_label='Vyber hlavný sklad', help_text='Hlavný sklad na ktorý sa vráti položka po ukončení bežného prevodu alebo výpožičky.')

	class Meta:
		model = Item
		fields = ['product', 'item_code', 'warehouse']
		labels = {
			"product": "Product",
			"item_code": "Item Code",
			"warehouse": "WareHouse",
    	}
		widgets = {
			'item_code': TextInput(attrs={'class': 'form-control', 'placeholder': 'Item Code'})
    	}

	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user')
		super(ItemForm, self).__init__(*args, **kwargs)
		self.fields['product'].queryset = Product.objects.filter(user=user).order_by('brand')
		self.fields['warehouse'].queryset = Location.objects.filter(user=user, is_warehouse=True).order_by('name')

class ItemDetailsForm(ModelForm):
	class Meta:
		model = ItemDetails
		fields = ['desc']
		labels = {
			"desc": "",
    	}
		widgets = {
			'desc': Textarea(attrs={'class':'form-control', 'placeholder':'Popis'})
    	}