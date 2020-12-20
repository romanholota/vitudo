from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:order_id>/', views.detail, name='detail'),
    path('<int:order_id>/print/', views.print, name='print'),
    path('<int:order_id>/payments/', views.payments, name='payments'),
    path('<int:order_id>/payments/delete/<int:payment_id>/', views.payment_delete, name='payment_delete'),    
    path('<int:order_id>/items/', views.items, name='items'),
    path('<int:order_id>/edit/', views.edit, name='edit'),
    path('<int:order_id>/done/', views.done, name='done'),
    path('<int:order_id>/activate/', views.not_done, name='not_done'),
]
