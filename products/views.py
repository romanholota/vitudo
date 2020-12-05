from django.shortcuts import render, redirect, reverse, get_object_or_404
from vitudo.forms import SearchForm
from vitudo.utils import pagination
from items.models import Item

from . models import Product, Category, Brand, CategoryForm, BrandForm, ProductForm, ProductDetailsForm

# Create your views here.
def index(request):
	if request.GET.get('category'):
		category = get_object_or_404(Category, id=request.GET.get('category'), user=request.user)
		products = Product.objects.this_user(request.user).this_category(category)
	else:
		products = Product.objects.this_user(request.user)

	categories = Category.objects.this_user(request.user).order_by('name')

	form = SearchForm(request.GET or None)

	# vyhladavanie
	if request.GET: products = products.search(request.GET.get('search'))

	products = pagination(request.GET.get('pg'), products)

	context = {
		'products': products,
		'categories': categories,
		'form': form,
		'page_title': 'Products',
	}
	return render(request, 'products/products/list/index.html', context)

def add(request):
	form = ProductForm(request.POST or None, user=request.user)
	details_form = ProductDetailsForm(request.POST or None, request.FILES or None)
	if request.POST:
		if form.is_valid() and details_form.is_valid():
			new_details = details_form.save()
			new_product = Product.objects.update_or_create_product(**form.cleaned_data, id=None, details=new_details, user=request.user, full_name=form.cleaned_data['brand'].name + " " + form.cleaned_data['model'])
			return redirect(reverse('products:detail', args=[new_product.id]))

	context = {
		'form': form,
		'details_form': details_form,
	}

	return render(request, 'products/products/list/new.html', context)

def items(request, product_id):
	product = get_object_or_404(Product, id=product_id, user=request.user)
	items = Item.objects.active().this_product(product).this_user(request.user)

	form = SearchForm(request.GET or None)

	if request.GET.get('search'): items = items.search(request.GET.get('search'))

	items = pagination(request.GET.get('pg'), items)

	context = {
		'product': product,
		'items': items,
		'form': form,
	}
	return render(request, 'products/products/detail/items.html', context)

def remove(request, product_id):
	product = get_object_or_404(Product, id=product_id, user=request.user)
	item_count = Item.objects.active().this_product(product).this_user(request.user).count()

	if not item_count: product.delete()

	return redirect(reverse('products:index'))

def detail(request, product_id):
	product = get_object_or_404(Product, id=product_id, user=request.user)
	form = ProductForm(request.POST or None, instance=product, user=request.user)
	details_form = ProductDetailsForm(request.POST or None, request.FILES or None, instance=product.details)

	if request.POST:
		if form.is_valid() and details_form.is_valid():
			new_details = details_form.save()
			product = Product.objects.update_or_create_product(**form.cleaned_data, id=product.id, details=new_details, user=request.user, full_name=form.cleaned_data['brand'].name + " " + form.cleaned_data['model'])

	context = {
		'product': product,
		'form': form,
		'details_form': details_form,
	}

	return render(request, 'products/products/detail/detail.html', context)

def product_operations(request, product_id):
	product = get_object_or_404(Product, id=product_id, user=request.user)
	items = Item.objects.active().this_product(product).this_user(request.user)
	form = ProductBulkOperationForm(request.POST or None, items=items)
	basket, created = Basket.objects.get_or_create(user=request.user)

	if request.POST and form.is_valid():
		items = form.cleaned_data['items']

		if request.POST.get('deactivate'):
			for item in items:
				if item.location.is_warehouse and item.is_available:
					item.is_active = False
					item.is_available = False
					item.save()
			return redirect(reverse('products:detail', args=[product.id]))

		if request.POST.get('transfer'):
			for item in items: transfered_item = Item.objects.transfer(item, basket)
			return redirect(reverse('transfers:transfer'))

	context = {
		'form': form,
		'product': product,
		'form': form,
	}

	return render(request, 'products/detail/bulk_operation.html', context)

	

# ZNAČKY

def brands(request):
	brands = Brand.objects.this_user(request.user).has_products(request.GET.get('hasproducts'))
	form = SearchForm(request.GET or None)

	#vyhladavanie
	if request.GET: brands = brands.search(request.GET.get('search'))

	brands = pagination(request.GET.get('pg'), brands)

	context = {
		'brands': brands,
		'form': form,
	}
	return render(request, 'products/brands/list/index.html', context)

def brand_add(request):
	form = BrandForm(request.POST or None)
	if request.POST and form.is_valid():
		new_brand = Brand.objects.create_brand(**form.cleaned_data, user=request.user)
		return redirect(reverse('products:brand_detail', args=[new_brand.id]))
	return render(request, 'products/brands/list/new.html', {'form': form})

def brand_products(request, brand_id):
	brand = get_object_or_404(Brand, id=brand_id, user=request.user)
	products = Product.objects.this_brand(brand).this_user(request.user)
	form = SearchForm(request.GET or None)

	if request.GET.get('search'): products = products.search(request.GET.get('search'))

	products = pagination(request.GET.get('pg'), products)

	context = {
		'brand': brand,
		'products': products,
		'form': form,
	}

	return render(request, 'products/brands/detail/products.html', context)

def brand_detail(request, brand_id):
	brand = get_object_or_404(Brand, id=brand_id, user=request.user)
	form = BrandForm(request.POST or None, instance=brand)
	if request.POST and form.is_valid():
		form.save()
		return redirect(reverse('products:brand_detail', args=[brand.id]))

	context = {
		'form': form,
		'brand': brand,
	}

	return render(request, 'products/brands/detail/detail.html', context)

def brand_remove(request, brand_id):
	brand = get_object_or_404(Brand, id=brand_id, user=request.user)
	product_count = Product.objects.this_brand(brand).this_user(request.user).count()

	if not product_count: brand.delete()

	return redirect(reverse('products:brands'))


# KATEGORIE PRODUKTOV

def categories(request):
	has_products = request.GET.get('hasproducts')
	categories = Category.objects.this_user(request.user).has_products(has_products)

	form = SearchForm(request.GET or None)

	#vyhladavanie
	if request.GET.get('search'): categories = categories.search(request.GET.get('search'))

	categories = pagination(request.GET.get('pg'), categories)

	context = {
		'categories': categories,
		'form': form,
	}
	return render(request, 'products/categories/list/index.html', context)

def category_add(request):
	form = CategoryForm(request.POST or None)
	if request.POST and form.is_valid():
		new_category = Category.objects.create_category(**form.cleaned_data, user=request.user)
		return redirect(reverse('products:categories'))
	return render(request, 'products/categories/list/new.html', {'form': form})

def category_detail(request, category_id):
	category = get_object_or_404(Category, id=category_id, user=request.user)
	form = CategoryForm(request.POST or None, instance=category)
	
	if request.POST and form.is_valid():
		form.save()

	context = {
		'category': category,
		'form': form,
	}

	return render(request, 'products/categories/detail/detail.html', context)

def category_products(request, category_id):
	category = get_object_or_404(Category, id=category_id, user=request.user)
	products = Product.objects.this_category(category).this_user(request.user)
	form = SearchForm(request.GET or None)

	if request.GET.get('search'): products = products.search(request.GET.get('search'))

	products = pagination(request.GET.get('pg'), products)

	context = {
		'category': category,
		'products': products,
		'form': form,
	}

	return render(request, 'products/categories/detail/products.html', context)

def category_remove(request, category_id):
	category = get_object_or_404(Category, id=category_id, user=request.user)
	product_count = Product.objects.this_category(category).this_user(request.user).count()

	if not product_count: category.delete()

	return redirect(reverse('products:categories'))
