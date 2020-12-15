from django.shortcuts import render, reverse, redirect, get_object_or_404
from transfers.models import Transfer
from orders.models import Order
from items.models import Item
from vitudo.forms import SearchForm
from vitudo.utils import pagination

from . models import Location, Customer, Employee, Address, LocationForm, CustomerForm, EmployeeForm, AddressForm


# LOKACIE

def index(request):
	locations = Location.objects.this_user(request.user).has_items(request.GET.get('hasitems'))
	form = SearchForm(request.GET or None)

	if request.GET.get('search'): locations = locations.search(request.GET.get('search'))

	locations = pagination(request.GET.get('pg'), locations)

	context = {
		'locations': locations,
		'form': form,
	}
	return render(request, 'locations/locations/list/index.html', context)

def add(request):
	form = LocationForm(request.POST or None, user=request.user)

	if request.POST and form.is_valid():
		new_location = Location.objects.create_location(**form.cleaned_data, user=request.user)
		return redirect(reverse('locations:index'))

	context = {
		'form': form
	}

	return render(request, 'locations/locations/list/new.html', context)

def items(request, location_id):
	location = get_object_or_404(Location, id=location_id, user=request.user)
	items = Item.objects.active().at_location(location).this_user(request.user)
	form = SearchForm(request.GET or None)

	if request.GET.get('search'): items = items.search(request.GET.get('search'))

	items = pagination(request.GET.get('pg'), items)

	context = {
		'location': location,
		'items': items,
		'form': form,
	}
	return render(request, 'locations/locations/detail/items.html', context)

def transfers(request, location_id):
	location = get_object_or_404(Location, id=location_id, user=request.user)
	transfers = Transfer.objects.this_location(location).this_user(request.user).is_order(request.GET.get('order'))
	form = SearchForm(request.GET or None)

	if request.GET.get('search'): transfers = transfers.search(request.GET.get('search'))

	transfers = pagination(request.GET.get('pg'), transfers.order_by('-date'))

	context = {
		'location': location,
		'transfers': transfers,
		'form': form,
	}
	return render(request, 'locations/locations/detail/transfers.html', context)	

def detail(request, location_id):
	location = get_object_or_404(Location, id=location_id, user=request.user)
	form = LocationForm(request.POST or None, instance=location, user=request.user)

	if request.POST and form.is_valid():
		location = form.save()

	context = {
		'location': location,
		'form': form,
	}

	return render(request, 'locations/locations/detail/detail.html', context)

def location_remove(request, location_id):
	location = get_object_or_404(Location, id=location_id, user=request.user)
	item_count = Item.objects.active().at_location(location).this_user(request.user).count()

	if not item_count: location.delete()

	return redirect(reverse('vitudo:locations'))


def customers(request):
	customers = Customer.objects.this_user(request.user).has_orders(request.GET.get('hasorders'))
	form = SearchForm(request.GET or None)

	if request.GET.get('search'): customers = customers.search(request.GET.get('search'))

	customers = pagination(request.GET.get('pg'), customers)

	context = {
		'customers': customers,
		'form': form,
	}
	return render(request, 'locations/customers/list/index.html', context)

def customer_add(request):
	form = CustomerForm(request.POST or None)

	if request.POST and form.is_valid():
		# ulozenie zakaznika
		new_customer = Customer.objects.create_customer(**form.cleaned_data, user=request.user)
		return redirect(reverse('locations:customers'))

	context = {
		'form': form,
	}

	return render(request, 'locations/customers/list/new.html', context)

def customer_orders(request, customer_id):
	customer = get_object_or_404(Customer, id=customer_id, user=request.user)
	orders = Order.objects.this_customer(customer).this_user(request.user).order_by('-start')
	form = SearchForm(request.GET or None)

	if request.GET: orders = orders.search(request.GET.get('search'))

	orders = pagination(request.GET.get('pg'), orders)

	context = {
		'customer': customer,
		'orders': orders,
		'form': form,
	}

	return render(request, 'locations/customers/detail/orders.html', context)

def customer_detail(request, customer_id):
	customer = get_object_or_404(Customer, id=customer_id, user=request.user)
	form = CustomerForm(request.POST or None, instance=customer)

	if request.POST and form.is_valid(): form.save()

	context = {
		'form': form,
		'customer': customer,
	}

	return render(request, 'locations/customers/detail/detail.html', context)

def customer_remove(request, customer_id):
	customer = get_object_or_404(Customer, id=customer_id, user=request.user)
	order_count = Order.objects.this_customer(customer).this_user(request.user).count()
	
	if not order_count: customer.delete()

	return redirect(reverse('locations:customers'))

# ADRESY

def addresses(request):
	if request.GET.get('city'):
		addresses = Address.objects.this_user(request.user).this_city(request.GET.get('city'))
	else:
		addresses = Address.objects.this_user(request.user)

	cities = Address.objects.this_user(request.user).values('city')

	form = SearchForm(request.GET or None)

	if request.GET.get('search'): addresses = addresses.search(request.GET.get('search'))

	addresses = pagination(request.GET.get('pg'), addresses)

	context = {
		'addresses': addresses,
		'cities': cities,
		'form': form,
	}
	return render(request, 'vitudo/addresses/list/index.html', context)

def address_add(request):
	form = AddressForm(request.POST or None, user=request.user)

	if request.POST and form.is_valid():
		#ulozenie novej adresy
		new_address = Address.objects.create_address(**form.cleaned_data, user=request.user)
		return redirect(reverse('vitudo:addresses'))

	context = {
		'form': form,
	}

	return render(request, 'vitudo/addresses/list/new.html', context)

def address_detail(request, address_id):
	# nacitanie adresy podla id
	address = get_object_or_404(Address, id=address_id, user=request.user)

	context = {
		'address': address,
	}

	return render(request, 'vitudo/addresses/detail/detail.html', context)

def address_edit(request, address_id):
	# nacitanie adresy podla id
	address = get_object_or_404(Address, id=address_id, user=request.user)
	form = AddressForm(request.POST or None, instance=address, user=request.user)

	# odoslanie formulara so zmenou udajov
	if request.POST and form.is_valid:
		address = form.save()

	context = {
		'form': form,
		'address': address,
	}

	return render(request, 'vitudo/addresses/detail/edit.html', context)

def address_remove(request, address_id):
	address = get_object_or_404(Address, id=address_id, user=request.user)
	address.delete()
	return redirect(reverse('vitudo:addresses'))

# ZAMESTNANCI

def employees(request):
	if request.GET.get('hasaddresses'):
		employees = Employee.objects.this_user(request.user).has_addresses(request.GET.get('hasaddresses'))
	else:
		employees = Employee.objects.this_user(request.user)

	form = SearchForm(request.GET or None)

	if request.GET.get('search'): employees = employees.search(request.GET.get('search'))

	employees = pagination(request.GET.get('pg'), employees.order_by('name'))

	context = {
		'employees': employees,
		'form': form,
	}
	return render(request, 'locations/employees/list/index.html', context)

def employee_add(request):
	form = EmployeeForm(request.POST or None)

	if request.POST and form.is_valid():
		new_employee = Employee.objects.create_employee(**form.cleaned_data, user=request.user)
		return redirect(reverse('locations:employees'))

	context = {
		'form': form,
	}

	return render(request, 'locations/employees/list/new.html', context)

def employee_addresses(request, employee_id):
	employee = get_object_or_404(Employee, id=employee_id, user=request.user)
	addresses = Address.objects.this_employee(employee).this_user(request.user)
	form = SearchForm(request.GET or None)

	if request.GET.get('search'): addresses = addresses.search(request.GET.get('search'))

	addresses = pagination(request.GET.get('pg'), addresses)

	context = {
		'employee': employee,
		'addresses': addresses,
		'form': form,
	}

	return render(request, 'locations/employees/detail/addresses.html', context)

def employee_detail(request, employee_id):
	employee = get_object_or_404(Employee, id=employee_id, user=request.user)
	form = EmployeeForm(request.POST or None, instance=employee)

	if request.POST and form.is_valid():
		employee = form.save()
		return redirect(reverse('vitudo:employee_detail', args=[employee.id]))

	context = {
		'employee': employee,
		'form': form,
	}

	return render(request, 'locations/employees/detail/detail.html', context)

def employee_remove(request, employee_id):
	employee = get_object_or_404(Employee, id=employee_id, user=request.user)
	employee.delete()

	return redirect(reverse('locations:employees'))
