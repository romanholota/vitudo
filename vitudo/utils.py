from io import BytesIO

from decimal import Decimal
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator

def pagination(page, qs):
	p = Paginator(qs, 10)
	qs = p.get_page(page if page else 1)
	return qs