from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:order_id>/', views.detail, name='order_detail'),
    path('<int:order_id>/print/', views.print, name='print_order'),
    path('<int:order_id>/payments/', views.payments, name='order_payments'),
    path('<int:order_id>/items/', views.items, name='order_items'),
    path('<int:order_id>/edit/', views.edit, name='order_edit'),
    path('<int:order_id>/done/', views.done, name='order_done'),
    path('<int:order_id>/activate/', views.not_done, name='order_not_done'),
    path('<int:order_id>/return/', views.return_order, name='return_order'),
]
