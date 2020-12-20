from django.urls import path, re_path

from . import views

app_name = 'locations'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('<int:location_id>/', views.detail, name='detail'),
    path('<int:location_id>/items/', views.items, name='items'),
    path('<int:location_id>/transfers/', views.transfers, name='transfers'),
    path('employees/', views.employees, name='employees'),
    path('employees/add/', views.employee_add, name='employee_add'),
    path('employees/<int:employee_id>/', views.employee_detail, name='employee_detail'),
    path('employees/<int:employee_id>/addresses/', views.employee_addresses, name='employee_addresses'),
    path('customers/', views.customers, name='customers'),
    path('customers/add/', views.customer_add, name='customer_add'),
    path('customers/<int:customer_id>/', views.customer_detail, name='customer_detail'),
    path('customers/<int:customer_id>/orders/', views.customer_orders, name='customer_orders'),
    path('addresses/', views.addresses, name='addresses'),
    path('addresses/add/', views.address_add, name='address_add'),
]
