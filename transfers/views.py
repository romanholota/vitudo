from django.shortcuts import render, redirect, reverse, get_object_or_404
from items.models import Item
from products.models import Product
from orders.models import Order, OrderItem
from locations.models import Location
from vitudo.forms import SearchForm
from vitudo.utils import pagination, get_order_no, get_item_price, final_price
import datetime
import decimal

from . models import Transfer, Basket
from . forms import TransferForm


# Create your views here.
def index(request):
	if request.GET.get('order'):
		transfers = Transfer.objects.this_user(request.user).is_order(request.GET.get('order'))
	else:
		transfers = Transfer.objects.this_user(request.user)

	form = SearchForm(request.GET or None)

	if request.GET.get('search'): transfers = transfers.search(request.GET.get('search'))

	transfers = pagination(request.GET.get('pg'), transfers.order_by('-id'))

	context = {
		'transfers': transfers,
		'form': form,
	}
	return render(request, 'transfers/list/index.html', context)

# presunutie do kosika, nastavenie priznaku v db
def transfer_item(request, item_id):
	item = get_object_or_404(Item, id=item_id, user=request.user)
	basket, created = Basket.objects.get_or_create(user=request.user)

	transfered_item = Item.objects.transfer(item, basket)

	return redirect(reverse('transfers:transfer'))

def transfer(request):
	basket, created = Basket.objects.get_or_create(user=request.user)
	items = basket.items.all()
	locations = Location.objects.none()
	transfer_form = TransferForm()

	search_form = SearchForm(request.GET or None)

	if request.GET.get('search'): locations = Location.objects.search(request.GET.get('search')).this_user(request.user)[:10]

	context = {
		'items': items,
		'locations': locations,
		'form': transfer_form,
		'search_form': search_form,
	}
	return render(request, 'transfers/list/transfer.html', context)

# VYTVARANIE PREVODOV

def create_transfer(request):
	basket = get_object_or_404(Basket, user=request.user)
	form = TransferForm(request.POST or None)

	if request.POST and form.is_valid():	
		# ak uzivatel nevybral lokaciu, hodi ho naspat na kosik
		if request.POST.get('location'):
			location = Location.objects.get(id=request.POST['location'], user=request.user)
		else:
			return redirect(reverse('vitudo:transfer'))

		# ak sa jedna o vypozicku priradi cenu, vytvori Order
		if location.customer:
			start = datetime.datetime.now()
			end = datetime.datetime.strptime(request.POST['end'], "%Y-%m-%d") + datetime.timedelta(days = 1)
			price = final_price(basket.items.all(), start, end)
			new_order = Order.objects.create_order(customer=location.customer, price=price, supposed_price=price, start=start, supposed_end=end, item_count=basket.items.all().count(), user=request.user, order_no=get_order_no(request.user), comment=request.POST.get('comment'))

		# vytvorenie zvlast prevodu pre kazdy item
		for item in basket.items.all():
			transfer = Transfer.objects.create_transfer(item=item, origin=item.location, target=location, date=datetime.datetime.now(), user=request.user, item_available=False, item_transfered=False)
			if location.customer:
				new_order.pin_order(transfer=transfer, item=item)
				new_order_item = OrderItem.objects.create_order_item(item=item, order=new_order, price=get_item_price(item, start, end))
			basket.items.remove(item)
			basket.save()

		return redirect(reverse('transfers:index'))
	else:
		return redirect(reverse('transfers:transfer'))

def return_item(request, item_id):
	item = get_object_or_404(Item, id=item_id, user=request.user)

	transfer = Transfer.objects.create_transfer(item=item, product=item.product, origin=item.location, target=item.warehouse, date=datetime.datetime.now(), user=request.user, item_available=True, item_transfered=False)

	if item.order: item.order.pin_order(transfer=transfer, item=item) # ak sa jedna o order, priradi prevodu order a z itemu ho vymaze
	
	return redirect(reverse('items:index'))

# vratenie vsetkych poloziek z lokacie
def return_location(request, location_id):
	location = get_object_or_404(Location, id=location_id, user=request.user)
	items = Item.objects.active().at_location(location)

	for item in items:
		transfer = Transfer.objects.create_transfer(item=item, product=item.product, origin=item.location, location=item.warehouse, date=datetime.datetime.now(), user=request.user, item_available=True, item_transfered=False)
	
		item.order and item.order.pin_order(transfer=transfer, item=item)


	return redirect(reverse('vitudo:location_detail', args=[location.id]))

def return_order(request, order_id):
	order = get_object_or_404(Order, id=order_id, user=request.user)
	items = Item.objects.active().at_order(order)

	for item in items:
		transfer = Transfer.objects.create_transfer(item=item, product=item.product, origin=item.location, location=item.warehouse, date=datetime.datetime.now(), user=request.user, item_available=True, item_transfered=False)
	
		order.pin_order(transfer=transfer, item=item)

	return redirect(reverse('vitudo:order_detail', args=[order.id]))

# AJAX VIEW

def get_locations(request):
	if request.GET.get('search'):
		locations = Location.objects.this_user(request.user).search(request.GET.get('search'))[:5]
	else:
		locations = Location.objects.none()

	return render(request, 'tables/json_location_table.html', {'locations': locations})

