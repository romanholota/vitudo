from django.shortcuts import render, get_object_or_404
from vitudo.forms import SearchForm
from vitudo.utils import pagination
from payments.models import Payment
from transfers.models import Transfer
from locations.models import Location
from django.utils import timezone

from . models import Order, OrderPriceForm

# Create your views here.
def index(request):
	if request.GET.get('isdone'):
		orders = Order.objects.this_account(request.user.details.account).is_done(request.GET.get('isdone'))
	else:
		orders = Order.objects.this_account(request.user.details.account)
		
	form = SearchForm(request.GET or None)

	if request.GET.get('search'): orders = orders.search(request.GET.get('search'))

	orders = pagination(request.GET.get('pg'), orders.order_by('-order_no'))

	context = {
		'orders': orders,
		'form': form,
	}
	return render(request, 'orders/list/index.html', context)

def detail(request, order_id):
	order = get_object_or_404(Order, id=order_id, account=request.user.details.account)
	payments = Payment.objects.this_order(order).this_account(request.user.details.account)
	transfers = Transfer.objects.this_order(order).this_account(request.user.details.account).order_by('-date')	
	total_amount = sum([payment.amount for payment in payments]) # celkova suma uhradena vo vypozicke
	location = get_object_or_404(Location, customer=order.customer, account=request.user.details.account)

	if order.is_done:
		duration = order.real_end - order.start
	else:
		duration = timezone.now() - order.start

	transfers = pagination(request.GET.get('pg'), transfers)

	context = {
		'order': order,
		'location': location,
		'total_amount': total_amount,
		'transfers': transfers,
		'hours': int(duration.seconds / 3600),
	}

	return render(request, 'orders/detail/detail.html', context)

def edit(request, order_id):
	order = get_object_or_404(Order, id=order_id, account=request.user.details.account)
	form = OrderPriceForm(request.POST or None, instance=order)

	if request.POST and form.is_valid():
		order = form.save()
		return redirect(reverse('vitudo:order_detail', args=[order.id]))

	context = {
		'order': order,
		'form': form,
	}

	return render(request, 'orders/detail/edit.html', context)

def payments(request, order_id):
	order = get_object_or_404(Order, id=order_id, account=request.user.details.account)
	payments = Payment.objects.this_order(order).this_account(request.user.details.account).order_by('-date')
	total_amount = sum([payment.amount for payment in payments])
	location = Location.objects.get(customer=order.customer, account=request.user.details.account)

	if order.is_done:
		duration = order.real_end - order.start
	else:
		duration = timezone.now() - order.start

	form = PaymentForm(request.POST or None)

	if request.POST and form.is_valid():
		new_payment = Payment.objects.create_payment(**form.cleaned_data, order=order, date=timezone.now(), account=request.user.details.account)
		return redirect(reverse('vitudo:order_payments', args=[order.id]))

	context = {
		'order': order,
		'payments': payments,
		'location': location,
		'total_amount': total_amount,
		'hours': int(duration.seconds / 3600),
		'form': form,
	}

	return render(request, 'vitudo/orders/detail/payments.html', context)

def items(request, order_id):
	order = get_object_or_404(Order, id=order_id)
	order_items = OrderItem.objects.this_order(order)
	form = SearchForm(request.GET or None)

	if request.GET: order_items = order_items.search(request.GET.get('search'))

	order_items = pagination(request.GET.get('pg'), order_items)

	context = {
		'order': order,
		'order_items': order_items,
		'form': form,
	}

	return render(request, 'vitudo/orders/detail/items.html', context)	


def payment_delete(request, payment_id, order_id):
	payment = get_object_or_404(Payment, id=payment_id, account=request.user.details.account)
	order = get_object_or_404(Order, id=order_id, account=request.user.details.account)
	if payment.amount > 0 and payment.deleted is False: return_payment = Payment.objects.create_payment(amount=-payment.amount, comment='Vymazanie platby', order=order, date=timezone.now(), account=request.user.details.account)
	payment.deleted = True
	payment.save()
	return redirect(reverse('vitudo:order_payments', args=[order.id]))

def done(request, order_id):
	order = Order.objects.is_done(id=order_id, is_done=True, real_end=timezone.now())

	return redirect(reverse('vitudo:order_detail', args=[order.id]))

def not_done(request, order_id):
	order = Order.objects.is_done(id=order_id, is_done=False, real_end=None)

	return redirect(reverse('vitudo:order_detail', args=[order.id]))

def print(request, order_id):
	company = get_object_or_404(Company, account=request.user.details.account)
	order = get_object_or_404(Order, id=order_id, account=request.user.details.account)
	items = Item.objects.at_order(order).this_account(request.user.details.account)

	return get_printed_order(company, order, items)