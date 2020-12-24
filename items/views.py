from django.shortcuts import render, get_object_or_404, redirect, reverse
from vitudo.forms import SearchForm, NumberForm
from vitudo.utils import pagination
from transfers.models import Transfer

from . models import Item, ItemImage, ItemDetails, ItemDetailsForm, ItemForm

def index(request):
	if request.GET.get('available'):
		items = Item.objects.untransfered().active().is_available(request.GET.get('available')).this_account(request.user.details.account) #zoznam vsetkych poloziek co nie su v prevode
	else:
		items = Item.objects.untransfered().active().this_account(request.user.details.account)

	form = SearchForm(request.GET or None) # vyhladavaci form

	#vyhladavanie
	if request.GET.get('search'): items = items.search(request.GET.get('search'))

	# strankovanie
	items = pagination(request.GET.get('pg'), items)

	context = {
		'items': items,
		'form': form,
		'page_title': 'Items',
	}
	return render(request, 'items/list/index.html', context)

def add(request):
	form = ItemForm(request.POST or None, account=request.user.details.account)
	number_form = NumberForm(request.POST or None)
	details_form = ItemDetailsForm(request.POST or None, request.FILES or None)	

	#ak je odoslany formular
	if request.POST and form.is_valid() and number_form.is_valid() and details_form.is_valid():
		amount = number_form.cleaned_data['amount'] if number_form.cleaned_data['amount'] > 0 else 1 # zisti kolko poloziek pridavame na sklad, ak je zaporna hodnota tak nastavi 1
		new_details = details_form.save()

		for i in range(amount):
			new_item = Item.objects.create_item(**form.cleaned_data, is_transfered=False, is_available=True, location=form.cleaned_data['warehouse'], account=request.user.details.account, details=new_details)
			for file in request.FILES.getlist('images'):
				new_image = ItemImage.objects.create_item_image(image=file, account=request.user.details.account, item=new_item)


		return redirect(reverse('items:index'))

	context = {
		'form': form,
		'number_form': number_form,
		'details_form': details_form,
	}

	return render(request, 'items/list/new.html', context)
		
def transfers(request, item_id):
	item = get_object_or_404(Item, id=item_id, account=request.user.details.account)
	form = SearchForm(request.GET or None)

	if request.GET.get('order'):
		transfers = Transfer.objects.this_item(item).this_account(request.user.details.account).is_order(request.GET.get('order'))
	else:
		transfers = Transfer.objects.this_item(item).this_account(request.user.details.account)

	if request.GET.get('search'): transfers = transfers.search(request.GET.get('search'))

	transfers = pagination(request.GET.get('pg'), transfers.order_by('-id'))

	context = {
		'item': item,
		'transfers': transfers,
		'form': form,
	}
	return render(request, 'items/detail/transfers.html', context)

def delete(request, item_id):
	if request.user.has_perm('delete_item'):
		item = get_object_or_404(Item, id=item_id, account=request.user.details.account)
		item.is_active = False
		item.save()

	return redirect(reverse('items:index'))

def detail(request, item_id):
	item = get_object_or_404(Item, id=item_id, account=request.user.details.account)
	form = ItemForm(request.POST or None, instance=item, account=request.user.details.account)
	details_form = ItemDetailsForm(request.POST or None, instance=item.details)

	if form.is_valid() and details_form.is_valid():
		item = form.save()
		item_details = details_form.save()
		return redirect(reverse('items:detail', args=[item.id]))

	context = {
		'item': item,
		'form': form,
		'details_form': details_form,
	}

	return render(request, 'items/detail/detail.html', context)

def edit_gallery(request, item_id):
	item = get_object_or_404(Item, id=item_id, account=request.user.details.account)

	context = {
		'item': item,
	}

	return render(request, 'items/detail/edit_gallery.html', context)

def image_remove(request, image_id, item_id):
	item = get_object_or_404(Item, id=item_id, account=request.user.details.account)
	image = get_object_or_404(ItemImage, id=image_id, account=request.user.details.account)
	image.delete()
	return redirect(reverse('items:edit_gallery', args=[item.id]))

def image_add(request, item_id):
	item = get_object_or_404(Item, id=item_id, account=request.user.details.account)
	if request.FILES:
		for file in request.FILES.getlist('images'):
			new_image = ItemImage.objects.create_item_image(image=file, account=request.user.details.account, item=item)
	return redirect(reverse('items:edit_gallery', args=[item.id]))
