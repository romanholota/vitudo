from django.urls import path

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
]
