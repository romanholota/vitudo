from io import BytesIO

from decimal import Decimal
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator

from orders.models import Order

def pagination(page, qs):
	p = Paginator(qs, 10)
	qs = p.get_page(page if page else 1)
	return qs

def get_item_price(item, start, end):
	delta = end - start
	days = Decimal(delta.days + delta.seconds / 86400)
	return item.product.details.price * days

def get_order_no(account):
	last_order = Order.objects.this_account(account).latest('order_no') if Order.objects.this_account(account).exists() else None
	if not last_order or last_order.order_no is None:
		return '00001'
	else:
		width = 5
		new_order_number = str(int(last_order.order_no) + 1)
		return (width - len(new_order_number)) * "0" + new_order_number

def final_price(items, start, end):
	delta = end - start
	price = 0
	days = Decimal(delta.days + delta.seconds / 86400)
	for item in items:
		item_price = item.product.details.price if item.product.details.price else 0
		price += item_price
	return price * days